from typing import Any, Dict, Union, Optional
import boto3
import os
import concurrent.futures
from tqdm.auto import tqdm


BYTES_PER_MB: int = 1024 * 1024
CHUNK_SIZE: int = 8 * BYTES_PER_MB
NUM_THREADS: int = min(32, (os.cpu_count() or 4) + 4)

COPY_CHUNK_SIZE: int = 32 * BYTES_PER_MB
COPY_NUM_THREADS: int = 32


def parallel_multipart_copy(
    source_bucket: str,
    source_key: str,
    dest_bucket: str,
    dest_key: str,
    chunk_size: int = COPY_CHUNK_SIZE,
    num_threads: int = COPY_NUM_THREADS,
    show_progress: bool = True,
) -> None:
    """Copy a large file in parallel parts using S3 Multipart Copy.

    Args:
        source_bucket (str): The name of the source S3 bucket.
        source_key (str): The key of the source object to copy.
        dest_bucket (str): The name of the destination S3 bucket.
        dest_key (str): The key of the destination object to copy to.
        chunk_size (int, optional): The size of each part in bytes. Defaults to CHUNK_SIZE.
        show_progress (bool, optional): Whether to show a progress bar. Defaults to True.
    """

    s3: Any = boto3.client("s3")

    def copy_part(
        part_number: int, start: int, end: int, upload_id: str, pbar: Optional[tqdm]
    ) -> Dict[str, Any]:
        response = s3.upload_part_copy(
            Bucket=dest_bucket,
            Key=dest_key,
            PartNumber=part_number,
            UploadId=upload_id,
            CopySource={"Bucket": source_bucket, "Key": source_key},
            CopySourceRange=f"bytes={start}-{end}",
        )

        if pbar:
            pbar.update(end - start + 1)

        return {"PartNumber": part_number, "ETag": response["CopyPartResult"]["ETag"]}

    try:
        # Get the size of the source object
        response: Dict[str, Any] = s3.head_object(Bucket=source_bucket, Key=source_key)
        file_size: int = response["ContentLength"]

        # Initiate the multipart upload
        mpu: Dict[str, Any] = s3.create_multipart_upload(
            Bucket=dest_bucket, Key=dest_key
        )
        upload_id: str = mpu["UploadId"]

        pbar = (
            tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Copying",
            )
            if show_progress
            else None
        )

        # Copy parts in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures: list[concurrent.futures.Future] = []
            for i in range(0, file_size, chunk_size):
                part_number: int = i // chunk_size + 1
                start: int = i
                end: int = min(i + chunk_size - 1, file_size - 1)
                futures.append(
                    executor.submit(copy_part, part_number, start, end, upload_id, pbar)
                )

            # Wait for all parts to be copied
            parts: list[Dict[str, Any]] = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        if pbar:
            pbar.close()

        # Complete the multipart upload
        s3.complete_multipart_upload(
            Bucket=dest_bucket,
            Key=dest_key,
            UploadId=upload_id,
            MultipartUpload={"Parts": sorted(parts, key=lambda x: x["PartNumber"])},
        )

    except Exception as e:
        # Attempt to abort the multipart upload if it was started
        if "upload_id" in locals():
            try:
                s3.abort_multipart_upload(
                    Bucket=dest_bucket, Key=dest_key, UploadId=upload_id
                )
            except Exception as abort_error:
                print(f"Error aborting multipart copy: {abort_error}")
                raise abort_error
        raise e
    finally:
        if "pbar" in locals() and pbar:
            pbar.close()


