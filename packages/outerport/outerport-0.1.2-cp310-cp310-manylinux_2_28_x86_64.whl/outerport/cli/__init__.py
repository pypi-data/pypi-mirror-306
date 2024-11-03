import sys
import enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from outerport.constants import YELLOW, MAGENTA, GREEN, RED, RESET
import math
from pathlib import Path
import time
from tqdm import tqdm
from datetime import datetime, timedelta
from typing import Dict
import outerport.client.apis
from outerport.generated.model_services_pb2 import (
    ModelState,
    ModelStatus,
)

RAM_SIZE_GB = 5

MODEL_STATUS_COLUMNS = {
    "model_id": 36,
    "tag": 8,
    "quant": 8,
    "status": 8,
    "size": 14,
    "last_used": 15,
}


def format_last_used(last_used: Optional[datetime]) -> str:
    """
    Format the last used time

    Args:
        last_used (Optional[datetime]): The last used time

    Returns:
        str: The formatted last used time
    """

    if not last_used:
        return "-"

    now = datetime.now()
    diff = now - last_used

    if diff < timedelta(minutes=1):
        return f"{diff.seconds}s ago"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f'{minutes} min{"s" if minutes > 1 else ""} ago'
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f'{hours} hr{"s" if hours > 1 else ""} ago'
    elif diff < timedelta(days=30):
        days = diff.days
        return f'{days} day{"s" if days > 1 else ""} ago'
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f'{months} month{"s" if months > 1 else ""} ago'
    else:
        years = diff.days // 365
        return f'{years} year{"s" if years > 1 else ""} ago'


def format_size(size: int) -> str:
    """
    Format the size (bytes)

    Args:
        size (int): The size in bytes

    Returns:
        str: The formatted size
    """
    if size < 1024:
        return f"{size:.2f} bytes"
    elif size < 1024**2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024**3:
        return f"{size / 1024 ** 2:.2f} MB"
    else:
        return f"{size / 1024 ** 3:.2f} GB"


class OuterportMode(str, enum.Enum):
    """Outerport CLI modes"""

    MODEL = "model"
    PULL = "pull"
    RM = "rm"


class QuantizationType(str, enum.Enum):
    """Quantization type"""

    INT8 = "int8"
    INT4 = "int4"
    FP32 = "fp32"
    FP16 = "fp16"


class ModelArgs(BaseModel):
    show_all: bool = False
    model: Optional[str] = None


class PullArgs(BaseModel):
    model: str
    quant: Optional[QuantizationType] = None
    disk: bool = False  # New flag for pulling to disk only


class RmArgs(BaseModel):
    model: str
    wipe: bool = False  # Optional flag to wipe the model from disk


class CLIArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    mode: OuterportMode
    model_args: Optional[ModelArgs] = None
    pull_args: Optional[PullArgs] = None
    rm_args: Optional[RmArgs] = None


