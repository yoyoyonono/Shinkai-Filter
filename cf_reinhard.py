"""Color transfer utilities based on Reinhard et al."""

from __future__ import annotations

import cv2
import numpy as np


def cf_reinhard(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Transfer color statistics from target to source using LAB space."""
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
    target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype(np.float32)

    src_mean, src_std = cv2.meanStdDev(source_lab)
    tgt_mean, tgt_std = cv2.meanStdDev(target_lab)

    src_mean = src_mean.reshape(1, 1, 3)
    src_std = np.maximum(src_std.reshape(1, 1, 3), 1e-6)
    tgt_mean = tgt_mean.reshape(1, 1, 3)
    tgt_std = np.maximum(tgt_std.reshape(1, 1, 3), 1e-6)

    transferred = (source_lab - src_mean) * (tgt_std / src_std) + tgt_mean
    transferred = np.clip(transferred, 0, 255).astype(np.uint8)
    return cv2.cvtColor(transferred, cv2.COLOR_LAB2BGR)
