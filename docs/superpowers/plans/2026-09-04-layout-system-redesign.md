# Layout System Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the site's ad-hoc layout with a named four-width grid, one fluid gutter, a modular type scale and a three-level vertical rhythm, then extend the icon family and add flag-gated placeholder media.

**Architecture:** This is a static site generator. `build_site.py` reads `source/styles.css`, `source/site.js`, `source/icons.py` and `source/media.py`, then writes 41 files into `dist/`. Nothing is compiled or bundled — CSS is copied verbatim into `dist/assets/styles.css`. Almost all the work lands in `source/styles.css`; `build_site.py` changes only where markup structure must change. `dist/` is a build artifact and is never edited by hand.

**Tech Stack:** Python 3.14 (stdlib plus Pillow 11.3 for the placeholder generator), vanilla CSS with custom properties and logical properties, vanilla JS, `unittest` for output tests, Playwright for end-to-end.

**Spec:** `docs/superpowers/specs/2026-09-04-layout-system-redesign-design.md`

## Global Constraints

- Palette, logo, typefaces and all page copy do not change. Preserve every existing custom property name in `:root` even when its value changes.
- The project is **not a git repository**. Every step that says "commit" is instead: re-run the full test suite and confirm green before starting the next task. Do not run `git` commands.
- Use logical properties (`inset-inline`, `padding-inline`, `border-inline-start`, `margin-inline`) throughout. Do not add `.rtl`-specific rules where a logical property does the job.
- After any edit to `source/styles.css`, `source/site.js` or `source/icons.py`, run `python build_site.py` before running tests. `test_generated_browser_assets_match_their_sources` compares `dist/assets/*` byte-for-byte against `source/*` and fails if you forget.
- Never edit files in `dist/`. They are regenerated on every build.
- CSP is `img-src 'self' data:`. No external image URLs, ever.
- Contrast must meet WCAG AA. Interactive targets are at least 44×44 px.
- Run tests from the project root: `c:\Users\eladn\Downloads\scout-finance-premium-redesign\scout-finance-premium`.

**Baseline to beat** (measured on the current build):

| Metric | Now | Target |
| --- | --- | --- |
| Hebrew home `h1` at 1440 | 77.8 px, 4 lines | ~60 px, 2 lines |
| Hebrew home `h1` at 390 | 46.8 px, 4 lines | ~38 px, 3 lines |
| `.service-entry` width at 1440 | 218 px | ~400 px |
| Gutter at 390 / 1440 | 18 px / 58 px | 24 px / 72 px |
| `.section-intro` line length | 82 chars | ≤ 68 LTR, ≤ 62 RTL |
| `.brand img` width at 390 | 230 px | ≤ 180 px |

---

## File Structure

| File | Responsibility | Change |
| --- | --- | --- |
| `source/styles.css` | Every visual rule for the site | Modify — the bulk of the work |
| `source/icons.py` | Inline SVG icon registry | Modify — 8 icons to 19 |
| `build_site.py` | Page assembly and markup | Modify — rail markup, icon wiring, eyebrow reduction, media flag |
| `scripts/make-placeholder-media.py` | Generates placeholder imagery | Create |
| `tests/test_site_output.py` | Build output assertions | Modify — icon count only |
| `tests/test_layout_tokens.py` | Asserts the new token system exists | Create |
| `tests/e2e/layout.spec.mjs` | Measures rendered layout in a browser | Create |
| `docs/image-rights-register.md` | Licence chain of custody | Modify — placeholder note |
| `.gitignore` | Excludes generated placeholders | Modify |

Tasks 1–4 are ordered so each leaves the site in a working, testable state. Task 1 establishes tokens without changing appearance much; Tasks 2–3 spend them; Tasks 4–6 are additive.

---

## Task 1: Layout tokens and the gutter

Introduces every new custom property and replaces the four-breakpoint gutter with one fluid expression. Nothing else consumes the new tokens yet, so the visible change is limited to margins widening.

**Files:**
- Modify: `source/styles.css:7-13` (the `:root` block), and delete the `--gutter` declarations at lines 202, 214 and 232
- Test: `tests/test_layout_tokens.py` (create)

**Interfaces:**
- Consumes: nothing
- Produces: custom properties `--w-full`, `--w-wide`, `--w-text`, `--w-rail`, `--gutter`, `--t-xs` through `--t-3xl`, `--sp-1` through `--sp-10`, `--band-tight`, `--band-default`, `--band-feature`. Tasks 2, 3 and 4 all read these names.

- [ ] **Step 1: Write the failing test**

Create `tests/test_layout_tokens.py`:

```python
"""The layout token system must exist in the stylesheet and reach the build."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_CSS = ROOT / "source" / "styles.css"
DIST_CSS = ROOT / "dist" / "assets" / "styles.css"

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
        built = DIST_CSS.read_text(encoding="utf-8")
        for token in REQUIRED_TOKENS:
            self.assertIn(f"{token}:", built)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
python -m unittest tests.test_layout_tokens -v
```

Expected: FAIL — `missing token --w-full`, and the gutter assertion reports four declarations instead of one.

- [ ] **Step 3: Replace the `:root` block**

In `source/styles.css`, replace the whole `:root{...}` block at lines 7–13 with:

