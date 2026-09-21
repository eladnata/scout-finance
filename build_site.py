from pathlib import Path
from html import escape
import json, os, textwrap, shutil

from source.icons import icon
from source.legal_config import SiteIdentity
from source.legal_content import POLICIES
from source.media import media_panel, optional_media_panel

SOURCE_ROOT = Path(__file__).resolve().parent
ROOT = SOURCE_ROOT / 'dist'
ASSETS = ROOT / 'assets'
STATIC_ASSETS = SOURCE_ROOT / 'static' / 'assets'
# Production detection. CONTEXT is Netlify's variable; Cloudflare Pages sets
# CF_PAGES=1 and CF_PAGES_BRANCH instead. Relying on CONTEXT alone is why the
# production gate never fired on Cloudflare and preview legal text reached the
# live site.
CONTEXT = os.environ.get('CONTEXT', '').strip().lower()
CF_PAGES = os.environ.get('CF_PAGES', '').strip() == '1'
CF_PAGES_BRANCH = os.environ.get('CF_PAGES_BRANCH', '').strip()
PRODUCTION_BRANCH = os.environ.get('PRODUCTION_BRANCH', '').strip() or 'master'
IS_PRODUCTION = CONTEXT == 'production' or (CF_PAGES and CF_PAGES_BRANCH == PRODUCTION_BRANCH)

PLACEHOLDER_MEDIA = os.environ.get('PLACEHOLDER_MEDIA', '').strip() == '1'
SITE_IDENTITY = SiteIdentity.from_environment(os.environ)
TURNSTILE_TEST_SITE_KEY = '1x00000000000000000000AA'
TURNSTILE_SITE_KEY = os.environ.get('TURNSTILE_SITE_KEY', '').strip() or TURNSTILE_TEST_SITE_KEY

# Only render the contact form where it can actually work. With Cloudflare's
# test key the widget always passes in the browser, so a visitor gets a form
# that looks protected and a submission that then fails server-side, while the
# privacy and cookies pages state that Turnstile guards the form. Publishing
# direct contact details instead keeps those statements true. Setting a real
# TURNSTILE_SITE_KEY restores the form automatically.
CONTACT_FORM_ENABLED = (not IS_PRODUCTION) or TURNSTILE_SITE_KEY != TURNSTILE_TEST_SITE_KEY

if IS_PRODUCTION:
    blank_legal_values = SITE_IDENTITY.validate_for_production()
    if blank_legal_values:
        raise SystemExit('Blank production legal configuration: ' + ', '.join(blank_legal_values))
ROOT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

if STATIC_ASSETS.exists():
    shutil.copytree(STATIC_ASSETS, ASSETS, dirs_exist_ok=True)

logo_url = '/assets/logo.png'
site_origin = 'https://www.scout-finance.co.il'

services = [
    ('audit', 'Audit & Internal Audit', 'ביקורת וביקורת פנימית'),
    ('sox', 'SOX, JSOX & ISOX', 'SOX, JSOX ו-ISOX'),
    ('risk-controls', 'Risk, Controls & Process Improvement', 'סיכונים, בקרות ושיפור תהליכים'),
    ('financial-advisory', 'Financial & Management Advisory', 'ייעוץ פיננסי וניהולי'),
    ('investigative-audit', 'Investigative Audit', 'ביקורת חקירתית'),
    ('technology-audit', 'Technology & Computerized Environment Audit', 'ביקורת מערכות וסביבה ממוחשבת'),
    ('international', 'International Advisory', 'ייעוץ ופעילות בינלאומית'),
]

