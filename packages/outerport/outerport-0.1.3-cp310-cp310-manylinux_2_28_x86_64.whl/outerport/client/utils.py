import json
import torch
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional, Union
import ctypes

PyCapsule_New = ctypes.pythonapi.PyCapsule_New
PyCapsule_New.restype = ctypes.py_object

from outerport.client._torch_extensions import (
    get_device_uuid,
    allocate_cuda_memory,
    free_cuda_memory,
    get_ipc_handle,
)
import xxhash
from concurrent.futures import ThreadPoolExecutor

from outerport.generated.model_services_pb2 import (
    TensorMemoryLayout,
    TensorMetadata,
    IpcGpuMemory,
    IpcTensorGroup,
    IpcTensorGroupList,
)

MEM_THRESHOLD = 0.99
DAEMON_PORT = 50051
METADATA_HEADER = "__metadata__"


def get_cpp_tensor_memory_layout_by_device_id(tensor_memory_layout_by_device_id):
    """
    convert TensorMetadata grpc object to tuple of (dtype, shape, offsets) so that it can be passed to C++ extension
    """
    cpp_tensor_memory_layout_by_device_id = {
        device_id: {
            tensor_name: (
                tensor_metadata.dtype,
                tensor_metadata.shape,
                tensor_metadata.offsets,
            )
            for tensor_name, tensor_metadata in tensor_memory_layout.map.items()
        }
        for device_id, tensor_memory_layout in tensor_memory_layout_by_device_id.items()
    }

    return cpp_tensor_memory_layout_by_device_id


def get_cpp_cuda_ptr(cuda_memory_address: int):
    return PyCapsule_New(ctypes.c_void_p(int(cuda_memory_address)), None, None)


def hash_file(file_path: Path) -> Tuple[Path, str]:
    """
    Hashes a file path and returns the file path and the hash.

    Args:
        file_path (Path): File path.

    Returns:
        Tuple[Path, str]: File path and the hash.
    """
    hasher = xxhash.xxh128(seed=0)
    file_path = Path(file_path)

    hasher.update(file_path.resolve().as_posix().encode(encoding="utf-8"))
    hasher.update(str(int(file_path.stat().st_mtime)).encode(encoding="utf-8"))

    return (file_path, hasher.hexdigest())


