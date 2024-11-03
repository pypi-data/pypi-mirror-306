import uuid
import time
import os
import grpc
from grpc._channel import _InactiveRpcError
from typing import List, Dict, Optional, Union
from pathlib import Path
import torch
from contextlib import contextmanager
from outerport.client._torch_extensions import construct_torch_tensors, get_device_uuid

from outerport.generated.model_services_pb2 import (
    LoadToRamRequest,
    UnloadFromRamRequest,
    LoadToGpuRequest,
    OffloadToRamRequest,
    TensorTransportRequestResponse,
    GetModelStatusesRequest,
    GetModelStatusesResponse,
    ModelState,
    IpcTensorGroup,
    IpcTensorGroupList,
)

from outerport.generated.model_services_pb2_grpc import TensorTransportServiceStub
from outerport.client.utils import (
    get_cpp_tensor_memory_layout_by_device_id,
    hash_files,
    get_global_tensor_memory_layout,
    map_tensors_to_devices,
    allocate_cuda_memory_for_devices,
    get_ipc_gpu_memory_by_device_id,
    get_per_device_ipc_tensor_groups,
    DAEMON_PORT,
)


@contextmanager
def handle_grpc_connection():
    try:
        yield
    except _InactiveRpcError as e:
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            raise Exception(
                f"Failed to connect to the daemon. Please ensure the daemon is running on port {DAEMON_PORT}."
            )
        else:
            raise Exception(e.details())
    except grpc.RpcError as e:
        raise Exception(f"RPC connection error: {e}")


def create_tensor_transport_service_stub() -> TensorTransportServiceStub:
    """
    Creates a stub for the TensorTransportService.

    Returns:
        TensorTransportServiceStub: Stub for the TensorTransportService.
    """
    # Load address from env
    address = os.getenv("OUTERPORT_ADDRESS", "localhost")
    channel = grpc.insecure_channel(f"{address}:{DAEMON_PORT}")
    stub = TensorTransportServiceStub(channel)
    return stub


def load_torch_tensors(
    model_files: List[Path],
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
    device: Optional[Union[int, str, torch.device]] = None,
    cache_id: Optional[str] = None,
) -> Dict[str, torch.Tensor]:
    """
    Loads a model from a list of files into a torch tensor.

    Args:
        model_files (List[Path]): List of files to load.
        device_map (Optional[Union[str, Dict[str, Union[int, str, torch.device]]]]):
            Device map. Defaults to "auto".
        device (Optional[Union[int, str, torch.device]]): If provided,
            device_map is ignored. Defaults to None.
        cache_id (Optional[str]): Cache id. Defaults to None.

    Returns:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of torch tensors.
    """
    start_time = time.perf_counter()
    # Add a fail safe for users who pass in strings instead of Path objects
    model_files = [Path(file).resolve() for file in model_files]
    if cache_id is None:
        model_hash = hash_files(model_files)
        cache_id = model_hash

    # this is where the tensors are placed in a single contiguous chunk of memory
    global_tensor_memory_layout = get_global_tensor_memory_layout(model_files)
    # this is where the tensors are placed on each GPU, as well as the memory requirements
    tensor_memory_layout_by_device_id, memory_requirements_by_device_id = (
        map_tensors_to_devices(global_tensor_memory_layout, device_map, device)
    )

    # memory allocations and ipc handles are created for each GPU
    cuda_allocations_by_device_id = allocate_cuda_memory_for_devices(
        memory_requirements_by_device_id
    )
    ipc_gpu_memory_by_device_id = get_ipc_gpu_memory_by_device_id(
        cuda_allocations_by_device_id, memory_requirements_by_device_id
    )

    per_device_ipc_tensor_groups = {}
    for device_id, tensor_memory_layout in tensor_memory_layout_by_device_id.items():
        device_uuid = get_device_uuid(device_id)

        ipc_gpu_memory = ipc_gpu_memory_by_device_id[device_id]
        ipc_tensor_group = IpcTensorGroup(
            ipc_gpu_memory=ipc_gpu_memory, tensor_memory_layout=tensor_memory_layout
        )
        per_device_ipc_tensor_groups[device_uuid] = IpcTensorGroupList(
            list=[ipc_tensor_group]
        )

    stub = create_tensor_transport_service_stub()
    end_time = time.perf_counter()
    # print(f"preparing load to gpu request: {end_time - start_time}")

    load_to_gpu_request = LoadToGpuRequest(
        model_name=cache_id,
        model_files=[str(file) for file in model_files],
        per_device_ipc_tensor_groups=per_device_ipc_tensor_groups,
    )
    with handle_grpc_connection():
        load_to_gpu_response: TensorTransportRequestResponse = stub.LoadToGpu(
            load_to_gpu_request
        )
    if not load_to_gpu_response.success:
        raise Exception("Failed to load model to GPU")

    cpp_tensor_memory_layout_by_device_id = get_cpp_tensor_memory_layout_by_device_id(
        tensor_memory_layout_by_device_id
    )
    torch_tensors = construct_torch_tensors(
        cpp_tensor_memory_layout_by_device_id, cuda_allocations_by_device_id
    )

    return torch_tensors


