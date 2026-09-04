# Scout Finance Site Publication Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** לפרסם אתר Scout Finance דו־לשוני, אמין, נגיש ומהיר, עם טפסי לידים פעילים ונכסי מותג מקומיים, תוך שמירה מלאה על פלטת הצבעים הקיימת.

**Architecture:** `build_site.py` יישאר מקור האמת לתוכן ולתבניות, אך יבנה פלט נקי אל `dist/` במקום לערבב קוד מקור וקובצי פרסום. נכסים מאושרים יישמרו תחת `static/assets/` ויועתקו ל־`dist/assets/`; בדיקות Python יאמתו את הפלט המבני ובדיקות Playwright+Axe יאמתו את מסלולי המשתמש בדפדפן.

**Tech Stack:** Python 3 stdlib, HTML5, CSS logical properties, JavaScript ללא framework, Netlify Forms, Playwright, `@axe-core/playwright`, Lighthouse CI.

**Spec:** `docs/superpowers/specs/2026-09-03-site-publication-readiness-design.md`

## Global Constraints

- פלטת המותג נשארת: `#071b33`, `#0b4f9c`, `#1769c2`, `#122337`, `#5e6d7e`, `#dbe3ec`, `#f4f7fa`, `#ffffff`.
- אין להוסיף צבעי מותג, תמונות מלאי, איורים, אייקונים מאולתרים או טענות עסקיות שלא אושרו.
- אין לערוך ידנית HTML/CSS/JS שנוצרו; עורכים את המחולל ואת `static/`, מריצים build ובודקים את `dist/`.
- יעד הפרסום הראשון הוא Netlify כדי לשמר את מנגנון הטפסים הקיים.
- שפת ברירת המחדל בדומיין הישראלי היא עברית; `/` מפנה בשרת אל `/he/`.
- עמוד "תובנות" אינו מופיע בניווט או ב־sitemap עד שיש שני פריטי תוכן מאושרים לפחות.
- אין לפרסם לפני אישור תוכן עסקי, מדיניות פרטיות והצהרת נגישות.

---

### Task 1: פלט build נקי ובדיקות מבניות

**Files:**
- Modify: `build_site.py:1-8, 202-206, 362-383`
- Create: `tests/test_site_output.py`
- Modify: `README.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: מילוני התוכן ופונקציות הרינדור הקיימים ב־`build_site.py`.
- Produces: `dist/` כ־publish directory יחיד; פונקציית בדיקה `iter_pages() -> list[Path]`.

- [ ] **Step 1: אתחל מעקב גרסאות לפני שינוי קוד**

```powershell
git init
git add .
git commit -m "chore: capture pre-publication baseline"
```

- [ ] **Step 2: כתוב בדיקה שנכשלת כאשר build נכתב מחוץ ל־`dist/`**

```python
# tests/test_site_output.py
from pathlib import Path
import subprocess
import sys
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

    def test_every_content_page_has_one_h1(self) -> None:
        for page in iter_pages():
            if page == DIST / "index.html":
                continue
            html = page.read_text(encoding="utf-8")
            self.assertEqual(html.count("<h1"), 1, page)
```

- [ ] **Step 3: הרץ את הבדיקה ואמת שהיא נכשלת**

```powershell
py -3 -m unittest tests.test_site_output -v
```

Expected: FAIL מפני שהמחולל כותב כעת אל שורש הפרויקט.

- [ ] **Step 4: העבר את פלט המחולל אל `dist/`**

```python
# build_site.py — replace the current ROOT/ASSETS setup
SOURCE_ROOT = Path(__file__).resolve().parent
OUT = SOURCE_ROOT / "dist"
ASSETS = OUT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
```

החלף כל כתיבה של קובץ פרסום מ־`ROOT / ...` ל־`OUT / ...`, ושמור קריאות למסמכי מקור יחסית ל־`SOURCE_ROOT`.

- [ ] **Step 5: הוסף התעלמות מפלט build ועדכן הוראות עבודה**

```gitignore
# .gitignore
dist/
__pycache__/
node_modules/
test-results/
playwright-report/
.lighthouseci/
```

```markdown
# README.md — commands section
## Build and preview

