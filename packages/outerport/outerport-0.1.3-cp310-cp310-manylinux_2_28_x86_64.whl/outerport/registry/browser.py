from botocore.exceptions import ClientError
from typing import List, Dict, Any, Protocol
import os
from outerport.registry.utils import (
    parallel_multipart_upload,
    parallel_multipart_download,
    parallel_multipart_copy,
    COPY_CHUNK_SIZE,
    get_s3_client,
)


class S3BrowserProtocol(Protocol):
    """Protocol defining the interface for S3 browser functionality.

    Attributes:
        s3: AWS S3 client instance
        bucket_name: Name of the S3 bucket
        current_dir: Current working directory path in the bucket
    """

    s3: Any
    bucket_name: str
    current_dir: str

    def _get_full_path(self, path: str) -> str:
        """Convert relative path to full S3 key path."""
        ...

    def _path_exists(self, path: str) -> bool:
        """Check if file or folder exists at given path."""
        ...

    def _folder_exists(self, path: str) -> bool:
        """Check if folder exists at given path."""
        ...

    def _format_size(self, size_in_bytes: float) -> str:
        """Format byte size to human readable string."""
        ...

    def get_folder_structure(self, path: str) -> Dict[str, Any]:
        """Get nested dictionary representing folder structure."""
        ...

    def list_contents(self, path: str) -> List[Dict[str, Any]]:
        """List immediate contents (files/folders) at given path."""
        ...


class S3InfoMixin(S3BrowserProtocol):
    def _path_exists(self, path: str) -> bool:
        """Check if a file or folder exists at the given path in S3.

        Args:
            path: Relative path to check

        Returns:
            bool: True if path exists, False otherwise
        """
        full_path = self._get_full_path(path)
        try:
            # Check if it's a file
            self.s3.head_object(Bucket=self.bucket_name, Key=f"{full_path}")
            return True
        except ClientError as e:
            # If it's not a file, check if it's a folder
            try:
                response = self.s3.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=f"{full_path}/",
                    Delimiter="/",
                    MaxKeys=1,
                )
                return "Contents" in response or "CommonPrefixes" in response
            except ClientError as e:
                return False

    def _file_exists(self, path: str) -> bool:
        """Check if a file exists at the given path in S3.

        Args:
            path: Relative path to check

        Returns:
            bool: True if file exists, False otherwise
        """
        full_path = self._get_full_path(path)
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=full_path)
            return True
        except ClientError as e:
            print(f"Error checking file existence: {e}")
            return False

    def _folder_exists(self, path: str) -> bool:
        """Check if a folder exists at the given path in S3.

        Args:
            path: Relative path to check

        Returns:
            bool: True if folder exists, False otherwise
        """
        full_path = self._get_full_path(path)
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{full_path}/",
                Delimiter="/",
                MaxKeys=1,
            )
            return "Contents" in response or "CommonPrefixes" in response
        except ClientError as e:
            print(f"Error checking folder existence: {e}")
            return False

    def _is_folder(self, path: str) -> bool:
        """Check if the given path represents a folder.

        Args:
            path: Relative path to check

        Returns:
            bool: True if path is a folder, False otherwise
        """
        return self._folder_exists(path)

    def _list_contents_base(
        self, path: str, delimiter: str = ""
    ) -> List[Dict[str, Any]]:
        """List contents of S3 path with optional delimiter for directory-like structure.

        Args:
            path: Relative path to list contents from
            delimiter: Optional delimiter (e.g. "/" for directory-like listing)

        Returns:
            List of dicts containing file/directory info with keys:
            - key: relative path
            - type: "file" or "directory"
            - size: file size in bytes (files only)
        """
        full_prefix = self._get_full_path(path)
        if not full_prefix.endswith("/"):
            full_prefix += "/"
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(
                Bucket=self.bucket_name, Prefix=full_prefix, Delimiter=delimiter
            )

            contents = []
            for page in page_iterator:
                if delimiter:
                    for prefix in page.get("CommonPrefixes", []):
                        relative_key = prefix["Prefix"][len(full_prefix) :].rstrip("/")
                        contents.append({"key": relative_key, "type": "directory"})
                for item in page.get("Contents", []):
                    if item["Key"] != full_prefix:
                        relative_key = item["Key"][len(full_prefix) :]
                        contents.append(
                            {"key": relative_key, "size": item["Size"], "type": "file"}
                        )
            return contents
        except ClientError as e:
            print(f"Error listing contents: {e}")
            return []

    def list_contents(self, path: str = "") -> List[Dict[str, Any]]:
        """List immediate contents (files and folders) at the given path.

        Args:
            path: Relative path to list contents from (defaults to current directory)

        Returns:
            List of dicts with keys: 'key' (str), 'type' (str), and 'size' (int, files only)

        Raises:
            ValueError: If the directory does not exist
        """
        if not self._path_exists(path):
            raise ValueError(f"Directory not found: {path}")
        return self._list_contents_base(path, delimiter="/")

    def get_folder_structure(self, path: str = "") -> Dict[str, Any]:
        """Get nested dictionary representing the complete folder structure.

        Args:
            path: Relative path to get structure from (defaults to current directory)

        Returns:
            Nested dict where each key is a folder/file name. Files have 'type' and 'size' attributes.
            Example:
            {
                'folder1': {
                    'file1.txt': {'type': 'file', 'size': 1234}
                }
            }
        """
        contents = self._list_contents_base(path)
        folder_structure: Dict[str, Any] = {}

        for item in contents:
            key = item["key"]
            if key.endswith("/"):
                continue  # Skip folder objects
            parts = key.split("/")
            current = folder_structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = {"type": item["type"], "size": item.get("size", 0)}

        return folder_structure

    def list_versions(self, file_name: str) -> List[Dict[str, Any]]:
        """List all versions of a specific file in S3.

        Args:
            file_name: Relative path to the file

        Returns:
            List of version dictionaries from S3, containing version metadata
            including VersionId, LastModified, Size, etc.
        """
        full_path = self._get_full_path(file_name)
        try:
            versions = self.s3.list_object_versions(
                Bucket=self.bucket_name, Prefix=full_path
            )
            return versions.get("Versions", [])
        except ClientError as e:
            print(f"Error listing versions: {e}")
            return []


