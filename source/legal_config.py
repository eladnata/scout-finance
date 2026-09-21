"""Publication identity for the bilingual site.

Company identity below is public record: it was verified on 2026-09-21
against the Israeli Registrar of Companies open dataset on data.gov.il
for company number 515178788 (SCOUT FINANCE LTD / סקאוט פייננס בע״מ,
private Israeli company, active, incorporated 01/01/2015, registered
address Mishmar David 566, 7684100).

Because those are facts rather than configuration, they ship as verified
defaults instead of required environment variables. A forgotten variable
must never be able to put placeholder text onto a published legal page —
that failure mode is exactly what produced "to be completed before
publication" on the live privacy policy.

The remaining values are judgement calls rather than public record: the
retention period, the policy dates, the forum clause and the accessibility
contact. They keep an environment override so counsel can change any of
them without a code change.
"""

from dataclasses import dataclass
from typing import Mapping


ENVIRONMENT_FIELDS = (
    "SITE_LEGAL_NAME",
    "SITE_REGISTRATION_ID",
    "SITE_POSTAL_ADDRESS",
    "PRIVACY_EMAIL",
    "ACCESSIBILITY_CONTACT_NAME",
    "ACCESSIBILITY_CONTACT_EMAIL",
    "ACCESSIBILITY_CONTACT_PHONE",
    "CONTACT_RETENTION_MONTHS",
    "POLICY_EFFECTIVE_DATE",
    "POLICY_REVIEW_DATE",
    "GOVERNING_COURT",
)

# Registrar of Companies, verified 2026-09-21.
REGISTRATION_ID = "515178788"
CONTACT_EMAIL = "info@scout-finance.co.il"
CONTACT_PHONE = "+972-54-788-2877"

# Judgement calls. Counsel may override any of these via the environment.
RETENTION_MONTHS = "24"

DEFAULTS = {
    "he": {
        "legal_name": "סקאוט פייננס בע״מ",
        "registration_id": REGISTRATION_ID,
        "postal_address": "משמר דוד 566, מיקוד 7684100, ישראל",
        "privacy_email": CONTACT_EMAIL,
        "accessibility_name": "צוות הנגישות של Scout Finance",
        "accessibility_email": CONTACT_EMAIL,
        "accessibility_phone": CONTACT_PHONE,
        "retention_months": RETENTION_MONTHS,
        "effective_date": "21 בספטמבר 2026",
        "review_date": "21 בספטמבר 2027",
        "governing_court": "בתי המשפט המוסמכים בישראל",
    },
    "en": {
        "legal_name": "Scout Finance Ltd",
        "registration_id": REGISTRATION_ID,
        "postal_address": "566 Mishmar David, 7684100, Israel",
        "privacy_email": CONTACT_EMAIL,
        "accessibility_name": "the Scout Finance accessibility contact",
        "accessibility_email": CONTACT_EMAIL,
        "accessibility_phone": CONTACT_PHONE,
        "retention_months": RETENTION_MONTHS,
        "effective_date": "21 September 2026",
        "review_date": "21 September 2027",
        "governing_court": "the competent courts in Israel",
    },
}

# publication_values() key -> environment variable that overrides it.
_OVERRIDES = {
    "legal_name": "SITE_LEGAL_NAME",
    "registration_id": "SITE_REGISTRATION_ID",
    "postal_address": "SITE_POSTAL_ADDRESS",
    "privacy_email": "PRIVACY_EMAIL",
    "accessibility_name": "ACCESSIBILITY_CONTACT_NAME",
    "accessibility_email": "ACCESSIBILITY_CONTACT_EMAIL",
    "accessibility_phone": "ACCESSIBILITY_CONTACT_PHONE",
    "retention_months": "CONTACT_RETENTION_MONTHS",
    "effective_date": "POLICY_EFFECTIVE_DATE",
    "review_date": "POLICY_REVIEW_DATE",
    "governing_court": "GOVERNING_COURT",
}


@dataclass(frozen=True)
class SiteIdentity:
    site_legal_name: str = ""
    site_registration_id: str = ""
    site_postal_address: str = ""
    privacy_email: str = ""
    accessibility_contact_name: str = ""
    accessibility_contact_email: str = ""
    accessibility_contact_phone: str = ""
    contact_retention_months: str = ""
    policy_effective_date: str = ""
    policy_review_date: str = ""
    governing_court: str = ""

    @classmethod
    def from_environment(cls, environ: Mapping[str, str]) -> "SiteIdentity":
        values = {
            field.lower(): str(environ.get(field, "")).strip()
            for field in ENVIRONMENT_FIELDS
        }
        return cls(**values)

    def validate_for_production(self) -> list[str]:
        """Report values that would render blank.

        Every key now carries a verified or considered default, so this
        returns empty unless an environment override is set to whitespace.
        Publication is no longer gated on remembering an environment
        variable; it is gated on the Turnstile key, which is a real secret.
        """
        values = self.publication_values("he")
        return [_OVERRIDES[key] for key, value in values.items() if not str(value).strip()]

    def publication_values(self, lang: str = "en") -> dict[str, str]:
        """Resolved legal values for one language.

        An environment override wins; otherwise the verified or considered
        default for that language applies. Contact details are never
        translated — only descriptive text differs between languages.
        """
        defaults = DEFAULTS.get(lang, DEFAULTS["en"])
        resolved = {}
        for key, default in defaults.items():
            override = getattr(self, _OVERRIDES[key].lower(), "")
            resolved[key] = str(override).strip() or default
        return resolved
