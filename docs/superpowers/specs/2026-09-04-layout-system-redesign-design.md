# Scout Finance — Layout system redesign

## Purpose

The Institutional Precision redesign (see `2026-09-04-institutional-redesign-compliance-design.md`) established the palette, typefaces and component inventory. Those are correct and are preserved.

What was never built is a **layout system**. The site has one container width for every kind of content, one section rhythm for every kind of section, and a type scale without a governing ratio. Every measured defect below traces back to those three gaps.

This spec replaces the ad-hoc layout with a named, four-width grid; a single fluid gutter expression; a modular type scale; and a three-level vertical rhythm. It also extends the icon family across the site and introduces flag-gated placeholder media so the design can be reviewed with imagery in place.

Palette, logo, typefaces, content and component inventory do not change.

## Confirmed direction

Between Big Four institutional restraint and sharp senior boutique. The discipline, whitespace and typographic quiet of a large firm, carried by one clear visual position rather than four competing ones.

Practically: the home hero is the memorable element and everything else lowers its voice.

## Baseline measurements

Measured on the live build at 1440×900 and 390×844, Hebrew home and contact pages.

| Property | Measured | Problem |
| --- | --- | --- |
| `--content-max` | 1420 px | One width serves grids and running text alike |
| `.section-intro` line length | 82 characters | Above the 80-character ceiling |
| Home `h1` (he, 1440) | 77.8 px, 4 lines | Orphan word `מורכבים.` on line 4 |
| Home `h1` (he, 390) | 46.8 px, 4 lines, 197 px tall | Consumes the fold |
| `.service-entry` (1440) | 218 px wide | Heading plus paragraph do not fit |
| `--gutter` | Redefined at 3 breakpoints; 18 px at 390 | Tight, and four places to change |
| `.section` padding | `clamp(74px,7vw,112px)`, 64 px mobile | Identical for every section role |
| `.brand img` (390) | 230 px wide — 59% of viewport | Oversized |
| Footer logo (390) | 354 px wide — full bleed | Oversized |
| Document height | 6062 px desktop / 9941 px mobile | Monotonous scroll |

No horizontal overflow was found at either viewport, and RTL is structurally sound. This is refinement, not rescue.

## Layout system

### Widths

Four named widths replace the single container. Each content block declares which it belongs to.

| Token | Value | Used by |
| --- | --- | --- |
| `--w-full` | `100%` | Hero, dark bands, media panels |
| `--w-wide` | `1280px` | Grids, cards, structural bands |
| `--w-text` | `68ch` (LTR) / `62ch` (RTL) | Headings, paragraphs, lists |
| `--w-rail` | `96px` | The narrow track (desktop only) |

`--w-text` is set in `ch` rather than pixels so the measure follows the font size instead of drifting from it. Hebrew is denser per character, so it takes the lower value.

`--content-max` drops from 1420 px to 1280 px, and `--reading-max` is replaced by `--w-text`.

### Gutter

One fluid expression replaces four breakpoint redefinitions:

```css
--gutter: clamp(24px, 5vw, 80px);
```

Resulting margins: 24 px at 390, 38 px at 768, 72 px at 1440, 80 px at 1600 and above. The `--gutter` declarations inside the 1120 px, 900 px and 600 px media queries are deleted.

### Type scale

A modular scale on a 1.25 ratio, fluid where size must respond to viewport.

| Token | Value | Role |
| --- | --- | --- |
| `--t-xs` | `0.75rem` | Labels, metadata |
| `--t-sm` | `0.875rem` | Card body, captions |
| `--t-base` | `1rem`, `1.0625rem` above 900 px | Running text |
| `--t-md` | `1.25rem` | Card headings |
| `--t-lg` | `clamp(1.5rem, 2vw, 1.75rem)` | `h3` |
| `--t-xl` | `clamp(1.875rem, 3vw, 2.5rem)` | `h2` |
| `--t-2xl` | `clamp(2.25rem, 4.5vw, 3.5rem)` | Interior `h1` |
| `--t-3xl` | `clamp(2.75rem, 5vw, 4.25rem)` | Home `h1` |

Hebrew display sizes take 88% of the Latin value. Hebrew has no ascender/descender variety, so it carries more visual weight at the same nominal size. The existing `body[dir=rtl]` override pattern is kept and recalibrated rather than replaced. Concretely, the two display tokens are overridden under `body[dir=rtl]`:

```css
--t-2xl: clamp(2rem, 4vw, 3.1rem);
--t-3xl: clamp(2.4rem, 4.4vw, 3.75rem);
```

Outcome: the Hebrew home `h1` resolves at 60 px on desktop (2 lines, no orphan) and 38 px at 390 (3 lines), against 77.8 px and 46.8 px today.

### Vertical rhythm

Section spacing becomes a function of the section's role rather than a constant.

| Token | Value | Applied to |
| --- | --- | --- |
| `--band-tight` | `clamp(40px, 5vw, 64px)` | Proof strip, CTA band |
| `--band-default` | `clamp(64px, 7vw, 104px)` | Standard sections |
| `--band-feature` | `clamp(88px, 10vw, 152px)` | The section following the hero |

Inner spacing uses a 4 px base: `--sp-1` 4 through `--sp-10` 128.

### Grid density

| Grid | Now | After |
| --- | --- | --- |
| `.services-grid` | 6 columns (218 px cards) | 3 columns (~400 px) |
| `.challenge-grid` | 4 columns | 3 columns |
| `.method-grid` | 5 columns | 5 columns (short items, correct as is) |

Tablet and mobile column counts follow from these proportionally.

### The narrow rail

