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

    def test_every_image_slot_renders_a_finished_accessible_panel(self) -> None:
        """No image slot may render as an unfinished or unlabelled state.

        A slot with an approved asset renders a <picture> carrying alt text;
        a slot without one renders the accessible abstract fallback. Both are
        finished states, and neither may leak the word "placeholder". The
        earlier version of this test asserted the fallback specifically, which
        stopped being true once real photography was supplied.
        """
        for lang in ("he", "en"):
            html = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertIn('data-image-slot="hero"', html)
            self.assertNotIn("placeholder", html.lower())
            panels = re.findall(r'<picture class="media-panel.*?</picture>', html, re.S)
            self.assertTrue(panels, f"{lang} home page renders no media panel")
            for panel in panels:
                if "media-panel--abstract" in panel:
                    continue
                self.assertRegex(panel, r'<img[^>]+alt="[^"]+"', panel[:200])

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

    def test_legal_identity_resolves_without_any_environment(self) -> None:
        """Publication must not depend on remembering an environment variable.

        The earlier contract required all eleven values to be supplied in
        production. On Cloudflare they never were, so the live policy shipped
        "to be completed before publication". Company identity is public
        record, so it now ships as a verified default and this asserts that
        nothing renders blank.
        """
        from source.legal_config import SiteIdentity

        identity = SiteIdentity.from_environment({})
        self.assertEqual(identity.validate_for_production(), [])
        for lang in ("he", "en"):
            values = identity.publication_values(lang)
            for key, value in values.items():
                self.assertTrue(str(value).strip(), f"{lang}/{key} is blank")
            self.assertEqual(values["registration_id"], "515178788")

    def test_blank_environment_override_is_reported(self) -> None:
        from source.legal_config import SiteIdentity

        identity = SiteIdentity.from_environment({"GOVERNING_COURT": "   "})
        self.assertEqual(identity.publication_values("he")["governing_court"], "בתי המשפט המוסמכים בישראל")

    def test_environment_override_wins_over_default(self) -> None:
        from source.legal_config import SiteIdentity

        identity = SiteIdentity.from_environment({"CONTACT_RETENTION_MONTHS": "12"})
        self.assertEqual(identity.publication_values("he")["retention_months"], "12")

    def test_published_legal_pages_carry_no_placeholder_or_wrong_vendor(self) -> None:
        """Guards the three defects that reached the live site.

        Unsubstituted {tokens}, preview identity text, the operational-draft
        banner, and Netlify named as the host after the move to Cloudflare.
        """
        banned = (
            "to be completed",
            "Operational draft",
            "טיוטה תפעולית",
            "legal-review-note",
            "Netlify",
            "התקופה התפעולית המאושרת",
            "the approved operational period",
            "מועד הבחינה המשפטית המתוכנן",
        )
        for lang in ("he", "en"):
            for slug in ("privacy", "cookies", "terms", "accessibility"):
                html = (DIST / lang / slug / "index.html").read_text(encoding="utf-8")
                self.assertNotRegex(html, r"\{[a-z_]+\}", f"{lang}/{slug} has an unsubstituted token")
                for phrase in banned:
                    self.assertNotIn(phrase, html, f"{lang}/{slug} still contains {phrase!r}")

    def test_accessibility_statement_meets_regulation_35(self) -> None:
        """Regulation 35(e) content: adaptations, contact route, and the standard."""
        for lang, needles in {
            "he": ("תקנה 35", "5568", "WCAG", "דיווח על חסם נגישות", "info@scout-finance.co.il", "+972-54-788-2877"),
            "en": ("regulation 35", "5568", "WCAG", "Reporting a barrier", "info@scout-finance.co.il", "+972-54-788-2877"),
        }.items():
            html = (DIST / lang / "accessibility" / "index.html").read_text(encoding="utf-8")
            for needle in needles:
                self.assertIn(needle, html, f"{lang} accessibility statement is missing {needle!r}")

    def test_privacy_policy_states_the_section_11_notice_elements(self) -> None:
        html = (DIST / "he" / "privacy" / "index.html").read_text(encoding="utf-8")
        for needle in (
            "515178788",            # controller identity
            "מרצון",                 # voluntary disclosure
            "לא ניתן יהיה לשלוח",     # consequence of refusing
            "Cloudflare",           # recipients
            "מחוץ לישראל",           # cross-border transfer
            "רשות להגנת הפרטיות",    # complaint route
        ):
            self.assertIn(needle, html, f"privacy policy is missing {needle!r}")

    def test_contact_form_is_not_published_with_the_turnstile_test_key(self) -> None:
        """A form that cannot work must not be offered as if it can.

        With Cloudflare's test key the widget always passes in the browser and
        the submission then fails server-side, while the privacy and cookies
        pages state that Turnstile protects the form.
        """
        import subprocess, sys, os

        env = dict(os.environ, CF_PAGES="1", CF_PAGES_BRANCH="master")
        env.pop("TURNSTILE_SITE_KEY", None)
        try:
            subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, env=env, check=True, capture_output=True)
            for lang in ("he", "en"):
                html = (DIST / lang / "contact" / "index.html").read_text(encoding="utf-8")
                self.assertNotIn("1x00000000000000000000AA", html)
                self.assertNotIn('class="contact-form"', html)
                self.assertIn("contact-form--direct", html)
                self.assertIn("mailto:info@scout-finance.co.il", html)
                self.assertNotIn("turnstile/v0/api.js", html)
        finally:
            subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=True, capture_output=True)

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

    def test_cloudflare_deploy_config_is_generated_into_dist(self) -> None:
        """Cloudflare Pages reads _headers and _redirects from the published
        directory. These used to be cross-checked against netlify.toml; the
        Netlify target is gone, so the generated files are now the only
        source of truth and are asserted directly."""
        redirects = (DIST / "_redirects").read_text(encoding="utf-8")
        headers = (DIST / "_headers").read_text(encoding="utf-8")
        self.assertIn("/he/", redirects)
        self.assertIn("/assets/*", headers)
        self.assertIn("immutable", headers)

    def test_security_headers_carry_the_full_policy(self) -> None:
        headers = (DIST / "_headers").read_text(encoding="utf-8")
        match = re.search(r"Content-Security-Policy: (.+)", headers)
        self.assertIsNotNone(match)
        policy = match.group(1).strip()
        directives = {
            part.strip().split(" ")[0]: part.strip()
            for part in policy.split(";")
            if part.strip()
        }
        self.assertEqual(directives["default-src"], "default-src 'self'")
        self.assertEqual(directives["base-uri"], "base-uri 'self'")
        self.assertEqual(directives["form-action"], "form-action 'self'")
        self.assertEqual(directives["frame-ancestors"], "frame-ancestors 'none'")
        self.assertEqual(directives["object-src"], "object-src 'none'")
        self.assertIn("https://challenges.cloudflare.com", directives["script-src"])
        self.assertIn("https://challenges.cloudflare.com", directives["frame-src"])
        self.assertIn("upgrade-insecure-requests", policy)
        # The Resend host carries the API key and must only ever be reached
        # from the server function, never from a browser.
        self.assertNotIn("api.resend.com", headers)
        for header in (
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy",
            "Permissions-Policy",
            "Cross-Origin-Opener-Policy",
        ):
            self.assertIn(header, headers)

    def test_cloudflare_function_delegates_to_the_shared_handler(self) -> None:
        cloudflare_function = (ROOT / "functions" / "api" / "contact.ts").read_text(encoding="utf-8")
        self.assertIn("shared/contact-handler", cloudflare_function)
        self.assertIn("handleContact", cloudflare_function)
        self.assertIn("CF-Connecting-IP", cloudflare_function)
        self.assertFalse((ROOT / "netlify.toml").exists(), "Netlify config should be gone")
        self.assertFalse((ROOT / "netlify").exists(), "Netlify functions should be gone")

    def test_production_build_publishes_clean_legal_pages(self) -> None:
        """A Cloudflare production build must succeed and ship no preview text.

        The build used to hard-fail when the legal environment variables were
        absent. On Cloudflare they always were absent and the gate itself
        never ran, so the preview text shipped regardless. Identity is now a
        verified default, so the guarantee is about the published output
        rather than about remembering to set an environment variable.
        """
        env = dict(os.environ, CF_PAGES="1", CF_PAGES_BRANCH="master")
        env.pop("TURNSTILE_SITE_KEY", None)
        env.pop("CONTEXT", None)
        try:
            result = subprocess.run(
                [sys.executable, "build_site.py"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for lang in ("he", "en"):
                html = (DIST / lang / "privacy" / "index.html").read_text(encoding="utf-8")
                self.assertNotRegex(html, r"\{[a-z_]+\}")
                self.assertIn("515178788", html)
                self.assertNotIn("Netlify", html)
        finally:
            subprocess.run(
                [sys.executable, "build_site.py"], cwd=ROOT, check=True, capture_output=True
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