Run `py -3 build_site.py`, then serve `dist/` with
`py -3 -m http.server 8080 --directory dist`.
```

- [ ] **Step 6: הרץ build ובדיקות**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
```

Expected: PASS ו־`dist/` מכיל רק קובצי פרסום.

- [ ] **Step 7: בצע commit**

```powershell
git add build_site.py tests/test_site_output.py README.md .gitignore
git commit -m "build: generate deployable site in dist"
```

### Task 2: נכסי מותג מקומיים ומטא־נתוני שיתוף

**Files:**
- Create: `static/assets/logo.png`
- Create: `static/assets/favicon.ico`
- Create: `static/assets/og/scout-finance-share.png`
- Modify: `build_site.py:8, 251-254`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: לוגו מקורי ומאושר של Scout Finance.
- Produces: `copy_static_assets() -> None`; head אחיד ללא תלות בנכסים חזותיים חיצוניים.

- [ ] **Step 1: הוסף בדיקה שנכשלת על תמונות חיצוניות ומטא חסר**

```python
def test_pages_use_local_brand_assets_and_complete_social_meta(self) -> None:
    for page in iter_pages():
        html = page.read_text(encoding="utf-8")
        self.assertNotIn('img src="http', html, page)
        self.assertIn('rel="icon" href="/assets/favicon.ico"', html, page)
        self.assertIn('property="og:image"', html, page)
        self.assertIn('property="og:url"', html, page)
        self.assertIn('name="twitter:card" content="summary_large_image"', html, page)
```

- [ ] **Step 2: הרץ את הבדיקה ואמת שהיא נכשלת**

```powershell
py -3 -m unittest tests.test_site_output.SiteOutputTests.test_pages_use_local_brand_assets_and_complete_social_meta -v
```

Expected: FAIL על URL הלוגו ועל metadata חסר.

- [ ] **Step 3: הכן נכסים מאושרים במידות ייצור**

```text
static/assets/logo.png                         transparent PNG, original aspect ratio, width >= 600px
static/assets/favicon.ico                      16, 32 and 48px sizes in one ICO
static/assets/og/scout-finance-share.png       1200x630px, navy background, approved logo, white title
```

ה־OG image משתמש רק ב־navy, white ובלוגו המאושר; אין להוסיף צילום או מסר שיווקי שלא אושר.

- [ ] **Step 4: העתק את `static/assets/` בזמן build**

```python
from shutil import copytree


def copy_static_assets() -> None:
    source = SOURCE_ROOT / "static" / "assets"
    copytree(source, ASSETS, dirs_exist_ok=True)
```

קרא ל־`copy_static_assets()` לפני כתיבת `styles.css` ו־`site.js`.

- [ ] **Step 5: הוסף ל־`doc()` מטא־נתונים מלאים**

```html
<link rel="icon" href="/assets/favicon.ico">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://www.scout-finance.co.il/assets/og/scout-finance-share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

- [ ] **Step 6: הרץ build ובדיקות ובצע commit**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
git add static build_site.py tests/test_site_output.py
git commit -m "feat: self-host approved brand assets"
```

### Task 3: תוכן, לוקליזציה ואמון

**Files:**
- Modify: `build_site.py:10-172, 231-249, 256-360`
- Create: `docs/content-signoff.md`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: אישור בעל העסק לטענות המופיעות ב־`docs/content-signoff.md`.
- Produces: עברית מקצועית מלאה, תוכן אנגלי ללא ניסוחי מקור פנימיים, וניווט ללא עמוד placeholder.

- [ ] **Step 1: צור רשימת אישור עובדות סגורה**

```markdown
# Content sign-off

| Claim | Hebrew/English locations | Owner | Status |
|---|---|---|---|
| Established in 2015 | home/about | Managing director | Awaiting signed approval |
| 20+ / 25+ years of experience | home/leadership | Managing director | Awaiting signed approval |
| Germany, Luxembourg, Canada, US, China, Japan | home/international | Managing director | Awaiting signed approval |
| Tomer Natan credentials and roles | leadership | Tomer Natan | Awaiting signed approval |
| SOX 404, JSOX and ISOX scope | services/FAQ | Professional lead | Awaiting signed approval |
| Privacy notice | privacy/contact | Legal reviewer | Awaiting signed approval |
| Accessibility statement | accessibility | Accessibility reviewer | Awaiting signed approval |
```

