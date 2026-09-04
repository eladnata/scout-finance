# Scout Finance — Institutional Precision redesign and compliance architecture

## Purpose

Transform the existing bilingual static site into a publication-grade website for a serious accounting, audit and financial-control firm. The redesign must create institutional authority without looking like a generic law-firm template, preserve the approved logo and core blue palette, fix all responsive and RTL defects, add a coherent icon and image system, and make privacy, accessibility, security and contact handling explicit and operational.

The website may reduce legal and operational exposure, but it cannot create complete legal immunity. Publication remains conditional on approval by Israeli counsel, an accessibility reviewer and the business owner.

## Confirmed direction

The chosen direction is **Institutional Precision**.

The visual language draws from audit working papers, management reports and controlled financial systems: disciplined columns, ledger rules, precise alignment, deep navy fields and a restrained paper texture. The memorable design element is a large editorial photography panel crossed by a subtle control-grid overlay. All other elements remain quiet and functional.

The design explicitly avoids stock-market charts, glowing dashboards, handshakes, gold luxury accents, glassmorphism, generic SaaS cards and decorative gradients.

## Design tokens

### Color

- `Ledger Navy`: `#071B33` — primary authority color, footer and selected fields.
- `Control Blue`: `#0B4F9C` — actions, links and icon emphasis.
- `Signal Blue`: `#1769C2` — keyboard focus and small active indicators.
- `Report Ink`: `#122337` — primary text.
- `Steel`: `#5E6D7E` — secondary copy and metadata.
- `Rule`: `#D7E1EA` — borders and ledger rules.
- `Mist`: `#EEF3F7` — alternate sections and image placeholders.
- `Paper`: `#F8FAFC` — textured page surface.
- `White`: `#FFFFFF` — clean reading surfaces.

No gold, green, purple or warm decorative accent is introduced. Contrast must meet WCAG AA for normal text and controls.

### Typography

- Hebrew display and body: locally hosted **IBM Plex Sans Hebrew**, weights 400, 500, 600 and 700.
- English display, body and numerals: locally hosted **Inter**, weights 400, 500, 600 and 700.
- Hebrew headings do not use negative letter-spacing. English display headings use `-0.025em` letter-spacing at desktop and `-0.015em` below 560 px.
- Body copy is 17–18 px on desktop, 16–17 px on mobile, with line lengths capped near 70 characters.
- Headings use weight and proportion rather than colored words, italics or all-caps labels.

### Shape and surface

- Primary buttons: 6 px radius; secondary controls: 6 px; editorial panels: 12 px.
- Cards use borders and spatial hierarchy, not repeated drop shadows.
- A CSS-only ledger grid appears at 3% contrast in the hero and at 4% contrast in dark sections. Texture must not reduce text contrast or create visual noise.
- Shadows are reserved for the mobile navigation drawer and the hero photography panel.

## Layout system

The maximum content width is 1240 px. The base desktop grid has 12 columns with 24 px gutters. Tablet and mobile use fluid logical padding.

Hebrew home page:

```text
┌──────────────────────────────────────────────────────────────┐
│ Logo                                  Navigation       CTA    │
├──────────────────────────────────────────────────────────────┤
│  Editorial image / control grid  │  Headline and actions     │
│                                  │  compact trust statement  │
├──────────────────────────────────────────────────────────────┤
│  Establishment │ Experience │ Markets │ Specialisms          │
├──────────────────────────────────────────────────────────────┤
│  Service icon + title + copy │ Service icon + title + copy   │
│  Service icon + title + copy │ Service icon + title + copy   │
├──────────────────────────────────────────────────────────────┤
│  Method copy                   │  Working-session image       │
├──────────────────────────────────────────────────────────────┤
│  International scope / selected markets / editorial image    │
├──────────────────────────────────────────────────────────────┤
│  Focused contact invitation                                  │
└──────────────────────────────────────────────────────────────┘
```