class S3UpdateMixin(S3BrowserProtocol):
    def create_folder(self, path: str) -> bool:
        """Create a new folder at the specified path in S3.

        Args:
            path: Relative path for the new folder

        Returns:
            bool: True if successful, False otherwise
        """
        full_path = self._get_full_path(path)
        if not full_path.endswith("/"):
            full_path += "/"
        try:
            # Check if the folder already exists
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name, Prefix=full_path, MaxKeys=1
            )
            if "Contents" in response or "CommonPrefixes" in response:
                print(f"Folder already exists: {path}")
                return True

            # Create the folder
            self.s3.put_object(Bucket=self.bucket_name, Key=full_path)
            print(f"Folder created: {path}")
            return True
        except ClientError as e:
            print(f"Error creating folder: {e}")
            return False

    def restore_version(self, file_name: str, version_id: str) -> bool:
        """Restore a specific version of a file.

        Args:
            file_name: Path to the file
            version_id: Version ID to restore

        Returns:
            bool: True if successful, False otherwise
        """
        full_path = self._get_full_path(file_name)
        try:
            self.s3.copy_object(
                Bucket=self.bucket_name,
                CopySource={
                    "Bucket": self.bucket_name,
                    "Key": full_path,
                    "VersionId": version_id,
                },
                Key=full_path,
            )
            print(f"Restored version {version_id} of {file_name}")
            return True
        except ClientError as e:
            print(f"Error restoring version: {e}")
            return False

    def copy_file(self, path: str, new_path: str) -> bool:
        """Copy a file to a new location within the same bucket.

        Args:
            path: Source file path
            new_path: Destination file path

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If source path doesn't exist
        """
        if not self._path_exists(path):
            raise ValueError(f"Directory not found: {path}")

        full_path = self._get_full_path(path)
        new_full_path = self._get_full_path(new_path)
        try:
            parallel_multipart_copy(
                source_bucket=self.bucket_name,
                source_key=full_path,
                dest_bucket=self.bucket_name,
                dest_key=new_full_path,
            )
            print(f"File copied: {path} -> {new_path}")
            return True
        except ClientError as e:
            print(f"Error copying file: {e}")
            return False

    def copy_folder(self, source_path: str, destination_path: str) -> bool:
        """Copy a folder and its contents to a new location.

        Args:
            source_path: Source folder path
            destination_path: Destination folder path

        Returns:
            bool: True if successful, False otherwise
        """
        source_prefix = self._get_full_path(source_path)
        destination_prefix = self._get_full_path(destination_path)

        if not source_prefix.endswith("/"):
            source_prefix += "/"
        if not destination_prefix.endswith("/"):
            destination_prefix += "/"

        try:
            # Create the destination folder
            self.s3.put_object(Bucket=self.bucket_name, Key=destination_prefix)

            # List all objects in the source folder
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=source_prefix)

            for page in pages:
                for obj in page.get("Contents", []):
                    old_key = obj["Key"]
                    object_size = obj["Size"]
                    is_directory = old_key.endswith("/")
                    new_key = destination_prefix + old_key[len(source_prefix) :]

                    print(old_key, new_key, len(source_prefix))

                    if is_directory:
                        self.s3.put_object(Bucket=self.bucket_name, Key=new_key)
                        print(new_key)
                    else:
                        if object_size > COPY_CHUNK_SIZE:
                            parallel_multipart_copy(
                                source_bucket=self.bucket_name,
                                source_key=old_key,
                                dest_bucket=self.bucket_name,
                                dest_key=new_key,
                            )
                        else:
                            self.s3.copy_object(
                                Bucket=self.bucket_name,
                                Key=new_key,
                                CopySource={"Bucket": self.bucket_name, "Key": old_key},
                            )

            print(f"Folder copied: {source_path} -> {destination_path}")
            return True
        except ClientError as e:
            print(f"Error copying folder: {e}")
            return False

    def delete_file(self, path: str) -> bool:
        """Delete a single file from S3.

        Args:
            path: Path to file

        Returns:
            bool: Success status
        """
        full_path = self._get_full_path(path)
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=full_path)
            print(f"File deleted: {path}")
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False

    def delete_folder(self, path: str) -> bool:
        """Delete a folder and all its contents from S3.

        Args:
            path: Path to folder

        Returns:
            bool: Success status
        """
        full_path = self._get_full_path(path)
        if not full_path.endswith("/"):
            full_path += "/"
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=full_path)

            delete_us: Dict[str, List[Dict[str, str]]] = dict(Objects=[])
            for page in pages:
                for item in page.get("Contents", []):
                    if item["Key"].startswith(full_path):
                        delete_us["Objects"].append(dict(Key=item["Key"]))

                        # Delete 1000 objects per API call
                        if len(delete_us["Objects"]) >= 1000:
                            self.s3.delete_objects(
                                Bucket=self.bucket_name, Delete=delete_us
                            )
                            delete_us = dict(Objects=[])

            # Final batch delete
            if len(delete_us["Objects"]):
                self.s3.delete_objects(Bucket=self.bucket_name, Delete=delete_us)

            print(f"Folder deleted: {path}")
            return True
        except ClientError as e:
            print(f"Error deleting folder: {e}")
            return False

    def rename_file(self, old_path: str, new_path: str) -> bool:
        """Rename/move a file by copying to new location and deleting original.

        Args:
            old_path: Current file path
            new_path: New file path

        Returns:
            bool: Success status
        """
        if self.copy_file(old_path, new_path):
            return self.delete_file(old_path)
        return False

    def rename_folder(self, old_path: str, new_path: str) -> bool:
        """Rename/move a folder by copying to new location and deleting original.

        Args:
            old_path: Current folder path
            new_path: New folder path

        Returns:
            bool: Success status
        """
        if self.copy_folder(old_path, new_path):
            return self.delete_folder(old_path)
        return False


