from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUT = ROOT / "static" / "assets" / "images"

OUT.mkdir(parents=True, exist_ok=True)

images = {
    "hero": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_17 PM (1).png",
    "method": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_18 PM (2).png",
    "international": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_18 PM (3).png",
    "sector-public": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_18 PM (4).png",
    "sector-purpose": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_18 PM (5).png",
    "sector-industry": DOCS / "ChatGPT Image Sep 4, 2026, 05_47_18 PM (6).png",
    "leadership": DOCS / "ChatGPT Image Sep 5, 2026, 03_29_50 PM.png",
}

for slot, source in images.items():
    if not source.exists():
        print(f"MISSING: {source}")
        continue

    with Image.open(source) as original:
        img = original.convert("RGB")

        for width in (960, 1440):
            height = round(img.height * width / img.width)
            resized = img.resize((width, height), Image.Resampling.LANCZOS)

            jpg = OUT / f"{slot}-{width}.jpg"
            webp = OUT / f"{slot}-{width}.webp"

            resized.save(jpg, "JPEG", quality=88, optimize=True)
            resized.save(webp, "WEBP", quality=86, method=6)

            print(f"Created {jpg}")
            print(f"Created {webp}")

print("DONE")