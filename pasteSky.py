"""Sky compositing utilities."""

from __future__ import annotations

import cv2
import numpy as np


def paste_sky(image: np.ndarray, sky: np.ndarray, sky_mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Blend the sky image into masked sky pixels of the source image."""
    h, w = image.shape[:2]
    sky_resized = cv2.resize(sky, (w, h), interpolation=cv2.INTER_LINEAR)
    mask = (sky_mask > 0)[..., None]

    out = image.astype(np.float32).copy()
    sky_float = sky_resized.astype(np.float32)
    out[mask] = sky_float[mask] * alpha + out[mask] * (1.0 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)


# Backward-compatible name
pasteSky = paste_sky
