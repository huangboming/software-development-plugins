#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Generate a self-contained HTML preview catalog from a DESIGN.md file.

Usage:
    uv run --script generate-preview.py DESIGN.md
    uv run --script generate-preview.py path/to/DESIGN.md --output custom.html

Parses the DESIGN.md to extract colors, typography, spacing, and radius
tokens, then emits a self-contained HTML file with light/dark surface
toggle. The output is `<input-stem>-preview.html` in the same directory
as the input unless --output is specified.

Parsing is heuristic and best-effort: it understands the template format
shipped with the write-design-system skill and the awesome-design-md
example format. Sections that can't be parsed are skipped silently.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Color:
    label: str
    light: str
    dark: str | None = None
    note: str = ""


@dataclass
class TypeRow:
    token: str
    size: str
    weight: str
    line_height: str = ""
    letter_spacing: str = ""
    family: str = ""
    usage: str = ""


@dataclass
class TokenRow:
    """Generic token row used for spacing, radius, shadow, motion."""

    token: str
    value: str
    usage: str = ""


@dataclass
class ParsedDesign:
    title: str = "Design System"
    last_updated: str = ""
    visual_theme: str = ""
    families: dict[str, str] = field(default_factory=dict)
    colors_by_group: dict[str, list[Color]] = field(default_factory=dict)
    typography: list[TypeRow] = field(default_factory=list)
    spacing: list[TokenRow] = field(default_factory=list)
    radius: list[TokenRow] = field(default_factory=list)
    shadows: list[TokenRow] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGBA_RE = re.compile(r"rgba?\([^)]+\)")
PLACEHOLDER_RE = re.compile(r"#<hex>|<[a-zA-Z]")


def is_placeholder(value: str) -> bool:
    return bool(PLACEHOLDER_RE.search(value))


def split_top_sections(content: str) -> dict[str, str]:
    """Split a markdown doc into top-level (## heading) sections."""
    sections: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []
    for line in content.split("\n"):
        m = re.match(r"^##\s+(?:\d+\.\s*)?(.+?)\s*$", line)
        if m:
            if current_name is not None:
                sections[current_name] = "\n".join(current_lines)
            current_name = m.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        sections[current_name] = "\n".join(current_lines)
    return sections


def split_sub_sections(section_body: str) -> dict[str, str]:
    """Split a section body into ### subsections (or #### sub-subsections)."""
    subs: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []
    for line in section_body.split("\n"):
        m = re.match(r"^####?\s+(.+?)\s*$", line)
        if m:
            if current_name is not None:
                subs[current_name] = "\n".join(current_lines)
            current_name = m.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        subs[current_name] = "\n".join(current_lines)
    return subs


def find_section(sections: dict[str, str], *keywords: str) -> str:
    for name, body in sections.items():
        lower = name.lower()
        if any(kw.lower() in lower for kw in keywords):
            return body
    return ""


def find_subsection(subs: dict[str, str], *keywords: str) -> str:
    for name, body in subs.items():
        lower = name.lower()
        if any(kw.lower() in lower for kw in keywords):
            return body
    return ""


# --- Color extraction ------------------------------------------------------


def extract_colors_from_section(section: str) -> dict[str, list[Color]]:
    r"""Extract colors from a Color section, grouped by subsection.

    Handles three formats:
      1. Template tables: `| brand-50 | #hex | notes |`
      2. Template semantic bullets: `**Label** (\`token\` → \`#hex\` light / \`#hex\` dark) — desc`
      3. awesome-design-md bullets: `**Label** (\`#hex\` / \`#hex\`): desc` or `**Label** (\`#hex\`): desc`
    """
    groups: dict[str, list[Color]] = {}

    current_group = "Palette"
    for raw_line in section.split("\n"):
        line = raw_line.rstrip()

        # Subsection header changes the current group
        m = re.match(r"^####?\s+(.+?)\s*$", line)
        if m:
            current_group = m.group(1).strip()
            continue

        if not line.strip():
            continue
        if is_placeholder(line):
            continue

        color = parse_color_line(line)
        if color is None:
            continue

        groups.setdefault(current_group, []).append(color)

    # Drop empty groups, dedupe within group
    out: dict[str, list[Color]] = {}
    for group, colors in groups.items():
        seen = set()
        unique = []
        for c in colors:
            key = (c.label, c.light)
            if key in seen:
                continue
            seen.add(key)
            unique.append(c)
        if unique:
            out[group] = unique
    return out


