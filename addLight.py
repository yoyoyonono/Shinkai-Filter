"""Light synthesis stage."""

from __future__ import annotations

import cv2
import numpy as np

from drawCircle import draw_circle
from drawParallelLine import draw_parallel_line
from drawRadixLine import draw_radix_line


def add_light(
    src: np.ndarray,
    image: np.ndarray,
    light_x: int | None = None,
    light_y: int | None = None,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    """Add a synthetic light bloom and rays."""
    h, w = image.shape[:2]
    if light_x is None or light_y is None:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        max_pos = np.unravel_index(np.argmax(gray), gray.shape)
        light_y, light_x = int(max_pos[0]), int(max_pos[1])

    x = int(np.clip(light_x, 0, w - 1))
    y = int(np.clip(light_y, 0, h - 1))

    radius = max(8, min(h, w) // 10)
    ray_count = max(1, radius // 25)

    light_filter = np.zeros((h, w), dtype=np.float32)
    light_filter = draw_circle(light_filter, x, y, radius)
    light_filter = cv2.GaussianBlur(light_filter, (0, 0), sigmaX=max(1.0, radius / 2.0))
    light_filter = draw_radix_line(light_filter, x, y, ray_count, seed=seed)
    light_filter = draw_parallel_line(light_filter, 0.0, max(1, ray_count // 2), seed=seed + 1)
    light_filter = cv2.GaussianBlur(light_filter, (0, 0), sigmaX=max(1.0, radius / 8.0))

    light_filter = np.clip(light_filter, 0.0, 1.0)

    out = image.astype(np.float32)
    bloom = light_filter[..., None]
    out = bloom * 255.0 + (1.0 - bloom) * out
    return np.clip(out, 0, 255).astype(np.uint8), (light_filter * 255).astype(np.uint8)


# Backward-compatible name
addLight = add_light