A fixed narrow track beside a wide content track, drawn from audit working-paper layout:

```
│ 01 │ הבנה
│    │ מיפוי תהליכים, זיהוי סיכונים
```

Applied to exactly two places, both of which already carry sequence information:

- `.method-grid` — the process section. Understanding, assessment, execution, implementation, retention is a genuine sequence, so ordinal markers are legitimate.
- `.services-grid > .service-card` on the services landing page, which already renders `.service-num`.

Everywhere else the rail is not used. Below 900 px it collapses to an inline label above the heading.

Built with logical properties (`inset-inline`, `padding-inline`, `border-inline`) so RTL needs no duplicate rules.

## Restraint

Boldness currently spends itself across five elements: the hero abstract panel, the dark method band, the international panel, the CTA band's rotated square, and the interior hero's diagonal. When everything is emphatic, nothing is.

The home hero becomes the single memorable element. Its composition is corrected so it resolves within roughly 640 px above the fold — today the assurance card falls below it. The headline gains real width, and the abstract panel loses visual weight so it supports the headline instead of competing with it.

Everything else quiets:

- The eyebrow label appears only where it distinguishes one section from another, not above every heading.
- Hairline rules remain inside grids, where they encode cell boundaries. Decorative hairlines are removed.

## Icons

Eight local inline SVG icons already exist in `source/icons.py`, used by the six home service cards. They are accessible and correctly built; the family is extended, not replaced.

New icons follow the existing contract exactly: a 24×24 viewBox, `stroke-width` 1.6, round caps and joins, `currentColor`, no fill.

They are added to three places, for a total of 19 icons:

| Location | Count | Icons |
| --- | --- | --- |
| `.challenge-grid` | 4 | `control-drift`, `documentation`, `transparency`, `subsidiaries` |
| `.industry-grid` | 4 | `biotech`, `hitech`, `public-sector`, `complex-org` |
| `.contact-meta` | 3 | `email` (reuses existing `contact`), `phone`, `location` |

The process steps deliberately receive **no** icons. They carry ordinal markers `01`–`05` in the rail, and an icon beside an ordinal would encode the same position twice. The rail is the information; a second marker would be decoration.

`test_service_icons_have_unique_paths` asserts eight entries with eight distinct paths; it is updated to assert 19 with distinctness preserved.

## Placeholder media

### Constraints

Two constraints govern this and neither is negotiable.

`netlify.toml` sets `img-src 'self' data:`. External image hosts are blocked, so every image must be a local file under `static/assets/images/`. That directory does not yet exist.

`docs/image-rights-register.md` requires source, author, licence and approval for every slot before publication, and `test_unsupplied_images_render_finished_accessible_fallbacks` asserts the home hero still renders the abstract fallback. This guardrail is deliberate and is preserved.

### Approach

Placeholder media is generated locally and gated behind an environment flag.

`scripts/make-placeholder-media.py` renders one composition per slot at the exact dimensions in the rights register (`hero` 1600×2000, `method` 1800×1200, `international` 1920×1200, sector slots 1600×1200, `leadership` 1600×2000), in the brand navy and steel range, and exports AVIF, WebP and JPEG derivatives at 960 px and 1440 px. Pillow 11.3 is present with AVIF and WebP support, so no new dependency is required.

Output goes to `static/assets/images/`, which is gitignored for these generated files.

`build_site.py` copies them into the build **only** when `PLACEHOLDER_MEDIA=1` is set. The default build, and therefore every production build, continues to render the approved abstract fallback. `media_panel()` needs no change — it already discovers derivatives by filename and emits a responsive `<picture>`.

Because the aspect ratios match the register exactly, replacing a placeholder with approved photography is a file swap with no layout consequence.

The rights register gains a line recording that generated placeholders exist, are not licensed photography, and must not ship.

## Scope

Changed:

- `source/styles.css` — the substantive work: tokens, widths, gutter, type scale, rhythm, grid density, rail, hero composition, mobile corrections.
- `source/icons.py` — additional icons.
- `build_site.py` — rail markup, eyebrow reduction, flag-gated media copy.
- `scripts/make-placeholder-media.py` — new.
- `docs/image-rights-register.md` — placeholder note.
- `tests/test_site_output.py` — icon count assertion only.

Not changed: palette, logo, typefaces, all page copy, the contact function, security headers, the legal content system.

## Mobile corrections

| Element | Now | After |
| --- | --- | --- |
| `.brand img` | 230 px at 390 viewport | `min(46vw, 180px)` |
| Footer logo | 354 px wide | 40 px tall |
| `.actions` below 600 px | Two cramped columns | Stacked, full width |
| `.privacy-actions .btn` | 40 px tall | 44 px |
| Privacy disclosure | Obscures content, tall | Stacked layout, reduced height |

## Verification

Each step is verified before the next begins.

- `python build_site.py` succeeds and regenerates `dist/`.
- `python -m unittest tests.test_site_output` — 26 tests, all passing. `test_generated_browser_assets_match_their_sources` will fail if a source edit is not followed by a rebuild, which is the intended behaviour.
- `npx playwright test` at 1440×1000 and 390×844, both languages.
- Measured checks against this spec: no horizontal overflow at 390, 768, 1440; body line length at or below 68 characters LTR and 62 RTL; Hebrew home `h1` at 2 lines desktop and 3 lines mobile; interactive targets at 44 px or more.
- Screenshot review of home, services and contact in both languages at both viewports, compared against `artifacts/release-qa/`.

Accessibility holds at the current level or improves: contrast at WCAG AA, visible keyboard focus, `prefers-reduced-motion` respected.