def parse_color_line(line: str) -> Color | None:
    """Try to parse a single line into a Color. Returns None if no color found."""

    # Template semantic bullet:
    # - **Page Canvas** (`background` → `#08090a` light / `#0f1011` dark) — desc
    m = re.search(
        r"\*\*([^*]+)\*\*\s*\([^)]*?→\s*`([^`]+)`(?:\s*light)?\s*/\s*`([^`]+)`(?:\s*dark)?",
        line,
    )
    if m:
        label = m.group(1).strip()
        light = m.group(2).strip()
        dark = m.group(3).strip()
        if not is_placeholder(light):
            return Color(label=label, light=light, dark=dark, note=_extract_note(line))

    # Template semantic bullet without dark:
    # - **Page Canvas** (`background` → `#08090a`) — desc
    m = re.search(r"\*\*([^*]+)\*\*\s*\([^)]*?→\s*`([^`]+)`\)", line)
    if m:
        light = m.group(2).strip()
        if not is_placeholder(light):
            return Color(label=m.group(1).strip(), light=light, note=_extract_note(line))

    # awesome-design-md bullet:
    # - **Marketing Black** (`#010102` / `#08090a`): description
    # - **Brand Indigo** (`#5e6ad2`): description
    m = re.search(
        r"\*\*([^*]+)\*\*\s*\(\s*`([^`]+)`(?:\s*/\s*`([^`]+)`)?\s*\)",
        line,
    )
    if m:
        label = m.group(1).strip()
        light = m.group(2).strip()
        dark = (m.group(3) or "").strip() or None
        if _looks_like_color(light) and not is_placeholder(light):
            return Color(label=label, light=light, dark=dark, note=_extract_note(line))

    # Markdown table row: | brand-50 | #hex | notes |
    if line.lstrip().startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and not _is_table_separator(cells):
            label, value = cells[0], cells[1]
            if _looks_like_color(value) and not is_placeholder(value):
                note = cells[2] if len(cells) >= 3 else ""
                return Color(label=label, light=value, note=note)

    return None


def _looks_like_color(value: str) -> bool:
    return bool(HEX_RE.fullmatch(value) or RGBA_RE.fullmatch(value))


def _is_table_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r"-+|:-+|-+:|:-+:", c) for c in cells if c)


def _extract_note(line: str) -> str:
    # Notes follow ":", "—", or "-" after the parenthetical
    m = re.search(r"\)\s*[—\-:]\s*(.+)$", line)
    return m.group(1).strip() if m else ""


# --- Typography extraction -------------------------------------------------


def extract_typography(section: str) -> list[TypeRow]:
    rows: list[TypeRow] = []
    in_table = False
    headers: list[str] = []
    for raw_line in section.split("\n"):
        line = raw_line.strip()
        if not line.startswith("|"):
            in_table = False
            headers = []
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if _is_table_separator(cells):
            continue
        # Header detection: must have something resembling size + weight columns
        if not in_table:
            lowered = [c.lower() for c in cells]
            if any("size" in c for c in lowered) and any("weight" in c for c in lowered):
                headers = lowered
                in_table = True
                continue
        if in_table and headers and len(cells) == len(headers):
            row_dict = dict(zip(headers, cells))
            size = row_dict.get("size", "")
            if not size or "<" in size:
                continue
            rows.append(
                TypeRow(
                    token=row_dict.get("token") or row_dict.get("role") or "",
                    size=size,
                    weight=row_dict.get("weight", ""),
                    line_height=row_dict.get("line height", ""),
                    letter_spacing=row_dict.get("letter spacing", ""),
                    family=row_dict.get("font", "") or row_dict.get("family", ""),
                    usage=row_dict.get("usage", "") or row_dict.get("notes", ""),
                )
            )
    return rows


