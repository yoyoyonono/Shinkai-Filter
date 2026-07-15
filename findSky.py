"""Sky segmentation helpers."""

from __future__ import annotations

import cv2
import numpy as np


def _largest_component(mask: np.ndarray) -> np.ndarray:
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if num_labels <= 1:
        return mask

    top_labels = set(labels[0, :].tolist()) - {0}
    if top_labels:
        best_label = max(top_labels, key=lambda lbl: stats[lbl, cv2.CC_STAT_AREA])
    else:
        best_label = int(np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1)

    return np.where(labels == best_label, 255, 0).astype(np.uint8)


def find_sky(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Find the sky mask and intermediate masks."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(hsv, np.array([85, 20, 50]), np.array([140, 255, 255]))

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(threshold, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    sky_mask = _largest_component(eroded)

    return sky_mask, threshold, dilated, eroded


# Backward-compatible name
findSky = find_sky