class OuterportCLI:
    def __init__(self) -> None:
        self.commands = {
            OuterportMode.MODEL: self.handle_model,
            OuterportMode.PULL: self.handle_pull,
            OuterportMode.RM: self.handle_rm,
        }

    def parse_args(self, args: List[str]) -> CLIArgs:
        """
        Parse the CLI arguments

        Args:
            args (List[str]): The CLI arguments

        Returns:
            CLIArgs: The parsed CLI arguments
        """
        if not args:
            raise ValueError("No command provided")

        try:
            mode = OuterportMode(args[0])
        except ValueError:
            raise ValueError(f"Invalid command: {args[0]}")

        if mode == OuterportMode.MODEL:
            if len(args) > 1:
                if args[1] == "--show-all":
                    return CLIArgs(mode=mode, model_args=ModelArgs(show_all=True))
                else:
                    return CLIArgs(mode=mode, model_args=ModelArgs(model=args[1]))
            return CLIArgs(mode=mode, model_args=ModelArgs())
        elif mode == OuterportMode.PULL:
            if len(args) < 2:
                raise ValueError("Model ID is required for pull command")
            pull_args = PullArgs(model=args[1])
            if "--quant" in args:
                quant_index = args.index("--quant")
                if quant_index + 1 < len(args):
                    pull_args.quant = QuantizationType(args[quant_index + 1])
            if "--disk" in args:
                pull_args.disk = True
            return CLIArgs(mode=mode, pull_args=pull_args)
        elif mode == OuterportMode.RM:
            if len(args) < 2:
                raise ValueError("Model ID is required for rm command")
            rm_args = RmArgs(model=args[1])
            if "--wipe" in args:
                rm_args.wipe = True
            return CLIArgs(mode=mode, rm_args=rm_args)
        else:
            raise ValueError(f"Invalid command: {args[0]}")

    def get_model_statuses(self, show_all: bool = False) -> Dict[str, ModelState]:
        """
        Get the model statuses

        Args:
            show_all (bool): Whether to show all models

        Returns:
            Dict[str, ModelState]: The model statuses
        """
        models = outerport.client.apis.get_model_statuses()

        if not show_all:
            models = {k: v for k, v in models.items() if v.status != ModelStatus.REMOTE}

        # Sort models by last used time
        models = sorted(models.items(), key=lambda x: x[1].last_used, reverse=True)
        models = dict(models)

        return models

    def print_model_info(self, model_id: str, model: ModelState) -> None:
        """
        Print the model info

        Args:
            model_id (str): The model ID to print
            model (ModelState): The model state object
        """
        last_used = format_last_used(datetime.fromtimestamp(model.last_used))
        model_tag = "na"
        model_quant = "na"

        model_info = {
            "model_id": model_id,
            "tag": model_tag,
            "quant": model_quant,
            "status": ModelStatus.Name(model.status),
            "size": format_size(model.model_size),
            "last_used": last_used,
        }

        for column, width in MODEL_STATUS_COLUMNS.items():
            print(f"{model_info[column]:<{width}}", end="")
        print()

    def print_header(self) -> None:
        """
        Print the header for the model status table
        """
        for column, width in MODEL_STATUS_COLUMNS.items():
            print(f"{column.upper().replace('_', ' '):<{width}}", end="")
        print()

    def parse_size(self, size_str: str) -> float:
        # Remove any whitespace and convert to lowercase
        size_str = size_str.strip().lower()

        # Check for 'gb' or 'mb' in the string
        if "gb" in size_str:
            return float(size_str.rstrip("gb"))
        elif "mb" in size_str:
            return float(size_str.rstrip("mb")) / 1024
        else:
            # If no unit is specified, assume GB
            return float(size_str)

    def handle_model(self, args: ModelArgs) -> None:
        if args.model:
            models = self.get_model_statuses(args.show_all)
            if args.model not in models:
                print(f"Error: Model '{args.model}' not found.")
                return

            model = models[args.model]
            self.print_header()
            self.print_model_info(args.model, model)
        else:
            models = self.get_model_statuses(args.show_all)
            self.print_header()

            if models:
                for id, model in models.items():
                    self.print_model_info(id, model)
            else:
                print("No models found.")

    def handle_pull(self, args: PullArgs) -> None:
        raise NotImplementedError("Registry not implemented")

    def handle_rm(self, args: RmArgs) -> None:
        outerport.client.apis.unload_from_ram(cache_id=args.model)

        if args.wipe:
            raise NotImplementedError("Wiping not implemented")

    def print_help(self) -> None:
        print("Usage:")
        print(f"  outerport {OuterportMode.MODEL.value} [--show-all]")
        print(f"  outerport {OuterportMode.MODEL.value} <model_id>")
        # print(
        #     f"  outerport {OuterportMode.PULL.value} <model_id> [--quant <quantization>] [--disk]"
        # )
        print(f"  outerport {OuterportMode.RM.value} <model_id> [--wipe]")

    def run(self, args: List[str]) -> None:
        try:
            parsed_args = self.parse_args(args)
            self.commands[parsed_args.mode](
                getattr(parsed_args, f"{parsed_args.mode.value}_args")
            )
        except ValueError as e:
            print(f"Error: {str(e)}")
            self.print_help()


def main():
    cli = OuterportCLI()
    cli.run(sys.argv[1:])