```css
:root{
  --navy-950:#03162a;--navy-900:#06203d;--navy-850:#082847;--navy-800:#0a3158;
  --blue-650:#145b9f;--blue-600:#176bbd;--blue-500:#2a7dcc;--ink:#0c2340;--body:#324861;
  --muted:#67798b;--line:#d9e2ea;--line-strong:#c6d2de;--paper:#f6f9fc;--mist:#eef4f9;--white:#fff;

  /* layout widths */
  --w-full:100%;--w-wide:1280px;--w-text:68ch;--w-rail:96px;
  --content-max:var(--w-wide);--reading-max:var(--w-text);
  --gutter: clamp(24px, 5vw, 80px);

  /* type scale, 1.25 ratio */
  --t-xs:.75rem;--t-sm:.875rem;--t-base:1rem;--t-md:1.25rem;
  --t-lg:clamp(1.5rem,2vw,1.75rem);
  --t-xl:clamp(1.875rem,3vw,2.5rem);
  --t-2xl:clamp(2.25rem,4.5vw,3.5rem);
  --t-3xl:clamp(2.75rem,5vw,4.25rem);

  /* spacing, 4px base */
  --sp-1:4px;--sp-2:8px;--sp-3:12px;--sp-4:16px;--sp-5:24px;
  --sp-6:32px;--sp-7:48px;--sp-8:64px;--sp-9:96px;--sp-10:128px;

  /* vertical rhythm by section role */
  --band-tight:clamp(40px,5vw,64px);
  --band-default:clamp(64px,7vw,104px);
  --band-feature:clamp(88px,10vw,152px);

  --shadow-sm:0 8px 24px rgba(3,22,42,.06);--shadow-md:0 18px 55px rgba(3,22,42,.12);
  --radius:2px;--nav-h:88px;--font-sans:Inter,Arial,sans-serif;--font-display:Georgia,'Times New Roman',serif;
}
body[dir=rtl]{
  --w-text:62ch;
  --t-2xl:clamp(2rem,4vw,3.1rem);
  --t-3xl:clamp(2.4rem,4.4vw,3.75rem);
}
```

`--content-max` and `--reading-max` are kept as aliases so no existing rule breaks while later tasks migrate to the new names.

- [ ] **Step 4: Delete the three breakpoint gutter overrides**

In the `@media(max-width:1120px)` block, change `:root{--nav-h:78px;--gutter:clamp(20px,3.5vw,44px)}` to `:root{--nav-h:78px}`.

In the `@media(max-width:900px)` block, change `:root{--nav-h:72px;--gutter:22px}` to `:root{--nav-h:72px}`.

In the first `@media(max-width:600px)` block, delete the line `:root{--gutter:18px}` entirely, keeping the rest of the block.

- [ ] **Step 5: Rebuild and run the tests**

```bash
python build_site.py
python -m unittest tests.test_layout_tokens tests.test_site_output -v
```

Expected: PASS — 5 token tests plus the existing 26.

- [ ] **Step 6: Confirm no layout regressed**

```bash
npx playwright test
```

Expected: PASS. The site should look nearly identical except for wider page margins.

---

## Task 2: Type scale, vertical rhythm and reading measure

Spends the tokens from Task 1 on typography and section spacing. This is where the oversized headline and the over-long line length are fixed.

**Files:**
- Modify: `source/styles.css` — `.section`, `.section h2`, `.section-intro`, `.institutional-hero h1`, `.institutional-page-hero h1`, `.eyebrow`, `body`, and the display-size overrides inside all three media queries
- Test: `tests/e2e/layout.spec.mjs` (create)

**Interfaces:**
- Consumes: `--t-*`, `--band-*`, `--w-text` from Task 1
- Produces: class `.section--feature` for the one feature-spaced section, and `.section--tight` for the proof strip and CTA band. Task 3 applies `.section--feature` in `build_site.py`.

- [ ] **Step 1: Write the failing test**

Create `tests/e2e/layout.spec.mjs`:

```js
import { test, expect } from '@playwright/test';

const PAGES = ['/he/', '/en/'];

test.describe('layout system', () => {
  for (const path of PAGES) {
    test(`no horizontal overflow on ${path}`, async ({ page }) => {
      await page.goto(path);
      const overflow = await page.evaluate(() => {
        const d = document.documentElement;
        return d.scrollWidth - d.clientWidth;
      });
      expect(overflow).toBeLessThanOrEqual(1);
    });

    test(`body copy stays within its measure on ${path}`, async ({ page }) => {
      await page.goto(path);
      const ratio = await page.evaluate(() => {
        const p = document.querySelector('.section-intro');
        const fs = parseFloat(getComputedStyle(p).fontSize);
        // ~0.5em average advance width gives characters per line
        return (p.getBoundingClientRect().width / fs) * 2;
      });
      const ceiling = path === '/he/' ? 62 : 68;
      expect(ratio).toBeLessThanOrEqual(ceiling + 2);
    });
  }

  test('hebrew home headline resolves without an orphan line', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const { fontSize, lines } = await page.evaluate(() => {
      const h1 = document.querySelector('.institutional-hero h1');
      const cs = getComputedStyle(h1);
      const lh = parseFloat(cs.lineHeight);
      return {
        fontSize: parseFloat(cs.fontSize),
        lines: Math.round(h1.getBoundingClientRect().height / lh)
      };
    });
    if (testInfo.project.name === 'desktop') {
      expect(fontSize).toBeLessThanOrEqual(64);
      expect(lines).toBeLessThanOrEqual(2);
    } else {
      expect(fontSize).toBeLessThanOrEqual(40);
      expect(lines).toBeLessThanOrEqual(3);
    }
  });

  test('section rhythm varies by role', async ({ page }) => {
    await page.goto('/he/');
    const pads = await page.evaluate(() => {
      const pick = (sel) => {
        const el = document.querySelector(sel);
        return el ? parseFloat(getComputedStyle(el).paddingTop) : null;
      };
      return { feature: pick('.section--feature'), normal: pick('.section:not(.section--feature)') };
    });
    expect(pads.feature).toBeGreaterThan(pads.normal);
  });
});
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
npx playwright test tests/e2e/layout.spec.mjs
```