copy = {
'en': {
    'dir':'ltr','lang_name':'English','switch':'עברית','switch_lang':'he',
    'nav': {'home':'Home','services':'Services','industries':'Industries','about':'About','insights':'Insights','contact':'Contact','menu':'Menu','primary':'Primary navigation','website':'Website','email':'Email','phone':'Phone','location':'Location'},
    'cta':'Discuss your needs', 'back':'Back to services',
    'footer_blurb':'Management consulting, audit and financial advisory for complex organizations in Israel and internationally.',
    'response':'We typically respond within one business day.',
    'privacy':'Privacy Policy','cookies':'Cookies','terms':'Terms of Use','accessibility':'Accessibility Statement','privacy_settings':'Privacy settings','privacy_details':'Details','privacy_accept':'Understood','rights':'All rights reserved.',
    'home': {
        'meta':'Audit, control and financial advisory for complex organizations.',
        'eyebrow':'Management Consulting & Audit · Israel',
        'title':'Audit, control and financial advisory for complex organizations.',
        'lead':'Independent professional judgement for organizations that need stronger visibility, disciplined controls and practical financial oversight — in Israel and across international operations.',
        'primary':'Explore our services','secondary':'Speak with us',
        'proof':[('2015','Founded'),('20+','Years of experience'),('6','International markets'),('Multi-disciplinary','Accountants, economists & technology specialists')],
        'services_title':'Where precision matters most',
        'services_intro':'Focused support across audit, controls, financial management and cross-border operations — structured around the realities of complex organizations.',
        'challenges_title':'Challenges we help management address',
        'challenges':[
            ('Control environments that no longer match the organization','Assess processes, responsibilities and control design so management can see where gaps, duplication or exposure may exist.'),
            ('SOX-style requirements and documentation pressure','Support structured control mapping, testing and process discipline across SOX 404, JSOX and ISOX environments.'),
            ('Complex financial operations with limited visibility','Map financial procedures, risk points and management information flows to improve clarity and oversight.'),
            ('Oversight across subsidiaries and international activity','Provide audit, internal audit, operational and financial control support for groups operating across multiple countries.'),
        ],
        'method_title':'A practical way of working',
        'method_intro':'The exact scope is tailored to the assignment, while the working logic stays disciplined and transparent.',
        'method':[('01','Understand','Objectives, stakeholders, processes and context.'),('02','Assess','Risks, controls, documentation and operating reality.'),('03','Prioritize','Focus attention where management judgement matters most.'),('04','Support','Translate findings into practical actions and working practices.'),('05','Improve','Follow through, refine and strengthen over time where relevant.')],
        'leadership_title':'Experienced leadership, hands-on judgement',
        'leadership_text':'Scout Finance’s advisory team is led by Tomer Natan (LLM, BA, CPA), with more than 25 years of experience across technology, finance and audit. His background includes CFO roles, board and audit-committee experience, biotechnology and R&D financial management, and an early career at Ernst & Young Israel.',
        'leader_link':'Meet Tomer Natan',
        'international_title':'International perspective without losing operational detail',
        'international_text':'Scout Finance supports companies in Germany, Luxembourg, Canada, the United States, China and Japan — including subsidiaries, headquarters and complex corporate groups.',
        'industries_title':'Experience in demanding environments',
        'industries':[('Biotechnology & R&D','Financial management and advisory experience in innovation-driven organizations.'),('Hi-Tech','Audit, finance and control support for technology-oriented companies.'),('Public & Nonprofit','Audit expertise for public and nonprofit organizations with complex financial activity.'),('Complex Organizations','Government offices, institutions and sizeable organizations requiring structured oversight.')],
        'faq_title':'Questions executives often ask',
        'faqs':[
            ('When should an organization bring in an external internal-audit or controls advisor?','Typically when management needs an independent view of risks, processes and controls, when responsibilities have become complex, or when regulatory and governance expectations require more structure.'),
            ('Can Scout Finance support SOX work across international subsidiaries?','Scout Finance supports SOX 404, JSOX and ISOX work in international groups, including subsidiaries and headquarters. The exact scope should be defined around your reporting structure and regulatory environment.'),
            ('Do you work in computerized and payroll environments?','Yes. The service portfolio includes audit in computerized environments, including payroll systems.'),
        ],
        'final_title':'Need a clearer view of risk, controls or financial operations?',
        'final_text':'Tell us what your organization is dealing with. We will help define the right scope for the conversation.',
    },
    'service_common': {
        'when':'When this service is typically relevant','scope':'Typical scope','workstreams':'What the work can include','related':'Related services','talk':'Discuss this service'
    },
    'pages': {}
},
'he': {
    'dir':'rtl','lang_name':'עברית','switch':'English','switch_lang':'en',
    'nav': {'home':'בית','services':'שירותים','industries':'תחומי התמחות','about':'אודות','insights':'תובנות','contact':'יצירת קשר','menu':'תפריט','primary':'ניווט ראשי','website':'אתר','email':'דוא״ל','phone':'טלפון','location':'מיקום'},
    'cta':'בואו נדבר', 'back':'חזרה לשירותים',
    'footer_blurb':'ייעוץ ניהולי, ביקורת וייעוץ פיננסי לארגונים מורכבים בישראל ובפעילות בינלאומית.',
    'response':'אנו משתדלים להשיב בתוך יום עסקים אחד.',
    'privacy':'מדיניות פרטיות','cookies':'Cookies ואחסון מקומי','terms':'תנאי שימוש','accessibility':'הצהרת נגישות','privacy_settings':'הגדרות פרטיות','privacy_details':'לפרטים','privacy_accept':'הבנתי','rights':'כל הזכויות שמורות.',
    'home': {
        'meta':'ביקורת, בקרה וייעוץ פיננסי לארגונים מורכבים.',
        'eyebrow':'ייעוץ ניהולי וביקורת · ישראל',
        'title':'ביקורת, בקרה וייעוץ פיננסי לארגונים מורכבים.',
        'lead':'ניסיון מקצועי ומומחיות בתחומי הביקורת, הבקרה והייעוץ הפיננסי, לצד הבנה מעמיקה של תהליכים עסקיים וארגוניים — לארגונים שזקוקים לשקיפות טובה יותר, סביבת בקרה סדורה ופיקוח פיננסי פרקטי, בישראל ובפעילות בינלאומית.',
        'primary':'לשירותים שלנו','secondary':'שיחה מקצועית',
        'proof':[('2015','שנת הקמה'),('+20','שנות ניסיון'),('6','שווקים בינלאומיים'),('רב-תחומי','רואי חשבון, כלכלנים ומומחי מחשוב')],
        'services_title':'במקומות שבהם דיוק באמת משנה',
        'services_intro':'מענה ממוקד בתחומי ביקורת, בקרות, ניהול פיננסי ופעילות חוצת גבולות — בהתאם למציאות של ארגונים מורכבים.',
        'challenges_title':'אתגרים שאנחנו מסייעים להנהלה להתמודד איתם',
        'challenges':[
            ('סביבת בקרה שכבר אינה מתאימה לארגון','בחינת תהליכים, תחומי אחריות ועיצוב בקרות כדי לזהות פערים, כפילויות וחשיפות אפשריות.'),
            ('דרישות SOX ותיעוד מורכב','סיוע במיפוי בקרות, בדיקות ותהליכי עבודה סדורים בסביבות SOX 404, JSOX ו-ISOX.'),
            ('פעילות פיננסית מורכבת עם שקיפות מוגבלת','מיפוי תהליכים פיננסיים, מוקדי סיכון וזרימת מידע ניהולי לשיפור בהירות ופיקוח.'),
            ('פיקוח על חברות-בנות ופעילות בינלאומית','שירותי ביקורת, ביקורת פנימית ובקרה תפעולית ופיננסית לקבוצות הפועלות במספר מדינות.'),
        ],
        'method_title':'דרך עבודה פרקטית וסדורה',
        'method_intro':'היקף העבודה מותאם לכל משימה, אך ההיגיון המקצועי נשאר שקוף, ממוקד ומבוסס סדרי עדיפויות.',
        'method':[('01','הבנה','מטרות, בעלי עניין, תהליכים והקשר עסקי.'),('02','הערכה','סיכונים, בקרות, תיעוד והמציאות התפעולית.'),('03','תיעדוף','מיקוד בנקודות שבהן שיקול דעת ניהולי חשוב במיוחד.'),('04','יישום ותמיכה','תרגום ממצאים לפעולות ונהלי עבודה פרקטיים.'),('05','שיפור','מעקב, התאמה וחיזוק לפי הצורך לאורך זמן.')],
        'leadership_title':'ניסיון בכיר עם מעורבות מקצועית ישירה',
        'leadership_text':'צוות הייעוץ של Scout Finance מובל על ידי תומר נתן (LLM, BA, CPA), בעל למעלה מ-25 שנות ניסיון בטכנולוגיה, כספים וביקורת. ניסיונו כולל תפקידי CFO, חברות בדירקטוריונים ובוועדות ביקורת, ניהול פיננסי בחברות ביוטכנולוגיה ומו״פ ותחילת קריירה ב-Ernst & Young ישראל.',
        'leader_link':'להכיר את תומר נתן',
        'international_title':'ראייה בינלאומית בלי לאבד את הפרטים התפעוליים',
        'international_text':'Scout Finance עובדת עם חברות בגרמניה, לוקסמבורג, קנדה, ארצות הברית, סין ויפן — לרבות חברות-בנות, מטות וקבוצות תאגידיות מורכבות.',
        'industries_title':'ניסיון בסביבות מורכבות ותובעניות',
        'industries':[('ביוטכנולוגיה ומו״פ','ניסיון בניהול פיננסי וייעוץ בארגונים עתירי חדשנות.'),('היי-טק','ביקורת, כספים ובקרות לחברות בסביבה טכנולוגית.'),('מגזר ציבורי ומלכ״רים','מומחיות בביקורת לארגונים ציבוריים וללא כוונת רווח בעלי פעילות פיננסית מורכבת.'),('ארגונים מורכבים','משרדי ממשלה, מוסדות וארגונים גדולים הזקוקים לפיקוח ותהליכים סדורים.')],
        'faq_title':'שאלות שמנהלים נוהגים לשאול',
        'faqs':[
            ('מתי נכון להיעזר בגורם חיצוני לביקורת פנימית או לבקרות?','כאשר ההנהלה זקוקה לנקודת מבט עצמאית על סיכונים, תהליכים ובקרות, כאשר תחומי האחריות נעשו מורכבים, או כאשר דרישות רגולציה וממשל תאגידי מחייבות יותר סדר ותיעוד.'),
            ('האם Scout Finance יכולה לתמוך בעבודת SOX בקבוצה בינלאומית?','Scout Finance תומכת ב-SOX 404, JSOX ו-ISOX וכן בעבודה עם קבוצות בינלאומיות, חברות-בנות ומטות. היקף העבודה המדויק צריך להיקבע לפי מבנה הדיווח והסביבה הרגולטורית.'),
            ('האם אתם מבצעים ביקורת בסביבה ממוחשבת ובמערכות שכר?','כן. סל השירותים כולל ביקורת בסביבה ממוחשבת, לרבות מערכות שכר.'),
        ],
        'final_title':'צריכים תמונה ברורה יותר של סיכונים, בקרות או פעילות פיננסית?',
        'final_text':'ספרו לנו עם מה הארגון מתמודד. נסייע להגדיר את היקף השיחה המקצועית הנכון.',
    },
    'service_common': {
        'when':'מתי השירות רלוונטי בדרך כלל','scope':'תחומי פעילות אופייניים','workstreams':'מה יכולה לכלול העבודה','related':'שירותים קשורים','talk':'שיחה על השירות'
    },
    'pages': {}
}}

