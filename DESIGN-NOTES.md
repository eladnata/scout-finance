# Scout Finance — Approved Premium Redesign

This build implements the approved premium visual direction directly in the uploaded Scout Finance project.

## Visual system
- White, navy and cool-gray corporate palette
- Editorial serif display typography in English; local IBM Plex Sans Hebrew for Hebrew/RTL
- Thin rules, restrained borders and minimal radius
- Large white-space rhythm and wide professional-services grids
- Sticky white navigation with responsive mobile drawer
- Dark high-impact homepage hero with an architectural abstract media treatment
- Six-column desktop service cards, responsive to 3/2/1 columns
- Light split interior page heroes with an architectural visual field
- Structured dark editorial sections, international panel, proof strip, FAQ and CTA bands
- Full bilingual RTL/LTR behavior

## Images
No new photography has been embedded in this revision. Existing media slots remain intact and currently render a designed abstract fallback. Later, approved real photography can be dropped into `static/assets/images/` using the documented slot names without changing the page layout.

Supported image slots include `hero`, `leadership`, `method`, `international`, and sector slots. See `docs/image-rights-register.md` and `source/media.py`.

## Build
Run:

```bash
python3 build_site.py
```

Deploy `dist/`.

## QA completed
- Python site-output suite: 26/26 passing
- Responsive horizontal-overflow check at 390px: no document overflow
- Desktop visual captures reviewed for Home, Services and Hebrew Contact

The Node contact-function test currently depends on the host runtime loading `.mts` directly; this is unrelated to the UI redesign.