- [ ] **Step 2: הוסף בדיקה שנכשלת על ניסוחים פנימיים ועל Insights בניווט**

```python
def test_public_copy_has_no_internal_editorial_language(self) -> None:
    banned = ("לפי נתוני", "מצוין באתר", "ללא מאמר דמה", "firm states", "current site")
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
```

- [ ] **Step 3: תקן לוקליזציה וניסוח**

החלף בעמודים העבריים את `Menu`, `Primary navigation`, `home`, `Email`, `Phone`, `Website` ו־`Mishmar David, Israel` במונחים עבריים; עטוף דוא״ל וטלפון ב־`<bdi dir="ltr">`. הסר את כל המשפטים שהבדיקה אוסרת, והשאר רק טענות שאושרו.

- [ ] **Step 4: הוצא את Insights מהניווט ומה־sitemap**

```python
PUBLIC_SLUGS = [
    "services", *service_defs,
    "industries", "about", "leadership", "faq", "contact", "privacy", "accessibility",
]
NON_INDEXED_SLUGS = ["insights"]
```

ב־`doc()` הוסף `robots="noindex,follow"` עבור `NON_INDEXED_SLUGS`, אך המשך לייצר את המסלול כדי שקישורים ישנים לא יישברו.

- [ ] **Step 5: הסר חצים טקסטואליים מכל CTA**

השתמש בתוויות טקסט בלבד כגון `לשירותים שלנו`, `שיחה על השירות`, `View services`, `Discuss this service` כדי למנוע כיוון שגוי ב־RTL ולשמור על שפה חזותית מאופקת.

- [ ] **Step 6: הרץ build ובדיקות ובצע commit לאחר אישור התוכן**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
git add build_site.py tests/test_site_output.py docs/content-signoff.md
git commit -m "content: finalize bilingual publication copy"
```

### Task 4: נגישות וניווט אינטראקטיבי

**Files:**
- Modify: `build_site.py:176-190, 231-254, 326-356`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: markup שנוצר על ידי `header()`, `generic_body()` ו־`doc()`.
- Produces: `data-nav-toggle`, `data-nav-menu`, `data-dropdown-toggle`, `data-faq-toggle`; התנהגות מקלדת עקבית ב־`site.js`.

- [ ] **Step 1: כתוב בדיקות לכותרות, דילוג, labels ומצבי ARIA**

```python
def test_accessibility_hooks_exist(self) -> None:
    for page in iter_pages():
        html = page.read_text(encoding="utf-8")
        self.assertIn('href="#main-content"', html, page)
        self.assertIn('<main id="main-content"', html, page)
        self.assertIn(':focus-visible', (DIST / "assets" / "styles.css").read_text(encoding="utf-8"))

def test_contact_labels_reference_controls(self) -> None:
    for lang in ("he", "en"):
        html = (DIST / lang / "contact" / "index.html").read_text(encoding="utf-8")
        for field in ("name", "organization", "email", "phone", "message"):
            self.assertIn(f'for="{lang}-{field}"', html)
            self.assertIn(f'id="{lang}-{field}"', html)
