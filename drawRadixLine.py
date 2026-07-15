"""Draw radial light rays."""

from __future__ import annotations

import math

import numpy as np


def draw_radix_line(mask: np.ndarray, x: int, y: int, n: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = mask.copy()
    h, w = out.shape[:2]

    line_count = max(1, 4 * int(n))
    p1 = rng.permutation(np.arange(1, 91))
    p2_size = max(line_count, int(math.floor(50 * n)))
    p2 = rng.permutation(np.arange(1, p2_size + 1))
    p3 = rng.permutation(np.arange(1, h + 1))

    line_data = np.zeros((line_count, 3), dtype=np.float32)
    for i in range(line_count):
        line_data[i, 0] = (p1[i % len(p1)] + (i // 4) * 90) * math.pi / 180.0
        line_data[i, 1] = p2[i % len(p2)]
        line_data[i, 2] = p3[i % len(p3)] + w

    for i in range(h):
        for j in range(w):
            newx = (i + 1) - x
            newy = (j + 1) - y
            if newx == 0:
                angle = math.pi / 2 if newy >= 0 else 3 * math.pi / 2
            else:
                angle = math.atan(newy / newx)
                if newx < 0:
                    angle += math.pi
                elif newy < 0:
                    angle += 2 * math.pi

            for k in range(line_count):
                if abs(angle - line_data[k, 0]) < 0.01:
                    d = math.hypot(newx, newy)
                    if line_data[k, 1] < d < (line_data[k, 1] + line_data[k, 2]):
                        out[i, j] = 1.0
                        break

    return out


# Backward-compatible name
drawRadixLine = draw_radix_line
