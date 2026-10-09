"""Screenshot comparison utilities using Pillow (no auto-resize, no auto-baseline update)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw


@dataclass(frozen=True)
class ComparisonResult:
    matched: bool
    baseline_path: str
    actual_path: str
    baseline_size: tuple[int, int]
    actual_size: tuple[int, int]
    dimension_mismatch: bool
    changed_pixels: int
    total_pixels: int
    diff_percent: float
    color_tolerance: int
    threshold_percent: float
    message: str
    diff_mask_path: str | None = None
    overlay_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_rgb_image(path: Path | str) -> Image.Image:
    """Load an image and validate it is a usable raster screenshot."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Image not found: {p}")
    if p.stat().st_size == 0:
        raise ValueError(f"Image file is empty: {p}")
    with Image.open(p) as img:
        img.load()
        if img.width < 1 or img.height < 1:
            raise ValueError(f"Invalid image dimensions for {p}: {img.size}")
        return img.convert("RGB")


def _pixel_diff_mask(
    baseline: Image.Image, actual: Image.Image, *, color_tolerance: int
) -> tuple[Image.Image, int]:
    """Return L-mode mask (255=diff) and count of changed pixels."""
    # Channel-wise absolute difference, then max across RGB exceeds tolerance.
    diff = ImageChops.difference(baseline, actual)
    # Convert to grayscale intensity of max channel delta approximately via convert L
    # More precise: evaluate per-pixel with point on each band.
    r, g, b = diff.split()
    # For each channel, pixels > tolerance become 255
    thr = max(0, min(255, int(color_tolerance)))

    def _binarize(ch: Image.Image) -> Image.Image:
        return ch.point(lambda v: 255 if v > thr else 0, mode="L")

    mask = ImageChops.lighter(ImageChops.lighter(_binarize(r), _binarize(g)), _binarize(b))
    # Count non-zero pixels
    hist = mask.histogram()
    changed = sum(hist[1:])  # index 0 is black (equal)
    return mask, changed


def _save_overlay(actual: Image.Image, mask: Image.Image, path: Path) -> None:
    """Draw semi-transparent red overlay on changed pixels."""
    overlay = actual.copy().convert("RGBA")
    red = Image.new("RGBA", actual.size, (220, 30, 30, 0))
    # Build alpha from mask
    alpha = mask.point(lambda v: 140 if v > 0 else 0)
    red.putalpha(alpha)
    composed = Image.alpha_composite(overlay, red)
    # Bounding boxes for clusters of diffs (optional outline of whole dirty region)
    bbox = mask.getbbox()
    if bbox:
        draw = ImageDraw.Draw(composed)
        draw.rectangle(bbox, outline=(255, 255, 0), width=3)
    composed.convert("RGB").save(path, format="PNG")


def compare_images(
    baseline_path: Path | str,
    actual_path: Path | str,
    *,
    color_tolerance: int = 12,
    threshold_percent: float = 0.5,
    artifacts_dir: Path | str | None = None,
    name: str = "compare",
) -> ComparisonResult:
    """Compare baseline vs actual screenshot.

    Images are never resized. Baselines are never overwritten by this function.
    """
    baseline_p = Path(baseline_path)
    actual_p = Path(actual_path)
    baseline = load_rgb_image(baseline_p)
    actual = load_rgb_image(actual_p)

    if baseline.size != actual.size:
        msg = (
            f"DIMENSION_MISMATCH: baseline={baseline.size[0]}x{baseline.size[1]} "
            f"actual={actual.size[0]}x{actual.size[1]} "
            f"(auto-resize disabled; layout/viewport difference must be investigated)"
        )
        return ComparisonResult(
            matched=False,
            baseline_path=str(baseline_p),
            actual_path=str(actual_p),
            baseline_size=(baseline.width, baseline.height),
            actual_size=(actual.width, actual.height),
            dimension_mismatch=True,
            changed_pixels=0,
            total_pixels=baseline.width * baseline.height,
            diff_percent=100.0,
            color_tolerance=color_tolerance,
            threshold_percent=threshold_percent,
            message=msg,
        )

    mask, changed = _pixel_diff_mask(baseline, actual, color_tolerance=color_tolerance)
    total = baseline.width * baseline.height
    diff_percent = (changed / total * 100.0) if total else 0.0
    matched = diff_percent <= float(threshold_percent)

    diff_mask_path = None
    overlay_path = None
    if artifacts_dir is not None:
        out = Path(artifacts_dir)
        out.mkdir(parents=True, exist_ok=True)
        diff_mask_path = str(out / f"{name}_diff_mask.png")
        overlay_path = str(out / f"{name}_overlay.png")
        mask.save(diff_mask_path, format="PNG")
        _save_overlay(actual, mask, Path(overlay_path))

    status = "MATCH" if matched else "DIFF_DETECTED"
    msg = (
        f"{status}: changed_pixels={changed}/{total} "
        f"({diff_percent:.4f}%), tolerance={color_tolerance}, "
        f"threshold={threshold_percent}%, size={baseline.width}x{baseline.height}"
    )
    return ComparisonResult(
        matched=matched,
        baseline_path=str(baseline_p),
        actual_path=str(actual_p),
        baseline_size=(baseline.width, baseline.height),
        actual_size=(actual.width, actual.height),
        dimension_mismatch=False,
        changed_pixels=changed,
        total_pixels=total,
        diff_percent=round(diff_percent, 6),
        color_tolerance=color_tolerance,
        threshold_percent=threshold_percent,
        message=msg,
        diff_mask_path=diff_mask_path,
        overlay_path=overlay_path,
    )


def write_summary_row(summary_path: Path, row: dict[str, Any]) -> None:
    """Append one JSON-lines summary row for reporting."""
    import json

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
