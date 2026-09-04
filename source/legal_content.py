"""Parallel legal and accessibility copy for the bilingual static site.

The text is a publication-ready operational draft, not a substitute for review by
Israeli counsel or a qualified accessibility reviewer.
"""

LEGAL_SECTION_KEYS = (
    "controller",
    "collection",
    "purposes",
    "voluntary",
    "recipients",
    "transfers",
    "retention",
    "security",
    "rights",
    "minors",
    "updates",
    "contact",
)


PRIVACY_SECTIONS_EN = {
    "controller": ("Who controls the information", "The website is operated by {legal_name}, registration number {registration_id}, at {postal_address}. Privacy enquiries may be sent to {privacy_email}."),
    "collection": ("Information we collect", "The contact form collects the name, work email and message you choose to provide and may also collect organization and phone details. Hosting and security systems may process IP address, device, browser, request time and fraud-prevention signals. Please do not submit confidential client records, regulated data, identification numbers, health information or other sensitive information."),
    "purposes": ("Purposes of use", "Information is used to receive, assess and respond to your enquiry; maintain the security and availability of the website; prevent abuse; keep necessary business records; and comply with legal obligations or establish and defend legal claims."),
    "voluntary": ("Providing information is voluntary", "You are not legally required to use the form. Name, email, message and acknowledgement are required only so the firm can assess and respond to the enquiry; without them the form cannot be submitted. Sending an enquiry does not create a professional engagement."),
    "recipients": ("Recipients and processors", "Information may be available to authorized Scout Finance personnel and to providers necessary to operate the service: Netlify for hosting and server functions, Cloudflare for Turnstile abuse prevention, and Resend for transactional email. It may also be disclosed where required by law, to professional advisers under confidentiality duties, or in connection with the protection of legal rights."),
    "transfers": ("Processing outside Israel", "The providers named above may process or store information outside Israel, including in the United States or other jurisdictions in which they or their subprocessors operate. Such processing is subject to the relevant provider terms and the safeguards required by applicable law."),
    "retention": ("Retention and deletion", "Enquiry data is intended to be retained for no longer than {retention_months} months unless a longer period is reasonably required for an active professional discussion, legal duty or legal claim. Operational deletion must include the receiving mailbox and provider records where the firm controls them."),
    "security": ("Security", "The site uses access controls, encrypted transport, anti-abuse checks, input validation and restricted service credentials. No internet transmission or storage system is completely secure, so absolute security cannot be guaranteed."),
    "rights": ("Inspection, correction and deletion requests", "Subject to applicable Israeli law, you may ask to inspect information held about you and request correction or deletion where appropriate. Send a verifiable request to {privacy_email}. The firm may need to confirm identity and may retain information where the law permits or requires it."),
    "minors": ("Minors", "This business website is not directed to minors. A minor should not submit personal information without the involvement of a parent or legal guardian."),
    "updates": ("Policy dates and changes", "Effective date: {effective_date}. Scheduled review: {review_date}. Material changes will be reflected on this page; the effective date will be updated when a revised policy is published."),
    "contact": ("Privacy contact", "Questions, objections and rights requests may be sent to {privacy_email} or by post to {postal_address}."),
}