# Service page definitions, grounded in the current website.
service_defs = {
'audit': {
'en': {'title':'Audit & Internal Audit','eyebrow':'Audit & Assurance','lead':'Independent, structured audit work designed to give management and governance bodies a clearer view of processes, controls and financial activity.','when':['When internal-audit coverage needs to be established or strengthened.','When management or an audit committee needs an independent view of a process or subsidiary.','When public, nonprofit or complex organizations require purposeful financial audit work.'],'scope':['Internal audit','External and financial audit support','Audits for public and nonprofit organizations','Focused audits in subsidiary companies'],'work':['Define audit scope and objectives','Map relevant processes and responsibilities','Review documentation, controls and operating practice','Develop findings and practical recommendations','Present conclusions in a clear management-oriented format']},
'he': {'title':'ביקורת וביקורת פנימית','eyebrow':'ביקורת ואבטחת תהליכים','lead':'עבודת ביקורת עצמאית וסדורה שמטרתה לתת להנהלה ולגורמי הממשל התאגידי תמונה ברורה יותר של תהליכים, בקרות ופעילות פיננסית.','when':['כאשר יש צורך להקים או לחזק כיסוי של ביקורת פנימית.','כאשר הנהלה או ועדת ביקורת זקוקות לנקודת מבט עצמאית על תהליך או חברה-בת.','כאשר ארגון ציבורי, מלכ״ר או ארגון מורכב זקוק לביקורת פיננסית ממוקדת.'],'scope':['ביקורת פנימית','תמיכה בביקורת חיצונית ופיננסית','ביקורת לארגונים ציבוריים ומלכ״רים','ביקורות ממוקדות בחברות-בנות'],'work':['הגדרת היקף ומטרות הביקורת','מיפוי תהליכים ותחומי אחריות','בחינת תיעוד, בקרות והמצב בפועל','גיבוש ממצאים והמלצות פרקטיות','הצגת מסקנות בפורמט ברור להנהלה']}
},
'sox': {
'en': {'title':'SOX, JSOX & ISOX Compliance','eyebrow':'Controls & Regulatory Compliance','lead':'Structured support for control environments operating under SOX 404, JSOX and ISOX requirements — from process understanding through control work and ongoing discipline.','when':['When a company is preparing for or operating under SOX 404 requirements.','When a Japanese group requires JSOX work across the SOX process.','When Israeli or internationally traded companies need a disciplined control framework and supporting documentation.'],'scope':['SOX 404 support','JSOX process support','ISOX / Israeli SOX-style compliance','Control mapping, documentation and testing support'],'work':['Understand significant processes and reporting flows','Map risks and controls','Structure control documentation','Support testing and evidence discipline','Identify control gaps and practical remediation actions']},
'he': {'title':'SOX, JSOX ו-ISOX','eyebrow':'בקרות וציות רגולטורי','lead':'תמיכה סדורה בסביבות בקרה הפועלות תחת SOX 404, JSOX ו-ISOX — מהבנת התהליך ועד עבודת בקרות ומשמעת תיעודית מתמשכת.','when':['כאשר חברה נערכת ל-SOX 404 או פועלת תחת דרישות אלה.','כאשר קבוצה יפנית נדרשת לעבודת JSOX לאורך שלבי תהליך ה-SOX.','כאשר חברה ישראלית או נסחרת בינלאומית זקוקה למסגרת בקרות ותיעוד סדורה.'],'scope':['תמיכה ב-SOX 404','תמיכה בתהליכי JSOX','ISOX / SOX ישראלי','מיפוי בקרות, תיעוד ותמיכה בבדיקות'],'work':['הבנת תהליכים מהותיים וזרימת דיווח','מיפוי סיכונים ובקרות','בניית תיעוד בקרה סדור','תמיכה בבדיקות ובראיות','זיהוי פערי בקרה ופעולות תיקון פרקטיות']}
},
'risk-controls': {
'en': {'title':'Risk, Controls & Process Improvement','eyebrow':'Risk & Operations','lead':'A practical view of financial processes, risk points and control design — focused on making complexity more visible and management action more structured.','when':['When processes have grown organically and responsibilities are unclear.','When management needs a current risk assessment or process map.','When efficiency, savings or working-practice improvements need to be grounded in the actual operating environment.'],'scope':['Financial process mapping','Risk assessments','Efficiency and savings mechanisms','Working-practice and financial procedure guidelines'],'work':['Document the current-state process','Identify handoffs, dependencies and risk points','Assess control coverage and duplication','Prioritize improvement opportunities','Support practical procedures and implementation guidance']},
'he': {'title':'סיכונים, בקרות ושיפור תהליכים','eyebrow':'סיכונים ותפעול','lead':'מבט פרקטי על תהליכים פיננסיים, מוקדי סיכון ועיצוב בקרות — כדי להפוך מורכבות לשקופה יותר ופעולה ניהולית לסדורה יותר.','when':['כאשר תהליכים התפתחו לאורך זמן ותחומי האחריות אינם ברורים.','כאשר ההנהלה זקוקה להערכת סיכונים עדכנית או למפת תהליך.','כאשר מהלכי התייעלות, חיסכון או שיפור נהלים צריכים להתבסס על סביבת העבודה בפועל.'],'scope':['מיפוי תהליכים פיננסיים','הערכות סיכונים','מנגנוני התייעלות וחיסכון','נהלי עבודה ונהלים פיננסיים'],'work':['תיעוד מצב קיים','זיהוי ממשקים, תלות ומוקדי סיכון','בחינת כיסוי בקרות וכפילויות','תיעדוף הזדמנויות לשיפור','תמיכה בנהלים פרקטיים ובהטמעה']}
},
'financial-advisory': {
'en': {'title':'Financial & Management Advisory','eyebrow':'Finance & Management','lead':'Senior financial and management support for organizations that need stronger structure, clearer decision support and experienced financial judgement.','when':['When management needs additional financial leadership or perspective.','When financial processes, management reporting or economic assignments require focused support.','When employees need guidance in financial working practices and procedures.'],'scope':['Financial consulting','Management strategy','Financial management','Economic assignments','Employee consulting and guidance'],'work':['Clarify the management question and decision context','Review financial information and current practices','Structure analyses and management-level outputs','Develop practical financial procedures where relevant','Support internal teams in applying agreed working practices']},
'he': {'title':'ייעוץ פיננסי וניהולי','eyebrow':'כספים וניהול','lead':'תמיכה פיננסית וניהולית בכירה לארגונים הזקוקים למבנה חזק יותר, בסיס החלטה ברור ושיקול דעת פיננסי מנוסה.','when':['כאשר ההנהלה זקוקה לחיזוק מקצועי או לנקודת מבט פיננסית נוספת.','כאשר תהליכים פיננסיים, דיווח ניהולי או משימות כלכליות דורשים מיקוד.','כאשר עובדים זקוקים להדרכה בנהלי עבודה ובהתנהלות פיננסית.'],'scope':['ייעוץ פיננסי','אסטרטגיה ניהולית','ניהול פיננסי','משימות כלכליות','ייעוץ והדרכת עובדים'],'work':['הגדרת השאלה הניהולית והקשר ההחלטה','בחינת מידע פיננסי ונהלי עבודה קיימים','בניית ניתוחים ותוצרים להנהלה','גיבוש נהלים פיננסיים לפי הצורך','תמיכה בצוותים פנימיים ביישום דרכי העבודה']}
},
'investigative-audit': {
'en': {'title':'Investigative Audit','eyebrow':'Sensitive Reviews','lead':'Focused investigative audit support when management needs facts, structure and professional independence around a sensitive financial or operational concern.','when':['When an unusual event, pattern or concern requires independent examination.','When management needs a structured fact base before deciding on next steps.','When international or subsidiary activity requires focused investigative review.'],'scope':['Investigative audit','Focused financial review','Process and evidence examination','International investigative audit support'],'work':['Define the question and scope carefully','Preserve a fact-based and independent approach','Review relevant records, processes and evidence','Identify inconsistencies and control implications','Report findings clearly to the appropriate governance level']},
'he': {'title':'ביקורת חקירתית','eyebrow':'בדיקות רגישות','lead':'תמיכה ממוקדת בביקורת חקירתית כאשר הנהלה זקוקה לעובדות, מסגרת עבודה ועצמאות מקצועית סביב חשש פיננסי או תפעולי רגיש.','when':['כאשר אירוע חריג, דפוס או חשש דורשים בדיקה עצמאית.','כאשר ההנהלה זקוקה לבסיס עובדתי סדור לפני החלטה על צעדים הבאים.','כאשר פעילות בינלאומית או חברה-בת דורשות בדיקה חקירתית ממוקדת.'],'scope':['ביקורת חקירתית','בדיקה פיננסית ממוקדת','בחינת תהליכים וראיות','תמיכה בביקורת חקירתית בינלאומית'],'work':['הגדרת השאלה והיקף הבדיקה בזהירות','שמירה על גישה עצמאית ומבוססת עובדות','בחינת מסמכים, תהליכים וראיות רלוונטיים','זיהוי אי-התאמות והשלכות על סביבת הבקרה','דיווח ברור לגורם הממשל התאגידי המתאים']}
},
'technology-audit': {
'en': {'title':'Technology & Computerized Environment Audit','eyebrow':'Systems & Payroll','lead':'Audit work in computerized environments, including payroll systems, with attention to the controls and process dependencies that sit between technology and financial operations.','when':['When key financial processes depend heavily on computerized systems.','When payroll environments require focused audit attention.','When process risk cannot be understood without looking at system-supported workflows.'],'scope':['Audit in computerized environments','Payroll-system audit','Technology-supported process review','Control dependencies across systems and finance'],'work':['Understand the system-supported process','Map key data and control dependencies','Review relevant access, processing or reconciliation points at a process level','Assess how technology affects financial controls','Document findings and recommended actions']},
'he': {'title':'ביקורת מערכות וסביבה ממוחשבת','eyebrow':'מערכות ושכר','lead':'עבודת ביקורת בסביבה ממוחשבת, לרבות מערכות שכר, תוך התמקדות בבקרות ובתלויות שבין הטכנולוגיה לבין התהליכים הפיננסיים.','when':['כאשר תהליכים פיננסיים מהותיים תלויים במערכות ממוחשבות.','כאשר סביבת השכר דורשת תשומת לב ביקורתית ממוקדת.','כאשר אי אפשר להבין את הסיכון התהליכי בלי לבחון זרימות עבודה הנתמכות במערכת.'],'scope':['ביקורת בסביבה ממוחשבת','ביקורת מערכות שכר','בחינת תהליכים הנתמכים בטכנולוגיה','תלויות בקרה בין מערכות וכספים'],'work':['הבנת התהליך הנתמך במערכת','מיפוי תלויות נתונים ובקרות מרכזיות','בחינת נקודות גישה, עיבוד או התאמה ברמת התהליך','הערכת השפעת הטכנולוגיה על בקרות פיננסיות','תיעוד ממצאים ופעולות מומלצות']}
},
'international': {
'en': {'title':'International Advisory','eyebrow':'Cross-Border Operations','lead':'Management, strategy, financial and operational control, audit and internal-audit support for companies operating across multiple countries, subsidiaries and headquarters.','when':['When management needs consistent oversight across subsidiaries or markets.','When headquarters requires clearer financial or operational control across a group.','When audit or investigative work spans multiple jurisdictions and operating teams.'],'scope':['Management and strategy support','Financial and operational control','Audit and internal audit','Investigative audit for international groups'],'work':['Understand group structure and reporting lines','Clarify responsibilities between headquarters and local entities','Review financial and operational oversight processes','Coordinate audit or control work across relevant entities','Deliver management-level findings with cross-border context']},
'he': {'title':'ייעוץ ופעילות בינלאומית','eyebrow':'פעילות חוצת גבולות','lead':'תמיכה בניהול, אסטרטגיה, בקרה פיננסית ותפעולית, ביקורת וביקורת פנימית לחברות הפועלות במספר מדינות, חברות-בנות ומטות.', 'when':['כאשר הנהלה זקוקה לפיקוח עקבי על חברות-בנות או שווקים.','כאשר המטה זקוק לבקרה פיננסית או תפעולית ברורה יותר ברחבי הקבוצה.','כאשר ביקורת או בדיקה חקירתית משתרעות על פני מספר מדינות וצוותים.'],'scope':['תמיכה ניהולית ואסטרטגית','בקרה פיננסית ותפעולית','ביקורת וביקורת פנימית','ביקורת חקירתית בקבוצות בינלאומיות'],'work':['הבנת מבנה הקבוצה וקווי הדיווח','הבהרת אחריות בין מטה לישויות מקומיות','בחינת תהליכי פיקוח פיננסיים ותפעוליים','תיאום עבודת ביקורת או בקרות בין ישויות','הצגת ממצאים להנהלה בהקשר חוצה גבולות']}
}}

