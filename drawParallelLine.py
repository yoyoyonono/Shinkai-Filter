"""Draw random parallel lines."""

from __future__ import annotations

import math

import numpy as np


def draw_parallel_line(mask: np.ndarray, angle: float, n: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = mask.copy()
    h, w = out.shape[:2]

    n = max(1, int(n))
    p1 = rng.permutation(np.arange(1, h + 1))
    p2 = rng.permutation(np.arange(1, w + 1))
    p3 = rng.permutation(np.arange(1, max(2, h // 2 + 1)))

    line_data = np.zeros((n, 3), dtype=np.float32)
    for i in range(n):
        line_data[i, 0] = p1[i % len(p1)]
        line_data[i, 1] = p2[i % len(p2)]
        line_data[i, 2] = p3[i % len(p3)]

    c = max(1, int(math.floor(w / 150)))
    b = -1 if angle < 0 else 1

    for i in range(h):
        for j in range(w):
            for k in range(n):
                for l in range(1, c + 1):
                    px = line_data[k, 0] - l
                    py = line_data[k, 1] + l * b

                    deltax = (i + 1) - px
                    deltay = (j + 1) - py
                    if deltax == 0:
                        theta = math.pi / 2 if deltay >= 0 else -math.pi / 2
                    else:
                        theta = math.atan(deltay / deltax)

                    if abs(theta - angle) < 0.01:
                        if math.hypot((i + 1) - px, (j + 1) - py) < line_data[k, 2]:
                            out[i, j] = 1.0
                            break
                if out[i, j] == 1.0:
                    break
            if out[i, j] == 1.0:
                continue

    return out


# Backward-compatible name
drawParallelLine = draw_parallel_line