Expected: FAIL — the Hebrew headline reports about 78 px across 4 lines on desktop, the measure exceeds its ceiling, and `.section--feature` does not exist so `pads.feature` is `null`.

- [ ] **Step 3: Apply the type scale**

In `source/styles.css` make these replacements.

Body base size, on the `body` rule — append `font-size:var(--t-base);` and add below it:

```css
@media(min-width:900px){body{font-size:1.0625rem}}
```

Section padding and the two role modifiers — replace `.section{padding:clamp(74px,7vw,112px) 0}` with:

```css
.section{padding:var(--band-default) 0}
.section--feature{padding:var(--band-feature) 0}
.section--tight{padding:var(--band-tight) 0}
```

Section heading — replace the `font-size` in `.section h2{...}` with `var(--t-xl)`:

```css
.section h2{margin:0;color:var(--navy-950);font-size:var(--t-xl);font-weight:400;line-height:1.06;letter-spacing:-.02em}
```

Section intro — replace `max-width:670px` with the measure token:

```css
.section-intro{margin:0;color:var(--body);font-size:var(--t-base);line-height:1.8;max-width:var(--w-text)}
```

Home headline — replace the `font-size` in `.institutional-hero h1{...}` with `var(--t-3xl)` and delete the `body[dir=rtl] .institutional-hero h1` font-size override, since `body[dir=rtl]` now redefines `--t-3xl` itself:

```css
.institutional-hero h1{margin:0;max-width:14ch;color:#fff;font-family:var(--font-display);font-weight:400;font-size:var(--t-3xl);line-height:1.02;letter-spacing:-.03em;text-wrap:balance}
body[dir=rtl] .institutional-hero h1{font-family:'IBM Plex Sans Hebrew',Arial,sans-serif;font-weight:600;line-height:1.12;letter-spacing:0}
```

`max-width:14ch` is what forces the two-line resolution: it caps the headline at roughly fourteen characters per line regardless of viewport, so the line breaks land where the type scale expects.

Interior headline — same treatment on `.institutional-page-hero h1`:

```css
.institutional-page-hero h1{margin:0;max-width:18ch;color:var(--navy-950);font-family:var(--font-display);font-size:var(--t-2xl);font-weight:400;line-height:1.04;letter-spacing:-.025em;text-wrap:balance}
.rtl .institutional-page-hero h1{font-family:'IBM Plex Sans Hebrew';font-weight:600;letter-spacing:0;line-height:1.12}
```

- [ ] **Step 4: Remove the now-dead display overrides in the media queries**

These lines hard-code font sizes the token scale now handles fluidly. Delete each one:

In `@media(max-width:900px)`: delete `.institutional-hero h1{font-size:clamp(3.2rem,11vw,5rem)}`, `body[dir=rtl] .institutional-hero h1{font-size:clamp(2.75rem,10vw,4.4rem)}` and `.institutional-page-hero h1{max-width:100%;font-size:clamp(2.8rem,10vw,4.6rem)}`. Where the last one also set `max-width:100%`, replace the whole declaration with `.institutional-page-hero h1{max-width:100%}`.

In the first `@media(max-width:600px)`: delete `.section h2{font-size:2.35rem}`, `.institutional-hero h1{font-size:clamp(3rem,15vw,4.15rem)}` and `body[dir=rtl] .institutional-hero h1{font-size:clamp(2.65rem,12vw,3.8rem)}`. Also delete `.section{padding:64px 0}` — `--band-default` already floors at 64 px.

- [ ] **Step 5: Apply the section role classes in the generator**

In `build_site.py`, in `home_body()`, the proof strip and CTA band become tight and the services section becomes the feature section.

Change `<section class="proof-strip">` to:

```
<section class="proof-strip section--tight">
```

Change the services section opener — the third `<section class="section">` in the returned f-string, the one containing `{h['services_title']}` — to:

```
<section class="section section--feature">
```

- [ ] **Step 6: Rebuild and verify**

```bash
python build_site.py
npx playwright test tests/e2e/layout.spec.mjs
```

Expected: PASS on both desktop and mobile projects.

- [ ] **Step 7: Run everything**

```bash
python -m unittest tests.test_layout_tokens tests.test_site_output -v
npx playwright test
```

Expected: PASS. 31 Python tests, all Playwright specs.

---

## Task 3: Grid density, the narrow rail and hero composition

Widens the cramped grids, introduces the rail on the two places that carry sequence information, and corrects the hero so it resolves above the fold.