```

- [ ] **Step 2: הרץ את הבדיקות ואמת שהן נכשלות**

```powershell
py -3 -m unittest tests.test_site_output -v
```

Expected: FAIL על skip link, focus ו־label associations.

- [ ] **Step 3: הוסף markup נגיש**

```html
<a class="skip-link" href="#main-content">דלג לתוכן הראשי</a>
<button data-dropdown-toggle aria-haspopup="true" aria-expanded="false" aria-controls="services-menu-he">שירותים</button>
<div id="services-menu-he" class="drop-menu" hidden>...</div>
<main id="main-content" tabindex="-1">...</main>
<label for="he-email">דוא״ל עסקי *</label>
<input id="he-email" type="email" name="email" required autocomplete="email">
```

צור מזהים מקבילים באנגלית ובשאר שדות הטופס. סמן את קישור העמוד הנוכחי ב־`aria-current="page"`.

- [ ] **Step 4: הוסף focus וניגודיות בלי לשנות פלטה**

```css
.skip-link{position:fixed;inset-block-start:8px;inset-inline-start:8px;z-index:1000;transform:translateY(-150%);background:var(--navy);color:var(--white);padding:10px 14px;border-radius:10px}
.skip-link:focus{transform:translateY(0)}
:where(a,button,input,textarea):focus-visible{outline:3px solid var(--blue2);outline-offset:3px}
.service-num,.breadcrumbs,.contact-label{color:var(--slate)}
```

- [ ] **Step 5: תקן את `site.js` לניהול state ומקלדת**

```javascript
const closeDropdown = (drop) => {
  const button = drop.querySelector('[data-dropdown-toggle]');
  drop.classList.remove('open');
  button.setAttribute('aria-expanded', 'false');
  drop.querySelector('.drop-menu').hidden = true;
};

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  document.querySelectorAll('.nav-drop.open').forEach((drop) => {
    closeDropdown(drop);
    drop.querySelector('[data-dropdown-toggle]').focus();
  });
});
```

בכל פתיחה עדכן `aria-expanded`, הסר `hidden`, ובסגירה מחוץ לתפריט עדכן את שני המצבים. בתפריט מובייל החזר מיקוד לכפתור לאחר סגירה.

- [ ] **Step 6: הרץ build ובדיקות ובצע commit**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
git add build_site.py tests/test_site_output.py
git commit -m "fix: make navigation and forms keyboard accessible"
```

### Task 5: טפסים, פרטיות ומסכי תוצאה

**Files:**
- Modify: `build_site.py:160-172, 326-360, 362-372`
- Create via generator: `dist/he/thank-you/index.html`
- Create via generator: `dist/en/thank-you/index.html`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: Netlify Forms, שמות הטפסים `contact-he` ו־`contact-en`.
- Produces: `render_contact_form(lang: str) -> str`; `render_thank_you(lang: str) -> str`.

- [ ] **Step 1: כתוב בדיקות ל־action, consent ומסכי הצלחה**

```python
def test_contact_forms_have_branded_success_routes(self) -> None:
    for lang in ("he", "en"):
        html = (DIST / lang / "contact" / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'action="/{lang}/thank-you/"', html)
        self.assertIn(f'href="/{lang}/privacy/"', html)
        self.assertTrue((DIST / lang / "thank-you" / "index.html").exists())
```

- [ ] **Step 2: הרץ את הבדיקה ואמת שהיא נכשלת**

```powershell
py -3 -m unittest tests.test_site_output.SiteOutputTests.test_contact_forms_have_branded_success_routes -v
```

- [ ] **Step 3: הוסף action וקישור פרטיות**

```html
<form name="contact-he" method="POST" action="/he/thank-you/" data-netlify="true" netlify-honeypot="website">
  <input type="hidden" name="form-name" value="contact-he">
  ...
  <label class="consent" for="he-consent">
    <input id="he-consent" type="checkbox" name="consent" required>
    אני מסכים/ה לשימוש בפרטים לצורך מענה לפנייה בהתאם ל<a href="/he/privacy/">מדיניות הפרטיות</a>.
  </label>
</form>
```

צור גרסה אנגלית מקבילה עם קישור ל־`/en/privacy/`.

- [ ] **Step 4: צור עמודי הצלחה ממותגים במחולל**

```python
thank_you = {
    "he": ("הפנייה נשלחה", "תודה. קיבלנו את הפרטים ונחזור אליכם בתוך יום עסקים אחד."),
    "en": ("Your enquiry was sent", "Thank you. We received your details and will respond within one business day."),
}
```

העמודים כוללים CTA אחד לחזרה לדף הבית וקישור ישיר לטלפון במקרה דחוף.

- [ ] **Step 5: השלם את מסמך האישור המשפטי**

יש לתעד ב־`docs/content-signoff.md` את זהות ספק הטופס, מטרת העיבוד, תקופת השמירה, דרך בקשת מחיקה, איש הקשר והנוסח שאושר. אין לשנות סטטוס ל־approved בלי אישור מפורש של הגורם המשפטי.

