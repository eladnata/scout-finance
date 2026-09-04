# Institutional Precision Redesign and Compliance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a bilingual, publication-grade Scout Finance website with an institutional visual system, correct RTL behavior, licensed-image slots, clear legal disclosures, consent-aware storage and a server-validated Cloudflare Turnstile contact flow.

**Architecture:** Keep the existing Python static-site generator, but move CSS, browser behavior, icons, media rendering and legal content into focused source files. Generated files remain in `dist/`. Contact submissions move from direct Netlify Forms to a same-origin Netlify Function that validates input and Turnstile before sending through Resend.

**Tech Stack:** Python 3 static generation, semantic HTML, CSS logical properties, vanilla JavaScript, inline SVG, Node.js built-in test runner, Netlify Functions, Cloudflare Turnstile, Resend HTTPS API, Playwright and Axe.

**Spec:** `docs/superpowers/specs/2026-09-04-institutional-redesign-compliance-design.md`

## Global Constraints

- Preserve the approved local Scout Finance logo and the navy/blue/white brand family.
- Use locally hosted IBM Plex Sans Hebrew for Hebrew and Inter for English.
- No analytics, advertising pixels, chat widget, newsletter, marketing opt-in or session recording in the initial release.
- No horizontal overflow at 320, 375, 390, 768, 1024 or 1440 px, including mixed LTR values inside RTL pages.
- Turnstile tokens must be validated server-side and production must fail closed when secrets are missing.
- Do not expose form content, email addresses or telephone numbers in server logs.
- Do not claim legal certification or complete accessibility compliance before external review.
- Production legal pages must not publish incomplete identity data; production build must fail when required identity configuration is absent.
- The workspace currently has no `.git` directory. Each task ends with a verified checkpoint. If the owner initializes Git, convert each checkpoint into the commit shown in the task.

## File Structure

- `build_site.py` — orchestration, route generation and composition of source modules.
- `source/styles.css` — complete design system, components and responsive/RTL rules.
- `source/site.js` — navigation, FAQ, cookie preferences and contact-form browser behavior.
- `source/icons.py` — trusted inline SVG icon registry and `icon(name, title=None)` renderer.
- `source/media.py` — image-slot manifest and localized `media_panel(slot, lang)` renderer.
- `source/legal_config.py` — environment-backed business identity and production validation.
- `source/legal_content.py` — parallel Hebrew/English Privacy, Cookies, Terms and Accessibility content.
- `static/assets/fonts/` — local font files and license notices.
- `static/assets/images/` — approved source images and optimized variants when supplied.
- `netlify/functions/contact.mjs` — validation, Turnstile verification, email delivery and rate-limit configuration.
- `tests/contact-function.test.mjs` — real Request/Response unit tests with dependency injection only at external HTTP boundaries.
- `tests/test_site_output.py` — generated-site contracts.
- `tests/e2e/site.spec.mjs` — navigation, consent and accessibility flows.
- `tests/e2e/responsive.spec.mjs` — viewport overflow and contact-layout regression tests.
- `docs/image-rights-register.md` — source, author, license and attribution register for every supplied image.
- `docs/release-checklist.md` — production identity, legal, email and staging gates.

---

### Task 1: Extract source assets and establish the design token foundation

**Files:**
- Create: `source/styles.css`
- Create: `source/site.js`
- Create: `static/assets/fonts/ibm-plex-sans-hebrew-400.woff2`
- Create: `static/assets/fonts/ibm-plex-sans-hebrew-500.woff2`
- Create: `static/assets/fonts/ibm-plex-sans-hebrew-600.woff2`
- Create: `static/assets/fonts/ibm-plex-sans-hebrew-700.woff2`
- Create: `static/assets/fonts/OFL-IBM-Plex.txt`
- Modify: `build_site.py`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: `SOURCE_ROOT: pathlib.Path` in `build_site.py`.
- Produces: `SOURCE_DIR`, `STYLES_PATH`, `SCRIPT_PATH`, and generated `/assets/styles.css` and `/assets/site.js` files.

- [ ] **Step 1: Write a failing build-contract test**

Add this test to `SiteOutputTests`:

```python
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
        self.assertTrue((DIST / "assets" / "fonts" / f"ibm-plex-sans-hebrew-{weight}.woff2").exists())
    css = (DIST / "assets" / "styles.css").read_text(encoding="utf-8")
    self.assertNotIn("fonts.googleapis.com", css)
    self.assertIn("font-family: 'IBM Plex Sans Hebrew'", css)
```

