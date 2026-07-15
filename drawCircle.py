"""Drawing helpers for synthetic light masks."""

from __future__ import annotations

import cv2
import numpy as np


def draw_circle(mask: np.ndarray, x: int, y: int, r: int) -> np.ndarray:
    out = mask.copy()
    cv2.circle(out, (int(x), int(y)), int(r), 1.0, thickness=-1)
    return out


# Backward-compatible name
drawCircle = draw_circle