def parallel_multipart_download(
    bucket_name: str,
    key: str,
    destination: str,
    chunk_size: int = CHUNK_SIZE,
    num_threads: int = NUM_THREADS,
    version_id: Optional[str] = None,
    show_progress: bool = True,
) -> None:
    """Download a large file in parallel parts using S3 Multipart Download.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key (str): The key of the object to download.
        destination (str): The local path to save the downloaded file.
        chunk_size (int, optional): The size of each part in bytes. Defaults to CHUNK_SIZE.
        show_progress (bool, optional): Whether to show a progress bar. Defaults to True.
        version_id (Optional[str], optional): The version ID of the object to download. Defaults to None.
    """

    s3: Any = boto3.client("s3")

    def download_part(
        start: int, end: int, pbar: Optional[tqdm], file_handle: str
    ) -> None:
        range_header: str = f"bytes={start}-{end}"
        get_object_params = {"Bucket": bucket_name, "Key": key, "Range": range_header}
        if version_id:
            get_object_params["VersionId"] = version_id
        response: Dict[str, Any] = s3.get_object(**get_object_params)
        data: bytes = response["Body"].read()

        # Write the part directly to the correct offset in the file
        with open(file_handle, "r+b") as f:
            f.seek(start)
            f.write(data)
        # Update progress bar with the size of the part downloaded
        if pbar:
            pbar.update(len(data))

    try:
        head_object_params = {"Bucket": bucket_name, "Key": key}
        if version_id:
            head_object_params["VersionId"] = version_id
        response: Dict[str, Any] = s3.head_object(**head_object_params)
        file_size: int = response["ContentLength"]

        # Create the output file with the appropriate size
        with open(destination, "wb") as f:
            f.truncate(file_size)  # Preallocate the file size

        pbar = (
            tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading",
            )
            if show_progress
            else None
        )

        # Download the file in parallel parts
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures: list[concurrent.futures.Future] = []
            for i in range(0, file_size, chunk_size):
                start: int = i
                end: int = min(i + chunk_size - 1, file_size - 1)

                futures.append(
                    executor.submit(download_part, start, end, pbar, destination)
                )

            # Wait for all parts to be downloaded
            concurrent.futures.wait(futures)
    except Exception as e:
        raise e

    finally:
        if "pbar" in locals() and pbar:
            pbar.close()


def parallel_multipart_upload(
    local_file_path: str,
    bucket_name: str,
    key: str,
    chunk_size: int = CHUNK_SIZE,
    num_threads: int = NUM_THREADS,
    show_progress: bool = True,
) -> None:
    """Upload a large file in parallel parts using S3 Multipart Upload.

    Args:
        local_file_path (str): The path to the local file to upload.
        remote_file_name (str): The name to give the file in S3.
        chunk_size (int, optional): The size of each part in bytes. Defaults to CHUNK_SIZE.
        show_progress (bool, optional): Whether to show a progress bar. Defaults to True.
    """

    s3: Any = boto3.client("s3")

    def upload_part(
        part_number: int, start: int, end: int, pbar: Optional[tqdm]
    ) -> Dict[str, Any]:
        with open(local_file_path, "rb") as f:
            f.seek(start)
            data: bytes = f.read(end - start + 1)

            response: Dict[str, Any] = s3.upload_part(
                Bucket=bucket_name,
                Key=key,
                PartNumber=part_number,
                UploadId=mpu["UploadId"],
                Body=data,
            )

            if pbar:
                pbar.update(len(data))

            return {"PartNumber": part_number, "ETag": response["ETag"]}

    try:
        file_size: int = os.path.getsize(local_file_path)

        # Initiate the multipart upload
        mpu: Dict[str, Any] = s3.create_multipart_upload(Bucket=bucket_name, Key=key)
        pbar = (
            tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Uploading",
            )
            if show_progress
            else None
        )

        # Upload parts in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures: list[concurrent.futures.Future] = []
            for i in range(0, file_size, chunk_size):
                part_number: int = i // chunk_size + 1
                start: int = i
                end: int = min(i + chunk_size - 1, file_size - 1)
                futures.append(
                    executor.submit(upload_part, part_number, start, end, pbar)
                )

            # Wait for all parts to be uploaded
            parts: list[Dict[str, Any]] = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        if pbar:
            pbar.close()

        # Complete the multipart upload
        s3.complete_multipart_upload(
            Bucket=bucket_name,
            Key=key,
            UploadId=mpu["UploadId"],
            MultipartUpload={"Parts": sorted(parts, key=lambda x: x["PartNumber"])},
        )

    except Exception as e:
        # Attempt to abort the multipart upload if it was started
        if "mpu" in locals():
            try:
                s3.abort_multipart_upload(
                    Bucket=bucket_name, Key=key, UploadId=mpu["UploadId"]
                )
            except Exception as abort_error:
                print(f"Error aborting multipart upload: {abort_error}")
                raise abort_error
        raise e
    finally:
        if "progress_bar" in locals() and pbar:
            pbar.close()
