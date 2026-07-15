"""Style transformation helpers."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def _ordfilt2_channel(channel: np.ndarray, order: int, size: int) -> np.ndarray:
    pad = size // 2
    padded = cv2.copyMakeBorder(channel, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    windows = sliding_window_view(padded, (size, size))
    flat = windows.reshape(channel.shape[0], channel.shape[1], -1)
    kth = np.partition(flat, order - 1, axis=2)[..., order - 1]
    return kth.astype(channel.dtype)


def change_style(image: np.ndarray) -> np.ndarray:
    """Apply order-statistic filtering like the original OMPC implementation."""
    pixels = image.shape[0] * image.shape[1]
    kernel = 3 if pixels < 2_000_000 else 5

    out = np.empty_like(image)
    for ch in range(3):
        out[..., ch] = _ordfilt2_channel(image[..., ch], order=5, size=kernel)
    return out


# Backward-compatible name
changeStyle = change_style
