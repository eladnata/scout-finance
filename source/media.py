"""Editorial media slots with safe, layout-stable fallbacks."""

from html import escape
from pathlib import Path


MEDIA_SLOTS = {
    "hero": {
        "width": 1600,
        "height": 2000,
        "alt": {
            "he": "צוות מקצועי בדיון על מסמכי בקרה פיננסית.",
            "en": "Finance professionals reviewing control documents in a working session.",
        },
    },
    "leadership": {
        "width": 1600,
        "height": 2000,
        "alt": {
            "he": "תומר נתן, מייסד ומוביל צוות הייעוץ של Scout Finance.",
            "en": "Tomer Natan, founder and advisory lead at Scout Finance.",
        },
    },
    "method": {
        "width": 1800,
        "height": 1200,
        "alt": {
            "he": "אנשי מקצוע בוחנים מסמכי בקרה ומפת תהליכים.",
            "en": "Professionals reviewing control documents and a process map.",
        },
    },
    "international": {
        "width": 1920,
        "height": 1200,
        "alt": {
            "he": "סביבת עבודה עסקית המשקפת פעילות בינלאומית מורכבת.",
            "en": "A business environment reflecting complex international operations.",
        },
    },
    "sector-public": {
        "width": 1600,
        "height": 1200,
        "alt": {"he": "סביבה של מוסד ציבורי.", "en": "A public institution environment."},
    },
    "sector-industry": {
        "width": 1600,
        "height": 1200,
        "alt": {"he": "סביבת תעשייה ותפעול.", "en": "An industrial and operational environment."},
    },
    "sector-purpose": {
        "width": 1600,
        "height": 1200,
        "alt": {"he": "צוות בארגון בעל שליחות ציבורית.", "en": "A team in a mission-driven organization."},
    },
}


def _available_images(slot: str, assets_root: Path) -> dict[str, list[tuple[int, str]]]:
    """Return every local responsive derivative grouped by file type."""
    image_root = assets_root / "images"
    variants: dict[str, list[tuple[int, str]]] = {}
    for extension in ("avif", "webp", "jpg", "jpeg"):
        for size in (960, 1440):
            candidate = image_root / f"{slot}-{size}.{extension}"
            if candidate.exists():
                variants.setdefault(extension, []).append(
                    (size, f"/assets/images/{candidate.name}")
                )
    return variants


def media_panel(slot: str, lang: str, assets_root: Path) -> str:
    """Render supplied editorial media or the approved abstract brand treatment."""
    if slot not in MEDIA_SLOTS:
        raise ValueError(f"Unknown media slot: {slot}")
    config = MEDIA_SLOTS[slot]
    alt = escape(config["alt"][lang])
    variants = _available_images(slot, assets_root)
    if not variants:
        return (
            f'<div class="media-panel media-panel--abstract" data-image-slot="{slot}" '
            f'role="img" aria-label="{alt}">'
            '<span class="media-grid" aria-hidden="true"></span>'
            '<span class="media-seal" aria-hidden="true">SF</span>'
            "</div>"
        )

    fallback_extension = next(
        (extension for extension in ("jpg", "jpeg", "webp", "avif") if extension in variants)
    )
    src = variants[fallback_extension][-1][1]
    sources = []
    for extension, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        if extension not in variants:
            continue
        srcset = ", ".join(f"{path} {size}w" for size, path in variants[extension])
        sources.append(
            f'<source type="{mime}" srcset="{srcset}" sizes="(max-width: 900px) 100vw, 42vw">'
        )
    loading = "eager" if slot == "hero" else "lazy"
    priority = ' fetchpriority="high"' if slot == "hero" else ""
    return (
        f'<picture class="media-panel" data-image-slot="{slot}">'
        f'{"".join(sources)}'
        f'<img src="{src}" width="{config["width"]}" height="{config["height"]}" '
        f'alt="{alt}" loading="{loading}" decoding="async"{priority}>'
        "</picture>"
    )
