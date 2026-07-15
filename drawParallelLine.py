"""Draw random parallel lines."""

from __future__ import annotations

import math

import cv2
import numpy as np


def draw_parallel_line(mask: np.ndarray, angle: float, n: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = mask.copy()
    h, w = out.shape[:2]

    dx = math.cos(angle)
    dy = math.sin(angle)
    nx = -dy
    ny = dx

    for _ in range(max(1, n * 2)):
        offset = rng.uniform(-max(h, w), max(h, w))
        cx = w / 2 + nx * offset
        cy = h / 2 + ny * offset
        p1 = (int(cx - dx * 2 * max(h, w)), int(cy - dy * 2 * max(h, w)))
        p2 = (int(cx + dx * 2 * max(h, w)), int(cy + dy * 2 * max(h, w)))
        cv2.line(out, p1, p2, 1.0, thickness=1)

    return out


# Backward-compatible name
drawParallelLine = draw_parallel_line