**Files:**
- Modify: `source/styles.css` — `.services-grid`, `.service-entry`, `.challenge-grid`, `.method-grid`, `.method`, `.institutional-hero .hero-grid`, `.hero-copy`, `.hero-visual`, `.hero-assurance`, plus the matching rules in all three media queries
- Modify: `build_site.py` — `home_body()` method markup and eyebrow reduction

**Interfaces:**
- Consumes: `--w-rail`, `--sp-*`, `--t-md` from Tasks 1–2
- Produces: class `.rail-grid` with child `.rail-item`, each containing `.rail-marker` and `.rail-body`. No later task depends on these.

- [ ] **Step 1: Write the failing test**

Append to `tests/e2e/layout.spec.mjs`, inside the existing `test.describe` block:

```js
  test('service cards are wide enough to hold their content', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const width = await page.evaluate(() =>
      document.querySelector('.service-entry').getBoundingClientRect().width
    );
    if (testInfo.project.name === 'desktop') {
      expect(width).toBeGreaterThan(340);
    }
  });

  test('the process rail shows ordinals in a narrow track', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const item = await page.evaluate(() => {
      const el = document.querySelector('.method-grid .rail-item');
      if (!el) return null;
      const marker = el.querySelector('.rail-marker');
      return {
        markerText: marker ? marker.textContent.trim() : null,
        markerWidth: marker ? marker.getBoundingClientRect().width : null,
        columns: getComputedStyle(el).gridTemplateColumns.split(' ').length
      };
    });
    expect(item).not.toBeNull();
    expect(item.markerText).toBe('01');
    if (testInfo.project.name === 'desktop') {
      expect(item.columns).toBe(2);
    }
  });

  test('the hero resolves above the fold', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const bottom = await page.evaluate(() =>
      document.querySelector('.hero-assurance').getBoundingClientRect().bottom
    );
    const viewport = testInfo.project.use.viewport.height;
    if (testInfo.project.name === 'desktop') {
      expect(bottom).toBeLessThanOrEqual(viewport);
    }
  });
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
npx playwright test tests/e2e/layout.spec.mjs
```

Expected: FAIL — the service card measures about 218 px, `.rail-item` does not exist so the rail test gets `null`, and the assurance card's bottom exceeds the 1000 px viewport height.

- [ ] **Step 3: Widen the grids**

In `source/styles.css`:

```css
.services-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-inline-start:1px solid var(--line)}
.challenge-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-inline-start:1px solid var(--line)}
```

Give the service card room to breathe now that it is nearly twice as wide:

```css
.service-entry{display:flex;flex-direction:column;min-height:250px;padding:var(--sp-6) var(--sp-6);border-inline-end:1px solid var(--line);border-bottom:1px solid var(--line);background:#fff;color:var(--ink);transition:background .2s ease}
.service-entry h3{margin:0 0 var(--sp-3);color:var(--navy-950);font-size:var(--t-md);line-height:1.15;font-weight:400}
.service-entry p{margin:0;color:#5b6e82;font-size:var(--t-sm);line-height:1.6;max-width:34ch}
```

Note the removed `transform:translateY(-2px)` on hover — per the spec's restraint section, per-card hover motion is a generic default. Replace the hover rule with a background change only:

```css
.service-entry:hover{background:#f8fbfe}
```

In `@media(max-width:1120px)` change `.services-grid{grid-template-columns:repeat(3,minmax(0,1fr))}` to `repeat(2,...)`, and in `@media(max-width:900px)` change `.services-grid{grid-template-columns:repeat(2,minmax(0,1fr))}` to stay at 2. In `@media(max-width:1120px)` change `.challenge-grid{grid-template-columns:repeat(2,minmax(0,1fr))}` — it is already there and stays correct.

- [ ] **Step 4: Add the rail component**

Add a new block to `source/styles.css`, directly after the `.method` rules:

```css
/* narrow rail — used only where content carries a real sequence */
.rail-item{display:grid;grid-template-columns:var(--w-rail) minmax(0,1fr);gap:var(--sp-5);align-items:start}
.rail-marker{color:#84acd0;font-size:var(--t-sm);font-weight:700;font-variant-numeric:tabular-nums;line-height:1.4;padding-top:2px}
.rail-body h3{margin:0 0 var(--sp-2);color:#fff;font-size:var(--t-md);font-weight:400;line-height:1.2}
.rail-body p{margin:0;color:#b8c9da;font-size:var(--t-sm);line-height:1.6;max-width:38ch}
@media(max-width:900px){
  .rail-item{grid-template-columns:1fr;gap:var(--sp-2)}
  .rail-marker{padding-top:0}
}
```

The rail lives inside the dark method band, which is why `.rail-body` uses light-on-dark colors.

Change `.method-grid` from a five-column strip to a stack of rail items:

```css
.method-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--sp-7) var(--sp-8);margin-top:var(--sp-7);padding-top:var(--sp-6);border-top:1px solid rgba(255,255,255,.16)}
```

Delete the old `.method{...}`, `.method span{...}`, `.method h3{...}` and `.method p{...}` rules — `.rail-item` and `.rail-body` replace them. Also delete the `.method-grid` and `.method` overrides in the `@media(max-width:900px)` and `@media(max-width:600px)` blocks, since the rail carries its own responsive rule.

