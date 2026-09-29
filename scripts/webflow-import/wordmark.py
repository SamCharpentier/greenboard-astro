"""Stand-in logos: a partner's name set in Outfit and drawn as outlines.

Used only where the real logo file has not arrived yet, so every logo slot
(cards, partner pages, the logo field) works the same before and after. The
outlines need no font to render, so the file behaves like any other logo.
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT = Path(__file__).resolve().parents[2] / "src/assets/fonts/outfit-variable.woff2"
COLOR = "#003738"  # midnight-800, the text color of the light themes
_font = None


def _load():
    global _font
    if _font is None:
        _font = instantiateVariableFont(TTFont(FONT), {"wght": 600})
    return _font


def _lines(name, limit=14):
    """Long names break onto two lines near the middle, so the mark stays compact."""
    if len(name) <= limit or " " not in name:
        return [name]
    words = name.split(" ")
    best = min(
        range(1, len(words)),
        key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))),
    )
    return [" ".join(words[:best]), " ".join(words[best:])]


def wordmark_svg(name):
    font = _load()
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    ascent = font["hhea"].ascent
    line = round(upm * 1.1)
    rows = [[cmap.get(ord(c)) or cmap[ord("?")] for c in text] for text in _lines(name)]
    widths = [sum(glyphs[g].width for g in row) for row in rows]
    width = max(widths)
    paths = []
    bounds = BoundsPen(glyphs)
    for index, row in enumerate(rows):
        x = (width - widths[index]) / 2
        baseline = ascent + index * line
        for glyph in row:
            pen = SVGPathPen(glyphs)
            transform = (1, 0, 0, -1, x, baseline)
            glyphs[glyph].draw(TransformPen(pen, transform))
            glyphs[glyph].draw(TransformPen(bounds, transform))
            if pen.getCommands():
                paths.append(pen.getCommands())
            x += glyphs[glyph].width
    # The box hugs the letters, so the mark is sized by its ink like a real logo
    left, top, right, bottom = (round(v) for v in bounds.bounds)
    width, height = right - left, bottom - top
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left} {top} {width} {height}" '
        f'width="{round(width / 10)}" height="{round(height / 10)}">'
        f'<path fill="{COLOR}" d="{" ".join(paths)}"/></svg>\n'
    )
