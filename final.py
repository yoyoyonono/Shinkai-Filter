"""CLI entrypoint for the Shinkai filter pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from ShinkaiMakotoFilter import shinkai_makoto_filter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Shinkai Makoto filter pipeline.")
    parser.add_argument("--src", required=True, help="Input source image path")
    parser.add_argument("--target", required=True, help="Guide/target image path")
    parser.add_argument("--sky", required=True, help="Sky texture image path")
    parser.add_argument("--out-dir", default="output", help="Output directory")
    parser.add_argument("--light-x", type=int, default=None, help="Optional light source X")
    parser.add_argument("--light-y", type=int, default=None, help="Optional light source Y")
    return parser.parse_args()


def _read_image(path: str) -> cv2.typing.MatLike:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def main() -> None:
    args = parse_args()
    src = _read_image(args.src)
    target = _read_image(args.target)
    sky = _read_image(args.sky)

    outputs = shinkai_makoto_filter(src, target, sky, args.light_x, args.light_y)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, image in outputs.items():
        out_file = out_dir / f"{name}.jpg"
        cv2.imwrite(str(out_file), image)

    print(f"Saved {len(outputs)} images to {out_dir}")


if __name__ == "__main__":
    main()