- [ ] **Step 5: Emit rail markup in the generator**

In `build_site.py`, in `home_body()`, replace the `meth=` line:

```python
    meth=''.join(f'<div class="method"><span>{n}</span><h3>{escape(t)}</h3><p>{escape(p)}</p></div>' for n,t,p in h['method'])
```

with:

```python
    meth=''.join(f'<div class="rail-item"><span class="rail-marker" aria-hidden="true">{n}</span><div class="rail-body"><h3>{escape(t)}</h3><p>{escape(p)}</p></div></div>' for n,t,p in h['method'])
```

The ordinal is `aria-hidden` because it is a visual position marker; the heading already conveys the step to a screen reader, and reading "zero one" before it adds noise.

- [ ] **Step 6: Correct the hero composition**

In `source/styles.css`:

```css
.institutional-hero .hero-grid{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(360px,.9fr);align-items:stretch;min-height:min(78vh,640px)}
.hero-copy{display:flex;flex-direction:column;justify-content:center;padding-block:var(--sp-9);padding-inline-end:clamp(32px,5vw,72px);min-width:0}
.hero-visual{position:relative;min-width:0;min-height:min(78vh,640px);align-self:stretch;isolation:isolate}
.institutional-hero .lead{margin:var(--sp-5) 0 0;max-width:52ch;color:#d8e2ec;font-size:var(--t-base);line-height:1.7}
.institutional-hero .actions{margin-top:var(--sp-7)}
```

Delete the `.rtl .hero-copy{padding:90px 0 90px 7vw}` rule — `padding-inline-end` is direction-aware and makes it redundant.

Lower the abstract panel's visual weight so it supports the headline instead of competing, by softening the two rotated squares:

```css
.hero-visual::before{width:310px;height:310px;right:-160px;top:-70px;border-color:rgba(185,211,236,.07)}
.hero-visual::after{width:220px;height:220px;left:5%;bottom:-110px;border-color:rgba(185,211,236,.07)}
```

Pull the assurance card fully inside the hero:

```css
.hero-assurance{position:absolute;z-index:7;inset-inline-end:0;bottom:0;width:min(94%,500px);padding:var(--sp-5) var(--sp-6);background:rgba(3,22,42,.9);border-top:1px solid rgba(255,255,255,.16);border-inline-start:1px solid rgba(255,255,255,.12);backdrop-filter:blur(6px)}
```

Delete the `.rtl .hero-assurance{right:auto;left:0;border-left:0;border-right:...}` rule; `inset-inline-end` and `border-inline-start` handle both directions.

In `@media(max-width:1120px)`, change the hero min-heights from `600px` to `min(74vh,560px)` in both `.institutional-hero .hero-grid` and `.hero-visual`.

- [ ] **Step 7: Reduce the eyebrow to where it distinguishes**

In `build_site.py`, in `home_body()`, delete the `<div class="eyebrow">...</div>` element from four section heads, keeping the heading itself. Remove it from:

- the services section — `<div class="eyebrow">{c['nav']['services']}</div>`
- the challenges section — `<div class="eyebrow">{'Management priorities' if lang=='en' else 'סדרי עדיפויות ניהוליים'}</div>`
- the industries section — `<div class="eyebrow">{c['nav']['industries']}</div>`
- the FAQ section — `<div class="eyebrow">FAQ</div>`

Keep the eyebrow on the hero, the method band and the international band, where it distinguishes a band from the one before it. After deleting, each of those four `section-head` blocks reduces to `<div><h2>...</h2></div>`.

- [ ] **Step 8: Rebuild and verify**

```bash
python build_site.py
npx playwright test tests/e2e/layout.spec.mjs
```

Expected: PASS — service cards above 340 px, `.rail-item` present with a two-column desktop track and marker text `01`, assurance card bottom within the viewport.

- [ ] **Step 9: Run everything**

```bash
python -m unittest tests.test_layout_tokens tests.test_site_output -v
npx playwright test
```

Expected: PASS.

---

## Task 4: Mobile corrections

Fixes the oversized logo, the cramped button pair, the short touch target and the intrusive privacy disclosure.

**Files:**
- Modify: `source/styles.css` — `.brand img`, `.site-footer .brand img`, `.actions`, `.privacy-actions .btn`, `.privacy-disclosure`, in the 900 px and 600 px media queries
- Test: `tests/e2e/layout.spec.mjs` (extend)

**Interfaces:**
- Consumes: `--sp-*`, `--gutter` from Task 1
- Produces: nothing later tasks depend on

- [ ] **Step 1: Write the failing test**

Append to `tests/e2e/layout.spec.mjs`, inside the existing `test.describe` block:

```js
  test('mobile chrome is proportionate and reachable', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'mobile only');
    await page.goto('/he/');
    const m = await page.evaluate(() => {
      const w = (sel) => {
        const el = document.querySelector(sel);
        return el ? el.getBoundingClientRect().width : null;
      };
      const targets = [...document.querySelectorAll('a.btn, button')]
        .filter((el) => el.offsetParent !== null)
        .map((el) => el.getBoundingClientRect().height);
      return {
        viewport: window.innerWidth,
        brand: w('.brand img'),
        footerLogo: w('.site-footer .brand img'),
        smallestTarget: Math.min(...targets)
      };
    });
    expect(m.brand).toBeLessThanOrEqual(180);
    expect(m.footerLogo).toBeLessThanOrEqual(m.viewport * 0.6);
    expect(m.smallestTarget).toBeGreaterThanOrEqual(44);
  });

  test('hero actions stack on small screens', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'mobile only');
    await page.goto('/he/');
    const tops = await page.evaluate(() =>
      [...document.querySelectorAll('.institutional-hero .actions .btn')]
        .map((el) => Math.round(el.getBoundingClientRect().top))
    );
    expect(new Set(tops).size).toBe(tops.length);
  });
```