- [ ] **Step 6: בדוק שליחה ב־Netlify Deploy Preview**

```text
Hebrew form: submission appears as contact-he and redirects to /he/thank-you/
English form: submission appears as contact-en and redirects to /en/thank-you/
Invalid required/email values: browser prevents submission and focuses the invalid field
Honeypot field: absent from the visible and keyboard flow
```

- [ ] **Step 7: הרץ בדיקות ובצע commit**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
git add build_site.py tests/test_site_output.py docs/content-signoff.md
git commit -m "feat: complete bilingual contact conversion flow"
```

### Task 6: SEO, fonts, hosting and security

**Files:**
- Create: `static/assets/fonts/Heebo-Variable.woff2`
- Create: `static/assets/fonts/Inter-Variable.woff2`
- Modify: `build_site.py:176-206, 251-254, 374-381`
- Create: `netlify.toml`
- Modify: `tests/test_site_output.py`

**Interfaces:**
- Consumes: `PUBLIC_SLUGS`, canonical production domain, local WOFF2 fonts.
- Produces: JSON-LD per page, sitemap without placeholders, server redirect, CSP and caching headers.

- [ ] **Step 1: כתוב בדיקות SEO ותלות עצמית**

```python
def test_pages_have_hreflang_and_structured_data(self) -> None:
    for page in iter_pages():
        if page == DIST / "index.html":
            continue
        html = page.read_text(encoding="utf-8")
        self.assertIn('hreflang="x-default"', html, page)
        self.assertIn('type="application/ld+json"', html, page)
        self.assertNotIn("fonts.googleapis.com", html, page)
        self.assertNotIn("fonts.gstatic.com", html, page)
```

- [ ] **Step 2: הוסף WOFF2 מקומי לפי שפה**

```css
@font-face{font-family:Heebo;src:url('/assets/fonts/Heebo-Variable.woff2') format('woff2');font-weight:400 800;font-style:normal;font-display:swap}
@font-face{font-family:Inter;src:url('/assets/fonts/Inter-Variable.woff2') format('woff2');font-weight:400 800;font-style:normal;font-display:swap}
```

הסר את קישורי Google Fonts מ־`doc()` ואת preconnect הנלווה.

- [ ] **Step 3: הוסף JSON-LD בטוח עם `json.dumps`**

```python
import json


