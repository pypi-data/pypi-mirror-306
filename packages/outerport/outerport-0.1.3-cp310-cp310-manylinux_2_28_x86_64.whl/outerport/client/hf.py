from typing import Union, Dict, Optional, List
from pathlib import Path
import torch
from concurrent.futures import ThreadPoolExecutor
from accelerate import init_empty_weights
from accelerate.utils import set_module_tensor_to_device, find_tied_parameters
from transformers import AutoConfig, AutoModelForCausalLM

from outerport.client.apis import load_torch_tensors


def map_named_buffers_to_devices(
    model: torch.nn.Module,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
) -> None:
    """
    Maps the named buffers of a PyTorch model to specified devices.

    This function iterates through all named buffers in the model and moves them
    to the appropriate device based on the provided device_map.

    Args:
        model (torch.nn.Module): The PyTorch model whose buffers need to be mapped.
        device_map (Union[str, Dict[str, Union[int, str, torch.device]]], optional):
            Specifies how to map model parts to devices. Defaults to 'auto'.
            If a string, it should be 'auto' (currently treated as 'cuda').
            If a dict, keys are module names and values are target devices.

    Note:
        This function allocates new memory for the buffers on the specified devices (usually small tensors).
    """

    for full_name, _ in model.named_buffers(recurse=True):
        # eg: "model.layers.0.self_attn.rotary_emb", "."", "inv_freq"
        submodule_name, _, buffer_name = full_name.rpartition(".")
        submodule = model.get_submodule(submodule_name)
        buffer = submodule._buffers[buffer_name]
        if buffer is None:
            continue
        if isinstance(device_map, dict):
            for group_name, device in device_map.items():
                # device_map doesn't always contain the full name, so we need to check for a prefix match
                if full_name.startswith(group_name):
                    device = device_map[full_name]
                    submodule._buffers[buffer_name] = buffer.to(device=device)
                    continue
        else:
            submodule._buffers[buffer_name] = buffer.to(device="cuda")


# TODO: (10/21/24, Allen): turn this into a HF compatible interface (like AutoModelForCausalLM.from_pretrained)
# Right this function looks for safetensors files within the provided path - it's missing looking into snapshots/ folder, etc.
def load_llm(
    path: Path,
    device_map: Optional[Union[str, Dict[str, Union[int, str, torch.device]]]] = "auto",
) -> AutoModelForCausalLM:
    """
    Load a large language model from path containing safetensors files and config.json.

    Args:
        path (Path): Directory containing the model files.
        device_map (Union[str, Dict[str, Union[int, str, torch.device]]], optional):
            Specifies how to map model parts to devices. Defaults to 'auto'.

    Returns:
        model (AutoModelForCausalLM): Loaded and initialized language model.
    """

    safetensor_files = list(sorted(Path(path).glob("*.safetensors")))

    # load the model without initializing the weights - could take 0.4 secs for llama3.1 8b
    def load_empty_model():
        config = AutoConfig.from_pretrained(path)
        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config).to(config.torch_dtype)

        model.tie_weights()
        map_named_buffers_to_devices(model, device_map)

        # find all tied parameters
        tied_parameters = find_tied_parameters(model)

        return model, tied_parameters

    with ThreadPoolExecutor() as executor:
        state_dict_future = executor.submit(
            load_torch_tensors, safetensor_files, device_map
        )
        model_future = executor.submit(load_empty_model)

        (model, tied_parameters), state_dict = executor.map(
            lambda f: f.result(), [model_future, state_dict_future]
        )

    with torch.no_grad():
        for name, tensor in state_dict.items():
            set_module_tensor_to_device(model, name, tensor.device, tensor)

        model_state_dict = model.state_dict()
        for group in tied_parameters:
            reference_tensor = None
            # for each tied group, find a reference tensor that is not a meta tensor
            for name in group:
                if model_state_dict[name].device != torch.device("meta"):
                    reference_tensor = model_state_dict[name]
            if reference_tensor is None:
                raise ValueError(
                    f"No reference tensor found for the tied parameters group {group}"
                )
            # set all tensors in the group to the device of the reference tensor
            for name in group:
                if name != reference_tensor.name:
                    set_module_tensor_to_device(
                        model, name, reference_tensor.device, reference_tensor
                    )

    model.eval()

    return model