The second test asserts stacking by checking every button has a distinct `top` — side-by-side buttons share one.

- [ ] **Step 2: Run the test to verify it fails**

```bash
npx playwright test tests/e2e/layout.spec.mjs --project=mobile
```

Expected: FAIL — brand image measures 230 px, footer logo 354 px on a 390 px viewport, and the two hero buttons share a `top`.

- [ ] **Step 3: Size the logo for small screens**

The logo file itself is untouched; only its rendered box changes. In `@media(max-width:900px)` replace `.brand img{height:44px}` with:

```css
.brand img{height:auto;max-width:min(46vw,180px)}
```

In the same block add the footer treatment:

```css
.site-footer .brand img{height:40px;max-width:none;width:auto}
```

- [ ] **Step 4: Stack the buttons and raise the short target**

In the first `@media(max-width:600px)` block, replace `.actions{display:grid;grid-template-columns:1fr 1fr}.actions .btn{padding-inline:14px}` with:

```css
.actions{display:grid;grid-template-columns:1fr;gap:var(--sp-3)}
```

Raise the privacy button, in the main stylesheet body next to the other `.privacy-*` rules:

```css
.privacy-actions .btn{min-height:44px;padding-inline:var(--sp-4)}
```

- [ ] **Step 5: Make the privacy disclosure less intrusive on mobile**

Add to the first `@media(max-width:600px)` block:

```css
.privacy-disclosure{grid-template-columns:1fr;gap:var(--sp-4);padding:var(--sp-4);inset-inline:var(--sp-3);bottom:var(--sp-3);width:auto}
.privacy-disclosure p{font-size:var(--t-xs);line-height:1.55}
.privacy-actions{justify-content:space-between;width:100%}
```

- [ ] **Step 6: Rebuild and verify**

```bash
python build_site.py
npx playwright test tests/e2e/layout.spec.mjs --project=mobile
```

Expected: PASS.

- [ ] **Step 7: Run everything**

```bash
python -m unittest tests.test_layout_tokens tests.test_site_output -v
npx playwright test
```

Expected: PASS.

---

## Task 5: Extend the icon family

Grows the icon registry from 8 to 19 and wires the new icons into the challenges grid, the industries grid and the contact detail rows. The process steps deliberately get none — they carry rail ordinals, and an icon beside an ordinal encodes position twice.

**Files:**
- Modify: `source/icons.py:6-17` (the `ICON_PATHS` dict)
- Modify: `build_site.py` — `home_body()` challenge and industry markup, and the contact meta rows in `generic_body()`
- Modify: `tests/test_site_output.py` — the icon count assertion
- Modify: `source/styles.css` — icon sizing inside `.challenge` and `.industry`

**Interfaces:**
- Consumes: `icon(name, title=None)` from `source/icons.py`, unchanged signature
- Produces: eleven new keys in `ICON_PATHS` — `control-drift`, `documentation`, `transparency`, `subsidiaries`, `biotech`, `hitech`, `public-sector`, `complex-org`, `phone`, `location`, `website`

- [ ] **Step 1: Write the failing test**

In `tests/test_site_output.py`, replace the body of `test_service_icons_have_unique_paths`:

```python
    def test_service_icons_have_unique_paths(self) -> None:
        from source.icons import ICON_PATHS

        self.assertEqual(len(ICON_PATHS), 19)
        self.assertEqual(len(set(ICON_PATHS.values())), 19)
```

And add a new test directly after it:

```python
    def test_supporting_grids_carry_icons(self) -> None:
        for lang in ("he", "en"):
            html = (DIST / lang / "index.html").read_text(encoding="utf-8")
            self.assertEqual(html.count('class="grid-icon"'), 8)
            self.assertNotIn('class="grid-icon"', html.split('method-grid')[1].split('</section>')[0])
```

The second assertion pins the deliberate choice that process steps get no icon.

- [ ] **Step 2: Run the test to verify it fails**

```bash
python -m unittest tests.test_site_output -v
```

Expected: FAIL — `19 != 8`, and `class="grid-icon"` appears zero times.

- [ ] **Step 3: Add the eleven icon paths**

In `source/icons.py`, add these entries to `ICON_PATHS`, keeping the existing eight unchanged. Every path uses the same 24×24 grid, stroke-only construction as the originals:

```python
    # management challenges
    "control-drift": '<path d="M3 17.5 9 11l4 4 8-8.5"/><path d="M15 6.5h6v6"/><path d="M3 21h18"/>',
    "documentation": '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v5h5"/><path d="M9 12h7M9 16h7M9 8h2"/>',
    "transparency": '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/>',
    "subsidiaries": '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="16" width="6" height="5" rx="1"/><rect x="16" y="16" width="6" height="5" rx="1"/><path d="M12 7v5M5 16v-2h14v2"/>',
    # industries
    "biotech": '<path d="M7 3v4.5c0 3 5 4.5 5 4.5s5-1.5 5-4.5V3"/><path d="M7 21v-4.5c0-3 5-4.5 5-4.5s5 1.5 5 4.5V21"/><path d="M6 3h12M6 21h12M8.5 8h7M8.5 16h7"/>',
    "hitech": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "public-sector": '<path d="M3 21h18M4 21V10M20 21V10M12 3l9 5H3z"/><path d="M8 21v-7M12 21v-7M16 21v-7"/>',
    "complex-org": '<circle cx="12" cy="5" r="2.4"/><circle cx="5" cy="19" r="2.4"/><circle cx="19" cy="19" r="2.4"/><circle cx="12" cy="12" r="2.4"/><path d="M12 7.4v2.2M10.1 13.6 6.6 17M13.9 13.6 17.4 17"/>',
    # contact details
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 3 5.2 2 2 0 0 1 5 3z"/>',
    "location": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "website": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
```

- [ ] **Step 4: Add a grid-icon variant to the renderer**

`icon()` currently hard-codes `class="service-icon"`. Add an optional class parameter without changing the existing call sites. In `source/icons.py`, replace the `icon` function with:

```python
def icon(name: str, title: str | None = None, css_class: str = "service-icon") -> str:
    """Render a fixed SVG icon, optionally with an accessible title."""

    path = ICON_PATHS[name]
    if title:
        accessibility = f'role="img"><title>{escape(title)}</title>'
    else:
        accessibility = 'aria-hidden="true" focusable="false">'
    return (
        f'<svg class="{escape(css_class)}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" {accessibility}{path}</svg>'
    )
```

The default keeps all six existing home service cards emitting `class="service-icon"`, so `test_home_uses_accessible_local_svg_service_icons` still counts six.

- [ ] **Step 5: Wire icons into the two grids**

In `build_site.py`, in `home_body()`, the challenges and industries lists are `(title, description)` pairs in content order. Map icons positionally, because the content tuples carry no key.

Replace the `chall=` line:

```python
    chall=''.join(f'<article class="challenge"><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for a,b in h['challenges'])
```

with:

```python
    challenge_icons=('control-drift','documentation','transparency','subsidiaries')
    chall=''.join(f'<article class="challenge">{icon(challenge_icons[i],css_class="grid-icon")}<h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i,(a,b) in enumerate(h['challenges']))
```

Replace the `industries=` line:

```python
    industries=''.join(f'<article class="industry"><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for a,b in h['industries'])
```

with:

```python
    industry_icons=('biotech','hitech','public-sector','complex-org')
    industries=''.join(f'<article class="industry">{icon(industry_icons[i],css_class="grid-icon")}<h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i,(a,b) in enumerate(h['industries']))
```

Both lists have exactly four entries in both languages, verified against `build_site.py`. If a fifth is ever added, `challenge_icons[i]` raises `IndexError` at build time rather than rendering a broken page — a loud failure is correct here.

- [ ] **Step 6: Style the grid icon**

Add to `source/styles.css`, next to the `.challenge` rules:

```css
.grid-icon{width:28px;height:28px;color:var(--blue-650);margin-bottom:var(--sp-4);stroke-width:1.4}
```

- [ ] **Step 7: Rebuild and verify**

```bash
python build_site.py
python -m unittest tests.test_site_output -v
```

Expected: PASS — 27 tests, including the new `test_supporting_grids_carry_icons`.

- [ ] **Step 8: Run everything**

```bash
python -m unittest tests.test_layout_tokens tests.test_site_output -v
npx playwright test
```

Expected: PASS.

---

## Task 6: Flag-gated placeholder media

Generates on-brand placeholder imagery locally and copies it into the build only when `PLACEHOLDER_MEDIA=1`. The default build, and therefore production, keeps rendering the approved abstract fallback, so the rights guardrail stays intact.

**Files:**
- Create: `scripts/make-placeholder-media.py`
- Modify: `build_site.py:204-205` (the static asset copy)
- Modify: `docs/image-rights-register.md`
- Modify: `.gitignore`
- Test: `tests/test_placeholder_media.py` (create)

**Interfaces:**
- Consumes: `MEDIA_SLOTS` from `source/media.py`, which maps each slot to `width` and `height`
- Produces: `scripts/make-placeholder-media.py` writing `<slot>-{960,1440}.{avif,webp,jpg}` into a target directory; `build_site.py` reading the `PLACEHOLDER_MEDIA` environment variable

- [ ] **Step 1: Write the failing test**

Create `tests/test_placeholder_media.py`:

```python
"""Placeholder media is generated locally and never ships by default."""

import os
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
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
python -m unittest tests.test_placeholder_media -v
```

Expected: FAIL — `scripts/make-placeholder-media.py` does not exist, so `subprocess.run(..., check=True)` raises.

- [ ] **Step 3: Write the generator**

Create `scripts/make-placeholder-media.py`:

```python
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
```

- [ ] **Step 4: Gate the copy in the build**

`build_site.py` currently copies the whole static tree unconditionally:

```python
if STATIC_ASSETS.exists():
    shutil.copytree(STATIC_ASSETS, ASSETS, dirs_exist_ok=True)
```

