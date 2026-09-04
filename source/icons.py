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
}


def icon(name: str, title: str | None = None) -> str:
    """Render a fixed SVG icon, optionally with an accessible title."""

    path = ICON_PATHS[name]
    if title:
        accessibility = f'role="img"><title>{escape(title)}</title>'
    else:
        accessibility = 'aria-hidden="true" focusable="false">'
    return (
        '<svg class="service-icon" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" {accessibility}{path}</svg>'
    )
