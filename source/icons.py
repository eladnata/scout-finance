"""Trusted inline SVG icons for Scout Finance service navigation."""

from html import escape


ICON_PATHS = {
    "audit": '<path d="M4 3h12l4 4v14H4z"/><path d="M16 3v5h5M8 13h8M8 17h5"/>',
    "sox": '<path d="M12 3l8 3v6c0 5-3.4 8.1-8 10-4.6-1.9-8-5-8-10V6z"/><path d="m8.5 12 2.2 2.2 4.8-5"/>',
    "controls": '<path d="M4 7h16M7 4v6M4 17h16M17 14v6M4 12h16M12 9v6"/>',
    "advisory": '<path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/>',
    "technology": '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M8 10l2 2 5-5"/>',
    "investigative": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M8 10.5l1.5 1.5 3.5-4"/>',
    "international": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "contact": '<path d="M4 5h16v14H4zM4 7l8 6 8-6"/>',
    # management challenges
    "control-drift": '<path d="M3 17.5 9 11l4 4 8-8.5"/><path d="M15 6.5h6v6"/><path d="M3 21h18"/>',
    "documentation": '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v5h5"/><path d="M9 12h7M9 16h7M9 8h2"/>',
    "transparency": '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/>',
    "subsidiaries": '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="16" width="6" height="5" rx="1"/><rect x="16" y="16" width="6" height="5" rx="1"/><path d="M12 7v5M5 16v-2h14v2"/>',
    # industries
    "biotech": '<path d="M7 3v4.5c0 3 5 4.5 5 4.5s5-1.5 5-4.5V3"/><path d="M7 21v-4.5c0-3 5-4.5 5-4.5s5 1.5 5 4.5V21"/><path d="M6 3h12M6 21h12M8.5 8h7M8.5 16h7"/>',
    "hitech": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "public-sector": '<path d="M3 21h18M4 21V10M20 21V10M12 3l9 5H3z"/><path d="M8 21v-7M12 21v-7M16 21v-7"/>',
    "complex-org": '<circle cx="12" cy="5" r="2.4"/><circle cx="5" cy="19" r="2.4"/><circle cx="19" cy="19" r="2.4"/><circle cx="12" cy="12" r="2.4"/><path d="M12 7.4v2.2M10.1 13.6 6.6 17M13.9 13.6 17.4 17"/>',
    # contact details
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 3 5.2 2 2 0 0 1 5 3z"/>',
    "location": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "website": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
}


def icon(name: str, title: str | None = None, css_class: str = "service-icon") -> str:
    """Render a fixed SVG icon, optionally with an accessible title."""

    path = ICON_PATHS[name]
    if title:
        accessibility = f'role="img"><title>{escape(title)}</title>'
    else:
        accessibility = 'aria-hidden="true" focusable="false">'
    return (
        f'<svg class="{escape(css_class)}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" {accessibility}{path}</svg>'
    )
