"""Drawing helpers for synthetic light masks."""

from __future__ import annotations

import numpy as np


def draw_circle(mask: np.ndarray, x: int, y: int, r: int) -> np.ndarray:
    out = mask.copy()
    h, w = out.shape[:2]
    yy, xx = np.indices((h, w))
    distance = np.sqrt((yy - x) ** 2 + (xx - y) ** 2)
    out[distance < r] = 1.0
    return out


# Backward-compatible name
drawCircle = draw_circle
