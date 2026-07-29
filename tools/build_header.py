#!/usr/bin/env python3
"""
Builds the profile header and status marks in assets/.

Why a script: GitHub serves README images through a proxy, so a web font named
inside an SVG never loads and the header would fall back to whatever the reader
has installed. Every glyph here is converted to a path instead, which means the
artwork cannot be edited by hand — change the settings below and re-run.

    pip install fonttools
    python3 tools/build_header.py

Fonts are fetched once into tools/.fonts/ (ignored by git). They are the same
three faces husodrn46.com uses, so the two stay one identity.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

# ─── Settings ────────────────────────────────────────────────────────────────
# Edit these, re-run, commit the changed SVGs.

EYEBROW = "PERSONAL SPEC SHEET · H.D / 2026"
STATUS = "ISTANBUL"
SENTENCE = [
    "I like understanding how things work,",
    "then making them better.",
]
NAME = "Hüseyin Durna"
ROLE = "IT INFRASTRUCTURE · SOFTWARE · ISTANBUL"

# The site's two faces. `rule_dashed` is the printed one: drawings rule in dashes.
FACES = {
    "live": dict(
        ground="#0f1519", line="#e6e9e8", graphite="#98a2a6",
        amber="#ffb400", green="#35d07f", rule_opacity=".30", rule_dashed=False,
    ),
    "sheet": dict(
        ground="#e9e7e1", line="#16181a", graphite="#5b5f5d",
        amber="#c98f00", green="#0e6b4e", rule_opacity=".45", rule_dashed=True,
    ),
}

# Status squares, matching the chips on the site.
MARKS = {
    "running": '<rect width="12" height="12" fill="#35d07f"/>',
    "building": '<rect width="12" height="12" fill="#ffb400"/>',
    "past": '<rect width="12" height="12" fill="#8b9297"/>',
    "variable": '<rect x="1" y="1" width="10" height="10" fill="none" '
                'stroke="#8b9297" stroke-width="1.5"/>',
}

WIDTH, HEIGHT, MARGIN = 1200, 316, 58

FONTS = {
    "hand": ("Caveat.ttf", {"wght": 600},
             "https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%5Bwght%5D.ttf"),
    "display": ("Archivo.ttf", {"wght": 620, "wdth": 102},
                "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf"),
    "mono": ("IBMPlexMono.ttf", None,
             "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf"),
}

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(__file__).resolve().parent / ".fonts"
ASSETS = ROOT / "assets"

# ─── Type ────────────────────────────────────────────────────────────────────

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    from fontTools.varLib.instancer import instantiateVariableFont
except ImportError:
    sys.exit("fontTools is missing. Install it with: pip install fonttools")


class Face:
    """One font at one instance, able to draw text as an SVG path."""

    def __init__(self, path: Path, variations: dict | None):
        font = TTFont(path)
        if variations and "fvar" in font:
            font = instantiateVariableFont(font, variations, inplace=False)
        self.font = font
        self.upem = font["head"].unitsPerEm
        self.cmap = font.getBestCmap()
        self.glyphs = font.getGlyphSet()
        self.hmtx = font["hmtx"]

    def _glyph(self, ch: str):
        return self.cmap.get(ord(ch)) or self.cmap.get(ord(" "))

    def width(self, text: str, size: float) -> float:
        return sum(self.hmtx[self._glyph(c)][0] for c in text) * size / self.upem

    def path(self, text: str, size: float, x: float, y: float) -> tuple[str, float]:
        """Path data for `text` sitting on the baseline at (x, y)."""
        scale = size / self.upem
        parts, cursor = [], 0.0
        for ch in text:
            name = self._glyph(ch)
            if name is None:
                continue
            pen = SVGPathPen(self.glyphs, ntos=lambda v: str(int(round(v))))
            # SVG's y axis points down, so the scale is negated.
            self.glyphs[name].draw(
                TransformPen(pen, Transform(scale, 0, 0, -scale, x + cursor, y))
            )
            if data := pen.getCommands():
                parts.append(data)
            cursor += self.hmtx[name][0] * scale
        return " ".join(parts), cursor

    def tracked(self, text: str, size: float, x: float, y: float, track: float):
        """Letter-spaced run — the mono labels need air to read as labels."""
        parts, cursor = [], x
        for ch in text:
            data, advance = self.path(ch, size, cursor, y)
            if data:
                parts.append(data)
            cursor += advance + track
        return " ".join(parts), cursor - x - track


def load_faces() -> dict[str, Face]:
    FONT_DIR.mkdir(exist_ok=True)
    faces = {}
    for role, (filename, variations, url) in FONTS.items():
        target = FONT_DIR / filename
        if not target.exists():
            print(f"  fetching {filename}")
            urllib.request.urlretrieve(url, target)
        faces[role] = Face(target, variations)
    return faces


# ─── Drawing ─────────────────────────────────────────────────────────────────

def build_header(faces: dict[str, Face], face: dict) -> str:
    hand, display, mono = faces["hand"], faces["display"], faces["mono"]
    parts = [f'<rect width="{WIDTH}" height="{HEIGHT}" rx="10" fill="{face["ground"]}"/>']

    # Registration marks — the sheet's only ornament.
    for cx, cy, dx, dy in (
        (22, 22, 1, 1), (WIDTH - 22, 22, -1, 1),
        (22, HEIGHT - 22, 1, -1), (WIDTH - 22, HEIGHT - 22, -1, -1),
    ):
        parts.append(
            f'<path d="M{cx} {cy}h{13 * dx}M{cx} {cy}v{13 * dy}" '
            f'stroke="{face["graphite"]}" stroke-opacity=".55" stroke-width="1" fill="none"/>'
        )

    data, _ = mono.tracked(EYEBROW, 16, MARGIN, 60, 2.0)
    parts.append(f'<path d="{data}" fill="{face["graphite"]}"/>')

    status_width = mono.width(STATUS, 16) + len(STATUS) * 2.0
    parts.append(
        f'<rect x="{WIDTH - MARGIN - status_width - 18:.0f}" y="52" '
        f'width="8" height="8" fill="{face["green"]}"/>'
    )
    data, _ = mono.tracked(STATUS, 16, WIDTH - MARGIN - status_width, 60, 2.0)
    parts.append(f'<path d="{data}" fill="{face["graphite"]}"/>')

    dashes = ' stroke-dasharray="5 5"' if face["rule_dashed"] else ""
    parts.append(
        f'<path d="M{MARGIN} 80H{WIDTH - MARGIN}" stroke="{face["graphite"]}" '
        f'stroke-opacity="{face["rule_opacity"]}" stroke-width="1"{dashes}/>'
    )

    for index, line in enumerate(SENTENCE):
        data, _ = hand.path(line, 46, MARGIN, 142 + index * 54)
        parts.append(f'<path d="{data}" fill="{face["line"]}"/>')

    parts.append(f'<rect x="{MARGIN}" y="224" width="64" height="3" fill="{face["amber"]}"/>')

    data, _ = display.path(NAME, 29, MARGIN, 268)
    parts.append(f'<path d="{data}" fill="{face["line"]}"/>')

    data, _ = mono.tracked(ROLE, 14, MARGIN, 294, 1.8)
    parts.append(f'<path d="{data}" fill="{face["amber"]}"/>')

    body = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="{NAME} — personal spec sheet">\n  {body}\n</svg>\n'
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    print("Loading fonts")
    faces = load_faces()

    print("Drawing headers")
    for name, face in FACES.items():
        target = ASSETS / f"header-{name}.svg"
        target.write_text(build_header(faces, face), encoding="utf-8")
        print(f"  assets/{target.name}  {target.stat().st_size // 1024} KiB")

    print("Drawing status marks")
    for name, shape in MARKS.items():
        target = ASSETS / f"dot-{name}.svg"
        target.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" '
            f'viewBox="0 0 12 12">{shape}</svg>\n',
            encoding="utf-8",
        )
        print(f"  assets/{target.name}")

    print("\nDone. Review the SVGs, then commit them.")


if __name__ == "__main__":
    main()
