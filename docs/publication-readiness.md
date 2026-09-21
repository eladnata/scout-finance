# Publication readiness — Scout Finance website

Prepared for legal review. Last updated 21 September 2026.

This document records what the site states, where each statement comes from, and
which decisions remain open. It is written so that a reviewer can verify a claim
without reading the code: every assertion below names the file or the test that
enforces it.

The site is a bilingual (Hebrew/English) marketing site with one interactive
feature — a contact form. It processes no payments, holds no accounts, and loads no
analytics, advertising or profiling technology of any kind.

---

## 1. Operator identity

Verified on 21 September 2026 against the Israeli Registrar of Companies open
dataset on data.gov.il, record for company number 515178788.

| Field | Value |
| --- | --- |
| Registered name | סקאוט פייננס בע״מ / SCOUT FINANCE LTD |
| Company number | 515178788 |
| Type | חברה פרטית ישראלית, status: פעילה |
| Incorporated | 01/01/2015 |
| Registered address | משמר דוד 566, מיקוד 7684100, ישראל |

These values are published in the privacy policy and the terms of use. They are
held in `source/legal_config.py` as verified defaults rather than environment
variables, deliberately: the previous design required eleven environment variables
in production, none of which were set on Cloudflare, and the live privacy policy
consequently read "to be completed before publication". Identity that is public
record should not be able to go missing.

Any value can still be overridden per environment — see the table in `README.md`.

---

## 2. Privacy

`source/legal_content.py`, published at `/he/privacy/` and `/en/privacy/`.

Drafted against the Privacy Protection Law, 1981, as amended by **Amendment 13**,
in force 14 August 2025. The policy is structured to carry each element of the
section 11 duty to inform:

| Section 11 element | Where it appears |
| --- | --- |
| Identity of the controller | "מי מפעיל את האתר ומי בעל השליטה במידע" |
| Whether disclosure is compulsory or voluntary | "מסירת המידע היא מרצון…" |
| **Consequences of refusing** | same section — states the form cannot be submitted and the enquiry cannot be handled |
| Purpose of collection | "מטרות העיבוד" |
| Recipients and the purpose of transfer | "למי נמסר המידע" — Cloudflare and Resend named |
| Data subject rights | "הזכויות שלכם" — inspection, correction, deletion, and the route to the Privacy Protection Authority |

Also covered: cross-border processing, citing תקנות הגנת הפרטיות (העברת מידע אל
מאגרי מידע שמחוץ לגבולות המדינה), התשס״א-2001; retention; security measures; and an
express statement that the site performs no profiling, makes no solely-automated
decisions with legal effect, and operates no direct-mailing database within the
meaning of sections 17C–17F.

`tests/test_site_output.py::test_privacy_policy_states_the_section_11_notice_elements`
fails the build if any of these disappear.

**Assessment, for confirmation by counsel:**

* **Database registration** — Amendment 13 removed the registration requirement for
  the large majority of databases. A contact-enquiry mailbox is not a sensitive-data
  database at scale, so registration appears not to be required.
* **Privacy Protection Officer (ממונה על הגנת הפרטיות)** — required of public
  bodies, data brokers, entities whose core activity is processing sensitive data at
  scale, and entities conducting systematic monitoring. None appears to apply.
* **GDPR** — the firm's published international work includes Germany and
  Luxembourg, and the site has an English version. Whether the site targets data
  subjects in the EU is a factual question the firm should answer; if it does, a
  GDPR-facing supplement would be needed.

---

## 3. Accessibility

`/he/accessibility/` and `/en/accessibility/`.

Drafted against regulation 35 of תקנות שוויון זכויות לאנשים עם מוגבלות (התאמות
נגישות לשירות), התשע״ג-2013, and IS 5568 (based on WCAG 2.0 AA). Regulation 35(e)
requires a prominent statement covering the adaptations made, the route for
reporting a missing adaptation, and any exemption relied on. All are present.

Every adaptation the statement claims is implemented in the markup and verified:
semantic headings and landmarks, keyboard-only operation including menus and
accordions, visible focus, skip link, image alt text, bound form labels, screen
reader status announcements, contrast ratios, responsive reflow, per-page language
and direction, and reduced-motion support.

Testing claimed, and actually performed: axe-core runs against every page in both
languages at desktop and mobile viewports, plus automated keyboard-operability
tests, on every change. 140 browser tests currently pass.

