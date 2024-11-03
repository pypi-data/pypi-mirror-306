from pathlib import Path
from typing import Optional, Union, Dict
import torch
from .client.apis import load_torch_tensors


def load(
    model_path: Path, device: Optional[Union[int, str, torch.device]] = None
) -> Dict[str, torch.Tensor]:
    """
    Loads a model from a path into a torch tensor.

    Args:
        model_path (Path): Path to the model.
        device (Optional[Union[int, str, torch.device]]):
            Device to load the model on.

    Returns:
        torch_tensors (Dict[str, torch.Tensor]): Dictionary of torch tensors.
    """
    return load_torch_tensors([model_path], device=device)