def load_to_ram(model_files: List[Path], cache_id: Optional[str] = None) -> None:
    """
    Loads a model to RAM.

    Args:
        model_files (List[Path]): List of files to load.
        cache_id (Optional[str]): Cache id. Defaults to None.
    """
    # Add a fail safe for users who pass in strings instead of Path objects
    model_files = [Path(file).resolve() for file in model_files]
    if cache_id is None:
        model_hash = hash_files(model_files)
        cache_id = model_hash

    stub = create_tensor_transport_service_stub()
    load_to_ram_request = LoadToRamRequest(
        model_name=cache_id, model_files=[str(file) for file in model_files]
    )
    with handle_grpc_connection():
        load_to_ram_response: TensorTransportRequestResponse = stub.LoadToRam(
            load_to_ram_request
        )
    if not load_to_ram_response.success:
        raise Exception("Failed to load model to RAM")


def unload_from_ram(
    model_files: Optional[List[Path]] = None, cache_id: Optional[str] = None
) -> None:
    """
    Unloads a model from RAM.

    If cache_id is None, model_files must be provided.

    Args:
        model_files (Optional[List[Path]]): List of files to unload. Defaults to None.
        cache_id (Optional[str]): Cache id. Defaults to None.
    """
    # Add a fail safe for users who pass in strings instead of Path objects
    if cache_id is None:
        if model_files is None:
            raise ValueError("model_files must be provided if cache_id is None")
        model_files = [Path(file).resolve() for file in model_files]
        model_hash = hash_files(model_files)
        cache_id = model_hash

    stub = create_tensor_transport_service_stub()
    unload_from_ram_request = UnloadFromRamRequest(
        model_name=cache_id,
    )
    with handle_grpc_connection():
        unload_from_ram_response = stub.UnloadFromRam.with_call(unload_from_ram_request)
    if not unload_from_ram_response.success:
        raise Exception("Failed to unload model from RAM")


def offload_to_ram(
    torch_tensors: Dict[str, torch.Tensor], cache_id: Optional[str] = None
) -> str:
    """
    Offloads a model to RAM.

    Args:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of torch tensors.
        cache_id (Optional[str]): Cache id. Defaults to None.

    Returns:
        str: Cache id.
    """
    if cache_id is None:
        cache_id = uuid.uuid4().hex  # Generate a random hex string

    per_device_ipc_tensor_groups = get_per_device_ipc_tensor_groups(torch_tensors)

    stub = create_tensor_transport_service_stub()
    offload_to_ram_request = OffloadToRamRequest(
        model_name=cache_id, per_device_ipc_tensor_groups=per_device_ipc_tensor_groups
    )
    with handle_grpc_connection():
        offload_to_ram_response: TensorTransportRequestResponse = stub.OffloadToRam(
            offload_to_ram_request
        )
    if not offload_to_ram_response.success:
        raise Exception("Failed to offload tensors to RAM")

    return cache_id


def get_model_statuses() -> Dict[str, ModelState]:
    """
    Gets the statuses of all models.

    Returns:
        Dict[str, str]: Dictionary of model statuses.
    """
    stub = create_tensor_transport_service_stub()

    get_model_statuses_request = GetModelStatusesRequest()
    with handle_grpc_connection():
        get_model_statuses_response: GetModelStatusesResponse = stub.GetModelStatuses(
            get_model_statuses_request
        )

    model_statuses: Dict[str, ModelState] = {
        key: value for key, value in get_model_statuses_response.map.items()
    }

    return model_statuses
