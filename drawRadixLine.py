"""Draw radial light rays."""

from __future__ import annotations

import math

import cv2
import numpy as np


def draw_radix_line(mask: np.ndarray, x: int, y: int, n: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = mask.copy()
    h, w = out.shape[:2]
    max_len = int(math.hypot(h, w))

    for _ in range(max(1, n * 4)):
        angle = rng.uniform(0.0, 2.0 * math.pi)
        length = rng.integers(max_len // 5, max_len)
        x2 = int(x + math.cos(angle) * length)
        y2 = int(y + math.sin(angle) * length)
        cv2.line(out, (int(x), int(y)), (x2, y2), 1.0, thickness=1)

    return out


# Backward-compatible name
drawRadixLine = draw_radix_line