for slug, defs in service_defs.items():
    for lang in ('en','he'):
        copy[lang]['pages'][slug] = defs[lang]

# Other pages.
copy['en']['pages'].update({
'services': {'title':'Services','eyebrow':'Capabilities','lead':'Audit, controls and financial advisory designed around the needs of complex organizations — from focused assignments to broader management support.'},
'industries': {'title':'Industries & Expertise','eyebrow':'Where we work','lead':'Scout Finance works across biotechnology, R&D, hi-tech, public and nonprofit organizations, government offices, institutions and sizeable organizations with complex financial activity.'},
'about': {'title':'About Scout Finance','eyebrow':'The Firm','lead':'Scout Finance Management Consulting & Audit is an Israeli firm specializing in accountancy, internal and external audit, consulting and risk management. Founded in 2015, the firm brings together accountants, economists, computer specialists and articled clerks.'},
'leadership': {'title':'Tomer Natan, LLM, BA, CPA','eyebrow':'Leadership','lead':'More than 25 years across technology, finance and audit, with CFO, board and audit-committee experience and particular expertise in biotechnology, R&D and hi-tech financial management.'},
'insights': {'title':'Insights & Resources','eyebrow':'Knowledge','lead':'Practical perspectives on audit, controls, financial management and international operations.'},
'faq': {'title':'Frequently Asked Questions','eyebrow':'Practical Answers','lead':'A concise starting point for common questions about Scout Finance’s services and working model.'},
 'contact': {'title':'Start a focused conversation','eyebrow':'Contact','lead':'Tell us what your organization is dealing with. A short description is enough to start — we typically respond within one business day.'},
 'thank-you': {'title':'Your enquiry was sent','eyebrow':'Thank you','lead':'We received your details and will respond within one business day.'},
'privacy': {'title':'Privacy Policy','eyebrow':'Legal','lead':'This page provides a practical privacy notice for enquiries submitted through this website.'},
'cookies': {'title':'Cookies & Local Storage','eyebrow':'Privacy controls','lead':'Essential storage and security technology used by this website.'},
'terms': {'title':'Website Terms of Use','eyebrow':'Legal','lead':'Important conditions and limitations relating to this website and its general content.'},
'accessibility': {'title':'Accessibility Statement','eyebrow':'Accessibility','lead':'Scout Finance aims to provide a clear and accessible digital experience for a broad range of users and devices.'},
})
copy['he']['pages'].update({
'services': {'title':'שירותים','eyebrow':'יכולות מקצועיות','lead':'ביקורת, בקרות וייעוץ פיננסי המותאמים לצרכים של ארגונים מורכבים — ממשימות ממוקדות ועד תמיכה רחבה בהנהלה.'},
'industries': {'title':'תחומי התמחות','eyebrow':'היכן אנחנו פועלים','lead':'Scout Finance פועלת בתחומי ביוטכנולוגיה, מו״פ, היי-טק, ארגונים ציבוריים ומלכ״רים, משרדי ממשלה, מוסדות וארגונים גדולים בעלי פעילות פיננסית מורכבת.'},
'about': {'title':'אודות Scout Finance','eyebrow':'המשרד','lead':'Scout Finance Management Consulting & Audit הוא משרד ישראלי המתמחה בחשבונאות, ביקורת פנימית וחיצונית, ייעוץ וניהול סיכונים. המשרד הוקם בשנת 2015 ומאגד רואי חשבון, כלכלנים, מומחי מחשוב ומתמחים.'},
'leadership': {'title':'תומר נתן, LLM, BA, CPA','eyebrow':'הנהלה','lead':'למעלה מ-25 שנות ניסיון בטכנולוגיה, כספים וביקורת, לרבות תפקידי CFO, חברות בדירקטוריונים ובוועדות ביקורת ומומחיות בניהול פיננסי לחברות ביוטכנולוגיה, מו״פ והיי-טק.'},
'insights': {'title':'תובנות ומשאבים','eyebrow':'ידע מקצועי','lead':'תכנים פרקטיים על ביקורת, בקרות, ניהול פיננסי ופעילות בינלאומית.'},
'faq': {'title':'שאלות נפוצות','eyebrow':'תשובות מעשיות','lead':'נקודת פתיחה קצרה לשאלות שכיחות על שירותי Scout Finance ואופן העבודה.'},
 'contact': {'title':'מתחילים בשיחה ממוקדת','eyebrow':'יצירת קשר','lead':'ספרו לנו בקצרה עם מה הארגון מתמודד. תיאור קצר מספיק כדי להתחיל — אנו משתדלים להשיב בתוך יום עסקים אחד.'},
 'thank-you': {'title':'הפנייה נשלחה','eyebrow':'תודה','lead':'קיבלנו את הפרטים ונחזור אליכם בתוך יום עסקים אחד.'},
'privacy': {'title':'מדיניות פרטיות','eyebrow':'משפטי','lead':'עמוד זה מציג הודעת פרטיות פרקטית לפניות הנשלחות דרך האתר.'},
'cookies': {'title':'קובצי Cookies ואחסון מקומי','eyebrow':'בקרות פרטיות','lead':'אחסון חיוני וטכנולוגיות אבטחה שבהם משתמש האתר.'},
'terms': {'title':'תנאי שימוש באתר','eyebrow':'משפטי','lead':'תנאים ומגבלות חשובים החלים על האתר ועל המידע הכללי בו.'},
'accessibility': {'title':'הצהרת נגישות','eyebrow':'נגישות','lead':'Scout Finance שואפת לספק חוויה דיגיטלית ברורה ונגישה למגוון משתמשים ומכשירים.'},
})

SOURCE_DIR = SOURCE_ROOT / 'source'
STYLE = (SOURCE_DIR / 'styles.css').read_text(encoding='utf-8')
SCRIPT = (SOURCE_DIR / 'site.js').read_text(encoding='utf-8')

if STATIC_ASSETS.exists():
    ignore = None if PLACEHOLDER_MEDIA else shutil.ignore_patterns('images')
    shutil.copytree(STATIC_ASSETS, ASSETS, dirs_exist_ok=True, ignore=ignore)
(ASSETS/'styles.css').write_bytes(STYLE.encode('utf-8'))
(ASSETS/'site.js').write_bytes(SCRIPT.encode('utf-8'))

