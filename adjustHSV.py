"""HSV adjustment helpers."""

from __future__ import annotations

import cv2
import numpy as np


def adjust_hsv(image: np.ndarray, saturation_boost: float = 0.2, value_boost: float = 0.35) -> np.ndarray:
    """Increase saturation and brightness in HSV space."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] + saturation_boost * 255.0, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] + value_boost * 255.0, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


# Backward-compatible name
adjustHSV = adjust_hsv
