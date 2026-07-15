"""Batch runner for input directory images."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from ShinkaiMakotoFilter import shinkai_makoto_filter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch process images with the Shinkai filter.")
    parser.add_argument("--input-dir", default="input", help="Directory containing source images")
    parser.add_argument("--target", required=True, help="Guide/target image path")
    parser.add_argument("--sky", required=True, help="Sky texture image path")
    parser.add_argument("--out-dir", default="batch_output", help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    target = cv2.imread(args.target, cv2.IMREAD_COLOR)
    sky = cv2.imread(args.sky, cv2.IMREAD_COLOR)
    if target is None:
        raise FileNotFoundError(f"Could not read target image: {args.target}")
    if sky is None:
        raise FileNotFoundError(f"Could not read sky image: {args.sky}")

    src_paths = sorted(list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")) + list(input_dir.glob("*.png")))
    if not src_paths:
        raise FileNotFoundError(f"No images found in {input_dir}")

    for src_path in src_paths:
        src = cv2.imread(str(src_path), cv2.IMREAD_COLOR)
        if src is None:
            continue
        outputs = shinkai_makoto_filter(src, target, sky)
        cv2.imwrite(str(out_dir / f"{src_path.stem}_final.jpg"), outputs["step6_sharpening"])

    print(f"Processed {len(src_paths)} images into {out_dir}")


if __name__ == "__main__":
    main()
