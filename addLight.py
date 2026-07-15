"""Light synthesis stage."""

from __future__ import annotations

import math

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
    """Add a synthetic light bloom and rays with original mode logic."""
    h, w = image.shape[:2]

    if light_x is None or light_y is None:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        py, px = np.unravel_index(np.argmax(gray), gray.shape)
        light_x, light_y = int(px), int(py)

    x = int(light_x)
    y = int(light_y)

    if x < 0 or x > h or y < 0 or y > w:
        mode = 2 if x > h / 2 else 1
    else:
        mode = 0

    light_filter = np.zeros((h, w), dtype=np.float32)
    r = max(1, int(math.floor(w / 10)))
    n = max(1, int(math.floor(r / 25)))

    if mode == 0:
        light_filter = draw_circle(light_filter, x, y, r)
        light_filter = cv2.GaussianBlur(light_filter, (0, 0), sigmaX=max(1e-3, r / 2.0))
        light_filter = draw_radix_line(light_filter, x, y, n, seed=seed)
        light_filter = cv2.GaussianBlur(light_filter, (0, 0), sigmaX=max(1e-3, r / 10.0))
    elif mode == 1:
        deltax = x - h
        deltay = y - w / 2.0
        angle = math.atan2(deltay, deltax)
        light_filter = draw_parallel_line(light_filter, angle, n * 2, seed=seed)
        light_filter = cv2.GaussianBlur(light_filter, (0, 0), sigmaX=max(1e-3, r / 20.0))

    light_filter = np.clip(light_filter, 0.0, 1.0)

    src_float = image.astype(np.float32) / 255.0
    if mode < 2:
        out = light_filter[..., None] + (1.0 - light_filter[..., None]) * src_float
    else:
        out = src_float

    return np.clip(out * 255.0, 0, 255).astype(np.uint8), (light_filter * 255.0).astype(np.uint8)


# Backward-compatible name
addLight = add_light