def organization_schema(lang: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Scout Finance",
        "url": f"https://www.scout-finance.co.il/{lang}/",
        "logo": "https://www.scout-finance.co.il/assets/logo.png",
        "telephone": "+972-54-788-2877",
        "email": "info@scout-finance.co.il",
        "areaServed": "IL",
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
```

הוסף `BreadcrumbList` לעמודי פנים ו־`FAQPage` רק לשאלות שבאמת מוצגות בעמוד FAQ.

- [ ] **Step 4: הוסף `x-default` ו־sitemap מדויק**

```html
<link rel="alternate" hreflang="x-default" href="https://www.scout-finance.co.il/he/">
```

בנה sitemap רק מ־`PUBLIC_SLUGS`, כולל `/he/` ו־`/en/`; אל תכלול thank-you, privacy form endpoints או insights.

- [ ] **Step 5: הגדר Netlify build, redirect וכותרות**

```toml
[build]
  command = "python3 build_site.py"
  publish = "dist"

[[redirects]]
  from = "/"
  to = "/he/"
  status = 302
  force = true

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    Content-Security-Policy = "default-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "DENY"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
```

- [ ] **Step 6: הוסף 404 דו־לשוני למחולל**

צור `dist/404.html` עם `lang="he"`, כותרת בעברית, קישורים ל־`/he/`, `/en/` ועמודי יצירת הקשר. שמור על אותה כותרת עליונה, פלטה ו־CTA styling.

- [ ] **Step 7: הרץ בדיקות ובצע commit**

```powershell
py -3 build_site.py
py -3 -m unittest tests.test_site_output -v
git add static build_site.py netlify.toml tests/test_site_output.py
git commit -m "feat: add production metadata fonts and headers"
```

### Task 7: בדיקות דפדפן, תקציבי איכות ושער פרסום

**Files:**
- Create: `package.json`
- Create: `playwright.config.mjs`
- Create: `tests/e2e/site.spec.mjs`
- Create: `lighthouserc.json`
- Create: `docs/release-checklist.md`

**Interfaces:**
- Consumes: אתר בנוי ב־`dist/` ו־Netlify Deploy Preview.
- Produces: `npm run test:e2e`, `npm run lighthouse`, צילומי מסך מאושרים ותיעוד go/no-go.

- [ ] **Step 1: הגדר כלי QA נעולים בגרסה**

```json
{
  "private": true,
  "scripts": {
    "test:e2e": "playwright test",
    "lighthouse": "lhci autorun"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.10.2",
    "@lhci/cli": "0.14.0",
    "@playwright/test": "1.55.0"
  }
}
```

- [ ] **Step 2: הגדר שרת בדיקה ו־viewports**

```javascript
// playwright.config.mjs
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  use: { baseURL: 'http://127.0.0.1:8080', trace: 'retain-on-failure' },
  webServer: {
    command: 'py -3 -m http.server 8080 --directory dist',
    url: 'http://127.0.0.1:8080/he/',
    reuseExistingServer: true
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1440, height: 1000 } } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } }
  ]
});
```

- [ ] **Step 3: כתוב בדיקות למסלולי הליבה ול־Axe**

```javascript
// tests/e2e/site.spec.mjs
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const lang of ['he', 'en']) {
  test(`${lang} home to contact`, async ({ page }) => {
    await page.goto(`/${lang}/`);
    await page.getByRole('link', { name: lang === 'he' ? 'בואו נדבר' : 'Discuss your needs' }).first().click();
    await expect(page).toHaveURL(new RegExp(`/${lang}/contact/$`));
    await expect(page.getByLabel(lang === 'he' ? 'דוא״ל עסקי *' : 'Work email *')).toBeVisible();
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations.filter(v => ['critical', 'serious'].includes(v.impact))).toEqual([]);
  });
}

test('mobile menu opens and closes with Escape', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/he/');
  const menu = page.getByRole('button', { name: 'תפריט' });
  await menu.click();
  await expect(menu).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
});
```

- [ ] **Step 4: הגדר תקציבי Lighthouse**

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "url": ["http://localhost/he/", "http://localhost/en/", "http://localhost/he/contact/"]
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.95 }],
        "categories:seo": ["error", { "minScore": 0.95 }]
      }
    }
  }
}
```

- [ ] **Step 5: הרץ את כל שערי האיכות**

```powershell
npm install
npx playwright install chromium
py -3 build_site.py
py -3 -m unittest discover -s tests -v
npm run test:e2e
npm run lighthouse
```

Expected: כל הבדיקות עוברות והציונים עומדים בספים המוגדרים.

- [ ] **Step 6: בצע ביקורת חזותית מתועדת**

צלם ושמור desktop ו־mobile עבור `/he/`, `/en/`, עמוד שירות אחד בכל שפה, שני עמודי contact, תפריט פתוח, FAQ פתוח, thank-you ו־404. בדוק חיתוכים, רווחים, RTL/LTR, focus, 200% zoom ו־320px. כל צילום לא יציב, חתוך או חלקי נלכד מחדש לפני אישור.

- [ ] **Step 7: בצע Deploy Preview ובדיקות ייצור**

```text
Verify custom domain and HTTPS
Verify / redirects to /he/
Verify canonical, hreflang, robots.txt and sitemap.xml on the production host
Submit both forms and confirm receipt
Verify branded thank-you pages and 404 response
Verify CSP and cache headers in the network panel
Submit sitemap in Google Search Console after production approval
```

- [ ] **Step 8: חתום על go/no-go ובצע commit**

`docs/release-checklist.md` צריך לכלול שם בודק, תאריך, תוצאות desktop/mobile, שני מזהי שליחת הטופס, סטטוס אישור תוכן/משפטי/נגישות והחלטת `GO` אחת. אם סעיף P0 נכשל, ההחלטה היא `NO-GO`.

```powershell
git add package.json package-lock.json playwright.config.mjs tests/e2e lighthouserc.json docs/release-checklist.md
git commit -m "test: add publication quality gates"
```