English mirrors the reading order rather than applying a visual transform to the whole page. Components use CSS logical properties; content order remains semantic in each language.

On screens below 900 px, all two-column sections become one column. On screens below 560 px, the logo is capped at `min(220px, calc(100vw - 92px))`, primary form actions become full width, other buttons remain content width, and contact values wrap without changing their LTR reading direction.

## Component architecture

### Header and navigation

- Approved local logo only.
- Desktop navigation with a controlled services disclosure menu.
- Mobile navigation opens as a full-width drawer below the header, traps no focus, closes with Escape and returns focus to the menu button.
- Current page receives `aria-current="page"`.
- Language switching keeps the equivalent route.

### Hero

- Text remains the primary element; the H1 is reduced from oversized marketing scale to a compact institutional scale.
- The image panel includes a deliberate crop, a navy tonal overlay and a subtle ledger grid.
- Until the approved hero image is supplied, the panel renders a finished branded abstract composition without the word “placeholder.”
- The primary action opens services; the secondary action starts a professional enquiry.

### Proof strip

- Four facts in a ruled horizontal system.
- Facts are rendered only after business-owner sign-off.
- Numbers are isolated as LTR where necessary.

### Services

- Six service entries with bespoke inline SVG icons: internal audit, SOX, risk and controls, financial advisory, technology audit and investigative audit.
- Icons share a 24 px view box, 1.6 px stroke and rounded joins. They use no external sprite, emoji or icon font.
- Each entry has a clear title, one-sentence outcome and accessible link name.

### Editorial image blocks

- Reusable `media-panel` component with `<picture>`, intrinsic dimensions, responsive sources and meaningful localized alternative text.
- Missing optional imagery falls back to the branded abstract composition without layout shift.
- Images are local, compressed to AVIF and WebP with JPEG fallback before production.

### Contact form

- One-column form at mobile and a constrained two-column form at desktop.
- A short privacy notice appears before the first field and states the controller, purpose, voluntary nature of submission, recipients and rights link.
- A required checkbox confirms that the person read the privacy notice. It is not worded as consent to marketing.
- Any future marketing opt-in is a separate, optional, unchecked checkbox and is excluded from the initial release.
- Clear validation, pending, success and failure states are available in Hebrew and English.
- Phone and email remain LTR inside the RTL page and wrap safely.

### Cookie and storage notice

- The initial site loads no analytics, advertising pixels or non-essential cookies.
- A compact first-visit disclosure explains essential local storage and links to the cookie policy. Dismissing the disclosure stores only `scout-consent-v1` locally.
- A preference center exposes “Essential” as always on and “Analytics” as unavailable/off in the initial release.
- Future analytics scripts must be loaded only after explicit opt-in through the preference state.

### Legal footer

- Persistent links to Privacy, Cookies, Terms of Use and Accessibility in both languages.
- Business identity and contact data are displayed only from centralized configuration.
- Legal pages show effective date and last-reviewed date.

## Image acquisition brief

### P0 — Hero editorial image

- Size: minimum 1600 × 2000 px, 4:5 portrait.
- Scene: senior financial professionals in a real working discussion in a contemporary meeting room.
- Tone: natural daylight, navy/steel/neutral palette, documentary rather than posed.
- Crop: important faces and hands inside the central 60% so the image survives desktop and mobile crops.
- Avoid: handshakes, visible client data, calculator close-ups, fake charts, exaggerated smiles and text embedded in the image.
- Hebrew alt intent: “צוות מקצועי בדיון על מסמכי בקרה פיננסית.”
- English alt intent: “Finance professionals reviewing control documents in a working session.”

### P0 — Leadership portrait

- Size: minimum 1600 × 2000 px, 4:5 portrait.
- Scene: authentic professional portrait of Tomer Natan, eye contact with camera, architectural office background.
- Crop: head and upper torso with sufficient space around the shoulders for responsive cropping.
- Avoid: busy office details, branded third-party material and artificial blur.
- Alt text identifies the person and role only after the role is owner-approved.

