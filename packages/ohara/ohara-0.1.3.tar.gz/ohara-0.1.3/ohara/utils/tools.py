from __future__ import annotations

from typing import Any
from collections.abc import Iterable
from dataclasses import dataclass

import torch


def auto_accelerator(device: str | None = None) -> torch.device:
    """
    Automatically selects and returns a torch device. If a device is specified, it validates and returns the specified device.
    If no device is specified, it checks for available devices in the order of CUDA, MPS (Apple Silicon GPUs), and defaults to CPU if none are available.

    Args:
        device (str, optional): The name of the device to use. Can be 'cpu', 'cuda', 'mps', or None. Defaults to None.

    Returns:
        torch.device: The selected torch device.

    Raises:
        AssertionError: If the device passed is not None, 'cpu', 'cuda', or 'mps'.
    """
    if isinstance(device, torch.device):
        return device
    if isinstance(device, str):
        return torch.device(device)
    assert device is None, "Pass Valid Device"
    accelerator = "cpu"
    if torch.cuda.is_available():
        accelerator = "cuda"
    if torch.backends.mps.is_built():
        accelerator = "mps"
    return torch.device(accelerator)


def build_mask(seq_len, sliding_window_attention=False, window_size=1):
    mask = torch.full((seq_len, seq_len), float("-inf"))

    assert window_size != 0, "window_size cannot be 0"
    if not sliding_window_attention:
        window_size = seq_len

    row_indices = torch.arange(seq_len).unsqueeze(-1)
    col_indices = torch.arange(seq_len)
    distance = row_indices - col_indices

    mask[(distance >= 0) & (distance <= (window_size - 1))] = 0

    mask = mask.unsqueeze(0).unsqueeze(0)
    return mask


@dataclass
class BetterCycle:
    """
    A data class that implements a better cycle iterator over any iterable. It cycles through the iterable indefinitely.

    Attributes:
        iterable (Iterable): The iterable to cycle through.
        idx (int): The current cycle index (how many times the iterable has been cycled through). Defaults to 0.
        _iterator (Iterable, optional): The iterator generated from the iterable. This is used to keep track of the current iteration state. Defaults to None.
    """

    iterable: Iterable
    idx: int = 0
    _iterator: Iterable = None

    def __iter__(self) -> BetterCycle:
        return self

    def __next__(self) -> Any:
        if self._iterator is None:
            self._iterator = iter(self.iterable)

        try:
            return next(self._iterator)
        except StopIteration:
            self.idx += 1
            self._iterator = iter(self.iterable)
            return next(self._iterator)


if __name__ == "__main__":
    data = [0, 1, 2, 3]

    cyc = BetterCycle(data)

    for idx, item in enumerate(cyc):
        print(f"{idx}: {item}")
        if idx == 7:
            break
        seq_len = 7
    # mask = build_mask(seq_len, sliding_window_attention=True, window_size=1)
    # print(mask)