def extract_font_families(section: str) -> dict[str, str]:
    families: dict[str, str] = {}
    # Template table: | Body | Inter | system... |
    in_table = False
    headers: list[str] = []
    for raw_line in section.split("\n"):
        line = raw_line.strip()
        if not line.startswith("|"):
            in_table = False
            headers = []
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if _is_table_separator(cells):
            continue
        if not in_table:
            lowered = [c.lower() for c in cells]
            if any("family" in c or "role" in c for c in lowered):
                headers = lowered
                in_table = True
                continue
        if in_table and headers and len(cells) >= 2:
            role = cells[0]
            family = cells[1]
            if family and not is_placeholder(family):
                families[role.lower()] = family

    # Bullet form: **Primary**: `Inter Variable`, ...
    for line in section.split("\n"):
        m = re.match(r"-\s*\*\*([^*]+)\*\*[:：]?\s*`?([^`,(]+)", line)
        if m:
            role = m.group(1).strip().lower()
            family = m.group(2).strip().rstrip(",").strip()
            if family and not is_placeholder(family):
                families.setdefault(role, family)
    return families


# --- Spacing / radius / shadow extraction ---------------------------------


def extract_token_table(
    section: str, *, token_prefix: str
) -> list[TokenRow]:
    """Extract rows from any token table whose row tokens start with token_prefix.

    Tables in the template use generic `Token | Value | Usage` headers, so we
    classify rows by inspecting the token name itself rather than the header.
    """
    rows: list[TokenRow] = []
    in_table = False
    headers: list[str] = []
    for raw_line in section.split("\n"):
        line = raw_line.strip()
        if not line.startswith("|"):
            in_table = False
            headers = []
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if _is_table_separator(cells):
            continue
        if not in_table:
            lowered = [c.lower() for c in cells]
            if any(c in ("token", "name") for c in lowered) and any(
                c in ("value", "treatment") for c in lowered
            ):
                headers = lowered
                in_table = True
                continue
        if in_table and headers and len(cells) == len(headers):
            row_dict = dict(zip(headers, cells))
            token = (row_dict.get("token") or row_dict.get("name") or "").strip()
            if not token.lower().startswith(token_prefix):
                continue
            value = (row_dict.get("value") or row_dict.get("treatment") or "").strip()
            if not value or "<" in value:
                continue
            rows.append(
                TokenRow(
                    token=token,
                    value=value,
                    usage=row_dict.get("usage", ""),
                )
            )
    return rows


# --- Top-level parser ------------------------------------------------------


def parse_design_md(path: Path) -> ParsedDesign:
    content = path.read_text()
    parsed = ParsedDesign()

    # Title from first H1
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        parsed.title = m.group(1).strip()

    # Last updated
    m = re.search(r"Last updated[:：]?\s*([^\n]+)", content)
    if m:
        parsed.last_updated = m.group(1).strip()

    sections = split_top_sections(content)

    color_section = find_section(sections, "Color")
    if color_section:
        parsed.colors_by_group = extract_colors_from_section(color_section)

    type_section = find_section(sections, "Typography", "Type")
    if type_section:
        parsed.typography = extract_typography(type_section)
        parsed.families = extract_font_families(type_section)

    layout_section = find_section(sections, "Layout")
    if layout_section:
        parsed.spacing = extract_token_table(layout_section, token_prefix="space")
        parsed.radius = extract_token_table(layout_section, token_prefix="radius")

    # Radius may be its own section in older templates
    if not parsed.radius:
        radius_section = find_section(sections, "Border Radius", "Radius")
        if radius_section:
            parsed.radius = extract_token_table(radius_section, token_prefix="radius")

    depth_section = find_section(sections, "Depth", "Elevation", "Shadow")
    if depth_section:
        parsed.shadows = extract_token_table(depth_section, token_prefix="shadow")

    # Visual theme — first paragraph after the heading
    theme_section = find_section(sections, "Visual Theme", "Atmosphere")
    if theme_section:
        first_para = []
        for line in theme_section.strip().split("\n"):
            if not line.strip():
                if first_para:
                    break
                continue
            if line.startswith("#"):
                break
            first_para.append(line.strip())
        parsed.visual_theme = " ".join(first_para)

    return parsed


