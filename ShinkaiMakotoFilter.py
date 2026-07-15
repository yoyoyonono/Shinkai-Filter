"""Main Shinkai-style image filtering pipeline."""

from __future__ import annotations

import cv2
import numpy as np

from addLight import add_light
from adjustHSV import adjust_hsv
from cf_reinhard import cf_reinhard
from changeStyle import change_style
from findSky import find_sky
from pasteSky import paste_sky


def shinkai_makoto_filter(
    src: np.ndarray,
    target: np.ndarray,
    sky: np.ndarray,
    light_x: int | None = None,
    light_y: int | None = None,
) -> dict[str, np.ndarray]:
    """Run the full processing pipeline and return all step outputs."""
    blur = change_style(src)
    color = cf_reinhard(blur, target)
    adjust = adjust_hsv(color)
    sky_mask, mask_threshold, mask_dilate, mask_erode = find_sky(src)
    change_sky = paste_sky(adjust, sky, sky_mask)
    light, light_filter = add_light(src, change_sky, light_x=light_x, light_y=light_y)
    dst = cv2.GaussianBlur(light, (0, 0), 1.0)
    dst = cv2.addWeighted(light, 1.8, dst, -0.8, 0)

    return {
        "src": src,
        "step1_median_filtering": blur,
        "guide": target,
        "step2_color_transfer": color,
        "step3_adjust": adjust,
        "step4_1_threshold": mask_threshold,
        "step4_2_dilation": mask_dilate,
        "step4_3_erosion": mask_erode,
        "step4_3_sky_mask": sky_mask,
        "step4_paste_sky": change_sky,
        "step5_1_light_filter": light_filter,
        "step5_add_light": light,
        "step6_sharpening": dst,
    }


# Backward-compatible name
ShinkaiMakotoFilter = shinkai_makoto_filter