# Root is crawlable HTML; Netlify redirects it to Hebrew in production.
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="ביקורת, בקרה וייעוץ פיננסי לארגונים מורכבים."><meta name="robots" content="index,follow"><title>Scout Finance</title><link rel="canonical" href="{site_origin}/"><link rel="alternate" hreflang="he" href="{site_origin}/he/"><link rel="alternate" hreflang="en" href="{site_origin}/en/"><link rel="alternate" hreflang="x-default" href="{site_origin}/he/"><link rel="icon" href="/assets/favicon.ico"><link rel="stylesheet" href="/assets/styles.css"></head><body dir="rtl"><main id="main-content" class="language-chooser" tabindex="-1"><img src="/assets/logo.png" alt="Scout Finance"><h1>Scout Finance</h1><p>בחרו שפה / Choose a language</p><p><a class="btn btn-primary" href="/he/">עברית</a> <a class="btn btn-secondary" href="/en/">English</a></p></main></body></html>''',encoding='utf-8')

service_desc = {
'en': {
'audit':'Independent audit work for complex financial and governance environments.',
'sox':'Control frameworks, documentation and testing support for SOX-style requirements.',
'risk-controls':'Map processes, assess risks and strengthen practical control design.',
'financial-advisory':'Financial and management support for better-structured decisions and operations.',
'investigative-audit':'Independent, fact-based review for sensitive financial or operational concerns.',
'technology-audit':'Audit in computerized environments, including payroll-system processes.',
'international':'Oversight, audit and advisory support across subsidiaries and international groups.'},
'he': {
'audit':'עבודת ביקורת עצמאית בסביבות פיננסיות וממשל תאגידי מורכבות.',
'sox':'מסגרות בקרה, תיעוד ותמיכה בבדיקות לדרישות SOX וסביבות דומות.',
'risk-controls':'מיפוי תהליכים, הערכת סיכונים וחיזוק בקרות פרקטיות.',
'financial-advisory':'תמיכה פיננסית וניהולית לקבלת החלטות ולפעילות סדורה יותר.',
'investigative-audit':'בדיקה עצמאית ומבוססת עובדות בנושאים פיננסיים או תפעוליים רגישים.',
'technology-audit':'ביקורת בסביבה ממוחשבת, לרבות תהליכים במערכות שכר.',
'international':'פיקוח, ביקורת וייעוץ לחברות-בנות ולקבוצות בינלאומיות.'}}


def url(lang, slug=None):
    if not slug or slug=='home': return f'/{lang}/'
    return f'/{lang}/{slug}/'

def header(lang, current):
    c=copy[lang]; sw=c['switch_lang'];
    active=lambda slug: ' aria-current="page"' if current == slug else ''
    service_links=''.join(f'<a href="{url(lang,s)}"{active(s)}>{escape(en if lang=="en" else he)}</a>' for s,en,he in services)
    same = current if current else 'home'
    switch_url = url(sw, same)
    menu_items = '' if current == 'insights' else f'<a href="{url(lang,"industries")}"{active("industries")}>{c["nav"]["industries"]}</a><a href="{url(lang,"about")}"{active("about")}>{c["nav"]["about"]}</a>'
    return f'''<header class="site-header"><div class="container nav">
<a class="skip-link" href="#main-content">{'Skip to main content' if lang=='en' else 'דלג לתוכן הראשי'}</a>
<a class="brand" href="{url(lang)}" aria-label="Scout Finance {c['nav']['home']}"><img class="brand-mark" src="{logo_url}" alt="Scout Finance"><span class="brand-fallback">SCOUT FINANCE</span></a>
<button class="menu-btn" type="button" aria-label="{c['nav']['menu']}" aria-expanded="false" aria-controls="main-nav">☰</button>
<nav id="main-nav" class="nav-links" aria-label="{c['nav']['primary']}">
<a href="{url(lang)}"{active('home')}>{c['nav']['home']}</a>
<div class="nav-drop"><button type="button" data-dropdown-toggle aria-haspopup="true" aria-expanded="false" aria-controls="services-menu-{lang}">{c['nav']['services']}</button><div id="services-menu-{lang}" class="drop-menu" hidden><a href="{url(lang,'services')}"><strong>{c['nav']['services']}</strong></a>{service_links}</div></div>
{menu_items}
<a class="lang-link" href="{switch_url}" hreflang="{sw}">{c['switch']}</a><a class="nav-cta" href="{url(lang,'contact')}"{active('contact')}>{c['cta']}</a>
</nav></div></header>'''

def footer(lang):
    c=copy[lang]
    nav=''.join(f'<a href="{url(lang,s)}">{escape(n if lang=="en" else h)}</a>' for s,n,h in services[:4])
    return f'''<footer class="site-footer"><div class="container"><div class="footer-grid"><div><a class="brand" href="{url(lang)}"><img src="{logo_url}" alt="Scout Finance"></a><p class="footer-blurb">{c['footer_blurb']}</p></div><div><div class="footer-title">{c['nav']['services']}</div><div class="footer-links">{nav}<a href="{url(lang,'services')}">{c['nav']['services']}</a></div></div><div><div class="footer-title">{c['nav']['contact']}</div><div class="footer-links"><a dir="ltr" href="tel:+972547882877">+972-54-788-2877</a><a dir="ltr" href="mailto:info@scout-finance.co.il">info@scout-finance.co.il</a><span>{c['nav']['location']}: {'משמר דוד' if lang=='he' else 'Mishmar David'}</span></div></div></div><div class="footer-bottom"><span>© 2026 Scout Finance. {c['rights']}</span><span class="legal-links"><a href="{url(lang,'privacy')}">{c['privacy']}</a><a href="{url(lang,'cookies')}">{c['cookies']}</a><a href="{url(lang,'terms')}">{c['terms']}</a><a href="{url(lang,'accessibility')}">{c['accessibility']}</a><button type="button" data-privacy-open>{c['privacy_settings']}</button></span></div></div></footer>'''

def organization_schema(lang):
    data = {
        '@context':'https://schema.org', '@type':'ProfessionalService',
        'name':'Scout Finance', 'url':f'{site_origin}/{lang}/',
        'logo':f'{site_origin}/assets/logo.png', 'telephone':'+972-54-788-2877',
        'email':'info@scout-finance.co.il', 'areaServed':'IL'
    }
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def breadcrumb_schema(lang, title, slug):
    return json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':copy[lang]['nav']['home'],'item':f'{site_origin}/{lang}/'},
        {'@type':'ListItem','position':2,'name':title,'item':f'{site_origin}{url(lang,slug)}'}
    ]}, ensure_ascii=False, separators=(',', ':'))

def doc(lang, slug, title, desc, body):
    c=copy[lang]; same=slug if slug else 'home'; path = url(lang, slug)
    xdefault = url('he', same)
    robots = 'noindex,follow' if slug == 'insights' else 'index,follow'
    schema_tags = f'<script type="application/ld+json">{organization_schema(lang)}</script>'
    if slug:
        schema_tags += f'<script type="application/ld+json">{breadcrumb_schema(lang, title, slug)}</script>'
    disclosure_text = ('This site uses essential local storage and Cloudflare security technology only. No analytics or advertising tools are loaded.' if lang=='en' else 'אתר זה משתמש באחסון מקומי חיוני ובטכנולוגיית האבטחה של Cloudflare בלבד. לא נטענים כלי אנליטיקה או פרסום.')
    disclosure = f'''<aside class="privacy-disclosure" data-privacy-disclosure aria-label="{c['privacy_settings']}"><p>{disclosure_text}</p><div class="privacy-actions"><a href="{url(lang,'cookies')}">{c['privacy_details']}</a><button type="button" class="btn btn-primary" data-privacy-accept>{c['privacy_accept']}</button></div></aside>'''
    turnstile_script = '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" defer></script>' if slug == 'contact' and CONTACT_FORM_ENABLED else ''
    return f'''<!doctype html><html lang="{lang}" dir="{c['dir']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(desc)}"><meta name="robots" content="{robots}"><title>{escape(title)} | Scout Finance</title><link rel="canonical" href="{site_origin}{path}"><link rel="alternate" hreflang="en" href="{site_origin}{url('en',same)}"><link rel="alternate" hreflang="he" href="{site_origin}{url('he',same)}"><link rel="alternate" hreflang="x-default" href="{site_origin}{xdefault}"><link rel="icon" href="/assets/favicon.ico"><meta property="og:title" content="{escape(title)} | Scout Finance"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{site_origin}{path}"><meta property="og:image" content="{site_origin}/assets/og/scout-finance-share.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#071b33"><link rel="stylesheet" href="/assets/styles.css">{schema_tags}</head><body dir="{c['dir']}" class="{'rtl' if lang=='he' else ''}">{header(lang, same)}<main id="main-content" tabindex="-1">{body}</main>{footer(lang)}{disclosure}<script src="/assets/site.js" defer></script>{turnstile_script}</body></html>'''