- [ ] **Step 2: Run the test and verify the missing-source failure**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_generated_browser_assets_match_their_sources -v`

Expected: FAIL because `source/styles.css` does not exist.

- [ ] **Step 3: Extract current CSS and JavaScript without behavior changes**

Move the complete existing `STYLE` value to `source/styles.css` and `SCRIPT` value to `source/site.js`. Replace the embedded values in `build_site.py` with:

```python
SOURCE_DIR = SOURCE_ROOT / "source"
STYLES_PATH = SOURCE_DIR / "styles.css"
SCRIPT_PATH = SOURCE_DIR / "site.js"

STYLES = STYLES_PATH.read_text(encoding="utf-8")
SITE_SCRIPT = SCRIPT_PATH.read_text(encoding="utf-8")
```

Write them during the build with:

```python
(ASSETS / "styles.css").write_text(STYLES, encoding="utf-8")
(ASSETS / "site.js").write_text(SITE_SCRIPT, encoding="utf-8")
```

- [ ] **Step 4: Replace the token block with the approved token system**

Start `source/styles.css` with:

```css
:root {
  --ledger-navy: #071b33;
  --control-blue: #0b4f9c;
  --signal-blue: #1769c2;
  --report-ink: #122337;
  --steel: #5e6d7e;
  --rule: #d7e1ea;
  --mist: #eef3f7;
  --paper: #f8fafc;
  --white: #fff;
  --content-max: 1240px;
  --gutter: clamp(18px, 3vw, 32px);
  --radius-control: 6px;
  --radius-panel: 12px;
  --focus-ring: 0 0 0 3px rgba(23, 105, 194, .28);
}
```

Map old variables to the new names only while migrating remaining selectors; remove the aliases before Task 9.

- [ ] **Step 5: Add the licensed local Hebrew font files**

Download weights 400, 500, 600 and 700 from the official IBM Plex release, convert only from an official WOFF/TTF source when WOFF2 is not published, and preserve the SIL Open Font License as `static/assets/fonts/OFL-IBM-Plex.txt`. Define one `@font-face` per weight with `font-display: swap` and use `font-family: 'IBM Plex Sans Hebrew', Heebo, Arial, sans-serif` only on Hebrew documents.

- [ ] **Step 6: Run the complete Python suite**

Run: `py -3 -m unittest discover -s tests -v`

Expected: all tests PASS and `dist/assets/styles.css` exactly matches `source/styles.css`.

- [ ] **Step 7: Record checkpoint**

Checkpoint files: `build_site.py`, `source/styles.css`, `source/site.js`, IBM Plex Hebrew font files and license, `tests/test_site_output.py`.

Suggested commit after Git initialization: `refactor: extract site assets and establish design tokens`.

---

### Task 2: Fix the RTL, header and mobile overflow contract

**Files:**
- Modify: `source/styles.css`
- Modify: `build_site.py`
- Create: `tests/e2e/responsive.spec.mjs`
- Modify: `tests/e2e/site.spec.mjs`

**Interfaces:**
- Consumes: generated routes and the existing `header(lang, current)` function.
- Produces: `.site-header`, `.brand-mark`, `.nav-drawer`, `.contact-value`, and `.bidi-value` layout contracts.

- [ ] **Step 1: Write failing browser overflow tests**

Create `tests/e2e/responsive.spec.mjs`:

```javascript
import { test, expect } from '@playwright/test';

const routes = ['/he/', '/he/contact/', '/he/audit/', '/en/', '/en/contact/', '/en/audit/'];
const widths = [320, 375, 390, 768, 1024, 1440];