PRIVACY_SECTIONS_HE = {
    "controller": ("מי שולט במידע", "האתר מופעל על ידי {legal_name}, מספר רישום {registration_id}, בכתובת {postal_address}. לפניות פרטיות ניתן לכתוב אל {privacy_email}."),
    "collection": ("המידע שאנו אוספים", "טופס יצירת הקשר אוסף את השם, הדוא״ל העסקי ותוכן ההודעה שתבחרו למסור, ועשוי לכלול גם ארגון וטלפון. מערכות האחסון והאבטחה עשויות לעבד כתובת IP, נתוני מכשיר ודפדפן, מועד הבקשה ואותות למניעת הונאה. אין למסור מסמכי לקוחות חסויים, מידע מפוקח, מספרי זיהוי, מידע רפואי או מידע רגיש אחר."),
    "purposes": ("מטרות השימוש", "המידע משמש לקבלת הפנייה, להערכתה ולמענה עליה; לשמירה על אבטחת האתר וזמינותו; למניעת שימוש לרעה; לניהול רשומות עסקיות נחוצות; ולעמידה בחובות דין או לביסוס והגנה על טענות משפטיות."),
    "voluntary": ("מסירת המידע היא מרצון", "אין חובה חוקית להשתמש בטופס. שם, דוא״ל, הודעה ואישור נדרשים רק כדי שהמשרד יוכל לבחון את הפנייה ולהשיב; בלעדיהם לא ניתן לשלוח את הטופס. שליחת פנייה אינה יוצרת התקשרות מקצועית."),
    "recipients": ("נמענים ומעבדי מידע", "המידע עשוי להיות נגיש לאנשי Scout Finance שהוסמכו לכך ולספקים הנדרשים להפעלת השירות: Netlify לאחסון ולפונקציות שרת, Cloudflare למנגנון Turnstile למניעת שימוש לרעה, ו-Resend למשלוח דוא״ל תפעולי. מידע עשוי להימסר גם לפי דרישת דין, ליועצים מקצועיים הכפופים לסודיות או לשם הגנה על זכויות משפטיות."),
    "transfers": ("עיבוד מחוץ לישראל", "הספקים המפורטים לעיל עשויים לעבד או לשמור מידע מחוץ לישראל, לרבות בארצות הברית או במדינות אחרות שבהן הם או קבלני המשנה שלהם פועלים. העיבוד כפוף לתנאי הספקים ולאמצעי ההגנה הנדרשים לפי הדין החל."),
    "retention": ("שמירה ומחיקה", "מידע מפניות מיועד להישמר לא יותר מ-{retention_months} חודשים, אלא אם תקופה ארוכה יותר נדרשת באופן סביר לשיחה מקצועית פעילה, לחובה חוקית או לטענה משפטית. נוהל המחיקה התפעולי צריך לכלול את תיבת הדוא״ל המקבלת ואת רשומות הספקים הנתונות לשליטת המשרד."),
    "security": ("אבטחת מידע", "האתר משתמש בבקרות גישה, תעבורה מוצפנת, בדיקות למניעת שימוש לרעה, אימות קלט והרשאות שירות מוגבלות. שום העברה או אחסון באינטרנט אינם בטוחים לחלוטין, ולכן לא ניתן להבטיח אבטחה מוחלטת."),
    "rights": ("בקשות לעיון, תיקון ומחיקה", "בכפוף לדין הישראלי החל, ניתן לבקש לעיין במידע המוחזק עליכם ולבקש תיקון או מחיקה במקרים המתאימים. יש לשלוח בקשה ניתנת לאימות אל {privacy_email}. המשרד עשוי להידרש לאמת זהות ולשמור מידע כאשר הדין מתיר או מחייב זאת."),
    "minors": ("קטינים", "אתר עסקי זה אינו מיועד לקטינים. על קטין להימנע ממסירת מידע אישי ללא מעורבות הורה או אפוטרופוס חוקי."),
    "updates": ("מועדי המדיניות ושינויים", "מועד תחילה: {effective_date}. מועד בחינה מתוכנן: {review_date}. שינויים מהותיים יוצגו בעמוד זה, ומועד התחילה יעודכן עם פרסום נוסח מתוקן."),
    "contact": ("יצירת קשר בנושאי פרטיות", "לשאלות, התנגדויות ובקשות למימוש זכויות ניתן לפנות אל {privacy_email} או בדואר לכתובת {postal_address}."),
}


def _policy(title, eyebrow, lead, sections):
    return {"title": title, "eyebrow": eyebrow, "lead": lead, "sections": sections}