# ---------------------------------------------------------------------------
# Color helpers (for contrast text computation)
# ---------------------------------------------------------------------------


def parse_hex(value: str) -> tuple[int, int, int] | None:
    m = HEX_RE.fullmatch(value.strip())
    if not m:
        return None
    h = m.group(0).lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def parse_rgba(value: str) -> tuple[float, float, float, float] | None:
    m = re.fullmatch(r"rgba?\(([^)]+)\)", value.strip())
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    if len(parts) < 3:
        return None
    try:
        r = float(parts[0])
        g = float(parts[1])
        b = float(parts[2])
        a = float(parts[3]) if len(parts) >= 4 else 1.0
        return r, g, b, a
    except ValueError:
        return None


def luminance(value: str) -> float | None:
    """Approximate relative luminance for picking light/dark text on a swatch."""
    rgb = parse_hex(value)
    if rgb is None:
        rgba = parse_rgba(value)
        if rgba is None:
            return None
        rgb = (rgba[0], rgba[1], rgba[2])

    def channel(v: float) -> float:
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def text_color_for(bg: str) -> str:
    lum = luminance(bg)
    if lum is None:
        return "#111"
    return "#0a0a0a" if lum > 0.5 else "#fafafa"


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------


CSS = """
:root {
    --bg: #ffffff;
    --bg-alt: #f7f7f8;
    --fg: #0a0a0a;
    --fg-muted: #6b6b73;
    --border: rgba(0, 0, 0, 0.08);
    --card: #ffffff;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.04);
}
body.dark {
    --bg: #0a0a0b;
    --bg-alt: #131316;
    --fg: #f7f8f8;
    --fg-muted: #8a8f98;
    --border: rgba(255, 255, 255, 0.08);
    --card: #131316;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.4), 0 4px 12px rgba(0, 0, 0, 0.3);
}
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, system-ui, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    transition: background 200ms ease, color 200ms ease;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 48px 32px 96px;
}
header.site {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 48px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}
header.site h1 {
    margin: 0 0 4px;
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
}
header.site .meta {
    color: var(--fg-muted);
    font-size: 13px;
}
.toggle {
    appearance: none;
    background: var(--bg-alt);
    color: var(--fg);
    border: 1px solid var(--border);
    border-radius: 9999px;
    padding: 8px 16px;
    font: inherit;
    font-size: 13px;
    cursor: pointer;
    transition: background 150ms ease;
}
.toggle:hover { background: var(--card); }
section.block {
    margin-bottom: 64px;
}
section.block > h2 {
    margin: 0 0 8px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--fg-muted);
}
section.block > h2 .count {
    font-weight: 400;
    text-transform: none;
    letter-spacing: normal;
    margin-left: 8px;
}
section.block > .lede {
    margin: 0 0 24px;
    color: var(--fg-muted);
    font-size: 14px;
    max-width: 720px;
}
.color-group {
    margin-bottom: 32px;
}
.color-group h3 {
    margin: 0 0 12px;
    font-size: 14px;
    font-weight: 600;
}
.swatch-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
}
.swatch {
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    background: var(--card);
    box-shadow: var(--shadow);
}
.swatch .chip {
    height: 96px;
    display: flex;
    align-items: flex-end;
    padding: 12px;
    font-size: 11px;
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
}
.swatch.split .chip {
    background: linear-gradient(to right, var(--swatch-light) 50%, var(--swatch-dark) 50%);
}
.swatch .meta {
    padding: 10px 12px 12px;
}
.swatch .label {
    font-size: 13px;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 4px;
}
.swatch .values {
    font-size: 11px;
    color: var(--fg-muted);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    line-height: 1.5;
    word-break: break-all;
}
.swatch .note {
    font-size: 11px;
    color: var(--fg-muted);
    margin-top: 6px;
    line-height: 1.4;
}
.type-ladder {
    display: flex;
    flex-direction: column;
    gap: 24px;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 32px;
    background: var(--card);
}
.type-row {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 32px;
    align-items: baseline;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}
.type-row:last-child { border-bottom: none; padding-bottom: 0; }
.type-row .meta {
    font-size: 11px;
    color: var(--fg-muted);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    line-height: 1.6;
}
.type-row .meta .token {
    font-weight: 600;
    color: var(--fg);
    font-size: 12px;
    margin-bottom: 4px;
    display: block;
}
.type-row .sample {
    color: var(--fg);
    overflow-wrap: break-word;
}
.scale-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
}
.scale-card {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    background: var(--card);
}
.scale-card .token {
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 4px;
}
.scale-card .value {
    font-size: 11px;
    color: var(--fg-muted);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    margin-bottom: 8px;
}
.scale-card .usage {
    font-size: 11px;
    color: var(--fg-muted);
    line-height: 1.4;
}
.spacing-bar {
    height: 8px;
    background: var(--fg);
    border-radius: 2px;
    margin: 8px 0;
}
.radius-demo {
    width: 64px;
    height: 64px;
    background: var(--fg);
    margin: 8px 0;
}
.empty {
    padding: 32px;
    text-align: center;
    color: var(--fg-muted);
    font-size: 13px;
    border: 1px dashed var(--border);
    border-radius: 12px;
}
.lede.theme {
    font-size: 15px;
    line-height: 1.65;
    color: var(--fg);
    max-width: 760px;
    margin-bottom: 0;
}
"""


