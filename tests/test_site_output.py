from html.parser import HTMLParser
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def iter_pages() -> list[Path]:
    return sorted(DIST.glob("**/index.html"))


class SiteOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=True)

    def test_build_is_self_contained(self) -> None:
        self.assertTrue((DIST / "he" / "index.html").exists())
        self.assertTrue((DIST / "en" / "index.html").exists())
        self.assertTrue((DIST / "assets" / "styles.css").exists())
        self.assertTrue((DIST / "assets" / "site.js").exists())

    def test_generated_browser_assets_match_their_sources(self) -> None:
        source = ROOT / "source"
        self.assertEqual(
            (DIST / "assets" / "styles.css").read_bytes(),
            (source / "styles.css").read_bytes(),
        )
        self.assertEqual(
            (DIST / "assets" / "site.js").read_bytes(),
            (source / "site.js").read_bytes(),
        )

    def test_hebrew_font_family_is_local_and_complete(self) -> None:
        for weight in (400, 500, 600, 700):
            self.assertTrue(
                (
                    DIST
                    / "assets"
                    / "fonts"
                    / f"ibm-plex-sans-hebrew-{weight}.woff2"
                ).exists()
            )
        css = (DIST / "assets" / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("fonts.googleapis.com", css)
        self.assertIn("font-family:'IBM Plex Sans Hebrew'", css)

    def test_home_uses_accessible_local_svg_service_icons(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertEqual(html.count('class="service-icon"'), 6)
            self.assertNotIn("<svg><use", html)
            self.assertIn('class="institutional-hero"', html)
            self.assertIn('class="proof-strip section--tight"', html)

    def test_service_icons_have_unique_paths(self) -> None:
        from source.icons import ICON_PATHS

        self.assertEqual(len(ICON_PATHS), 19)
        self.assertEqual(len(set(ICON_PATHS.values())), 19)

    def test_supporting_grids_carry_icons(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertEqual(html.count('class="grid-icon"'), 8)
            self.assertNotIn('class="grid-icon"', html.split('method-grid')[1].split('</section>')[0])

    def test_inner_pages_use_the_institutional_page_shell(self) -> None:
        for lang in ("he", "en"):
            for slug in ("audit", "about", "faq", "contact"):
                html = (DIST / lang / slug / "index.html").read_text(
                    encoding="utf-8"
                )
                self.assertIn('class="institutional-page-hero page-hero"', html)

    def test_primary_navigation_marks_the_current_page(self) -> None:
        for lang in ("he", "en"):
            about = (DIST / lang / "about" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn(
                f'href="/{lang}/about/" aria-current="page"', about
            )
            audit = (DIST / lang / "audit" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn(
                f'href="/{lang}/audit/" aria-current="page"', audit
            )

    def test_unsupplied_images_render_finished_accessible_fallbacks(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertIn('data-image-slot="hero"', html)
            self.assertIn('class="media-panel media-panel--abstract"', html)
            self.assertNotIn("placeholder", html.lower())

    def test_image_rights_register_has_every_slot(self) -> None:
        register = (ROOT / "docs" / "image-rights-register.md").read_text(
            encoding="utf-8"
        )
        for slot in (
            "hero",
            "leadership",
            "method",
            "international",
            "sector-public",
            "sector-industry",
            "sector-purpose",
        ):
            self.assertIn(f"| `{slot}` |", register)

    def test_supplied_media_uses_responsive_modern_sources(self) -> None:
        from source.media import media_panel

        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            images = assets / "images"
            images.mkdir()
            for name in (
                "hero-960.avif",
                "hero-1440.avif",
                "hero-960.webp",
                "hero-1440.webp",
                "hero-1440.jpg",
            ):
                (images / name).write_bytes(b"image-test")
            html = media_panel("hero", "en", assets)
            self.assertIn('type="image/avif"', html)
            self.assertIn('hero-960.avif 960w', html)
            self.assertIn('hero-1440.avif 1440w', html)
            self.assertIn('type="image/webp"', html)
            self.assertIn('src="/assets/images/hero-1440.jpg"', html)
            self.assertIn('fetchpriority="high"', html)

    def test_legal_routes_and_footer_links_exist_in_both_languages(self) -> None:
        for lang in ("he", "en"):
            footer = (DIST / lang / "index.html").read_text(encoding="utf-8")
            for slug in ("privacy", "cookies", "terms", "accessibility"):
                self.assertTrue((DIST / lang / slug / "index.html").exists())
                self.assertIn(f'href="/{lang}/{slug}/"', footer)

    def test_production_identity_validation_names_every_missing_value(self) -> None:
        from source.legal_config import SiteIdentity

        missing = SiteIdentity.from_environment({}).validate_for_production()
        self.assertEqual(
            missing,
            [
                "SITE_LEGAL_NAME",
                "SITE_REGISTRATION_ID",
                "SITE_POSTAL_ADDRESS",
                "PRIVACY_EMAIL",
                "ACCESSIBILITY_CONTACT_NAME",
                "ACCESSIBILITY_CONTACT_EMAIL",
                "ACCESSIBILITY_CONTACT_PHONE",
                "CONTACT_RETENTION_MONTHS",
                "POLICY_EFFECTIVE_DATE",
                "POLICY_REVIEW_DATE",
                "GOVERNING_COURT",
            ],
        )

    def test_legal_content_is_parallel_and_storage_is_disclosed(self) -> None:
        from source.legal_content import LEGAL_SECTION_KEYS, POLICIES

        self.assertEqual(set(POLICIES), {"he", "en"})
        for lang in ("he", "en"):
            self.assertEqual(tuple(POLICIES[lang]["privacy"]["sections"]), LEGAL_SECTION_KEYS)
            home = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="privacy-disclosure"', home)
            self.assertIn('data-privacy-accept', home)
            self.assertIn('data-privacy-open', home)

    def test_every_content_page_has_one_h1(self) -> None:
        for page in iter_pages():
            html = page.read_text(encoding="utf-8")
            if page == DIST / "index.html":
                continue
            self.assertEqual(html.count("<h1"), 1, page)

    def test_pages_have_complete_social_meta(self) -> None:
        self.assertTrue((DIST / "assets" / "logo.png").exists())
        self.assertTrue((DIST / "assets" / "favicon.ico").exists())
        self.assertTrue((DIST / "assets" / "og" / "scout-finance-share.png").exists())
        for page in iter_pages():
            if page == DIST / "index.html":
                continue
            html = page.read_text(encoding="utf-8")
            self.assertIn('rel="icon" href="/assets/favicon.ico"', html, page)
            self.assertIn('property="og:image"', html, page)
            self.assertIn('property="og:url"', html, page)
            self.assertIn('hreflang="x-default"', html, page)
            self.assertIn('type="application/ld+json"', html, page)
            self.assertNotIn("fonts.googleapis.com", html, page)
            self.assertNotIn('img src="http', html, page)

    def test_public_copy_has_no_internal_editorial_language(self) -> None:
        banned = ("לפי נתוני", "מצוין באתר", "ללא פרסום מאמר דמה", "firm states", "current site")
        for page in iter_pages():
            html = page.read_text(encoding="utf-8")
            for phrase in banned:
                self.assertNotIn(phrase, html, page)

    def test_placeholder_insights_is_not_indexed_or_in_primary_nav(self) -> None:
        sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn("/insights/", sitemap)
        for lang in ("he", "en"):
            home = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertNotIn(f'href="/{lang}/insights/"', home)

    def test_contact_labels_reference_controls(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "contact" / "index.html").read_text(encoding="utf-8")
            for field in ("name", "organization", "email", "phone", "message"):
                self.assertIn(f'for="{lang}-{field}"', html)
                self.assertIn(f'id="{lang}-{field}"', html)
            self.assertIn(f'href="/{lang}/privacy/"', html)
            self.assertTrue((DIST / lang / "thank-you" / "index.html").exists())

    def test_contact_form_exposes_privacy_notice_and_secure_endpoint(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "contact" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn('action="/api/contact"', html)
            self.assertIn('class="contact-form"', html)
            self.assertIn('name="privacy_ack"', html)
            self.assertIn('name="cf-turnstile-response"', html)
            self.assertIn('class="collection-notice"', html)
            self.assertIn(f'href="/{lang}/privacy/"', html)
            self.assertIn('https://challenges.cloudflare.com/turnstile/v0/api.js', html)
            self.assertNotIn('data-netlify="true"', html)

    def test_accessibility_hooks_exist(self) -> None:
        css = (DIST / "assets" / "styles.css").read_text(encoding="utf-8")
        self.assertIn(":focus-visible", css)
        for page in iter_pages():
            if page == DIST / "index.html":
                continue
            html = page.read_text(encoding="utf-8")
            self.assertIn('href="#main-content"', html, page)
            self.assertIn('<main id="main-content"', html, page)

    def test_local_internal_links_resolve(self) -> None:
        for page in iter_pages():
            html = page.read_text(encoding="utf-8")
            for href in _hrefs(html):
                if not href.startswith("/"):
                    continue
                path = href.split("#", 1)[0].split("?", 1)[0]
                target = DIST / path.lstrip("/")
                if path.endswith("/"):
                    target /= "index.html"
                self.assertTrue(target.exists(), f"{page}: {href}")

    def test_deploy_configuration_publishes_dist_with_security_headers(self) -> None:
        config = (ROOT / "netlify.toml").read_text(encoding="utf-8")
        self.assertIn('publish = "dist"', config)
        self.assertIn('to = "/he/"', config)
        self.assertIn("Content-Security-Policy", config)
        self.assertIn("Cache-Control", config)

    def test_security_headers_allow_only_required_turnstile_browser_domains(self) -> None:
        config = (ROOT / "netlify.toml").read_text(encoding="utf-8")
        self.assertIn("object-src 'none'", config)
        self.assertIn("upgrade-insecure-requests", config)
        self.assertIn("Strict-Transport-Security", config)
        self.assertIn("https://challenges.cloudflare.com", config)
        self.assertNotIn("api.resend.com", config)

    def test_cloudflare_pages_config_matches_netlify_security_headers(self) -> None:
        headers = (DIST / "_headers").read_text(encoding="utf-8")
        redirects = (DIST / "_redirects").read_text(encoding="utf-8")
        netlify_config = (ROOT / "netlify.toml").read_text(encoding="utf-8")
        self.assertIn("/he/", redirects)
        self.assertIn("Content-Security-Policy", headers)
        self.assertIn("https://challenges.cloudflare.com", headers)
        self.assertIn("Strict-Transport-Security", headers)
        self.assertIn("Cache-Control", headers)
        self.assertNotIn("api.resend.com", headers)
        # The two configs are hand-kept in sync; catch drift by comparing the
        # actual CSP directive string, not just presence of the header name.
        netlify_csp = re.search(r'Content-Security-Policy = "([^"]+)"', netlify_config)
        headers_csp = re.search(r"Content-Security-Policy: (.+)", headers)
        self.assertIsNotNone(netlify_csp)
        self.assertIsNotNone(headers_csp)
        self.assertEqual(netlify_csp.group(1), headers_csp.group(1).strip())

    def test_cloudflare_pages_function_shares_the_netlify_contact_logic(self) -> None:
        cloudflare_function = (ROOT / "functions" / "api" / "contact.ts").read_text(encoding="utf-8")
        netlify_function = (ROOT / "netlify" / "functions" / "contact.mts").read_text(encoding="utf-8")
        self.assertIn("shared/contact-handler", cloudflare_function)
        self.assertIn("shared/contact-handler", netlify_function)
        self.assertIn("handleContact", cloudflare_function)
        self.assertIn("CF-Connecting-IP", cloudflare_function)

    def test_production_build_rejects_missing_legal_identity(self) -> None:
        env = {"CONTEXT": "production", "PATH": os.environ.get("PATH", "")}
        result = subprocess.run(
            [sys.executable, "build_site.py"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Missing production legal configuration", result.stderr + result.stdout
        )

    def test_release_qa_configuration_exists(self) -> None:
        package = (ROOT / "package.json").read_text(encoding="utf-8")
        self.assertIn('"test:e2e"', package)
        self.assertTrue((ROOT / "playwright.config.mjs").exists())
        self.assertTrue((ROOT / "tests" / "e2e" / "site.spec.mjs").exists())
        self.assertTrue((ROOT / "lighthouserc.json").exists())

    def test_content_signoff_lists_required_approvals(self) -> None:
        signoff = (ROOT / "docs" / "content-signoff.md").read_text(encoding="utf-8")
        for label in ("Managing director", "Professional lead", "Legal reviewer", "Accessibility reviewer"):
            self.assertIn(label, signoff)


def _hrefs(html: str) -> list[str]:
    class Links(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.values: list[str] = []

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag == "a":
                value = dict(attrs).get("href")
                if value:
                    self.values.append(value)

    parser = Links()
    parser.feed(html)
    return parser.values


if __name__ == "__main__":
    unittest.main()