The statement says plainly what has **not** been done: no external audit by a
licensed מורשה נגישות שירות, and no comprehensive commercial screen-reader testing.
The previous version instead said that a formal review "remains a publication gate",
which was an internal note that should never have been public.

**Open items:**

* **רכז נגישות** — mandatory at 25 or more employees. If Scout Finance is at or
  above that threshold, a coordinator must be formally appointed and named in the
  statement; set `ACCESSIBILITY_CONTACT_NAME` accordingly. Below it, the current
  contact route satisfies the regulation.
* **External audit** — not legally mandatory for this statement to stand, but it is
  the only way to move from "no known barriers" to a positive conformance claim.
* The turnover exemption (below ₪100,000 annual turnover) does not apply here.

---

## 4. Contact form and security

* Served only over HTTPS, with HSTS, a strict Content-Security-Policy,
  `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy` and `Permissions-Policy`.
  Enforced by `tests/test_site_output.py::test_security_headers_carry_the_full_policy`.
* The form validates server-side, checks the request origin, carries a honeypot
  field, escapes all output, and accepts only an allow-list of fields.
* Turnstile is verified server-side, not merely rendered in the browser.
* Published Cloudflare **test** secrets are now rejected whenever the platform looks
  like production, on Cloudflare as well as Netlify. Previously this check keyed
  only on `CONTEXT`, which Cloudflare never sets.
* **The form is not published unless it can work.** In a production build without a
  real `TURNSTILE_SITE_KEY`, the page shows direct email and telephone details
  instead, and the Turnstile script is not loaded. This was the state of the live
  site: the form used Cloudflare's test key, so the widget always passed in the
  browser, and every submission then failed with a 503 because the Resend and
  Turnstile secrets were unset. A prospect filling in that form received an error.

**Required before the form goes back:** set `TURNSTILE_SITE_KEY`,
`TURNSTILE_SECRET_KEY`, `TURNSTILE_EXPECTED_HOSTNAME`, `RESEND_API_KEY`,
`CONTACT_TO_EMAIL`, `CONTACT_FROM_EMAIL` and `SITE_ORIGIN` in the Cloudflare Pages
project, then send a test enquiry from a preview deploy and confirm it arrives.

**Recommended:** a Cloudflare WAF rate-limiting rule on `/api/contact`. There is no
rate limiting in application code.

---

## 5. Decisions that remain with the firm

| # | Item | Why it needs a decision |
| --- | --- | --- |
| 1 | **Retention period** — currently stated as 24 months | A published retention promise binds the firm. 24 months is a defensible default, not an instruction. Override with `CONTACT_RETENTION_MONTHS`. |
| 2 | **Deletion actually happens** | The policy promises deletion. Nothing in the code deletes anything: enquiries live in the destination mailbox and in Resend's logs. A manual deletion routine and a Resend retention setting are needed, or the promise is not kept. |
| 3 | **Forum clause** — "בתי המשפט המוסמכים בישראל" | Valid as drafted. Narrowing it to a specific district is a choice, not a correction. |
| 4 | **AI-generated photography** | Five of the seven editorial images were generated with an AI image tool and depict people who do not exist, on the site of an audit firm. No row in `docs/image-rights-register.md` is marked approved. The terms of use now carry an express statement that images other than identified portraits of the firm's own personnel do not depict its staff, offices, clients or engagements. Whether that disclosure is sufficient, or whether the images should be replaced, is a judgement about how the firm wishes to present itself. |
| 5 | **Leadership portrait** | Supplied by the user and treated as depicting the real founder. The register records the author as not determined — the photographer and the licence should be confirmed. |
| 6 | **Professional advertising rules** | The site states CPA and LLM qualifications, names a former employer, and advertises audit services. Compliance with the Auditors Law and its professional-conduct rules is outside what can be checked from the code. |
| 7 | **Experience claims** | The home page says "20+ שנות ניסיון"; the leadership page says "למעלה מ-25 שנות ניסיון". Not contradictory, but a reviewer will notice the inconsistency. |
| 8 | **Domain** | `www.scout-finance.co.il` has no DNS record. Every canonical URL, the sitemap, `robots.txt` and the form's default origin check point at it. Until DNS exists, the canonical tags point at a hostname that does not resolve. |

---

## 6. Verification

```bash
python3 -m unittest discover -s tests -p "test_*.py"   # 43 tests
npx playwright test                                     # 140 tests
node --test tests/contact-function.test.mjs             # 18 tests
```

The build itself refuses to publish an unsubstituted `{token}`, preview identity
text, the operational-draft banner, or a contact form backed by a test key.