JS = """
const stored = localStorage.getItem('design-preview-mode');
if (stored === 'dark') document.body.classList.add('dark');
function toggleMode() {
    document.body.classList.toggle('dark');
    localStorage.setItem(
        'design-preview-mode',
        document.body.classList.contains('dark') ? 'dark' : 'light'
    );
    const btn = document.getElementById('mode-toggle');
    btn.textContent = document.body.classList.contains('dark') ? '☀ Light' : '☾ Dark';
}
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mode-toggle');
    btn.textContent = document.body.classList.contains('dark') ? '☀ Light' : '☾ Dark';
});
"""


def render_color_swatch(color: Color) -> str:
    label = escape(color.label)
    light = color.light
    dark = color.dark or ""
    note = escape(color.note) if color.note else ""
    chip_text_color = text_color_for(light)

    if dark and dark != light:
        chip_style = (
            f"--swatch-light: {escape(light)}; --swatch-dark: {escape(dark)}; "
            f"color: {chip_text_color};"
        )
        values = f"<div class='values'>{escape(light)}<br>{escape(dark)}</div>"
        chip_class = "chip"
        wrapper_class = "swatch split"
    else:
        chip_style = f"background: {escape(light)}; color: {chip_text_color};"
        values = f"<div class='values'>{escape(light)}</div>"
        chip_class = "chip"
        wrapper_class = "swatch"

    note_html = f"<div class='note'>{note}</div>" if note else ""
    return (
        f"<div class='{wrapper_class}'>"
        f"<div class='{chip_class}' style='{chip_style}'>{escape(light)}</div>"
        f"<div class='meta'><div class='label'>{label}</div>{values}{note_html}</div>"
        f"</div>"
    )