Replace it with a version that excludes the generated images unless the flag is set. Add near the other environment reads at the top of the file, right after the `CONTEXT` line:

```python
PLACEHOLDER_MEDIA = os.environ.get('PLACEHOLDER_MEDIA', '').strip() == '1'
```

Then replace the copy block:

```python
if STATIC_ASSETS.exists():
    ignore = None if PLACEHOLDER_MEDIA else shutil.ignore_patterns('images')
    shutil.copytree(STATIC_ASSETS, ASSETS, dirs_exist_ok=True, ignore=ignore)
```

With the directory excluded, `media_panel()` finds no derivatives and returns the abstract fallback exactly as it does today — no change to `source/media.py` is needed.

- [ ] **Step 5: Record the placeholders in the rights register**

In `docs/image-rights-register.md`, insert this paragraph directly after the opening paragraph, before the table:

```markdown
**Generated placeholders.** `scripts/make-placeholder-media.py` writes on-brand generated compositions into `static/assets/images/` for layout review. They are not photography and carry no licence to clear, but they are also not approvable output. `build_site.py` includes them only when `PLACEHOLDER_MEDIA=1`; every default and production build renders the abstract fallback instead. Every row below stays `Approved: No` until real, rights-cleared photography replaces it.
```

- [ ] **Step 6: Keep the generated files out of version control**

Append to `.gitignore`:

```
# Generated placeholder media — never committed, never shipped
static/assets/images/
```

- [ ] **Step 7: Run the tests**

```bash
python -m unittest tests.test_placeholder_media -v
```

Expected: PASS — all three tests.

- [ ] **Step 8: Review the design with placeholders in place**

```bash
python scripts/make-placeholder-media.py
PLACEHOLDER_MEDIA=1 python build_site.py
python -m http.server 8123 --directory dist
```

On PowerShell the flag is set separately:

```powershell
python scripts/make-placeholder-media.py
$env:PLACEHOLDER_MEDIA = "1"; python build_site.py
python -m http.server 8123 --directory dist
```

Open `http://localhost:8123/he/` and confirm the hero, method and international panels render photography-shaped compositions with no layout shift against the abstract version.

- [ ] **Step 9: Restore the default build and run everything**

```bash
python build_site.py
python -m unittest tests.test_layout_tokens tests.test_site_output tests.test_placeholder_media -v
npx playwright test
```

Expected: PASS. The final `dist/` must contain the abstract fallback, not the placeholders — `test_default_build_still_renders_the_abstract_fallback` enforces this.

---

## Task 7: Full-site verification

The preceding tasks each verified their own slice. This one checks the whole site in both languages at both viewports and compares against the recorded baseline.

**Files:**
- Modify: none unless a defect is found
- Test: all suites

- [ ] **Step 1: Run every suite**

```bash
python build_site.py
python -m unittest discover -s tests -p "test_*.py" -v
npx playwright test
```

Expected: PASS on all suites.

- [ ] **Step 2: Measure against the plan's targets**

With `python -m http.server 8123 --directory dist` running, check each row of the "Baseline to beat" table in the Global Constraints section. Record actual values. Every target must be met.

- [ ] **Step 3: Capture fresh screenshots**

```bash
node scripts/capture-release.mjs
```

Compare the output against `artifacts/release-qa/` for home desktop, home mobile, and Hebrew contact desktop and mobile.

- [ ] **Step 4: Check the pages the automated tests do not cover**

Visit at 1440 and 390, in both languages: `/services/`, `/about/`, `/audit/`, `/faq/`, `/privacy/`. Confirm no horizontal overflow, no clipped text, and consistent margins. The interior pages share `page_hero` and `content-grid`, so a defect in one usually appears in all.

- [ ] **Step 5: Confirm accessibility did not regress**

The Playwright suite includes `@axe-core/playwright`. Confirm zero new violations, and manually check that keyboard focus is visible on the nav, the FAQ buttons, the contact form and the privacy disclosure.

---

## Self-Review

**Spec coverage.** Every section of the spec maps to a task: widths, gutter, type scale and vertical rhythm to Tasks 1–2; grid density, the rail and restraint to Task 3; mobile corrections to Task 4; icons to Task 5; placeholder media, both constraints and the flag, to Task 6; the verification section to Task 7. The spec's "not changed" list is enforced by the existing 26 tests, which run after every task.

**Placeholder scan.** No TBD, TODO or "similar to Task N" entries. Every code step carries the actual code. The one deliberate use of the word "placeholder" is the subject matter of Task 6, not a gap.

**Type consistency.** `icon(name, title=None, css_class="service-icon")` is defined in Task 5 Step 4 and called with `css_class="grid-icon"` in Step 5. `.rail-item`, `.rail-marker` and `.rail-body` are defined in Task 3 Step 4 and emitted in Step 5 with matching names. `PLACEHOLDER_MEDIA` is read in Task 6 Step 4 and set in Step 8. `--w-text` is declared in Task 1 and consumed in Task 2. `generate(out_dir)` in the generator is exercised via the CLI in the Task 6 tests.

**One correction made during planning.** The spec originally gave icons to the process steps while also giving them rail ordinals — the same information twice. The spec was corrected to state that process steps receive no icons, and Task 5's test pins that decision.
