# Scout Finance production release checklist

Status date: 4 September 2026. “Passed locally” is technical evidence, not permission to publish.

## P0 external approvals

| Gate | Status | Required evidence |
| --- | --- | --- |
| Legal entity, registration number, postal address and governing court | Pending | Business owner and Israeli counsel; named reviewer and date. |
| Privacy, Cookies, Terms and contact collection notice | Pending | Written Israeli privacy-counsel approval. |
| Contact retention and deletion procedure | Pending | Approved duration plus mailbox/provider deletion owner. |
| Accessibility statement and physical arrangements | Pending | Qualified accessibility reviewer; named coordinator and date. |
| Content and professional claims | Pending | Every row in `docs/content-signoff.md` approved. |
| Image rights and final crops | Pending | Every used row in `docs/image-rights-register.md` complete and approved. Current abstract treatments are safe to display without third-party photography. |

## Verified local technical controls

| Check | Status | Evidence |
| --- | --- | --- |
| Static generator and output contracts | Passed locally | 26 Python tests; zero failures. |
| Server contact validation | Passed locally | 18 Node tests covering input, origin, Turnstile and Resend boundaries. |
| Responsive, keyboard, privacy and Axe checks | Passed locally | 120 Playwright tests across desktop/mobile; zero failures. |
| Viewport overflow | Passed locally | Hebrew/English home, contact and audit at 320, 375, 390, 768, 1024 and 1440 px. |
| Release screenshots | Passed visual review | Seven PNGs in `artifacts/release-qa/`; Hebrew/English desktop/mobile plus Hebrew tablet service page. |
| Lighthouse median — Hebrew home | Passed locally | Performance 0.95, Accessibility 1.00, Best Practices 1.00, SEO 1.00. |
| Lighthouse median — English home | Passed locally | Performance 0.97, Accessibility 1.00, Best Practices 1.00, SEO 1.00. |
| Lighthouse median — Hebrew contact | Passed locally | Performance 0.94, Accessibility 1.00, Best Practices 1.00, SEO 1.00. |
| Production dependency audit | Passed locally | `npm audit --omit=dev --audit-level=high`: zero production vulnerabilities. |

## P0 staging and production checks

- [ ] All production identity and policy environment variables are set; production build succeeds without preview fallback values.
- [ ] Real `TURNSTILE_SITE_KEY` and secret are configured; Cloudflare test keys are absent.
- [ ] `TURNSTILE_EXPECTED_HOSTNAME` exactly matches the published host.
- [ ] Resend sender domain is verified; `CONTACT_FROM_EMAIL` and `CONTACT_TO_EMAIL` are correct.
- [ ] A staging submission reaches the intended mailbox and Reply-To targets the visitor address.
- [ ] Netlify logs show rate limiting is deployed without containing form fields, email addresses, telephone numbers or message text.
- [ ] CSP produces no console violations on the home, contact and legal pages.
- [ ] `/` redirects to `/he/`; HTTPS, HSTS, canonical, hreflang, robots and sitemap are correct on the production domain.
- [ ] Keyboard and screen-reader checks are completed on the published build.
- [ ] Counsel and accessibility reviewer approve the exact published build.

## Decision

- [ ] GO — every P0 external and production check above is complete.
- [x] NO-GO — external legal, identity, image and production-integration approvals remain unresolved.

Reviewer: ____________________

Date: ____________________
