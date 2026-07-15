"""Sky compositing utilities."""

from __future__ import annotations

import cv2
import numpy as np


def paste_sky(image: np.ndarray, sky: np.ndarray, sky_mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Blend sky into masked region with original-style scaled tiling."""
    output = image.astype(np.float32).copy()
    mask = sky_mask > 0
    if not np.any(mask):
        return image.copy()

    rows, cols = np.where(mask)
    a1, a2 = int(rows.min()), int(rows.max())
    b1, b2 = int(cols.min()), int(cols.max())

    sky_h, sky_w = sky.shape[:2]
    target_h = max(1, a2 - a1 + 1)
    target_w = max(1, b2 - b1 + 1)
    scale = max(target_h / max(1, sky_h), target_w / max(1, sky_w))

    resized_h = max(1, int(round(sky_h * scale)))
    resized_w = max(1, int(round(sky_w * scale)))
    sky_scaled = cv2.resize(sky, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR).astype(np.float32)

    rr, cc = np.indices(image.shape[:2])
    tiled = sky_scaled[rr % resized_h, cc % resized_w]
    output[mask] = tiled[mask] * alpha + output[mask] * (1.0 - alpha)

    return np.clip(output, 0, 255).astype(np.uint8)


# Backward-compatible name
pasteSky = paste_sky
