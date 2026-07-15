"""Color transfer utilities based on Reinhard et al."""

from __future__ import annotations

import numpy as np


def cf_reinhard(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Transfer color statistics from target to source using the original LMS pipeline."""
    src_rgb = source[..., ::-1].astype(np.float64) / 255.0
    tgt_rgb = target[..., ::-1].astype(np.float64) / 255.0

    img_s = src_rgb.reshape(-1, 3)
    img_t = tgt_rgb.reshape(-1, 3)

    a = np.array(
        [
            [0.3811, 0.5783, 0.0402],
            [0.1967, 0.7244, 0.0782],
            [0.0241, 0.1288, 0.8444],
        ],
        dtype=np.float64,
    )
    b = np.array(
        [
            [1.0 / np.sqrt(3.0), 0.0, 0.0],
            [0.0, 1.0 / np.sqrt(6.0), 0.0],
            [0.0, 0.0, 1.0 / np.sqrt(2.0)],
        ],
        dtype=np.float64,
    )
    c = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, -2.0],
            [1.0, -1.0, 0.0],
        ],
        dtype=np.float64,
    )
    b2 = np.array(
        [
            [np.sqrt(3.0) / 3.0, 0.0, 0.0],
            [0.0, np.sqrt(6.0) / 6.0, 0.0],
            [0.0, 0.0, np.sqrt(2.0) / 2.0],
        ],
        dtype=np.float64,
    )
    c2 = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0],
            [1.0, -2.0, 0.0],
        ],
        dtype=np.float64,
    )

    img_s = np.maximum(img_s, 1.0 / 255.0)
    img_t = np.maximum(img_t, 1.0 / 255.0)

    lms_s = a @ img_s.T
    lms_t = a @ img_t.T

    lms_s = np.log10(lms_s)
    lms_t = np.log10(lms_t)

    lab_s = b @ c @ lms_s
    lab_t = b @ c @ lms_t

    mean_s = np.mean(lab_s, axis=1, keepdims=True)
    std_s = np.std(lab_s, axis=1, keepdims=True)
    mean_t = np.mean(lab_t, axis=1, keepdims=True)
    std_t = np.std(lab_t, axis=1, keepdims=True)

    std_s = np.maximum(std_s, 1e-6)
    scale = std_t / std_s

    res_lab = (lab_s - mean_s) * scale + mean_t

    lms_res = c2 @ b2 @ res_lab
    lms_res = np.power(10.0, lms_res)

    rgb_from_lms = np.array(
        [
            [4.4679, -3.5873, 0.1193],
            [-1.2186, 2.3809, -0.1624],
            [0.0497, -0.2439, 1.2045],
        ],
        dtype=np.float64,
    )

    est_im = (rgb_from_lms @ lms_res).T
    est_im = est_im.reshape(source.shape)
    est_im = np.clip(est_im, 0.0, 1.0)

    est_bgr = (est_im[..., ::-1] * 255.0).astype(np.uint8)
    return est_bgr