class S3TransferMixin(S3BrowserProtocol):
    def upload_file(
        self, local_file_path: str, remote_file_name: str, show_progress: bool = True
    ) -> bool:
        try:
            full_path = self._get_full_path(remote_file_name)
            parallel_multipart_upload(
                local_file_path,
                self.bucket_name,
                full_path,
                show_progress=show_progress,
            )
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def download_file(
        self, remote_file_name: str, local_file_path: str, show_progress: bool = True
    ) -> bool:
        try:
            full_path = self._get_full_path(remote_file_name)
            parallel_multipart_download(
                self.bucket_name,
                full_path,
                local_file_path,
                show_progress=show_progress,
            )
            return True
        except Exception as e:
            return False

    def download_version(
        self,
        remote_file_name: str,
        local_file_path: str,
        version_id: str,
        show_progress: bool = True,
    ) -> bool:
        try:
            full_path: str = self._get_full_path(remote_file_name)
            # You'd need to modify parallel_multipart_download to accept a version_id parameter
            parallel_multipart_download(
                self.bucket_name,
                full_path,
                local_file_path,
                version_id=version_id,
                show_progress=show_progress,
            )
            return True
        except Exception as e:
            print(f"Error downloading version: {e}")
            return False


class S3DisplayMixin(S3BrowserProtocol):
    def _print_structure(
        self, structure: Dict[str, Any], prefix: str, folder: str = ""
    ) -> None:
        items = list(sorted(structure.items()))
        for i, (key, value) in enumerate(items):
            is_last = i == len(items) - 1
            current_path = os.path.join(folder, key).strip("/")
            level = len(current_path.split("/"))
            indent = "    " * (level - 1)

            if isinstance(value, dict) and "type" not in value:
                is_current = self.current_dir == os.path.join(prefix, current_path)
                current_marker = " 📍 You are here" if is_current else ""
                print(f"{indent}{'└──' if is_last else '├──'} {key}/{current_marker}")
                self._print_structure(value, current_path, prefix)
            else:
                size = self._format_size(value["size"])
                print(f"{indent}{'└──' if is_last else '├──'} {key} ({size})")

    def print_folder_structure(self, path: str = "") -> None:
        if not self._folder_exists(path):
            raise ValueError(f"Directory not found: {path}")

        if path.startswith("/"):
            prefix = os.path.normpath(path).strip("/")
        else:
            prefix = os.path.normpath(os.path.join(self.current_dir, path)).strip("/")

        folder_structure = self.get_folder_structure(path)
        print(f"Current directory: /{self.current_dir}")
        self._print_structure(folder_structure, prefix, "")

    def print_contents(self, path: str = "") -> None:
        if not self._path_exists(path):
            raise ValueError(f"Directory not found: {path}")
        full_path = self._get_full_path(path)
        contents = self.list_contents(path)

        print(f"Contents of /{full_path}:")
        for item in contents:
            rel_path = item["key"]
            if item["type"] == "directory":
                print(f"  📁 {rel_path}/")
            else:
                size = self._format_size(item["size"])
                print(f"  📄 {rel_path} ({size})")