def render_color_section(parsed: ParsedDesign) -> str:
    if not parsed.colors_by_group:
        return (
            "<section class='block'>"
            "<h2>Colors</h2>"
            "<div class='empty'>No color tokens detected. "
            "Make sure colors are listed as bullets like "
            "<code>**Name** (`#hex`): description</code> "
            "or in markdown tables under a Color section.</div>"
            "</section>"
        )

    groups_html = []
    total = 0
    for group, colors in parsed.colors_by_group.items():
        total += len(colors)
        swatches = "".join(render_color_swatch(c) for c in colors)
        groups_html.append(
            f"<div class='color-group'>"
            f"<h3>{escape(group)}</h3>"
            f"<div class='swatch-grid'>{swatches}</div>"
            f"</div>"
        )
    return (
        "<section class='block'>"
        f"<h2>Colors <span class='count'>{total} tokens</span></h2>"
        f"{''.join(groups_html)}"
        "</section>"
    )


def render_type_section(parsed: ParsedDesign) -> str:
    if not parsed.typography:
        return (
            "<section class='block'>"
            "<h2>Typography</h2>"
            "<div class='empty'>No typography scale detected. "
            "Add a markdown table with <code>Token | Size | Weight</code> columns under a Typography section.</div>"
            "</section>"
        )

    body_family = (
        parsed.families.get("primary")
        or parsed.families.get("body")
        or next(iter(parsed.families.values()), "")
    )
    family_css = (
        f"font-family: {escape(body_family)}, system-ui, sans-serif;"
        if body_family
        else ""
    )

    rows_html = []
    for row in parsed.typography:
        size_css = _css_size(row.size)
        weight_css = _css_weight(row.weight)
        ls_css = _css_letter_spacing(row.letter_spacing)
        lh_css = _css_line_height(row.line_height)
        sample_style_parts = []
        if size_css:
            sample_style_parts.append(f"font-size: {size_css}")
        if weight_css:
            sample_style_parts.append(f"font-weight: {weight_css}")
        if ls_css:
            sample_style_parts.append(f"letter-spacing: {ls_css}")
        if lh_css:
            sample_style_parts.append(f"line-height: {lh_css}")
        if family_css:
            sample_style_parts.append(family_css.rstrip(";"))
        sample_style = "; ".join(sample_style_parts)

        token = escape(row.token) or "—"
        meta_lines = [f"<span class='token'>{token}</span>"]
        if row.size:
            meta_lines.append(escape(row.size))
        if row.weight:
            meta_lines.append(f"weight {escape(row.weight)}")
        if row.line_height:
            meta_lines.append(f"lh {escape(row.line_height)}")
        if row.letter_spacing and row.letter_spacing.lower() not in ("normal", ""):
            meta_lines.append(f"ls {escape(row.letter_spacing)}")
        if row.usage:
            meta_lines.append(f"<em>{escape(row.usage)}</em>")
        meta_html = "<br>".join(meta_lines)

        sample_text = "The quick brown fox jumps over the lazy dog"
        rows_html.append(
            f"<div class='type-row'>"
            f"<div class='meta'>{meta_html}</div>"
            f"<div class='sample' style='{sample_style}'>{sample_text}</div>"
            f"</div>"
        )

    return (
        "<section class='block'>"
        f"<h2>Typography <span class='count'>{len(parsed.typography)} sizes</span></h2>"
        f"<div class='type-ladder'>{''.join(rows_html)}</div>"
        "</section>"
    )


def render_token_grid(
    title: str,
    rows: list[TokenRow],
    *,
    visualizer: str | None = None,
) -> str:
    if not rows:
        return ""

    cards = []
    for row in rows:
        if is_placeholder(row.value):
            continue
        token = escape(row.token) or "—"
        value = escape(row.value)
        usage = escape(row.usage) if row.usage else ""
        viz_html = ""
        if visualizer == "spacing":
            px = _extract_pixels(row.value)
            if px:
                viz_html = f"<div class='spacing-bar' style='width: {min(px, 200)}px'></div>"
        elif visualizer == "radius":
            px = _extract_pixels(row.value)
            if px is not None:
                viz_html = (
                    f"<div class='radius-demo' style='border-radius: {min(px, 32)}px'></div>"
                )
        cards.append(
            f"<div class='scale-card'>"
            f"<div class='token'>{token}</div>"
            f"<div class='value'>{value}</div>"
            f"{viz_html}"
            f"<div class='usage'>{usage}</div>"
            f"</div>"
        )

    if not cards:
        return ""

    return (
        "<section class='block'>"
        f"<h2>{escape(title)} <span class='count'>{len(cards)} tokens</span></h2>"
        f"<div class='scale-grid'>{''.join(cards)}</div>"
        "</section>"
    )