for (const route of routes) {
  for (const width of widths) {
    test(`${route} has no horizontal overflow at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route);
      const sizes = await page.evaluate(() => ({
        scroll: document.documentElement.scrollWidth,
        client: document.documentElement.clientWidth,
      }));
      expect(sizes.scroll).toBeLessThanOrEqual(sizes.client);
    });
  }
}

test('Hebrew contact values stay inside the mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/he/contact/');
  for (const value of await page.locator('.contact-value').all()) {
    const box = await value.boundingBox();
    expect(box).not.toBeNull();
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(390);
  }
});
```

- [ ] **Step 2: Run the focused browser test and confirm the current defect**

Run: `npm run test:e2e -- tests/e2e/responsive.spec.mjs --project=mobile`

Expected: FAIL on Hebrew contact at 320–390 px because the current document width exceeds the viewport.

- [ ] **Step 3: Implement structural overflow fixes**

Add these rules, then adjust component-specific spacing without using overflow hiding as the only fix:

```css
html, body { max-inline-size: 100%; }
body { margin: 0; }
.container { inline-size: min(calc(100% - (2 * var(--gutter))), var(--content-max)); }
.nav > *, .hero-grid > *, .contact-layout > *, .content-grid > *, .form-grid > * {
  min-inline-size: 0;
}
.brand-mark {
  inline-size: min(260px, calc(100vw - 100px));
  block-size: auto;
}
.contact-value, .bidi-value {
  direction: ltr;
  unicode-bidi: isolate;
  overflow-wrap: anywhere;
  max-inline-size: 100%;
}
.field input, .field textarea, form { min-inline-size: 0; max-inline-size: 100%; }
@media (max-width: 560px) {
  .brand-mark { inline-size: min(220px, calc(100vw - 92px)); }
  .contact-form .btn-primary { inline-size: 100%; }
}
```

Update header markup to use `class="brand-mark"` on the image and preserve semantic source order in each language.

- [ ] **Step 4: Localize breadcrumb separators and current-page state**

Render a visually hidden separator using CSS and add `aria-current="page"` to the active primary navigation link. Use `/` for English and `‹` for Hebrew through localized copy, not CSS mirroring.

- [ ] **Step 5: Run responsive and navigation tests**

Run: `npm run test:e2e -- tests/e2e/responsive.spec.mjs tests/e2e/site.spec.mjs`

Expected: all viewport cases PASS; mobile navigation still opens and closes with Escape.

- [ ] **Step 6: Record checkpoint**

Checkpoint files: `source/styles.css`, `build_site.py`, `tests/e2e/responsive.spec.mjs`, `tests/e2e/site.spec.mjs`.

Suggested commit: `fix: make rtl navigation and contact layout viewport safe`.

---

### Task 3: Build the institutional home page and SVG icon system

**Files:**
- Create: `source/icons.py`
- Modify: `build_site.py`
- Modify: `source/styles.css`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Produces: `icon(name: str, title: str | None = None) -> str`.
- Supported names: `audit`, `sox`, `controls`, `advisory`, `technology`, `investigative`, `international`, `contact`.
- The renderer raises `KeyError` for an unsupported icon name.

- [ ] **Step 1: Write failing icon and home-structure tests**

Add:

```python
def test_home_uses_accessible_local_svg_service_icons(self) -> None:
    for lang in ("he", "en"):
        html = (DIST / lang / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="service-icon"'), 6)
        self.assertNotIn("<svg><use", html)
        self.assertIn('class="institutional-hero"', html)
        self.assertIn('class="proof-strip"', html)

def test_inner_pages_use_the_institutional_page_shell(self) -> None:
    for lang in ("he", "en"):
        for slug in ("audit", "about", "faq", "contact"):
            html = (DIST / lang / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="institutional-page-hero"', html)

def test_service_icons_have_unique_paths(self) -> None:
    from source.icons import ICON_PATHS
    self.assertEqual(len(ICON_PATHS), 8)
    self.assertEqual(len(set(ICON_PATHS.values())), 8)
```

- [ ] **Step 2: Run tests and verify missing module/markup failures**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_home_uses_accessible_local_svg_service_icons tests.test_site_output.SiteOutputTests.test_service_icons_have_unique_paths -v`

Expected: FAIL because `source.icons` and the new home classes do not exist.

- [ ] **Step 3: Implement the trusted icon registry**

Create `source/icons.py` with fixed path strings and an escaped optional title:

```python
from html import escape

ICON_PATHS = {
    "audit": '<path d="M4 3h12l4 4v14H4z"/><path d="M16 3v5h5M8 13h8M8 17h5"/>',
    "sox": '<path d="M12 3l8 3v6c0 5-3.4 8.1-8 10-4.6-1.9-8-5-8-10V6z"/><path d="m8.5 12 2.2 2.2 4.8-5"/>',
    "controls": '<path d="M4 7h16M7 4v6M4 17h16M17 14v6M4 12h16M12 9v6"/>',
    "advisory": '<path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/>',
    "technology": '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M8 10l2 2 5-5"/>',
    "investigative": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M8 10.5l1.5 1.5 3.5-4"/>',
    "international": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "contact": '<path d="M4 5h16v14H4zM4 7l8 6 8-6"/>',
}

def icon(name: str, title: str | None = None) -> str:
    path = ICON_PATHS[name]
    accessible = f'<title>{escape(title)}</title>' if title else 'aria-hidden="true"'
    title_markup = accessible if title else ""
    aria = 'role="img"' if title else 'aria-hidden="true" focusable="false"'
    return f'<svg class="service-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" {aria}>{title_markup}{path}</svg>'
```

- [ ] **Step 4: Recompose the home page**

Replace the current signal-card hero with `.institutional-hero`, `.hero-copy`, `.hero-media`, and `.hero-assurance`. Render the proof facts in `.proof-strip`. Render six service items as `.service-entry` with an icon, title, outcome copy and descriptive link label. Add the working-method and international editorial sections defined in the spec.

- [ ] **Step 5: Implement the visual language**

In `source/styles.css`, implement the 12-column hero, ledger-grid background, restrained 6/12 px radii, ruled proof strip and non-card service grid. Remove circular decorations, generic per-card shadows and text arrows. Add only action-triggered transitions and respect `prefers-reduced-motion`.

Rebuild inner-page heroes as `.institutional-page-hero`, apply the same report-grid alignment to service content, replace rounded sticky cards with ruled `.advisory-panel` sections, and restyle FAQ, about, leadership, legal and contact shells with the same type scale and spacing system. Preserve one H1 and the existing semantic heading order on every route.

- [ ] **Step 6: Run the Python and Axe suites**

Run: `py -3 -m unittest discover -s tests -v`

Run: `npm run test:e2e -- tests/e2e/site.spec.mjs`

Expected: service icon and home structure tests PASS; no critical or serious Axe findings.

- [ ] **Step 7: Record checkpoint**

Checkpoint files: `source/icons.py`, `build_site.py`, `source/styles.css`, `tests/test_site_output.py`.

Suggested commit: `feat: introduce institutional home layout and service icons`.

---

### Task 4: Add image slots, fallbacks and rights tracking

**Files:**
- Create: `source/media.py`
- Create: `docs/image-rights-register.md`
- Modify: `build_site.py`
- Modify: `source/styles.css`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Produces: `MEDIA_SLOTS: dict[str, dict]` and `media_panel(slot: str, lang: str, assets_root: Path) -> str`.
- Supported slots: `hero`, `leadership`, `method`, `international`, `sector-public`, `sector-industry`, `sector-purpose`.
- A slot looks for `/assets/images/<slot>-{960,1440}.{avif,webp,jpg}` in that priority order.

- [ ] **Step 1: Write failing fallback and rights-register tests**

Add:

```python
def test_unsupplied_images_render_finished_accessible_fallbacks(self) -> None:
    for lang in ("he", "en"):
        html = (DIST / lang / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-image-slot="hero"', html)
        self.assertIn('class="media-panel media-panel--abstract"', html)
        self.assertNotIn("placeholder", html.lower())

def test_image_rights_register_has_every_slot(self) -> None:
    register = (ROOT / "docs" / "image-rights-register.md").read_text(encoding="utf-8")
    for slot in ("hero", "leadership", "method", "international", "sector-public", "sector-industry", "sector-purpose"):
        self.assertIn(f"| `{slot}` |", register)
```

- [ ] **Step 2: Run tests and verify failures**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_unsupplied_images_render_finished_accessible_fallbacks tests.test_site_output.SiteOutputTests.test_image_rights_register_has_every_slot -v`

Expected: FAIL because no media renderer or rights register exists.

- [ ] **Step 3: Implement the media manifest and renderer**

Each manifest entry contains exact Hebrew/English alt intent, aspect ratio and priority. `media_panel` checks available files; if none exist it returns:

```html
<div class="media-panel media-panel--abstract" data-image-slot="hero"
     role="img" aria-label="קומפוזיציה מופשטת של קווי בקרה פיננסית">
  <span class="media-grid" aria-hidden="true"></span>
  <span class="media-seal" aria-hidden="true">SF</span>
</div>
```

When files exist, return `<picture>` with AVIF, WebP and JPEG sources, explicit width/height, `loading="lazy"` except for the hero, and the localized alt text.

- [ ] **Step 4: Create the rights register with explicit status**

Create a table with columns `Slot`, `Priority`, `Required crop`, `Source URL`, `Author`, `License`, `Downloaded`, `Attribution`, `Approved`. Set every unsupplied source field to `Not supplied` and every approval to `No`; these values are explicit publication blockers rather than hidden placeholders.

- [ ] **Step 5: Integrate media panels**

Use `hero` on the home hero, `method` in the working-method section, `international` in the international section and `leadership` on the leadership page. Optional sector slots render only after assets exist, so the initial public layout never shows empty repeated blocks.

- [ ] **Step 6: Run output tests**

Run: `py -3 -m unittest discover -s tests -v`

Expected: fallback and rights-register tests PASS; all internal links still resolve.

- [ ] **Step 7: Record checkpoint**

Checkpoint files: `source/media.py`, `docs/image-rights-register.md`, `build_site.py`, `source/styles.css`, `tests/test_site_output.py`.

Suggested commit: `feat: add editorial media slots and rights tracking`.

---

### Task 5: Implement legal identity, policies and consent-aware storage

**Files:**
- Create: `source/legal_config.py`
- Create: `source/legal_content.py`
- Modify: `build_site.py`
- Modify: `source/site.js`
- Modify: `source/styles.css`
- Modify: `tests/test_site_output.py`
- Modify: `tests/e2e/site.spec.mjs`

**Interfaces:**
- Produces: `SiteIdentity.from_environment(environ: Mapping[str, str]) -> SiteIdentity`.
- Produces: `SiteIdentity.validate_for_production() -> list[str]` returning missing field names.
- Produces localized content dictionaries for `privacy`, `cookies`, `terms`, and `accessibility`.
- Browser storage key: `scout-consent-v1` with JSON `{ "essential": true, "analytics": false, "version": 1 }`.

- [ ] **Step 1: Write failing legal-route and production-validation tests**

Add:

```python
def test_legal_routes_and_footer_links_exist_in_both_languages(self) -> None:
    for lang in ("he", "en"):
        for slug in ("privacy", "cookies", "terms", "accessibility"):
            self.assertTrue((DIST / lang / slug / "index.html").exists())
            footer = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertIn(f'href="/{lang}/{slug}/"', footer)

def test_production_identity_validation_names_every_missing_value(self) -> None:
    from source.legal_config import SiteIdentity
    missing = SiteIdentity.from_environment({}).validate_for_production()
    self.assertEqual(missing, [
        "SITE_LEGAL_NAME", "SITE_REGISTRATION_ID", "SITE_POSTAL_ADDRESS",
        "PRIVACY_EMAIL", "ACCESSIBILITY_CONTACT_NAME",
        "ACCESSIBILITY_CONTACT_EMAIL", "ACCESSIBILITY_CONTACT_PHONE",
        "CONTACT_RETENTION_MONTHS", "POLICY_EFFECTIVE_DATE",
        "POLICY_REVIEW_DATE", "GOVERNING_COURT",
    ])
```

- [ ] **Step 2: Run tests and verify missing module/routes failures**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_legal_routes_and_footer_links_exist_in_both_languages tests.test_site_output.SiteOutputTests.test_production_identity_validation_names_every_missing_value -v`

Expected: FAIL because the cookies/terms routes and legal configuration do not exist.

- [ ] **Step 3: Implement immutable legal configuration**

Create a frozen dataclass whose fields map exactly to the environment names in the expected list. `validate_for_production` returns missing names in that order. In `build_site.py`, when `CONTEXT == "production"`, raise `SystemExit("Missing production legal configuration: ...")` if the list is non-empty.

- [ ] **Step 4: Implement complete parallel policy structures**

In `source/legal_content.py`, define the same section keys in Hebrew and English:

```python
LEGAL_SECTION_KEYS = (
    "controller", "collection", "purposes", "voluntary",
    "recipients", "transfers", "retention", "security",
    "rights", "minors", "updates", "contact",
)
```

Privacy content must state that the public form is voluntary, that failure to provide required contact fields prevents a response, and that users should not submit regulated, confidential or sensitive data. Cookies content must list `scout-consent-v1`, the language preference key and Turnstile security processing. Terms must contain the no-professional-engagement and no-reliance statements from the spec. Accessibility content must name the target standard without claiming certification.

- [ ] **Step 5: Add the storage disclosure and preference center**

Render a localized `.privacy-disclosure` on first visit with “Details” and “Understood” controls. Add a footer “Privacy settings” button that reopens `.privacy-preferences`. JavaScript must parse invalid stored JSON safely, always force `essential: true`, and always keep `analytics: false` in version 1.

- [ ] **Step 6: Write and run cookie-behavior browser tests**

Add:

```javascript
test('cookie disclosure stores essential-only preferences', async ({ page }) => {
  await page.goto('/en/');
  await page.getByRole('button', { name: 'Understood' }).click();
  const stored = await page.evaluate(() => localStorage.getItem('scout-consent-v1'));
  expect(JSON.parse(stored)).toEqual({ essential: true, analytics: false, version: 1 });
  await page.reload();
  await expect(page.locator('.privacy-disclosure')).toBeHidden();
});
```

Run: `npm run test:e2e -- tests/e2e/site.spec.mjs`

Expected: PASS with no network request to an analytics domain.

- [ ] **Step 7: Run all static tests**

Run: `py -3 -m unittest discover -s tests -v`

Expected: policy routes, footer links and identity validation PASS.

- [ ] **Step 8: Record checkpoint**

Checkpoint files: `source/legal_config.py`, `source/legal_content.py`, `build_site.py`, `source/site.js`, `source/styles.css`, `tests/test_site_output.py`, `tests/e2e/site.spec.mjs`.

Suggested commit: `feat: add legal policies and essential-only privacy controls`.

---

### Task 6: Rebuild the contact experience and browser-side submission states

**Files:**
- Modify: `build_site.py`
- Modify: `source/site.js`
- Modify: `source/styles.css`
- Modify: `tests/test_site_output.py`
- Modify: `tests/e2e/site.spec.mjs`

**Interfaces:**
- Form action: `/api/contact`.
- Required fields: `lang`, `name`, `email`, `message`, `privacy_ack`, `cf-turnstile-response`.
- Optional fields: `organization`, `phone`, `website` honeypot.
- Success response: `{ "ok": true, "requestId": string }`.
- Error response: `{ "ok": false, "code": string, "message": string }`.

- [ ] **Step 1: Write failing generated-form tests**

Replace the old Netlify action expectation with:

```python
def test_contact_form_exposes_privacy_notice_and_secure_endpoint(self) -> None:
    for lang in ("he", "en"):
        html = (DIST / lang / "contact" / "index.html").read_text(encoding="utf-8")
        self.assertIn('action="/api/contact"', html)
        self.assertIn('name="privacy_ack"', html)
        self.assertIn('name="cf-turnstile-response"', html)
        self.assertIn('class="collection-notice"', html)
        self.assertIn(f'href="/{lang}/privacy/"', html)
        self.assertNotIn('data-netlify="true"', html)
```

- [ ] **Step 2: Run the focused test and verify current direct-form failure**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_contact_form_exposes_privacy_notice_and_secure_endpoint -v`

Expected: FAIL because the form still posts directly to the localized thank-you page and uses Netlify Forms.

- [ ] **Step 3: Render the revised form**

Add the short collection notice before fields, a hidden `lang`, the unchanged honeypot, the required acknowledgement, a Turnstile container using the build-time `TURNSTILE_SITE_KEY`, and a live status region:

```html
<div class="turnstile-shell">
  <div class="cf-turnstile" data-sitekey="PUBLIC_SITE_KEY"></div>
</div>
<p class="form-status" role="status" aria-live="polite"></p>
```

Load `https://challenges.cloudflare.com/turnstile/v0/api.js` only on contact pages. Local builds use Cloudflare's always-pass public test site key `1x00000000000000000000AA`. Production builds require `TURNSTILE_SITE_KEY` and reject that test key.

- [ ] **Step 4: Implement progressive submission behavior**

Intercept only `.contact-form`. Disable the submit button, set localized pending copy, post `new FormData(form)` to `/api/contact`, and handle JSON codes. On success, navigate to `/{lang}/thank-you/`. On failure, restore the button, place the localized message in `.form-status`, and focus the status region with `tabindex="-1"`.

- [ ] **Step 5: Add browser tests using route interception**

Test a successful mocked response and a `turnstile_failed` response. Assert disabled/pending state, success navigation and focused error status. Do not assert on the route mock itself; assert on visible form behavior.

- [ ] **Step 6: Run form tests**

Run: `py -3 -m unittest discover -s tests -v`

Run: `npm run test:e2e -- tests/e2e/site.spec.mjs`

Expected: contact output and visible state tests PASS in Hebrew and English.

- [ ] **Step 7: Record checkpoint**

Checkpoint files: `build_site.py`, `source/site.js`, `source/styles.css`, `tests/test_site_output.py`, `tests/e2e/site.spec.mjs`.

Suggested commit: `feat: rebuild contact flow with clear privacy acknowledgement`.

---

### Task 7: Implement server-side validation, Turnstile and email delivery

**Files:**
- Create: `netlify/functions/contact.mjs`
- Create: `tests/contact-function.test.mjs`
- Modify: `package.json`

**Interfaces:**
- Produces: `validateFields(input: Record<string, string>) -> { valid: boolean, errors: string[] }`.
- Produces: `handleContact(request: Request, deps: { fetch: typeof fetch, env: Record<string, string>, requestId: string }) -> Promise<Response>`.
- Default export calls `handleContact` with real `fetch`, `process.env`, and `crypto.randomUUID()`.
- Function route: `/api/contact`; rate limit: 8 requests per 60 seconds per IP and domain.

- [ ] **Step 1: Add the Node test command**

Set:

```json
"test:function": "node --test tests/contact-function.test.mjs"
```

- [ ] **Step 2: Write failing method and input-validation tests**

Create tests using real `Request` and `FormData` objects. Cover:

```javascript
test('rejects non-POST requests with 405', async () => { /* expect status 405 */ });
test('rejects an invalid origin with 403', async () => { /* Origin is https://attacker.example */ });
test('rejects missing privacy acknowledgement with 400', async () => { /* code invalid_form */ });
test('rejects name over 120 characters with 400', async () => { /* code invalid_form */ });
test('rejects message over 5000 characters with 400', async () => { /* code invalid_form */ });
test('accepts optional empty organization and phone', async () => { /* external calls succeed */ });
```

Use literal expected JSON codes and a complete valid form fixture. External HTTP doubles must return full `Response` objects.

- [ ] **Step 3: Run tests and verify missing-module failure**

Run: `npm run test:function`

Expected: FAIL because `netlify/functions/contact.mjs` does not exist.

- [ ] **Step 4: Implement deterministic field validation**

Allow only the exact interface fields. Trim text, normalize CRLF to LF, strip ASCII control characters except newline, validate email length and shape, enforce `name <= 120`, `email <= 254`, `organization <= 160`, `phone <= 40`, `message <= 5000`, require `privacy_ack == "yes"`, and silently return success for a non-empty honeypot without calling external services.

- [ ] **Step 5: Write failing Turnstile boundary tests**

Cover missing token, Cloudflare network failure, non-2xx response, `{ success: false }`, expired token, hostname mismatch and valid success. Assert that email delivery never occurs in failure cases through the final response and a dependency call counter used only at the external boundary.

- [ ] **Step 6: Implement Turnstile verification**

POST URL-encoded `secret`, `response`, `remoteip` and `idempotency_key` to `https://challenges.cloudflare.com/turnstile/v0/siteverify`. Require `success === true`; when `TURNSTILE_EXPECTED_HOSTNAME` is configured, require an exact hostname match. Map all verification failures to status 400 and code `turnstile_failed` without exposing Cloudflare error details.

- [ ] **Step 7: Write failing Resend delivery tests**

Cover missing production secrets, a non-2xx Resend response and success. Verify the request body contains escaped plain text and HTML, reply-to is the validated visitor email, and the subject includes only the localized fixed prefix plus request ID—not visitor-supplied subject text.

- [ ] **Step 8: Implement delivery and fail-closed behavior**

POST to `https://api.resend.com/emails` with bearer `RESEND_API_KEY`, `from`, `to`, fixed localized subject, `reply_to`, `text` and escaped `html`. Return `delivery_failed` with 502 when delivery fails. Never log form fields. Reject Cloudflare published test secrets when `CONTEXT == "production"`.

- [ ] **Step 9: Export Netlify routing and rate limiting**

Add:

```javascript
export const config = {
  path: '/api/contact',
  method: 'POST',
  rateLimit: {
    windowLimit: 8,
    windowSize: 60,
    aggregateBy: ['ip', 'domain'],
  },
};
```

- [ ] **Step 10: Run function and full tests**

Run: `npm run test:function`

Run: `py -3 -m unittest discover -s tests -v`

Expected: all function branches and generated-site tests PASS.

- [ ] **Step 11: Record checkpoint**

Checkpoint files: `netlify/functions/contact.mjs`, `tests/contact-function.test.mjs`, `package.json`, `package-lock.json` if npm changes it.

Suggested commit: `feat: validate turnstile and deliver contact mail server side`.

---

### Task 8: Tighten deployment configuration, CSP and production gates

**Files:**
- Modify: `netlify.toml`
- Modify: `build_site.py`
- Modify: `tests/test_site_output.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: contact route `/api/contact` and Turnstile domains.
- Produces: production build validation and browser security policy.

- [ ] **Step 1: Write failing security-policy tests**

Add:

```python
def test_security_headers_allow_only_required_turnstile_browser_domains(self) -> None:
    config = (ROOT / "netlify.toml").read_text(encoding="utf-8")
    self.assertIn("object-src 'none'", config)
    self.assertIn("upgrade-insecure-requests", config)
    self.assertIn("Strict-Transport-Security", config)
    self.assertIn("https://challenges.cloudflare.com", config)
    self.assertNotIn("api.resend.com", config)

def test_production_build_rejects_missing_legal_identity(self) -> None:
    env = {"CONTEXT": "production", "PATH": os.environ.get("PATH", "")}
    result = subprocess.run(
        [sys.executable, "build_site.py"], cwd=ROOT, env=env,
        text=True, capture_output=True,
    )
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("Missing production legal configuration", result.stderr + result.stdout)
```

Import `os` in the test file.

- [ ] **Step 2: Run tests and verify header/gate failures**

Run: `py -3 -m unittest tests.test_site_output.SiteOutputTests.test_security_headers_allow_only_required_turnstile_browser_domains tests.test_site_output.SiteOutputTests.test_production_build_rejects_missing_legal_identity -v`

Expected: FAIL because the current CSP lacks Turnstile, HSTS and `object-src`, and production validation is not active.

- [ ] **Step 3: Update Netlify headers**

Use this CSP shape, preserving a single-line header value:

```text
default-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self' https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; connect-src 'self' https://challenges.cloudflare.com; upgrade-insecure-requests
```

Add `Strict-Transport-Security = "max-age=31536000; includeSubDomains"`, `Cross-Origin-Opener-Policy = "same-origin-allow-popups"`, retain strict referrer and permissions policies, and do not add Resend to browser CSP.

- [ ] **Step 4: Document environment configuration**

In `README.md`, list every legal identity variable, `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY`, `TURNSTILE_EXPECTED_HOSTNAME`, `RESEND_API_KEY`, `CONTACT_TO_EMAIL` and `CONTACT_FROM_EMAIL`. State that form delivery is disabled until all production variables are set and a staging submission is received.

- [ ] **Step 5: Parse configuration and run security tests**

Run: `py -3 -c "import tomllib; tomllib.load(open('netlify.toml','rb')); print('netlify.toml: OK')"`

Run: `py -3 -m unittest discover -s tests -v`

Expected: TOML parses and all security tests PASS.

- [ ] **Step 6: Record checkpoint**

Checkpoint files: `netlify.toml`, `build_site.py`, `tests/test_site_output.py`, `README.md`.

Suggested commit: `security: enforce production identity and turnstile policy`.

---

### Task 9: Complete visual, accessibility and release verification

**Files:**
- Modify: `tests/e2e/site.spec.mjs`
- Modify: `tests/e2e/responsive.spec.mjs`
- Modify: `lighthouserc.json`
- Modify: `docs/release-checklist.md`
- Modify: `docs/content-signoff.md`

**Interfaces:**
- Consumes: all public bilingual routes and `/api/contact`.
- Produces: evidence-backed release gate with explicit external approvals.

- [ ] **Step 1: Expand Axe coverage before final styling changes**

Run Axe critical/serious checks for home, contact, privacy, cookies, terms, accessibility and one service page in both languages. Add keyboard checks for header menu, service disclosure, FAQ, privacy preferences and form error recovery.

- [ ] **Step 2: Run the browser suite and correct every reproducible failure**

Run: `npm run test:e2e`

Expected: PASS on desktop and mobile projects. If the local Playwright browser is absent, install the matching build with `npx playwright install chromium`; do not mark browser QA complete until it runs.

- [ ] **Step 3: Capture visual evidence at release widths**

Capture full-page PNGs for:

- Hebrew home at 1440 × 1100 and 390 × 844.
- Hebrew contact at 1440 × 1100 and 390 × 844.
- English home at 1440 × 1100 and 390 × 844.
- One Hebrew service page at 768 × 1024.

Inspect each saved image for clipping, unintended empty space, text/image crop, logo scale, focus visibility and legal-disclosure obstruction. Reject and recapture any incomplete image.

- [ ] **Step 4: Run Lighthouse against the built site**

Run: `npm run lighthouse`

Expected minimums: Performance 0.90, Accessibility 0.95, Best Practices 0.95, SEO 0.95 on representative Hebrew and English pages.

- [ ] **Step 5: Run the complete deterministic verification set**

Run:

```powershell
py -3 -m py_compile build_site.py
py -3 -m unittest discover -s tests -v
npm run test:function
npm run test:e2e
npm audit --omit=dev --audit-level=high
```

Expected: all tests PASS and production dependency audit reports zero high-severity vulnerabilities.

- [ ] **Step 6: Update release gates with exact status**

Add checklist rows for legal identity, counsel approval, accessibility review, image rights, staging Turnstile, Resend receipt, reply-to behavior, Netlify deploy-log rate-limit confirmation, CSP console errors, browser screenshots and Lighthouse scores. Keep each external approval `Pending` until a named reviewer and date are recorded.

- [ ] **Step 7: Record final checkpoint**

Checkpoint files: all files listed in this plan plus generated `dist/` output for local inspection. `dist/` remains ignored and is rebuilt during deployment.

Suggested commit: `chore: verify institutional redesign release readiness`.
