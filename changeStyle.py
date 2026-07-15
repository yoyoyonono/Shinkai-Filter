"""Style transformation helpers."""

from __future__ import annotations

import cv2
import numpy as np


def change_style(image: np.ndarray) -> np.ndarray:
    """Apply a median filter similar to the original MATLAB pipeline."""
    pixels = image.shape[0] * image.shape[1]
    kernel = 3 if pixels < 2_000_000 else 5
    return cv2.medianBlur(image, kernel)


# Backward-compatible name
changeStyle = change_style