def home_body(lang):
    c=copy[lang]; h=c['home']
    signals = [('EN','Independent judgement'),('SOX','Structured controls'),('INTL','Cross-border oversight')] if lang=='en' else [('IL','שיקול דעת עצמאי'),('SOX','בקרות סדורות'),('INTL','פיקוח בינלאומי')]
    sg=''.join(f'<div class="signal-line"><span>{escape(t)}</span><span>{escape(x)}</span></div>' for t,x in signals)
    proofs=''.join(f'<div class="proof-item"><span class="proof-number">{escape(a)}</span><div class="proof-label">{escape(b)}</div></div>' for a,b in h['proof'])
    icon_names={'audit':'audit','sox':'sox','risk-controls':'controls','financial-advisory':'advisory','investigative-audit':'investigative','technology-audit':'technology'}
    svc=''.join(f'<a class="service-entry" href="{url(lang,s)}">{icon(icon_names[s])}<span class="service-index">0{i}</span><div><h3>{escape(en if lang=="en" else he)}</h3><p>{escape(service_desc[lang][s])}</p><span class="service-action">{("Explore service" if lang=="en" else "לפרטי השירות")}</span></div></a>' for i,(s,en,he) in enumerate(services[:6],1))
    challenge_icons=('control-drift','documentation','transparency','subsidiaries')
    chall=''.join(f'<article class="challenge">{icon(challenge_icons[i],css_class="grid-icon")}<h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i,(a,b) in enumerate(h['challenges']))
    meth=''.join(f'<div class="rail-item"><span class="rail-marker" aria-hidden="true">{n}</span><div class="rail-body"><h3>{escape(t)}</h3><p>{escape(p)}</p></div></div>' for n,t,p in h['method'])
    countries=['Germany','Luxembourg','Canada','United States','China','Japan'] if lang=='en' else ['גרמניה','לוקסמבורג','קנדה','ארצות הברית','סין','יפן']
    countries_html=''.join(f'<div class="country"><strong>{x}</strong></div>' for x in countries)
    industry_icons=('biotech','hitech','public-sector','complex-org')
    industries=''.join(f'<article class="industry">{icon(industry_icons[i],css_class="grid-icon")}<h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i,(a,b) in enumerate(h['industries']))
    faqs=''.join(f'<div class="faq"><button type="button" aria-expanded="false" aria-controls="faq-{lang}-{i}"><span>{escape(q)}</span><span aria-hidden="true">+</span></button><div id="faq-{lang}-{i}" class="faq-answer" hidden>{escape(a)}</div></div>' for i,(q,a) in enumerate(h['faqs']))
    hero_media=media_panel('hero',lang,STATIC_ASSETS)
    method_media=media_panel('method',lang,STATIC_ASSETS)
    international_media=media_panel('international',lang,STATIC_ASSETS)
    hero_label='Scout Finance professional focus' if lang=='en' else 'המיקוד המקצועי של Scout Finance'
    return f'''<section class="institutional-hero"><div class="container hero-grid"><div class="hero-copy"><div class="eyebrow">{h['eyebrow']}</div><h1>{h['title']}</h1><p class="lead">{h['lead']}</p><div class="actions"><a class="btn btn-primary" href="{url(lang,'services')}">{h['primary']}</a><a class="btn btn-secondary" href="{url(lang,'contact')}">{h['secondary']}</a></div></div><aside class="hero-visual" aria-label="{hero_label}">{hero_media}<div class="hero-assurance"><div class="signal-top">Scout Finance</div><strong>{'Precision. Accountability. Clarity. Control.' if lang=='en' else 'דיוק. אחריות. בהירות. בקרה.'}</strong><div class="signal-lines">{sg}</div></div></aside></div></section>
<section class="proof-strip section--tight"><div class="container proof-grid">{proofs}</div></section>
<section class="section section--feature"><div class="container"><div class="section-head"><div><h2>{h['services_title']}</h2></div><p class="section-intro">{h['services_intro']}</p></div><div class="services-grid">{svc}</div></div></section>
<section class="section alt"><div class="container"><div class="section-head"><div><h2>{h['challenges_title']}</h2></div><p class="section-intro">{'The starting point is not a service catalogue. It is the management issue that needs a clearer answer.' if lang=='en' else 'נקודת הפתיחה אינה קטלוג שירותים, אלא הסוגיה הניהולית שזקוקה לתשובה ברורה יותר.'}</p></div><div class="challenge-grid">{chall}</div></div></section>
 <section class="section dark"><div class="container"><div class="method-editorial"><div><div class="section-head"><div><div class="eyebrow dark-accent">{'Method' if lang=='en' else 'מתודולוגיה'}</div><h2>{h['method_title']}</h2></div><p class="section-intro">{h['method_intro']}</p></div><div class="method-grid">{meth}</div></div>{method_media}</div></div></section>
 <section class="section"><div class="container split"><div><div class="eyebrow">{'Leadership' if lang=='en' else 'הנהלה'}</div><h2>{h['leadership_title']}</h2></div><div class="quote-panel"><p>{h['leadership_text']}</p><a class="text-link" href="{url(lang,'leadership')}">{h['leader_link']}</a></div></div></section>
<section class="section alt"><div class="container international-editorial"><div><div class="section-head"><div><div class="eyebrow">{'International' if lang=='en' else 'בינלאומי'}</div><h2>{h['international_title']}</h2></div><p class="section-intro">{h['international_text']}</p></div><div class="country-grid">{countries_html}</div></div>{international_media}</div></section>
<section class="section"><div class="container"><div class="section-head"><div><h2>{h['industries_title']}</h2></div><p class="section-intro">{'Experience matters most when the operating environment is complex, regulated or changing.' if lang=='en' else 'ניסיון חשוב במיוחד כאשר סביבת הפעילות מורכבת, מפוקחת או משתנה.'}</p></div><div class="industry-grid">{industries}</div></div></section>
 <section class="section alt"><div class="container"><div class="section-head"><div><h2>{h['faq_title']}</h2></div><a class="text-link" href="{url(lang,'faq')}">{'View all questions' if lang=='en' else 'לכל השאלות'}</a></div><div class="faq-list">{faqs}</div></div></section>
 <section class="section section--tight"><div class="container"><div class="cta-band"><div><h2>{h['final_title']}</h2><p>{h['final_text']}</p></div><div class="actions"><a class="btn btn-primary" href="{url(lang,'contact')}">{c['cta']}</a></div></div></div></section>'''

PAGE_HERO_MEDIA = {
    'services': 'page-services',
    'about': 'page-about',
    'industries': 'page-industries',
    'audit': 'page-audit',
    'sox': 'page-sox',
    'risk-controls': 'page-risk-controls',
    'financial-advisory': 'page-financial-advisory',
    'investigative-audit': 'page-investigative-audit',
    'technology-audit': 'page-technology-audit',
    'international': 'page-international',
    'contact': 'page-contact',
}

def page_hero(lang, slug, p):
    home = copy[lang]['nav']['home'];
    separator = '‹' if lang == 'he' else '/'
    hero_class = 'institutional-page-hero page-hero'
    media_html = ''
    slot = PAGE_HERO_MEDIA.get(slug)
    if slot:
        panel = optional_media_panel(slot, lang, STATIC_ASSETS)
        if panel:
            hero_class += ' institutional-page-hero--media'
            media_html = f'<div class="page-hero-media">{panel}</div>'
    return f'''<section class="{hero_class}"><div class="container"><div class="breadcrumbs"><a href="{url(lang)}">{home}</a><span aria-hidden="true">{separator}</span><span>{escape(p['title'])}</span></div><div class="eyebrow">{escape(p.get('eyebrow',''))}</div><h1>{escape(p['title'])}</h1><p class="lead">{escape(p['lead'])}</p></div>{media_html}</section>'''

def service_body(lang, slug):
    p=copy[lang]['pages'][slug]; c=copy[lang]; cm=c['service_common']
    bullets=lambda arr: '<ul class="bullet-list">'+''.join(f'<li>{escape(x)}</li>' for x in arr)+'</ul>'
    related=[x for x in services if x[0]!=slug][:4]
    rel=''.join(f'<a href="{url(lang,s)}">{escape(en if lang=="en" else he)}</a>' for s,en,he in related)
    return page_hero(lang,slug,p)+f'''<section class="section"><div class="container content-grid"><article class="content-main"><h2>{cm['when']}</h2>{bullets(p['when'])}<h2>{cm['scope']}</h2>{bullets(p['scope'])}<h2>{cm['workstreams']}</h2>{bullets(p['work'])}<div class="quote-panel spaced"><p>{'The scope is tailored to the organization, the governance need and the operating environment. The purpose is to create a usable management view — not additional complexity.' if lang=='en' else 'היקף העבודה מותאם לארגון, לצורכי הממשל התאגידי ולסביבת הפעילות. המטרה היא לייצר תמונה ניהולית שימושית — לא להוסיף מורכבות.'}</p></div></article><aside><div class="side-card"><h3>{cm['related']}</h3><div class="related">{rel}</div><div class="actions"><a class="btn btn-primary" href="{url(lang,'contact')}">{cm['talk']}</a></div></div></aside></div></section>'''

def legal_policy_body(lang, slug):
    policy = POLICIES[lang][slug]
    values = SITE_IDENTITY.publication_values(lang)
    sections = []
    for heading, paragraph in policy['sections'].values():
        rendered = paragraph.format_map(values)
        sections.append(f'<section class="legal-section"><h2>{escape(heading)}</h2><p>{escape(rendered)}</p></section>')
    return page_hero(lang,slug,policy)+f'''<section class="section"><div class="container content-main legal-main">{''.join(sections)}</div></section>'''

def generic_body(lang, slug):
    p=copy[lang]['pages'][slug]; h=copy[lang]['home'];
    body=page_hero(lang,slug,p)
    if slug=='services':
        cards=''.join(f'<a class="service-card" href="{url(lang,s)}"><span class="service-num">0{i}</span><div><h3>{escape(en if lang=="en" else he)}</h3><p>{escape(service_desc[lang][s])}</p></div></a>' for i,(s,en,he) in enumerate(services,1))
        body+=f'<section class="section"><div class="container"><div class="services-grid">{cards}</div></div></section>'
    elif slug=='industries':
        inds=''.join(f'<article class="industry"><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for a,b in h['industries'])
        extra = [('Packaging Law','Consulting and expert opinions on Israel’s Packaging Law.') if lang=='en' else ('חוק האריזות','ייעוץ וחוות דעת מקצועיות בנושא חוק האריזות בישראל.')]
        inds+=''.join(f'<article class="industry"><h3>{a}</h3><p>{b}</p></article>' for a,b in extra)
        body+=f'<section class="section"><div class="container"><div class="industry-grid industry-grid--listing">{inds}</div></div></section>'
    elif slug=='about':
        paras = [
            'Scout Finance provides accountancy, internal and external audit, consulting and risk-management services to government offices, institutions, companies, public organizations and nonprofits with complex financial activity.',
            'The firm was founded in 2015. Its professional staff includes accountants, economists, computer specialists and articled clerks, combining financial and operational perspectives around each assignment.',
             'The firm’s work spans Israel and international operations, including Germany, Luxembourg, Canada, the United States, China and Japan.'
        ] if lang=='en' else [
            'Scout Finance מספקת שירותי חשבונאות, ביקורת פנימית וחיצונית, ייעוץ וניהול סיכונים למשרדי ממשלה, מוסדות, חברות, ארגונים ציבוריים ומלכ״רים בעלי פעילות פיננסית מורכבת.',
            'המשרד הוקם בשנת 2015. הצוות המקצועי כולל רואי חשבון, כלכלנים, מומחי מחשוב ומתמחים, ומשלב נקודות מבט פיננסיות ותפעוליות בהתאם למשימה.',
             'פעילות המשרד כוללת את ישראל וכן עבודה בינלאומית בגרמניה, לוקסמבורג, קנדה, ארצות הברית, סין ויפן.'
        ]
        ps=''.join(f'<p>{x}</p>' for x in paras)
        body+=f'<section class="section"><div class="container content-grid"><article class="content-main"><h2>{"A firm built around professional judgement" if lang=="en" else "משרד המבוסס על ניסיון, מומחיות ועבודה מדויקת"}</h2>{ps}</article><aside><div class="side-card"><h3>{"Leadership" if lang=="en" else "הנהלה"}</h3><p>{h["leadership_text"]}</p><a class="text-link" href="{url(lang,"leadership")}">{h["leader_link"]}</a></div></aside></div></section>'
    elif slug=='leadership':
        details = [
            'Tomer Natan leads Scout Finance’s advisory team and brings more than 25 years of experience in technology, finance and audit.',
            'He serves as Chief Financial Officer at several companies and previously served as CFO of Quark Pharmaceuticals Inc.',
            'His experience also includes board and audit-committee roles and financial management expertise in biotechnology, R&D and hi-tech companies.',
            'Tomer began his professional career at Ernst & Young Israel.'
        ] if lang=='en' else [
            'תומר נתן מוביל את צוות הייעוץ של Scout Finance ומביא עמו למעלה מ-25 שנות ניסיון בטכנולוגיה, כספים וביקורת.',
            'הוא משמש כ-CFO במספר חברות ושימש בעבר כ-CFO של Quark Pharmaceuticals Inc.',
            'ניסיונו כולל גם תפקידים בדירקטוריונים ובוועדות ביקורת ומומחיות בניהול פיננסי בחברות ביוטכנולוגיה, מו״פ והיי-טק.',
            'את דרכו המקצועית החל ב-Ernst & Young ישראל.'
        ]
        leadership_media=media_panel('leadership',lang,STATIC_ASSETS)
        body+=f'<section class="section"><div class="container leadership-editorial">{leadership_media}<div><h2>{"Experience across finance, audit and technology" if lang=="en" else "ניסיון המחבר כספים, ביקורת וטכנולוגיה"}</h2><div class="quote-panel">'+''.join(f'<p class="profile-line">{x}</p>' for x in details)+'</div></div></div></section>'
    elif slug=='insights':
        topics=['Internal audit priorities','SOX and control environments','Financial process design','International oversight'] if lang=='en' else ['סדרי עדיפויות בביקורת פנימית','SOX וסביבות בקרה','תכנון תהליכים פיננסיים','פיקוח בינלאומי']
        items=''.join(f'<article class="industry"><div class="eyebrow">{("Topic" if lang=="en" else "נושא")}</div><h3>{x}</h3></article>' for x in topics)
        body+=f'<section class="section"><div class="container"><div class="industry-grid">{items}</div></div></section>'
    elif slug=='faq':
        extra = h['faqs'] + ([('Which countries does Scout Finance work in?','Germany, Luxembourg, Canada, the United States, China and Japan, in addition to Israel.'),('What kinds of organizations does the firm serve?','The firm works with government offices, institutions, sizeable companies, public organizations and nonprofits with complex financial activity.')] if lang=='en' else [('באילו מדינות Scout Finance פועלת?','גרמניה, לוקסמבורג, קנדה, ארצות הברית, סין ויפן, בנוסף לישראל.'),('עם אילו סוגי ארגונים המשרד עובד?','המשרד עובד עם משרדי ממשלה, מוסדות, חברות גדולות, ארגונים ציבוריים ומלכ״רים בעלי פעילות פיננסית מורכבת.')])
        faqs=''.join(f'<div class="faq"><button type="button" aria-expanded="false" aria-controls="faq-{lang}-{i}"><span>{escape(q)}</span><span aria-hidden="true">+</span></button><div id="faq-{lang}-{i}" class="faq-answer" hidden>{escape(a)}</div></div>' for i,(q,a) in enumerate(extra))
        body+=f'<section class="section"><div class="container"><div class="faq-list">{faqs}</div></div></section>'
    elif slug=='contact':
        labels = {'name':'Name','company':'Organization','email':'Work email','phone':'Phone','message':'What would you like to discuss?','submit':'Send enquiry','consent':'I acknowledge the collection notice and agree that the details I provide may be used to assess and respond to my enquiry in accordance with the Privacy Policy.'} if lang=='en' else {'name':'שם','company':'ארגון','email':'דוא״ל עסקי','phone':'טלפון','message':'על מה תרצו לדבר?','submit':'שליחת פנייה','consent':'קראתי את הודעת האיסוף ואני מסכים/ה שהפרטים שאמסור ישמשו לבחינת הפנייה ולמענה עליה בהתאם למדיניות הפרטיות.'}
        form_copy = {'en': {'location':'Location','website':'Website'}, 'he': {'location':'מיקום','website':'אתר'}}[lang]
        consent = labels['consent']
        if lang == 'en':
            consent = consent.replace('Privacy Policy', f'<a href="/{lang}/privacy/">Privacy Policy</a>')
        else:
            consent = consent.replace('מדיניות הפרטיות', f'<a href="/{lang}/privacy/">מדיניות הפרטיות</a>')
        notice = (f'Providing information is voluntary. Name, email, message and acknowledgement are required so we can respond. Authorized firm personnel and our hosting, anti-abuse and email providers may process the submission. Do not send confidential or sensitive information. <a href="/{lang}/privacy/">Read about purposes, recipients, retention and your rights.</a>' if lang=='en' else f'מסירת המידע היא מרצון. שם, דוא״ל, הודעה ואישור נדרשים כדי שנוכל להשיב. אנשי משרד מורשים וספקי האחסון, מניעת השימוש לרעה והדוא״ל עשויים לעבד את הפנייה. אין לשלוח מידע חסוי או רגיש. <a href="/{lang}/privacy/">למידע על המטרות, הנמענים, תקופת השמירה והזכויות שלכם.</a>')
        security_label = 'Security verification' if lang=='en' else 'אימות אבטחה'
        form_markup = f'''<form class="contact-form" name="contact-{lang}" method="POST" action="/api/contact"><input type="hidden" name="lang" value="{lang}"><p class="visually-hidden"><label for="{lang}-website">{form_copy['website']} <input id="{lang}-website" name="website" tabindex="-1" autocomplete="off"></label></p><div class="collection-notice" role="note"><strong>{'Before you submit' if lang=='en' else 'לפני השליחה'}</strong><p>{notice}</p></div><div class="form-grid"><div class="field"><label for="{lang}-name">{labels['name']} *</label><input id="{lang}-name" name="name" required maxlength="120" autocomplete="name"></div><div class="field"><label for="{lang}-organization">{labels['company']}</label><input id="{lang}-organization" name="organization" maxlength="160" autocomplete="organization"></div><div class="field"><label for="{lang}-email">{labels['email']} *</label><input id="{lang}-email" type="email" name="email" required maxlength="254" autocomplete="email"></div><div class="field"><label for="{lang}-phone">{labels['phone']}</label><input id="{lang}-phone" type="tel" name="phone" maxlength="40" autocomplete="tel"></div><div class="field full"><label for="{lang}-message">{labels['message']} *</label><textarea id="{lang}-message" name="message" required maxlength="5000"></textarea></div><div class="field full"><label class="consent" for="{lang}-consent"><input id="{lang}-consent" type="checkbox" name="privacy_ack" value="yes" required> <span>{consent}</span></label></div><div class="field full turnstile-shell"><span class="turnstile-label visually-hidden">{security_label}</span><input type="hidden" name="cf-turnstile-response" data-turnstile-token required><div class="cf-turnstile" data-sitekey="{escape(TURNSTILE_SITE_KEY)}" data-appearance="interaction-only" data-response-field="false" data-callback="scoutTurnstileSuccess" data-expired-callback="scoutTurnstileExpired" data-error-callback="scoutTurnstileExpired"></div></div><div class="field full"><button class="btn btn-primary" type="submit" data-idle-label="{labels['submit']}">{labels['submit']}</button><p class="form-status" role="status" aria-live="polite" tabindex="-1"></p></div></div></form>'''
        direct_markup = f'''<div class="contact-form contact-form--direct"><h2>{'Write to us directly' if lang=='en' else 'כתבו אלינו ישירות'}</h2><p>{'The enquiry form is temporarily unavailable. Please email or call us directly and we will respond within one business day.' if lang=='en' else 'טופס הפנייה אינו זמין כרגע. ניתן לפנות אלינו ישירות בדוא״ל או בטלפון, ונשיב בתוך יום עסקים אחד.'}</p><div class="actions"><a class="btn btn-primary" dir="ltr" href="mailto:info@scout-finance.co.il">info@scout-finance.co.il</a><a class="btn btn-secondary" dir="ltr" href="tel:+972547882877">+972-54-788-2877</a></div></div>'''
        contact_panel = form_markup if CONTACT_FORM_ENABLED else direct_markup
        body+=f'''<section class="section"><div class="container contact-layout"><div><div class="contact-meta"><div>{icon('contact',css_class='grid-icon')}<span class="contact-label">{copy[lang]['nav']['email']}</span><a class="contact-value" dir="ltr" href="mailto:info@scout-finance.co.il">info@scout-finance.co.il</a></div><div>{icon('phone',css_class='grid-icon')}<span class="contact-label">{copy[lang]['nav']['phone']}</span><a class="contact-value" dir="ltr" href="tel:+972547882877">+972-54-788-2877</a></div><div>{icon('location',css_class='grid-icon')}<span class="contact-label">{form_copy['location']}</span><span class="contact-value">{'משמר דוד, ישראל' if lang=='he' else 'Mishmar David, Israel'}</span></div></div><p>{copy[lang]['response']}</p></div>{contact_panel}</div></section>'''
    elif slug=='thank-you':
        title, lead = (('Your enquiry was sent', 'We received your details and will respond within one business day.') if lang=='en' else ('הפנייה נשלחה', 'קיבלנו את הפרטים ונחזור אליכם בתוך יום עסקים אחד.'))
        home_label = copy[lang]['nav']['home']
        body += f'<section class="section"><div class="container content-main"><div class="quote-panel"><h2>{title}</h2><p>{lead}</p><div class="actions"><a class="btn btn-primary" href="{url(lang)}">{home_label}</a><a class="btn btn-secondary" dir="ltr" href="tel:+972547882877">+972-54-788-2877</a></div></div></div></section>'
    return body

# Build all pages. Insights remains available for existing links but is not indexed until
# approved articles are published; thank-you pages are never included in the sitemap.
all_slugs = ['services'] + list(service_defs) + ['industries','about','leadership','insights','faq','contact','thank-you','privacy','cookies','terms','accessibility']
public_slugs = [slug for slug in all_slugs if slug not in ('insights', 'thank-you')]
for lang in ('en','he'):
    langdir=ROOT/lang; langdir.mkdir(parents=True,exist_ok=True)
    h=copy[lang]['home']
    (langdir/'index.html').write_text(doc(lang,None,h['title'],h['meta'],home_body(lang)),encoding='utf-8')
    for slug in all_slugs:
        p=copy[lang]['pages'][slug]
        body=service_body(lang,slug) if slug in service_defs else (legal_policy_body(lang,slug) if slug in POLICIES[lang] else generic_body(lang,slug))
        d=p['lead']
        ddir=langdir/slug; ddir.mkdir(parents=True,exist_ok=True)
        (ddir/'index.html').write_text(doc(lang,slug,p['title'],d,body),encoding='utf-8')

# Branded not-found page served by static hosts.
(ROOT/'404.html').write_text(f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>העמוד לא נמצא | Scout Finance</title><link rel="icon" href="/assets/favicon.ico"><link rel="stylesheet" href="/assets/styles.css"></head><body dir="rtl"><main id="main-content" class="language-chooser" tabindex="-1"><img src="/assets/logo.png" alt="Scout Finance"><h1>העמוד לא נמצא</h1><p>הקישור שחיפשתם אינו זמין.</p><div class="actions"><a class="btn btn-primary" href="/he/">חזרה לבית</a><a class="btn btn-secondary" href="/en/">English</a></div></main></body></html>''',encoding='utf-8')

# robots + sitemap
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://www.scout-finance.co.il/sitemap.xml\n',encoding='utf-8')
urls=[]
for lang in ('en','he'):
    urls.append(f'https://www.scout-finance.co.il/{lang}/')
    for slug in public_slugs: urls.append(f'https://www.scout-finance.co.il/{lang}/{slug}/')
sitemap='''<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>'
(ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8')

# Cloudflare Pages routing/header config (Netlify's equivalents live in
# the only deploy surface: Cloudflare Pages reads these from dist/.
(ROOT/'_redirects').write_text('/  /he/  302\n',encoding='utf-8')
(ROOT/'_headers').write_text('''/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*
  Content-Security-Policy: default-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self' https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; connect-src 'self' https://challenges.cloudflare.com; upgrade-insecure-requests
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Cross-Origin-Opener-Policy: same-origin-allow-popups
  Referrer-Policy: strict-origin-when-cross-origin
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
''',encoding='utf-8')

(ROOT/'README.md').write_text('''# Scout Finance Premium Website\n\nStatic bilingual (English/Hebrew) corporate website generated from the existing Scout Finance public-site facts.\n\n## Preview locally\n\n```bash\npython3 -m http.server 8080\n```\n\nOpen `http://localhost:8080/en/` or `/he/`.\n\n## Deploy\n\nThe output is fully static and can be deployed to Netlify, Cloudflare Pages, GitHub Pages (with path considerations), or any static host. Contact forms include Netlify Forms markup.\n\n## Important\n\nThe official logo is currently referenced from the existing Scout Finance website URL because the source asset could not be downloaded in this environment. For production, copy the official logo into `assets/` and replace the remote URL in `build_site.py`, then rebuild.\n\nRun `python3 build_site.py` to regenerate all pages after copy changes.\n''',encoding='utf-8')

print('Built', len(all_slugs)*2+3, 'files/pages')
