"""Placeholder media is generated locally and never ships by default."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "make-placeholder-media.py"


class PlaceholderMedia(unittest.TestCase):
    def test_generator_produces_every_slot_in_three_formats(self) -> None:
        sys.path.insert(0, str(ROOT))
        from source.media import MEDIA_SLOTS

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(
                [sys.executable, str(GENERATOR), "--out", str(target)],
                check=True,
                capture_output=True,
            )
            for slot in MEDIA_SLOTS:
                for size in (960, 1440):
                    for extension in ("avif", "webp", "jpg"):
                        produced = target / f"{slot}-{size}.{extension}"
                        self.assertTrue(produced.exists(), f"missing {produced.name}")
                        self.assertGreater(produced.stat().st_size, 0)

    def test_generated_aspect_ratio_matches_the_rights_register(self) -> None:
        sys.path.insert(0, str(ROOT))
        from PIL import Image

        from source.media import MEDIA_SLOTS

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(
                [sys.executable, str(GENERATOR), "--out", str(target)],
                check=True,
                capture_output=True,
            )
            for slot, config in MEDIA_SLOTS.items():
                expected = config["width"] / config["height"]
                with Image.open(target / f"{slot}-1440.jpg") as produced:
                    actual = produced.width / produced.height
                self.assertAlmostEqual(actual, expected, places=2, msg=slot)

    def test_default_build_still_renders_the_abstract_fallback(self) -> None:
        images_dir = ROOT / "static" / "assets" / "images"
        if images_dir.exists():
            shutil.rmtree(images_dir)

        environment = dict(os.environ)
        environment.pop("PLACEHOLDER_MEDIA", None)
        subprocess.run(
            [sys.executable, str(ROOT / "build_site.py")],
            check=True,
            capture_output=True,
            env=environment,
            cwd=ROOT,
        )
        html = (ROOT / "dist" / "he" / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="media-panel media-panel--abstract"', html)
        self.assertNotIn("placeholder", html.lower())


if __name__ == "__main__":
    unittest.main()