POLICIES = {
    "en": {
        "privacy": _policy("Privacy Policy", "Privacy", "How personal information is collected, used, shared and protected when you contact Scout Finance through this website.", PRIVACY_SECTIONS_EN),
        "cookies": _policy("Cookies & Local Storage", "Privacy controls", "The initial release uses essential storage and security technology only; it does not use analytics, advertising or profiling tools.", {
            "essential": ("Essential browser storage", "The key scout-consent-v1 records that essential-only use has been explained. The key scout-language records the selected site language. Both are stored in your browser and are not used for advertising or analytics."),
            "turnstile": ("Cloudflare Turnstile", "The contact page loads Cloudflare Turnstile to distinguish legitimate submissions from automated abuse. Cloudflare may process IP, browser and device signals and may use essential security tokens or cookies. The form cannot be submitted without a successful security check."),
            "choices": ("Your choices", "You can delete local storage or site data through browser settings. The notice can be reopened using Privacy settings in the footer. Version 1 has no optional analytics switch because no analytics are loaded."),
            "updates": ("Policy dates", "Effective date: {effective_date}. Scheduled review: {review_date}."),
        }),
        "terms": _policy("Website Terms of Use", "Legal", "Conditions governing use of the Scout Finance website and its general professional information.", {
            "information": ("General information only", "Website content is general information and is not accounting, audit, tax, legal, investment or other professional advice. Do not act or refrain from acting in reliance on it without advice tailored to the relevant facts and jurisdiction."),
            "engagement": ("No professional engagement", "Sending a form, email or document does not create a client, accountant, auditor, fiduciary or other professional relationship. An engagement exists only after authorized parties sign a written engagement agreement."),
            "accuracy": ("Availability and accuracy", "Reasonable care is taken in preparing the website, but completeness, currency, fitness for a particular purpose and uninterrupted availability are not guaranteed to the extent permitted by law."),
            "confidentiality": ("Do not send sensitive material", "Do not submit confidential, privileged, regulated or sensitive information through the public website. Contact the firm first to agree an appropriate secure channel."),
            "intellectual": ("Intellectual property", "Unless stated otherwise, website text, visual design and firm marks belong to their respective owners and may not be copied or reused except as permitted by law or with prior written permission."),
            "links": ("Third-party services", "Links and embedded security services are provided for operation or convenience. Third-party terms and privacy practices apply to their services."),
            "law": ("Applicable law", "These terms are governed by Israeli law. Subject to mandatory law, exclusive jurisdiction lies with {governing_court}."),
            "contact": ("Contact", "Questions about these terms may be sent to {privacy_email}."),
        }),
        "accessibility": _policy("Accessibility Statement", "Accessibility", "Scout Finance is working toward an accessible experience aligned with Israeli Standard 5568 and WCAG 2.1 Level AA, without claiming certification before an external review.", {
            "approach": ("Digital accessibility approach", "The site uses semantic headings, keyboard-accessible controls, visible focus, responsive layouts, reduced-motion support, alternative text and contrast-aware colors. Automated and manual checks are part of the release process."),
            "limits": ("Known limits", "Editorial photographs are currently represented by accessible abstract treatments until approved assets and alternative text are supplied. A formal accessibility review and screen-reader check remain publication gates."),
            "contact": ("Accessibility coordinator", "If you encounter a barrier, contact {accessibility_name} at {accessibility_email} or {accessibility_phone}. Please include the page, action and assistive technology involved. We will review the report and seek a reasonable solution."),
            "dates": ("Statement dates", "Effective date: {effective_date}. Scheduled review: {review_date}. Physical accessibility arrangements must be confirmed by the firm before they are described publicly."),
        }),
    },
    "he": {
        "privacy": _policy("מדיניות פרטיות", "פרטיות", "כיצד נאסף, נעשה שימוש, מועבר ומוגן מידע אישי בעת פנייה אל Scout Finance באמצעות האתר.", PRIVACY_SECTIONS_HE),
        "cookies": _policy("קובצי Cookies ואחסון מקומי", "בקרות פרטיות", "בגרסה הראשונית נעשה שימוש באחסון ובטכנולוגיות אבטחה חיוניים בלבד; אין כלי אנליטיקה, פרסום או יצירת פרופיל.", {
            "essential": ("אחסון חיוני בדפדפן", "המפתח scout-consent-v1 מתעד שהוצג הסבר על שימוש חיוני בלבד. המפתח scout-language מתעד את שפת האתר שנבחרה. שניהם נשמרים בדפדפן ואינם משמשים לפרסום או לאנליטיקה."),
            "turnstile": ("Cloudflare Turnstile", "עמוד יצירת הקשר טוען את Cloudflare Turnstile כדי להבחין בין פנייה לגיטימית לבין שימוש אוטומטי לרעה. Cloudflare עשויה לעבד כתובת IP ואותות דפדפן ומכשיר, ולהשתמש באסימוני אבטחה או בקובצי Cookie חיוניים. לא ניתן לשלוח את הטופס בלי בדיקת אבטחה מוצלחת."),
            "choices": ("הבחירות שלכם", "ניתן למחוק אחסון מקומי או נתוני אתר דרך הגדרות הדפדפן. אפשר לפתוח מחדש את ההודעה באמצעות הגדרות פרטיות בתחתית האתר. בגרסה 1 אין מתג אנליטיקה אופציונלי מפני שלא נטענת אנליטיקה."),
            "updates": ("מועדי המדיניות", "מועד תחילה: {effective_date}. מועד בחינה מתוכנן: {review_date}."),
        }),
        "terms": _policy("תנאי שימוש באתר", "משפטי", "התנאים לשימוש באתר Scout Finance ובמידע המקצועי הכללי המופיע בו.", {
            "information": ("מידע כללי בלבד", "תוכן האתר הוא מידע כללי ואינו ייעוץ חשבונאי, ביקורתי, מס, משפטי, השקעות או ייעוץ מקצועי אחר. אין לפעול או להימנע מפעולה בהסתמך עליו בלי ייעוץ המותאם לעובדות ולדין הרלוונטיים."),
            "engagement": ("אין התקשרות מקצועית", "שליחת טופס, דוא״ל או מסמך אינה יוצרת יחסי לקוח, רואה חשבון, מבקר, נאמנות או התקשרות מקצועית אחרת. התקשרות נוצרת רק לאחר חתימת הצדדים המוסמכים על הסכם התקשרות בכתב."),
            "accuracy": ("זמינות ודיוק", "נעשים מאמצים סבירים בהכנת האתר, אך במידה המותרת בדין אין התחייבות לשלמות, עדכניות, התאמה למטרה מסוימת או זמינות רציפה."),
            "confidentiality": ("אין לשלוח מידע רגיש", "אין למסור דרך האתר הפומבי מידע חסוי, חסוי מכוח דין, מפוקח או רגיש. יש ליצור קשר תחילה כדי להסכים על ערוץ מאובטח מתאים."),
            "intellectual": ("קניין רוחני", "אלא אם צוין אחרת, הטקסט, העיצוב החזותי וסימני המשרד שייכים לבעליהם ואין להעתיקם או לעשות בהם שימוש חוזר אלא לפי דין או באישור מראש ובכתב."),
            "links": ("שירותי צד שלישי", "קישורים ושירותי אבטחה משובצים ניתנים לצורך תפעול או נוחות. על שירותי צד שלישי חלים התנאים ומדיניות הפרטיות שלהם."),
            "law": ("דין וסמכות שיפוט", "על תנאים אלה חל דין מדינת ישראל. בכפוף להוראות דין מחייבות, סמכות השיפוט הייחודית נתונה ל-{governing_court}."),
            "contact": ("יצירת קשר", "שאלות על תנאים אלה ניתן לשלוח אל {privacy_email}."),
        }),
        "accessibility": _policy("הצהרת נגישות", "נגישות", "Scout Finance פועלת להנגשת האתר בהתאם לתקן הישראלי 5568 ולהנחיות WCAG 2.1 ברמה AA, בלי לטעון להסמכה לפני בדיקה חיצונית.", {
            "approach": ("גישת הנגישות הדיגיטלית", "האתר משתמש בכותרות סמנטיות, פקדים הנגישים במקלדת, מיקוד נראה, פריסה רספונסיבית, תמיכה בהפחתת תנועה, טקסט חלופי וצבעים בעלי ניגודיות. בדיקות אוטומטיות וידניות הן חלק מתהליך הפרסום."),
            "limits": ("מגבלות ידועות", "צילומים מערכתיים מיוצגים כעת בקומפוזיציות מופשטות נגישות עד לקבלת נכסים מאושרים וטקסט חלופי. בדיקת נגישות רשמית ובדיקת קורא מסך עדיין מהוות תנאי לפרסום."),
            "contact": ("רכז/ת נגישות", "אם נתקלתם בחסם, ניתן לפנות אל {accessibility_name} בדוא״ל {accessibility_email} או בטלפון {accessibility_phone}. אנא ציינו את העמוד, הפעולה וטכנולוגיית הסיוע. הפנייה תיבדק וייעשה מאמץ לספק פתרון סביר."),
            "dates": ("מועדי ההצהרה", "מועד תחילה: {effective_date}. מועד בחינה מתוכנן: {review_date}. יש לאשר מול המשרד את הסדרי הנגישות הפיזיים לפני תיאורם לציבור."),
        }),
    },
}