### P1 — Working method

- Size: minimum 1800 × 1200 px, 3:2 landscape.
- Scene: two or three people reviewing printed controls, process maps or a non-sensitive report.
- Tone: precise, calm, candid, with restrained blue and grey materials.
- Avoid: readable personal data, mock stock charts and generic laptop-only compositions.

### P1 — International activity

- Size: minimum 1920 × 1200 px, 16:10 landscape.
- Scene: credible international business architecture, logistics infrastructure or a cross-border working environment.
- Avoid: flag collages, glowing world maps, airport departure boards and landmark tourism imagery.

### P2 — Sector set

- Three coordinated images, minimum 1600 × 1200 px each, 4:3.
- Subjects: public institution, industrial/operational environment and mission-driven organization.
- The images must share color temperature, contrast and documentary style.

Each supplied file must include source, author, license, download date and any attribution requirement in an image-rights register before publication.

## RTL and responsive rules

- Every grid and flex child that contains text receives `min-inline-size: 0` where overflow is possible.
- `html` and `body` must never exceed the visual viewport; hiding overflow is not accepted as the sole fix.
- Email, telephone numbers, URLs and mixed-language identifiers use `dir="ltr"`, `unicode-bidi: isolate` and safe wrapping.
- Form controls use `inline-size: 100%`, `max-inline-size: 100%` and `min-inline-size: 0`.
- The logo uses an inline-size cap derived from available header space, not a fixed height that creates an oversized width.
- Hebrew breadcrumbs use a localized separator and correct visual order.
- Automated regression checks compare `document.documentElement.scrollWidth` with `clientWidth` at 320, 375, 390, 768, 1024 and 1440 px on home, contact and one service page in both languages.

## Privacy and legal architecture

### Collection notice

The form notice implements the information points described by the Israeli Privacy Protection Authority for collection under section 11: why the information is requested, whether provision is voluntary, the consequence of not providing it, who receives it, controller identity and contact details, and links to inspection and correction rights.

### Privacy policy

The policy includes:

- controller identity and contact channels;
- categories of information collected directly and automatically;
- purposes and legal basis/voluntary submission context;
- recipients and processors;
- international transfers;
- retention and deletion practice;
- security measures described without making absolute guarantees;
- inspection, correction and deletion-request channels;
- minors;
- changes to the policy;
- effective and review dates.

### Cookie policy

The policy lists essential local storage, its purpose and duration. Cloudflare Turnstile processing is disclosed separately as security processing. Analytics is documented as disabled in the initial release.

### Terms of use

The terms state that public website content is general information, not accounting, audit, tax, legal or investment advice; no professional engagement exists without a signed agreement; users must not submit confidential, regulated or sensitive information through the public form; intellectual-property and acceptable-use terms apply; third-party services have their own terms; and Israeli law/jurisdiction wording is subject to counsel approval.

### Accessibility statement

The statement identifies the target standard, supported interaction patterns, known limitations, feedback process, accessibility contact and review date. It does not claim certified compliance without a completed audit.

### Required production identity configuration

Production deployment is blocked until all of these values are supplied and reviewed:

- legal entity name and registration/authorized-dealer number;
- postal address;
- privacy contact email;
- accessibility contact name, email and telephone;
- approved retention period for contact enquiries;
- approved governing-law and jurisdiction wording;
- policy effective date and legal-review date;
- approved list of processors and transfer locations.

Local preview uses the public display name “Scout Finance,” and legal pages display a visible draft-review notice until the production identity configuration is complete.

## Secure form delivery

The existing direct Netlify Forms submission is replaced by a Netlify Function at `/.netlify/functions/contact`.

Submission flow:

```text
Browser form
   → client validation
   → Cloudflare Turnstile token
   → Netlify Function
      → validate origin, method, content type and field lengths
      → validate Turnstile token with Siteverify
      → rate-limit through Netlify function configuration where available
      → send email through the configured transactional-email adapter
      → return localized success/error response
```

