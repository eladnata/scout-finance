"""Generate on-brand placeholder media for every registered image slot.

These are generated compositions, not licensed photography. They exist so the
layout can be reviewed with imagery in place. They must never ship: build_site.py
copies them only when PLACEHOLDER_MEDIA=1, and the rights register records that
every slot is still awaiting an approved photograph.

Usage:
    python scripts/make-placeholder-media.py --out static/assets/images
"""

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from source.media import MEDIA_SLOTS  # noqa: E402

# Brand navy through steel, sampled from the palette in source/styles.css.
NAVY_DEEP = (3, 22, 42)
NAVY_MID = (11, 44, 76)
STEEL = (22, 61, 98)
LIGHT = (116, 170, 220)

RENDER_WIDTH = 1440


def _vertical_gradient(size: tuple[int, int], top: tuple, bottom: tuple) -> Image.Image:
    width, height = size
    base = Image.new("RGB", (1, height))
    pixels = base.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        pixels[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((width, height), Image.BILINEAR)


def _compose(slot: str, width: int, height: int) -> Image.Image:
    """Draw an architectural composition seeded deterministically by slot name."""
    canvas = _vertical_gradient((width, height), STEEL, NAVY_DEEP)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    seed = sum(ord(c) for c in slot)
    unit = width / 22

    # Vertical structure — a curtain-wall rhythm that varies per slot.
    x = -unit
    index = 0
    while x < width:
        step = unit * (1.6 if (index + seed) % 3 == 0 else 1.0)
        alpha = 26 if (index + seed) % 4 else 44
        draw.rectangle([x, 0, x + 1.4, height], fill=(255, 255, 255, alpha))
        x += step
        index += 1

    # Horizontal floor lines.
    spacing = height / 13
    for row in range(1, 13):
        y = row * spacing
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 20), width=1)

    # One angled plane, the brand's recurring diagonal.
    angle = math.radians(24 + (seed % 5) * 3)
    run = height / math.tan(angle)
    draw.polygon(
        [
            (width * 0.42, 0),
            (width, 0),
            (width, height),
            (width * 0.42 + run * 0.35, height),
        ],
        fill=(*LIGHT, 34),
    )

    # A soft light wash from the upper corner.
    wash = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wash_draw = ImageDraw.Draw(wash)
    radius = int(width * 0.55)
    wash_draw.ellipse(
        [width - radius, -radius // 2, width + radius // 2, radius],
        fill=(*LIGHT, 30),
    )
    overlay = Image.alpha_composite(overlay, wash)

    composed = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

    # A quiet inner rule, echoing the site's hairlines.
    frame = ImageDraw.Draw(composed)
    inset = int(min(width, height) * 0.045)
    frame.rectangle(
        [inset, inset, width - inset, height - inset],
        outline=(*NAVY_MID, ),
        width=max(1, width // 900),
    )
    return composed


def generate(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for slot, config in MEDIA_SLOTS.items():
        ratio = config["height"] / config["width"]
        master = _compose(slot, RENDER_WIDTH, round(RENDER_WIDTH * ratio))
        for size in (960, 1440):
            resized = master.resize((size, round(size * ratio)), Image.LANCZOS)
            for extension, options in (
                ("jpg", {"quality": 82, "optimize": True}),
                ("webp", {"quality": 80, "method": 5}),
                ("avif", {"quality": 62}),
            ):
                path = out_dir / f"{slot}-{size}.{extension}"
                resized.save(path, **options)
                written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=str(ROOT / "static" / "assets" / "images"),
        help="directory to write derivatives into",
    )
    arguments = parser.parse_args()
    written = generate(Path(arguments.out))
    print(f"Wrote {len(written)} placeholder derivatives to {arguments.out}")
    print("These are generated placeholders. They must not ship.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