# --- CSS coercion helpers --------------------------------------------------


def _extract_pixels(value: str) -> int | None:
    m = re.search(r"(-?\d+(?:\.\d+)?)px", value)
    if m:
        try:
            return int(float(m.group(1)))
        except ValueError:
            return None
    return None


def _css_size(value: str) -> str:
    m = re.search(r"(\d+(?:\.\d+)?)px", value)
    if m:
        return f"{m.group(1)}px"
    m = re.search(r"(\d+(?:\.\d+)?)rem", value)
    if m:
        return f"{m.group(1)}rem"
    return ""


def _css_weight(value: str) -> str:
    m = re.search(r"\b(\d{3})\b", value)
    if m:
        return m.group(1)
    return ""


def _css_letter_spacing(value: str) -> str:
    m = re.search(r"(-?\d+(?:\.\d+)?)px", value)
    if m:
        return f"{m.group(1)}px"
    return ""


def _css_line_height(value: str) -> str:
    m = re.search(r"\d+(?:\.\d+)?", value)
    if m:
        return m.group(0)
    return ""


# ---------------------------------------------------------------------------
# Top-level rendering
# ---------------------------------------------------------------------------


def render_html(parsed: ParsedDesign) -> str:
    title = escape(parsed.title)
    last_updated = escape(parsed.last_updated) if parsed.last_updated else ""
    theme = escape(parsed.visual_theme) if parsed.visual_theme else ""
    meta_html = ""
    if last_updated:
        meta_html += f"<div class='meta'>Last updated {last_updated}</div>"

    color_section = render_color_section(parsed)
    type_section = render_type_section(parsed)
    spacing_section = render_token_grid(
        "Spacing", parsed.spacing, visualizer="spacing"
    )
    radius_section = render_token_grid(
        "Border Radius", parsed.radius, visualizer="radius"
    )
    shadow_section = render_token_grid("Elevation", parsed.shadows)

    theme_html = (
        f"<section class='block'><h2>Visual Theme</h2>"
        f"<p class='lede theme'>{theme}</p></section>"
        if theme
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Preview</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<header class="site">
<div>
<h1>{title}</h1>
{meta_html}
</div>
<button id="mode-toggle" class="toggle" type="button" onclick="toggleMode()">☾ Dark</button>
</header>
{theme_html}
{color_section}
{type_section}
{spacing_section}
{radius_section}
{shadow_section}
</div>
<script>{JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a self-contained HTML preview from a DESIGN.md file."
    )
    parser.add_argument(
        "input", type=Path, help="Path to the DESIGN.md (or compatible) file."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output HTML path. Defaults to <input-stem>-preview.html next to the input.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        return 1

    parsed = parse_design_md(args.input)
    html = render_html(parsed)

    output = args.output or args.input.with_name(f"{args.input.stem}-preview.html")
    output.write_text(html)

    print(f"wrote preview: {output}")
    counts = []
    if parsed.colors_by_group:
        total = sum(len(c) for c in parsed.colors_by_group.values())
        counts.append(f"{total} colors in {len(parsed.colors_by_group)} groups")
    if parsed.typography:
        counts.append(f"{len(parsed.typography)} type rows")
    if parsed.spacing:
        counts.append(f"{len(parsed.spacing)} spacing tokens")
    if parsed.radius:
        counts.append(f"{len(parsed.radius)} radius tokens")
    if parsed.shadows:
        counts.append(f"{len(parsed.shadows)} elevation tokens")
    if counts:
        print("  parsed: " + ", ".join(counts))
    else:
        print("  warning: no tokens parsed — check that the input matches the expected format")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
