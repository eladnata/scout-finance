"""The layout token system must exist in the stylesheet and reach the build."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_CSS = ROOT / "source" / "styles.css"


def dist_css() -> Path:
    """The stylesheet ships under a content-addressed filename so the
    immutable cache header on /assets/* cannot pin a stale copy."""
    matches = sorted((ROOT / "dist" / "assets").glob("styles.*.css"))
    assert len(matches) == 1, matches
    return matches[0]

REQUIRED_TOKENS = (
    "--w-full", "--w-wide", "--w-text", "--w-rail",
    "--t-xs", "--t-sm", "--t-base", "--t-md",
    "--t-lg", "--t-xl", "--t-2xl", "--t-3xl",
    "--sp-1", "--sp-10",
    "--band-tight", "--band-default", "--band-feature",
)


class LayoutTokens(unittest.TestCase):
    def setUp(self) -> None:
        self.css = SOURCE_CSS.read_text(encoding="utf-8")

    def test_every_layout_token_is_declared(self) -> None:
        for token in REQUIRED_TOKENS:
            self.assertIn(f"{token}:", self.css, f"missing token {token}")

    def test_gutter_is_one_fluid_expression(self) -> None:
        declarations = re.findall(r"--gutter:\s*([^;}]+)", self.css)
        self.assertEqual(
            declarations,
            ["clamp(24px, 5vw, 80px)"],
            "the gutter must be declared exactly once, as a fluid clamp",
        )

    def test_reading_width_is_set_in_ch_not_pixels(self) -> None:
        match = re.search(r"--w-text:\s*([^;}]+)", self.css)
        self.assertIsNotNone(match)
        self.assertIn("ch", match.group(1))

    def test_hebrew_display_sizes_are_overridden(self) -> None:
        self.assertRegex(
            self.css,
            r"body\[dir=rtl\][^{]*\{[^}]*--t-3xl:",
            "Hebrew needs its own display scale",
        )

    def test_tokens_reach_the_build(self) -> None:
        built = dist_css().read_text(encoding="utf-8")
        for token in REQUIRED_TOKENS:
            self.assertIn(f"{token}:", built)


if __name__ == "__main__":
    unittest.main()
