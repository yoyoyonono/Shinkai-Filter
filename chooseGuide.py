"""Guide image selection helpers."""

from __future__ import annotations

from pathlib import Path


def choose_guide(guide_dir: str | Path) -> Path:
    """Select a default guide image from a directory."""
    guide_dir = Path(guide_dir)
    guides = sorted([p for p in guide_dir.glob("*.jpg") if p.is_file()])
    if not guides:
        raise FileNotFoundError(f"No .jpg guide images found in {guide_dir}")
    return guides[0]


# Backward-compatible name
chooseGuide = choose_guide