def hash_files(file_paths: List[Path]) -> str:
    """
    Hashes a list of file paths and returns a combined hash.

    Args:
        file_paths (List[Path]): List of file paths.

    Returns:
        str: Hash.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(hash_file, file_paths))
    hash_list = [file_hash for _, file_hash in results]
    hash_list.sort()
    # Convert back into int (from hex)
    hash_list = [int(hash, 16) for hash in hash_list]
    xor_hashes = hash_list[0]
    for hash in hash_list[1:]:
        xor_hashes ^= hash
    return format(xor_hashes, "x")


from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TensorInfo(BaseModel):
    dtype: str
    shape: List[int]
    data_offsets: Tuple[int, int]
    extra: Dict[str, Any] = Field(default_factory=dict, alias="__extra__")


class SafetensorHeader(BaseModel):
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="__metadata__")
    tensors: Dict[str, TensorInfo] = Field(default_factory=dict)


def read_safetensor_header(file_path: Path) -> SafetensorHeader:
    """
    Reads the safetensor header and returns the header.

    Safetensors header is a dict like:
    `{"TENSOR_NAME": {"dtype": "F16", "shape": [1, 16, 256], "data_offsets": [BEGIN, END]}, "NEXT_TENSOR_NAME": {...}, ...}`
    with a special key `__metadata__` that contains arbitrary metadata about the model.

    Args:
        file_path (Path): File path.

    Returns:
        SafetensorHeader: Safetensor header.
    """
    file_path = Path(file_path)

    with open(file_path, "rb") as f:
        header_size = int.from_bytes(f.read(8), "little")
        header_dict = json.loads(f.read(header_size))
        return SafetensorHeader(
            __metadata__=header_dict.pop(METADATA_HEADER, {}),
            tensors={k: TensorInfo(**v) for k, v in header_dict.items()},
        )


def get_global_tensor_memory_layout(file_paths: List[Path]) -> TensorMemoryLayout:
    """
    Gets the global tensor memory layout.

    The global tensor memory layout is a dictionary that maps the tensor name to the
    tensor metadata- which contains the dtype, shape, and offsets (start and end) of the tensor.

    Args:
        file_paths (List[Path]): List of file paths.

    Returns:
        TensorMemoryLayout: Global tensor memory layout.
    """
    global_tensor_memory_layout = TensorMemoryLayout()
    global_running_offset = 0
    for file_path in file_paths:
        file_size = 0
        try:
            header = read_safetensor_header(file_path)
            for tensor_name, tensor_info in header.tensors.items():
                offsets = tensor_info.data_offsets
                global_tensor_memory_layout.map[tensor_name].CopyFrom(
                    TensorMetadata(
                        dtype=tensor_info.dtype,
                        shape=tensor_info.shape,
                        offsets=[
                            global_running_offset + offsets[0],
                            global_running_offset + offsets[1],
                        ],
                    )
                )
                file_size += offsets[1] - offsets[0]
            global_running_offset += file_size
        except Exception as e:
            # TODO: Better error handling here?
            print(f"Error processing {file_path}: {e}")

    return global_tensor_memory_layout


def filter_global_tensor_memory_layout(
    global_tensor_memory_layout: TensorMemoryLayout,
    device_map: Dict[str, Union[int, str, torch.device]],
) -> TensorMemoryLayout:
    """
    Filters the global tensor memory layout to only include tensors that are present in the device map.

    Args:
        global_tensor_memory_layout (TensorMemoryLayout): Global tensor memory layout.
        device_map (Dict[str, Union[int, str, torch.device]]): Device map.

    Returns:
        TensorMemoryLayout: Filtered tensor memory layout.
    """
    filtered_tensor_memory_layout = TensorMemoryLayout()
    for tensor_name, tensor_metadata in global_tensor_memory_layout.map.items():
        if tensor_name in device_map:
            filtered_tensor_memory_layout.map[tensor_name].CopyFrom(tensor_metadata)
    return filtered_tensor_memory_layout


def get_device_id(device: Union[int, str, torch.device]) -> int:
    """
    Gets the device id from a device.

    Args:
        device (Union[int, str, torch.device]): Device.

    Returns:
        int: Device id.
    """
    if isinstance(device, str):
        device = int(device)
    if isinstance(device, torch.device):
        device = device.index
    return device


def get_device_map_for_device_id(
    device_map: Dict[str, Union[int, str, torch.device]], device_id: int
) -> Dict[str, Union[int, str, torch.device]]:
    """
    Gets the device map for a particular device id.

    Args:
        device_map (Dict[str, Union[int, str, torch.device]]): Device map.
        device_id (int): Device id.

    Returns:
        Dict[int, Union[int, str, torch.device]]: Device map for the device id.
    """
    device_map_for_device_id = {}
    for name, device in device_map.items():
        if get_device_id(device) == device_id:
            device_map_for_device_id[name] = device_id
    return device_map_for_device_id


def map_tensors_to_devices(
    global_tensor_memory_layout: TensorMemoryLayout,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
    device: Optional[Union[int, str, torch.device]] = None,
) -> Tuple[Dict[int, TensorMemoryLayout], Dict[int, int]]:
    """
    Maps the global tensor memory layout to the devices.

    Args:
        global_tensor_memory_layout (TensorMemoryLayout): Global tensor memory layout.
        device_map (Optional[Union[str, Dict[str, Union[int, str, torch.device]]]]):
            Device map. Defaults to "auto".
        device (Optional[Union[int, str, torch.device]]): If provided, device_map is ignored.
            Defaults to None.

    Returns:
        Tuple[Dict[int, TensorMemoryLayout], Dict[int, int]]:
            Tensor memory layout by device id and memory requirement by device id.
    """

    # TODO: add support for automatic sharding model across multiple GPUs. Currently model is placed on
    # the first GPU with enough memory.
    # This is a pretty deep topic since how you place tensors on different GPUs can
    # affect performance and there are also concepts like no-split modules

    tensor_memory_layout_by_device_id: Dict[int, TensorMemoryLayout] = {}
    memory_requirement_by_device_id: Dict[int, int] = {}
    device_count = torch.cuda.device_count()

    if device is not None:
        device_id = get_device_id(device)
        tensor_memory_layout_by_device_id[device_id] = global_tensor_memory_layout
        memory_requirement_by_device_id[device_id] = sum(
            [
                tensor_metadata.offsets[1] - tensor_metadata.offsets[0]
                for tensor_metadata in global_tensor_memory_layout.map.values()
            ]
        )
        free_mem, _ = torch.cuda.mem_get_info(device_id)
        if free_mem < memory_requirement_by_device_id[device_id]:
            raise Exception(
                f"Not enough memory on device {device_id} to load the model. "
                f"Required free memory: {int(memory_requirement_by_device_id[device_id] / MEM_THRESHOLD)} bytes."
            )
    elif device_map == "auto":
        model_size = sum(
            [
                tensor_metadata.offsets[1] - tensor_metadata.offsets[0]
                for tensor_metadata in global_tensor_memory_layout.map.values()
            ]
        )
        suitable_device = None

        for i in range(device_count):
            free_mem, _ = torch.cuda.mem_get_info(i)
            if free_mem * MEM_THRESHOLD > model_size:
                suitable_device = i
                break

        if suitable_device is None:
            raise Exception(
                "No GPU with sufficient memory found. "
                f"Required free memory: {int(model_size / MEM_THRESHOLD)} bytes."
            )

        tensor_memory_layout_by_device_id[suitable_device] = global_tensor_memory_layout
        memory_requirement_by_device_id[suitable_device] = model_size
    elif isinstance(device_map, Dict):
        for i in range(device_count):
            device_map_for_device_id = get_device_map_for_device_id(device_map, i)

            if len(device_map_for_device_id) == 0:
                continue

            filtered_tensor_memory_layout = filter_global_tensor_memory_layout(
                global_tensor_memory_layout, device_map_for_device_id
            )
            tensor_memory_layout_by_device_id[i] = filtered_tensor_memory_layout

            memory_requirement_by_device_id[i] = sum(
                [
                    tensor_metadata.offsets[1] - tensor_metadata.offsets[0]
                    for tensor_metadata in filtered_tensor_memory_layout.map.values()
                ]
            )
            free_mem, _ = torch.cuda.mem_get_info(i)
            if free_mem < memory_requirement_by_device_id[i]:
                raise Exception(
                    f"Not enough memory on device {i} to load the model. "
                    f"Required free memory: {int(memory_requirement_by_device_id[i] / MEM_THRESHOLD)} bytes."
                )
    else:
        raise ValueError(
            f"Invalid device map type ({type(device_map)}), expected str or Dict"
        )

    return tensor_memory_layout_by_device_id, memory_requirement_by_device_id


def allocate_cuda_memory_for_devices(
    memory_requirement_by_device_id: Dict[int, int],
) -> Dict[int, int]:
    """
    Allocates CUDA memory for each device based on the memory requirements.

    Args:
        memory_requirement_by_device_id (Dict[int, int]): Memory requirements by device id.

    Returns:
        Dict[int, int]: CUDA pointers by device id.
    """
    cuda_pointer_by_device_id = {}
    for device_id, memory_size in memory_requirement_by_device_id.items():
        cuda_pointer_by_device_id[device_id] = allocate_cuda_memory(
            device_id, memory_size
        )

    return cuda_pointer_by_device_id


def get_ipc_gpu_memory_by_device_id(
    cuda_pointer_by_device_id: Dict[int, int],
    memory_requirement_by_device_id: Dict[int, int],
) -> Dict[int, IpcGpuMemory]:
    """
    Gets the IPC handles for each device.

    Args:
        cuda_pointer_by_device_id (Dict[int, int]): CUDA pointers by device id.
        memory_requirement_by_device_id (Dict[int, int]): Memory requirements by device id.

    Returns:
        Dict[int, IpcGpuMemory]: IPC handles by device id.
    """
    ipc_gpu_memory_by_device_id: Dict[int, IpcGpuMemory] = {}
    for device_id, ptr in cuda_pointer_by_device_id.items():
        ipc_handle = get_ipc_handle(device_id, ptr)
        ipc_gpu_memory_by_device_id[device_id] = IpcGpuMemory(
            ipc_handle=ipc_handle, size=memory_requirement_by_device_id[device_id]
        )

    return ipc_gpu_memory_by_device_id


def get_per_device_ipc_tensor_groups(
    torch_tensors: Dict[str, torch.Tensor],
) -> Dict[str, IpcTensorGroupList]:
    """
    Gets the IPC tensor groups from the torch tensors. PyTorch manages its own CUDA memory pool.
    Figures out which memory segment (obtained via cudaMalloc) and offset within that segment each tensor belongs to.

    Args:
        torch_tensors (Dict[str, torch.Tensor]): Torch tensors.

    Returns:
        per_device_ipc_tensor_groups (Dict[str, IpcTensorGroupList]): IPC tensor groups by device uuid.
    """

    tensors_by_base_address_by_device_id: Dict[int, Dict[int, TensorMemoryLayout]] = {}
    segment_sizes_by_base_address_by_device_id: Dict[int, Dict[int, int]] = {}

    for tensor_name, tensor in torch_tensors.items():
        assert tensor.is_cuda
        device_id = tensor.device.index  # Extract the device index

        # important to do .contiguous() here to ensure tensor is contiguous in memory
        tensor = tensor.contiguous()
        cuda_memory_address = tensor.data_ptr()

        base_address = None
        segment_size = None
        memory_snapshot = torch.cuda.memory._snapshot(device_id)
        # find which memory segment the tensor belongs to
        for segment in memory_snapshot["segments"]:
            if (
                segment["address"] <= cuda_memory_address
                and segment["address"] + segment["total_size"] > cuda_memory_address
            ):
                base_address = segment["address"]
                segment_size = segment["total_size"]
                break
        if base_address is None or segment_size is None:
            raise ValueError(f"Could not find base address for tensor {tensor_name}")

        offset_from_base = cuda_memory_address - base_address

        if device_id not in tensors_by_base_address_by_device_id:
            tensors_by_base_address_by_device_id[device_id] = {}
            segment_sizes_by_base_address_by_device_id[device_id] = {}

        if base_address not in tensors_by_base_address_by_device_id[device_id]:
            tensors_by_base_address_by_device_id[device_id][base_address] = (
                TensorMemoryLayout(map={})
            )
            segment_sizes_by_base_address_by_device_id[device_id][base_address] = (
                segment_size
            )

        tensors_by_base_address_by_device_id[device_id][base_address].map[
            tensor_name
        ].CopyFrom(
            TensorMetadata(
                dtype=str(tensor.dtype),
                shape=tensor.shape,
                offsets=[offset_from_base, offset_from_base + tensor.nbytes],
            )
        )

    per_device_ipc_tensor_groups: Dict[str, IpcTensorGroupList] = {}
    for device_id, base_addresses in tensors_by_base_address_by_device_id.items():
        device_uuid = get_device_uuid(device_id)
        ipc_tensor_groups = []
        for base_address, tensor_memory_layout in base_addresses.items():
            cuda_ptr = get_cpp_cuda_ptr(base_address)
            ipc_handle = get_ipc_handle(device_id, cuda_ptr)

            ipc_gpu_memory = IpcGpuMemory(
                ipc_handle=ipc_handle,
                size=segment_sizes_by_base_address_by_device_id[device_id][
                    base_address
                ],
            )

            ipc_tensor_group = IpcTensorGroup(
                ipc_gpu_memory=ipc_gpu_memory,
                tensor_memory_layout=tensor_memory_layout,
            )
            ipc_tensor_groups.append(ipc_tensor_group)

        per_device_ipc_tensor_groups[device_uuid] = IpcTensorGroupList(
            list=ipc_tensor_groups
        )

    return per_device_ipc_tensor_groups


def warmup_cuda() -> None:
    """
    Warmup the CUDA memory.
    """
    device_count = torch.cuda.device_count()
    FRACTION = 0.5
    for i in range(device_count):
        free_mem, _ = torch.cuda.mem_get_info(i)
        cuda_ptr = allocate_cuda_memory(i, int(free_mem * FRACTION - 0.5))
        free_cuda_memory(i, cuda_ptr)