class S3Browser(S3InfoMixin, S3UpdateMixin, S3TransferMixin, S3DisplayMixin):
    """Browser interface for S3 buckets with file system-like operations."""

    def __init__(self, bucket_name: str) -> None:
        """Initialize S3Browser with bucket name.

        Args:
            bucket_name: Name of S3 bucket to browse

        Raises:
            ValueError: If bucket doesn't exist or is inaccessible
        """

        self.s3 = get_s3_client()
        self.bucket_name: str = bucket_name
        self.current_dir: str = ""  # Start at the root
        self._validate_init_args(bucket_name)

    def _validate_init_args(self, bucket_name: str) -> None:
        """Validate bucket exists and is accessible.

        Args:
            bucket_name: Name of S3 bucket

        Raises:
            ValueError: If bucket validation fails
        """
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                raise ValueError(f"Bucket does not exist: {bucket_name}")
            elif error_code == 403:
                raise ValueError(f"No permission to access bucket: {bucket_name}")
            else:
                raise ValueError(f"Error accessing bucket: {e}")

    def _handle_uplevel(self, path: str) -> str:
        """Handle special path cases like '.' and '..' by converting to empty string.

        Args:
            path: Path to process

        Returns:
            Processed path string
        """
        if path == ".":
            path = ""
        elif all(part == ".." for part in path.split(os.sep)):
            path = ""
        return path

    def _get_full_path(self, path: str) -> str:
        """Convert relative path to full S3 key path.

        Args:
            path: Relative or absolute path

        Returns:
            Full normalized S3 key path
        """
        if path.startswith("/"):
            return os.path.normpath(path).strip("/")
        else:
            full_path = os.path.normpath(os.path.join(self.current_dir, path)).strip(
                "/"
            )
            full_path = self._handle_uplevel(full_path)
            print("hi")
            print(full_path)
            return full_path

    def _format_size(self, size_in_bytes: float) -> str:
        """Format byte size to human readable string with units.

        Args:
            size_in_bytes: Size in bytes

        Returns:
            Formatted string like "1.23 MB"

        Raises:
            ValueError: If size is too large to format
        """
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0

        raise ValueError(f"Size too large: {size_in_bytes}")

    def cd(self, path: str) -> None:
        """Change current directory to specified path.

        Args:
            path: Target directory path

        Raises:
            ValueError: If directory doesn't exist
        """
        try:
            if path == "/":
                new_path = ""
            elif path.startswith("/"):
                new_path = os.path.normpath(path)
            else:
                new_path = os.path.normpath(os.path.join(self.current_dir, path))
                new_path = self._handle_uplevel(new_path)

            if self._folder_exists(path):
                self.current_dir = new_path.strip("/")
            else:
                raise ValueError(f"Directory not found: {path}")
        except Exception as e:
            print(f"Error changing directory: {e}")

    def mkdir(self, path: str) -> bool:
        """Create a new directory in S3.

        Args:
            path: Path for new directory

        Returns:
            bool: Success status
        """
        return self.create_folder(path)

    def rm(self, path: str, recursive: bool = False) -> bool:
        """Remove a file or directory.

        Args:
            path: Path to remove
            recursive: If True, recursively delete directories

        Returns:
            bool: Success status
        """
        if not self._path_exists(path):
            print(f"Path does not exist: {path}")
            return False

        if self._is_folder(path):
            if recursive:
                return self.delete_folder(path)
            else:
                print(f"Path is a folder, use recursive=True: {path}")
                return False
        else:
            return self.delete_file(path)

    def rmdir(self, path: str) -> bool:
        """Remove a directory and all its contents.

        Args:
            path: Directory path to remove

        Returns:
            bool: Success status
        """
        return self.rm(path, recursive=True)

    def mv(self, old_path: str, new_path: str) -> bool:
        """Move/rename a file or directory.

        Args:
            old_path: Source path
            new_path: Destination path

        Returns:
            bool: Success status
        """
        if not self._path_exists(old_path):
            print(f"Path does not exist: {old_path}")
            return False

        if self._is_folder(old_path):
            return self.rename_folder(old_path, new_path)
        else:
            return self.rename_file(old_path, new_path)

    def cp(self, old_path: str, new_path: str) -> bool:
        """Copy a file or directory.

        Args:
            old_path: Source path
            new_path: Destination path

        Returns:
            bool: Success status
        """
        if not self._path_exists(old_path):
            print(f"Path does not exist: {old_path}")
            return False

        if self._is_folder(old_path):
            return self.copy_folder(old_path, new_path)
        else:
            return self.copy_file(old_path, new_path)

    def ls(self, path: str = "", recursive: bool = False) -> None:
        """List contents of a directory.

        Args:
            path: Directory path to list (default: current directory)
            recursive: If True, show complete folder structure
        """
        if recursive:
            self.print_folder_structure(path)
        else:
            self.print_contents(path)

    def pwd(self) -> None:
        """Print current working directory."""
        print(f"Current directory: /{self.current_dir}")


