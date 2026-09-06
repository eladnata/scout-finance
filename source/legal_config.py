"""Central, environment-backed publication identity."""

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
        return [field for field in ENVIRONMENT_FIELDS if not getattr(self, field.lower())]

    def publication_values(self, lang: str = "en") -> dict[str, str]:
        """Safe preview values; production never reaches rendering with missing fields.

        Fallbacks are language-aware: a Hebrew legal page must never fall back
        to English prose. Contact details (email, phone) are not translated —
        only the descriptive fallback text differs by language. The company
        registration number is public information with a real value, not a
        "to be completed" placeholder, so it defaults the same in both
        languages unless overridden by SITE_REGISTRATION_ID.
        """
        if lang == "he":
            return {
                "legal_name": self.site_legal_name or "Scout Finance – ייעוץ ניהולי, חשבונאות וביקורת",
                "registration_id": self.site_registration_id or "515178788",
                "postal_address": self.site_postal_address or "משמר דוד, ישראל",
                "privacy_email": self.privacy_email or "info@scout-finance.co.il",
                "accessibility_name": self.accessibility_contact_name or "רכז/ת הנגישות של Scout Finance",
                "accessibility_email": self.accessibility_contact_email or "info@scout-finance.co.il",
                "accessibility_phone": self.accessibility_contact_phone or "+972-54-788-2877",
                "retention_months": self.contact_retention_months or "התקופה התפעולית המאושרת",
                "effective_date": self.policy_effective_date or "מועד הפרסום",
                "review_date": self.policy_review_date or "מועד הבחינה המשפטית המתוכנן",
                "governing_court": self.governing_court or "בתי המשפט המוסמכים בישראל",
            }
        return {
            "legal_name": self.site_legal_name or "Scout Finance Management Consulting & Audit",
            "registration_id": self.site_registration_id or "515178788",
            "postal_address": self.site_postal_address or "Mishmar David, Israel",
            "privacy_email": self.privacy_email or "info@scout-finance.co.il",
            "accessibility_name": self.accessibility_contact_name or "Scout Finance accessibility coordinator",
            "accessibility_email": self.accessibility_contact_email or "info@scout-finance.co.il",
            "accessibility_phone": self.accessibility_contact_phone or "+972-54-788-2877",
            "retention_months": self.contact_retention_months or "the approved operational period",
            "effective_date": self.policy_effective_date or "the publication date",
            "review_date": self.policy_review_date or "the scheduled legal review date",
            "governing_court": self.governing_court or "the competent courts in Israel",
        }
