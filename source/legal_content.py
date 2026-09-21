"""Parallel legal and accessibility copy for the bilingual static site.

Drafting references, so a reviewer can check the text against its source:

* Privacy - חוק הגנת הפרטיות, התשמ״א-1981 as amended by Amendment 13
  (in force 14 August 2025). The notice sections follow the section 11
  duty to inform: whether disclosure is voluntary or compulsory, the
  consequences of refusing, the purpose, the controller's identity, the
  recipients, and the data subject's rights.
* Cross-border - תקנות הגנת הפרטיות (העברת מידע אל מאגרי מידע שמחוץ
  לגבולות המדינה), התשס״א-2001.
* Direct marketing - sections 17C-17F of the Privacy Protection Law.
* Accessibility - תקנה 35 לתקנות שוויון זכויות לאנשים עם מוגבלות
  (התאמות נגישות לשירות), התשע״ג-2013, and IS 5568. Regulation 35(e)
  requires a prominent statement covering the adaptations made, the
  contact route for reporting a barrier, and any exemption relied on.

Every factual claim in the accessibility statement is verifiable against
the built site. Do not add a claim here that the markup does not support.
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
    "no_direct_marketing",
    "rights",
    "minors",
    "updates",
    "contact",
)


PRIVACY_SECTIONS_EN = {
    "controller": ("Who operates the site and controls the information", "This website is operated by {legal_name}, company number {registration_id}, of {postal_address}. The company is the controller of personal information collected through the site. Privacy enquiries may be sent to {privacy_email}."),
    "collection": ("What information is collected", "The contact form collects your name, email address and the content of your message, and optionally your organization and telephone number. Separately, and for security purposes only, technical data such as IP address, browser and device type, request time and anti-abuse signals are processed automatically. The site loads no analytics, advertising or profiling tools, so no browsing profile is built. Please do not submit confidential client records, privileged material, regulated data, identification numbers or health information through this public form."),
    "purposes": ("Purposes of processing", "Information is used to receive, assess and respond to your enquiry; to keep the site secure and available and to prevent abuse; to maintain necessary business records; and to comply with legal obligations or to establish, exercise and defend legal claims. It is not used for marketing, and it is not sold or shared with third parties for their own purposes."),
    "voluntary": ("Providing information is voluntary, and what happens if you do not", "You are under no legal obligation to provide any information. Disclosure is voluntary and based on your consent. Name, email, message and the acknowledgement are marked as required only because without them an enquiry cannot be identified or answered: if you do not provide them the form cannot be submitted and the enquiry cannot be handled. You may contact the firm by email or telephone instead. Sending an enquiry does not create a professional engagement."),
    "recipients": ("Who receives the information", "Information is accessible to authorized personnel of {legal_name} who need it in order to handle the enquiry, and to the service providers that operate parts of the site on the firm's behalf: Cloudflare, Inc. for hosting, security and the Turnstile anti-abuse check, and Resend (Plus Five Five, Inc.) for delivering the enquiry to the firm by email. Information may also be disclosed where required by law or by order of a competent authority, to professional advisers bound by confidentiality, and where necessary to protect legal rights."),
    "transfers": ("Processing outside Israel", "The providers named above may process and store information outside Israel, including in the United States and in other jurisdictions in which they or their subprocessors operate. Such transfers are made under those providers' contractual terms and the conditions required by the Privacy Protection Regulations (Transfer of Information to Databases Abroad), 2001."),
    "retention": ("How long information is kept", "Enquiry data is kept for up to {retention_months} months from the enquiry or from the end of the correspondence, whichever is later. A longer period applies only where reasonably required for an active professional engagement, a legal obligation, or the establishment or defence of a legal claim. At the end of the period the information is deleted or moved to access-restricted archival storage."),
    "security": ("Information security", "The site is served exclusively over encrypted connections (HTTPS) with a strict content security policy and enforced transport security. Access to enquiry data is limited to authorized recipients; the contact endpoint validates input server-side, checks the request origin, and is protected by Cloudflare Turnstile. No online system can be guaranteed completely secure, and no such guarantee is given here."),
    "no_direct_marketing": ("No profiling, direct marketing or automated decisions", "The site does not perform profiling, does not make decisions producing legal effects by automated means alone, and does not operate a database for direct-mailing services within the meaning of sections 17C to 17F of the Privacy Protection Law. You will not receive marketing messages as a result of contacting the firm through this site."),
    "rights": ("Your rights", "Under the Privacy Protection Law, 1981, you are entitled to inspect information held about you, to request its correction where it is inaccurate, incomplete, unclear or out of date, and to request its deletion in the appropriate cases. Send a request to {privacy_email}; the firm will respond within the periods set by law. Identity may need to be verified before a request is processed, and information may be retained where the law permits or requires it. If the firm's response does not satisfy you, you may complain to the Privacy Protection Authority at the Ministry of Justice."),
    "minors": ("Minors", "This is a business website addressed to organizations and is not directed to minors. A minor should not submit personal information through it without the involvement of a parent or legal guardian."),
    "updates": ("Dates and changes to this policy", "Last updated: {effective_date}. Next scheduled review: {review_date}. Material changes will be published on this page and the date above updated accordingly."),
    "contact": ("Privacy contact", "Questions, objections and requests to exercise your rights may be sent to {privacy_email}, or by post to {legal_name}, {postal_address}."),
}

PRIVACY_SECTIONS_HE = {
    "controller": ("מי מפעיל את האתר ומי בעל השליטה במידע", "האתר מופעל על ידי {legal_name}, ח.פ. {registration_id}, מכתובת {postal_address}. החברה היא בעלת השליטה במידע האישי הנאסף באמצעות האתר. לפניות בנושאי פרטיות ניתן לכתוב אל {privacy_email}."),
    "collection": ("איזה מידע נאסף", "טופס יצירת הקשר אוסף את שמכם, את כתובת הדוא״ל ואת תוכן ההודעה, ולבחירתכם גם את שם הארגון ומספר טלפון. בנפרד, ולצורכי אבטחה בלבד, מעובדים באופן אוטומטי נתונים טכניים כגון כתובת IP, סוג הדפדפן והמכשיר, מועד הבקשה ואותות למניעת שימוש לרעה. באתר אינם פועלים כלי אנליטיקה, פרסום או פרופיילינג, ולכן לא נבנה פרופיל גלישה. אין למסור באמצעות הטופס הפומבי מסמכי לקוחות חסויים, חומר חסוי מכוח דין, מידע מפוקח, מספרי זיהוי או מידע רפואי."),
    "purposes": ("מטרות העיבוד", "המידע משמש לקבלת פנייתכם, לבחינתה ולמתן מענה; לשמירה על אבטחת האתר וזמינותו ולמניעת שימוש לרעה; לניהול רשומות עסקיות נדרשות; ולעמידה בחובות שבדין או לביסוס, למימוש ולהגנה על זכויות וטענות משפטיות. המידע אינו משמש למטרות שיווק, ואינו נמכר או נמסר לצדדים שלישיים לשימושם שלהם."),
    "voluntary": ("מסירת המידע היא מרצון, ומה קורה אם לא תמסרו", "אינכם חייבים על פי דין למסור מידע כלשהו. המסירה נעשית מרצונכם ובהסכמתכם. השדות שם, דוא״ל, תוכן ההודעה ואישור ההודעה מסומנים כשדות חובה רק מפני שבלעדיהם לא ניתן לזהות את הפנייה ולהשיב לה: אם לא תמסרו אותם, לא ניתן יהיה לשלוח את הטופס ולא נוכל לטפל בפנייה. תמיד ניתן לפנות אלינו במקום זאת בדוא״ל או בטלפון. שליחת פנייה אינה יוצרת התקשרות מקצועית."),
    "recipients": ("למי נמסר המידע", "המידע נגיש לעובדים מורשים של {legal_name} הנדרשים לו לצורך הטיפול בפנייה, ולספקי השירות המפעילים חלקים מהאתר עבור החברה: Cloudflare, Inc. לאירוח האתר, לאבטחתו ולשירות Turnstile למניעת שימוש אוטומטי לרעה, ו-Resend (Plus Five Five, Inc.) להעברת הפנייה אל המשרד בדוא״ל. מידע עשוי להימסר גם כאשר הדבר נדרש לפי דין או לפי צו של רשות מוסמכת, ליועצים מקצועיים החבים בחובת סודיות, וכאשר הדבר נחוץ להגנה על זכויות משפטיות."),
    "transfers": ("עיבוד מחוץ לישראל", "ספקי השירות המפורטים לעיל עשויים לעבד ולאחסן מידע מחוץ לישראל, לרבות בארצות הברית ובמדינות נוספות שבהן הם או קבלני המשנה שלהם פועלים. ההעברה נעשית בהתאם לתנאי ההתקשרות עם אותם ספקים ולתנאים הקבועים בתקנות הגנת הפרטיות (העברת מידע אל מאגרי מידע שמחוץ לגבולות המדינה), התשס״א-2001."),
    "retention": ("משך שמירת המידע", "מידע שהתקבל בפנייה נשמר לתקופה של עד {retention_months} חודשים ממועד הפנייה או מסיום ההתכתבות, לפי המאוחר מביניהם. תקופה ארוכה יותר תחול רק כאשר היא נדרשת באופן סביר לצורך התקשרות מקצועית פעילה, חובה שבדין, או ביסוס והגנה על טענה משפטית. בתום התקופה המידע נמחק או מועבר לאחסון ארכיוני מוגבל גישה."),
    "security": ("אבטחת המידע", "האתר מוגש בתעבורה מוצפנת (HTTPS) בלבד, עם מדיניות אבטחת תוכן מחמירה ואכיפת תעבורה מאובטחת. הגישה למידע מוגבלת לנמענים מורשים; נקודת הקצה של הטופס מאמתת את הקלט בצד השרת, בודקת את מקור הבקשה ומוגנת באמצעות Cloudflare Turnstile. אין מערכת מקוונת שניתן להבטיח את אבטחתה המוחלטת, ולא ניתנת כאן התחייבות כזו."),
    "no_direct_marketing": ("אין פרופיילינג, דיוור ישיר או החלטות אוטומטיות", "האתר אינו מבצע פרופיילינג, אינו מקבל באמצעים אוטומטיים בלבד החלטות בעלות תוצאה משפטית, ואינו מנהל מאגר לשירותי דיוור ישיר כמשמעותם בסעיפים 17ג עד 17ו לחוק הגנת הפרטיות. פנייה אל המשרד באמצעות האתר לא תגרור משלוח דברי פרסומת."),
    "rights": ("הזכויות שלכם", "על פי חוק הגנת הפרטיות, התשמ״א-1981, אתם זכאים לעיין במידע המוחזק אודותיכם, לבקש את תיקונו אם אינו נכון, שלם, ברור או מעודכן, ולבקש את מחיקתו במקרים המתאימים. בקשה יש לשלוח אל {privacy_email}, ונשיב לה בתוך המועדים הקבועים בדין. ייתכן שנידרש לאמת את זהותכם לפני הטיפול בבקשה, ונהיה רשאים להוסיף ולהחזיק מידע כאשר הדין מתיר או מחייב זאת. אם תשובת המשרד אינה מניחה את דעתכם, אתם רשאים להגיש תלונה לרשות להגנת הפרטיות במשרד המשפטים."),
    "minors": ("קטינים", "זהו אתר עסקי הפונה לארגונים ואינו מיועד לקטינים. על קטין להימנע ממסירת מידע אישי באמצעותו ללא מעורבות הורה או אפוטרופוס חוקי."),
    "updates": ("מועדים ושינויים במדיניות", "מועד העדכון האחרון: {effective_date}. מועד הבחינה המתוכנן הבא: {review_date}. שינויים מהותיים יפורסמו בעמוד זה, והמועד שלעיל יעודכן בהתאם."),
    "contact": ("יצירת קשר בנושאי פרטיות", "שאלות, התנגדויות ובקשות למימוש זכויות ניתן לשלוח אל {privacy_email}, או בדואר אל {legal_name}, {postal_address}."),
}


def _policy(title, eyebrow, lead, sections):
    return {"title": title, "eyebrow": eyebrow, "lead": lead, "sections": sections}


COOKIES_SECTIONS_EN = {
    "essential": ("Essential browser storage", "The key scout-consent-v1 records that the essential-only notice has been shown and acknowledged. The key scout-language records the site language you selected. Both are stored in your own browser, are not transmitted to the firm, and are not used for advertising or analytics."),
    "turnstile": ("Cloudflare Turnstile", "The contact page loads Cloudflare Turnstile to distinguish a genuine enquiry from automated abuse. Cloudflare may process IP, browser and device signals, and may set essential security tokens or cookies for that purpose. The form cannot be submitted without a successful security check. Turnstile is used on the contact page only."),
    "no_tracking": ("No tracking technologies", "No analytics, advertising, retargeting, social media or session-recording technology is loaded anywhere on this site. There is no optional consent toggle because there is no optional processing to consent to."),
    "choices": ("Your choices", "You can clear local storage and site data at any time through your browser settings; the site continues to work and the notice is simply shown again. The notice can also be reopened from Privacy settings in the footer."),
    "updates": ("Dates", "Last updated: {effective_date}. Next scheduled review: {review_date}."),
}

COOKIES_SECTIONS_HE = {
    "essential": ("אחסון חיוני בדפדפן", "המפתח scout-consent-v1 מתעד שההודעה על שימוש חיוני בלבד הוצגה ואושרה. המפתח scout-language מתעד את שפת האתר שבחרתם. שניהם נשמרים בדפדפן שלכם, אינם נשלחים אל המשרד, ואינם משמשים לפרסום או לאנליטיקה."),
    "turnstile": ("Cloudflare Turnstile", "עמוד יצירת הקשר טוען את שירות Cloudflare Turnstile כדי להבחין בין פנייה אמיתית לבין שימוש אוטומטי לרעה. Cloudflare עשויה לעבד כתובת IP ואותות דפדפן ומכשיר, ולהגדיר לשם כך אסימוני אבטחה או קובצי Cookie חיוניים. לא ניתן לשלוח את הטופס בלי בדיקת אבטחה מוצלחת. השירות פועל בעמוד יצירת הקשר בלבד."),
    "no_tracking": ("אין טכנולוגיות מעקב", "בשום עמוד באתר אינם נטענים כלי אנליטיקה, פרסום, ריטרגטינג, רשתות חברתיות או הקלטת גלישה. אין מתג הסכמה אופציונלי מפני שאין עיבוד אופציונלי שנדרשת לו הסכמה."),
    "choices": ("הבחירות שלכם", "ניתן למחוק בכל עת את האחסון המקומי ואת נתוני האתר דרך הגדרות הדפדפן; האתר ימשיך לפעול, וההודעה פשוט תוצג שוב. כמו כן ניתן לפתוח את ההודעה מחדש באמצעות הגדרות פרטיות בתחתית האתר."),
    "updates": ("מועדים", "מועד העדכון האחרון: {effective_date}. מועד הבחינה המתוכנן הבא: {review_date}."),
}

TERMS_SECTIONS_EN = {
    "information": ("General information only", "Website content is general information and is not accounting, audit, tax, legal, investment or other professional advice. Do not act or refrain from acting in reliance on it without advice tailored to the relevant facts and jurisdiction."),
    "engagement": ("No professional engagement", "Sending a form, an email or a document does not create a client, accountant, auditor, fiduciary or other professional relationship. An engagement arises only once authorized parties have signed a written engagement agreement."),
    "accuracy": ("Availability and accuracy", "Reasonable care is taken in preparing the website, but to the extent permitted by law no warranty is given as to completeness, currency, fitness for a particular purpose or uninterrupted availability."),
    "confidentiality": ("Do not send sensitive material", "Do not submit confidential, privileged, regulated or otherwise sensitive information through the public website. Contact the firm first so that an appropriate secure channel can be agreed."),
    "imagery": ("Photography and illustrations", "Photographs and illustrations on this site are used for editorial and illustrative purposes. Except for identified portraits of the firm's own personnel, they do not depict the firm's staff, offices, clients or actual engagements, and no inference should be drawn from them about any client, matter or result."),
    "intellectual": ("Intellectual property", "Unless stated otherwise, website text, visual design and firm marks belong to their respective owners and may not be copied or reused except as permitted by law or with prior written permission."),
    "links": ("Third-party services", "Links and embedded security services are provided for operation or convenience. Third-party terms and privacy practices apply to those services."),
    "law": ("Governing law and forum", "These terms are governed by the laws of the State of Israel. Subject to any mandatory provision of law, exclusive jurisdiction lies with {governing_court}."),
    "contact": ("Contact", "Questions about these terms may be sent to {privacy_email}."),
}

TERMS_SECTIONS_HE = {
    "information": ("מידע כללי בלבד", "תוכן האתר הוא מידע כללי ואינו מהווה ייעוץ חשבונאי, ביקורתי, מס, משפטי, השקעות או ייעוץ מקצועי אחר. אין לפעול או להימנע מפעולה בהסתמך עליו ללא ייעוץ המותאם לעובדות ולדין הרלוונטיים."),
    "engagement": ("אין התקשרות מקצועית", "שליחת טופס, דוא״ל או מסמך אינה יוצרת יחסי לקוח, רואה חשבון, מבקר, נאמנות או התקשרות מקצועית אחרת. התקשרות נוצרת רק לאחר חתימת הצדדים המוסמכים על הסכם התקשרות בכתב."),
    "accuracy": ("זמינות ודיוק", "נעשים מאמצים סבירים בהכנת האתר, אך במידה המותרת בדין לא ניתנת התחייבות לשלמות, לעדכניות, להתאמה למטרה מסוימת או לזמינות רציפה."),
    "confidentiality": ("אין לשלוח מידע רגיש", "אין למסור באמצעות האתר הפומבי מידע חסוי, חסוי מכוח דין, מפוקח או רגיש אחר. יש ליצור קשר תחילה כדי לסכם ערוץ מאובטח מתאים."),
    "imagery": ("תצלומים ואיורים", "התצלומים והאיורים באתר משמשים למטרות עריכה והמחשה. למעט דיוקנאות מזוהים של אנשי המשרד עצמו, אין הם מציגים את עובדי המשרד, את משרדיו, את לקוחותיו או התקשרויות בפועל, ואין להסיק מהם דבר לגבי לקוח, עניין או תוצאה כלשהם."),
    "intellectual": ("קניין רוחני", "אלא אם צוין אחרת, הטקסט, העיצוב החזותי וסימני המשרד שייכים לבעליהם, ואין להעתיקם או לעשות בהם שימוש חוזר אלא כמותר בדין או באישור מראש ובכתב."),
    "links": ("שירותי צד שלישי", "קישורים ושירותי אבטחה משובצים ניתנים לצורכי תפעול או נוחות. על שירותים אלה חלים התנאים ומדיניות הפרטיות של אותם צדדים שלישיים."),
    "law": ("דין וסמכות שיפוט", "על תנאים אלה חל דין מדינת ישראל. בכפוף להוראת דין קוגנטית, סמכות השיפוט הייחודית נתונה ל{governing_court}."),
    "contact": ("יצירת קשר", "שאלות בנוגע לתנאים אלה ניתן לשלוח אל {privacy_email}."),
}

ACCESSIBILITY_SECTIONS_EN = {
    "standard": ("The standard applied", "This site has been made accessible in accordance with regulation 35 of the Equal Rights for Persons with Disabilities (Service Accessibility Adjustments) Regulations, 2013, and with Israeli Standard IS 5568, which is based on the WCAG 2.0 Level AA guidelines. The work was carried out with reference to WCAG 2.1 Level AA as well."),
    "adaptations": ("Accessibility adjustments implemented", "Semantic document structure with an ordered heading hierarchy and defined landmark regions; full operation by keyboard alone, including the navigation menus and the expandable sections; a visible focus indicator; a skip-to-main-content link; alternative text for images; labels bound to every form field, with status messages announced to screen readers; colour contrast ratios meeting the standard; a responsive layout that supports zoom and reflow; an explicit language and text direction on every page; and respect for the operating system reduced-motion preference."),
    "testing": ("How accessibility was tested", "Every page of the site, in both languages and at both desktop and mobile viewport sizes, is checked automatically with the axe-core accessibility engine, and keyboard operation of the interactive components is covered by automated tests. These checks run again on every change to the site, before it is published."),
    "limits": ("Known limitations", "No external audit by a licensed service-accessibility expert has been carried out, and no comprehensive testing with commercial screen readers has been performed. Automated testing does not detect every barrier. We are not currently aware of a specific accessibility barrier on this site; if you find one, we want to hear about it."),
    "contact": ("Reporting a barrier", "If you encounter an accessibility barrier on this site, or need an accessibility adjustment in order to receive the service, contact {accessibility_name}: email {accessibility_email}, telephone {accessibility_phone}. It helps if you include the page address, what you were trying to do, and the assistive technology you were using. Every report is reviewed, and we will seek a solution or a suitable alternative within a reasonable time."),
    "dates": ("Statement dates", "Last updated: {effective_date}. Next scheduled review: {review_date}."),
}

ACCESSIBILITY_SECTIONS_HE = {
    "standard": ("התקן שלפיו הונגש האתר", "אתר זה הונגש בהתאם לתקנה 35 לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע״ג-2013, ובהתאם לתקן הישראלי ת״י 5568, המבוסס על הנחיות WCAG 2.0 ברמה AA. עבודת ההנגשה בוצעה תוך התייחסות גם להנחיות WCAG 2.1 ברמה AA."),
    "adaptations": ("התאמות הנגישות שבוצעו", "מבנה מסמך סמנטי עם היררכיית כותרות מסודרת ואזורי ניווט מוגדרים; הפעלה מלאה באמצעות מקלדת בלבד, לרבות תפריטי הניווט והמקטעים הנפתחים; סימון מיקוד נראה לעין; קישור לדילוג אל התוכן הראשי; טקסט חלופי לתמונות; תוויות המקושרות לכל שדה בטופס, והודעות מצב המוכרזות לקוראי מסך; יחסי ניגודיות צבע העומדים בדרישות התקן; פריסה רספונסיבית התומכת בהגדלה ובזרימה מחדש של התוכן; הגדרת שפה וכיווניות מפורשת בכל עמוד; וכיבוד העדפת מערכת ההפעלה להפחתת אנימציה."),
    "testing": ("כיצד נבדקה הנגישות", "כל עמודי האתר, בשתי השפות ובשני גדלי תצוגה, שולחני ונייד, נבדקים אוטומטית באמצעות מנוע הנגישות axe-core, והפעלת הרכיבים האינטראקטיביים באמצעות מקלדת מכוסה בבדיקות אוטומטיות. הבדיקות מורצות מחדש בכל שינוי באתר, לפני פרסומו."),
    "limits": ("מגבלות ידועות", "טרם בוצעה ביקורת חיצונית על ידי מורשה נגישות שירות, ולא בוצעה בדיקה מקיפה באמצעות קוראי מסך מסחריים. בדיקה אוטומטית אינה מאתרת כל חסם. אין לנו כיום ידיעה על חסם נגישות ספציפי באתר; אם נתקלתם בחסם, נשמח לשמוע על כך."),
    "contact": ("דיווח על חסם נגישות", "אם נתקלתם בחסם נגישות באתר, או אם דרושה לכם התאמת נגישות לשם קבלת השירות, ניתן לפנות אל {accessibility_name}: דוא״ל {accessibility_email}, טלפון {accessibility_phone}. יסייע לנו אם תציינו את כתובת העמוד, את הפעולה שניסיתם לבצע ואת טכנולוגיית הסיוע שבה השתמשתם. כל פנייה נבדקת, ונפעל למצוא פתרון או חלופה מתאימה בתוך זמן סביר."),
    "dates": ("מועדי ההצהרה", "מועד העדכון האחרון: {effective_date}. מועד הבחינה המתוכנן הבא: {review_date}."),
}


POLICIES = {
    "en": {
        "privacy": _policy("Privacy Policy", "Privacy", "How personal information is collected, used, shared and protected when you contact Scout Finance through this website.", PRIVACY_SECTIONS_EN),
        "cookies": _policy("Cookies & Local Storage", "Privacy controls", "This site uses essential browser storage and security technology only. It loads no analytics, advertising or profiling tools.", COOKIES_SECTIONS_EN),
        "terms": _policy("Website Terms of Use", "Legal", "Conditions governing use of the Scout Finance website and the general professional information published on it.", TERMS_SECTIONS_EN),
        "accessibility": _policy("Accessibility Statement", "Accessibility", "Scout Finance treats access to its digital service as part of the service itself. This statement describes how the site was made accessible, how that was tested, and how to reach us if something still blocks you.", ACCESSIBILITY_SECTIONS_EN),
    },
    "he": {
        "privacy": _policy("מדיניות פרטיות", "פרטיות", "כיצד נאסף, נעשה שימוש, מועבר ומוגן מידע אישי בעת פנייה אל Scout Finance באמצעות האתר.", PRIVACY_SECTIONS_HE),
        "cookies": _policy("קובצי Cookies ואחסון מקומי", "בקרות פרטיות", "באתר זה נעשה שימוש באחסון דפדפן חיוני ובטכנולוגיית אבטחה בלבד. אין בו כלי אנליטיקה, פרסום או יצירת פרופיל.", COOKIES_SECTIONS_HE),
        "terms": _policy("תנאי שימוש באתר", "משפטי", "התנאים החלים על השימוש באתר Scout Finance ועל המידע המקצועי הכללי המתפרסם בו.", TERMS_SECTIONS_HE),
        "accessibility": _policy("הצהרת נגישות", "נגישות", "ב-Scout Finance רואים בנגישות השירות הדיגיטלי חלק מהשירות עצמו. הצהרה זו מתארת כיצד הונגש האתר, כיצד נבדק, וכיצד לפנות אלינו אם משהו עדיין חוסם אתכם.", ACCESSIBILITY_SECTIONS_HE),
    },
}