class RegistryBrowser(S3Browser):
    """S3Browser subclass that scopes all operations to a user's directory.

    All paths are automatically prefixed with the user's directory name.
    """

    def __init__(self, bucket_name: str, user: str) -> None:
        """Initialize browser with bucket name and user.

        Args:
            bucket_name: Name of S3 bucket
            user: Username to scope operations under
        """
        self.s3 = get_s3_client()

        self._validate_init_args(bucket_name, user)
        self.bucket_name: str = bucket_name
        self.current_dir: str = ""  # Start at the root
        self.user = user

    def _validate_init_args(self, bucket_name: str, user: str) -> None:
        """Validate bucket exists and is accessible.

        Args:
            bucket_name: Name of S3 bucket

        Raises:
            ValueError: If bucket validation fails
        """
        if not user.endswith("/"):
            user += "/"
        try:
            # Check only the specific directory
            response = self.s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=user,  # The public folder path
                MaxKeys=1,
                Delimiter="/",  # This ensures we only look at the specified directory level
            )
            if not (response.get("Contents") or response.get("CommonPrefixes")):
                raise ValueError(
                    f"Directory does not exist or is not accessible: {user}"
                )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDenied":
                raise ValueError(f"No permission to access directory: {user}")
            else:
                raise ValueError(f"Error accessing directory: {e}")

    def _get_full_path(self, path: str) -> str:
        """Convert relative/absolute path to full S3 key path under user directory.

        Args:
            path: Relative or absolute path

        Returns:
            Full S3 key path prefixed with user directory
        """
        if path.startswith("/"):
            full_path = os.path.normpath(path).strip("/")
        else:
            full_path = os.path.normpath(os.path.join(self.current_dir, path)).strip(
                "/"
            )
        full_path = self._handle_uplevel(full_path)
        return os.path.join(self.user, full_path).strip("/")

    def print_contents(self, path: str = "") -> None:
        """List contents of a directory under the user's directory.

        Args:
            path: Directory path to list (default: current directory)
        """
        contents = self.list_contents(path)

        if path.startswith("/"):
            full_path = os.path.normpath(path).strip("/")
        else:
            full_path = os.path.normpath(os.path.join(self.current_dir)).strip("/")
            full_path = self._handle_uplevel(full_path)

        print(f"Contents of /{full_path}:")
        for item in contents:
            rel_path = item["key"]
            if item["type"] == "directory":
                print(f"  📁 {rel_path}/")
            else:
                size = self._format_size(item["size"])
                print(f"  📄 {rel_path} ({size})")