The initial transactional-email adapter uses the Resend HTTPS API without a browser-side secret. Required secrets are `TURNSTILE_SECRET_KEY`, `RESEND_API_KEY`, `CONTACT_TO_EMAIL` and `CONTACT_FROM_EMAIL`. The public `TURNSTILE_SITE_KEY` is injected at build time. No secret is written to generated HTML.

Production fails closed when a required secret is absent. Local and automated testing use Cloudflare's published test keys and a stubbed local mail endpoint; test keys are rejected when Netlify reports a production context.

The function validates field length, normalizes line breaks, strips control characters, rejects unexpected fields and never reflects submitted HTML. Logs contain request identifiers and status only, not message content, email addresses or telephone numbers.

## Security headers

- Keep `default-src 'self'`.
- Permit `https://challenges.cloudflare.com` only in the directives required for Turnstile.
- Permit the transactional-email domain only from the server function; it is never added to browser CSP.
- Add HSTS for production HTTPS, `frame-ancestors 'none'`, `base-uri 'self'`, `form-action 'self'`, `object-src 'none'`, strict referrer policy and restrictive permissions policy.
- Do not add inline-script or inline-style exceptions.

## Content and configuration model

Design tokens, legal identity values, processor disclosures and image metadata are centralized rather than repeated across page strings. Hebrew and English content are parallel entries with the same semantic structure. The build validates that every public route has both languages and that no production legal field is missing.

## Test strategy

Implementation follows red-green-refactor.

1. Generator tests fail first for the new routes, icons, image panels, legal links, form notice and centralized legal configuration.
2. Function unit tests fail first for invalid method, malformed input, missing acknowledgement, failed Turnstile, oversized content, delivery failure and successful delivery.
3. Static output tests verify CSP, no exposed secrets, localized metadata, local assets and no unapproved analytics.
4. Browser tests verify keyboard navigation, menu/FAQ/form states, cookie preferences and the no-horizontal-overflow contract at all required widths.
5. Axe checks report no critical or serious findings on home, contact, privacy, terms and one service page in both languages.
6. Visual screenshots are reviewed at desktop, tablet and mobile before publication.

## Publication gates

- Approved legal identity values are present and the production build passes.
- Israeli counsel approves Privacy, Cookies, Terms, collection notice and processor disclosures.
- An accessibility reviewer validates the statement and core flows.
- Turnstile and email delivery are tested on a staging deploy with production-shaped configuration.
- The recipient confirms receipt and reply handling without leaking form data into logs.
- No horizontal scroll exists at the specified widths or 200% zoom.
- Image rights are recorded and every image crop/alt text is approved.
- Lighthouse mobile scores remain at least 90 performance, 95 accessibility, 95 best practices and 95 SEO on representative pages.

## Deliberate exclusions

- No analytics, advertising pixels, chat widget or session recording in the initial release.
- No newsletter or marketing consent flow.
- No client portal or document upload through the public form.
- No claim of legal certification or full accessibility certification before external review.

## Authoritative implementation references

- Israeli Privacy Protection Authority, duty to notify in collection and use of personal information: <https://www.gov.il/BlobFolder/legalinfo/duty_to_notify/he/notify13.pdf>
- Israeli Privacy Protection Authority, Amendment 13 questions and answers: <https://www.gov.il/he/pages/tikun13_qa>
- Commission for Equal Rights of Persons with Disabilities, website accessibility: <https://www.gov.il/he/pages/website_accessibility>
- Cloudflare Turnstile, mandatory server-side token validation: <https://developers.cloudflare.com/turnstile/get-started/server-side-validation/>
- Netlify Functions overview: <https://docs.netlify.com/build/functions/overview/>
- Netlify Forms spam-filter reference for the existing implementation: <https://docs.netlify.com/manage/forms/spam-filters/>
