from __future__ import annotations

import base64
import io
import re
from functools import lru_cache
from importlib.resources import files
from typing import TYPE_CHECKING

import svgwrite
from fontTools import subset
from fontTools.ttLib import TTFont
from svgwrite.animate import Animate
from svgwrite.text import TSpan

from .avatar import Grid, build_pixels
from .constants import (
    CANVAS_WIDTH,
    FONT_SIZE,
    LINE_HEIGHT,
    PIXEL_COLS,
    PIXEL_SIZE,
    PIXEL_X,
)
from .panel import build_panel

if TYPE_CHECKING:
    from svgwrite.drawing import Drawing

    from .models import Profile, Settings, Theme

PORTRAIT_TOP = 16
PORTRAIT_BOTTOM_GAP = LINE_HEIGHT + 12  # clearance above the terminal line
FOOTER_GAP = 2 * LINE_HEIGHT
BOTTOM_MARGIN = 20
RULE_CELLS = 103

LORE_PID = """<!--
     $ ps -p 0
       PID  PPID  START   CMD
         0     0  1945    [eniac]
     no parent. it started before init.
     PID 0 - do not kill.
-->"""
FONT_FAMILY = "JetBrainsMono"
FONT_STACK = f"'{FONT_FAMILY}', ui-monospace, SFMono-Regular, monospace"
FONT_FILE = "JetBrainsMonoNF.woff2"
BASE_CHARS = "".join(chr(c) for c in range(0x20, 0x7F)) + "─█●—∞·"


@lru_cache(maxsize=1)
def _source_font() -> bytes:
    return (files("neocard") / "assets" / FONT_FILE).read_bytes()


@lru_cache(maxsize=8)
def _font_face(charset: str) -> str:
    """Embed JetBrains Mono Nerd Font, subset to charset, as a base64 face"""
    font = TTFont(io.BytesIO(_source_font()))
    options = subset.Options(desubroutinize=True)
    options.flavor = "woff2"
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=[ord(c) for c in charset])
    subsetter.subset(font)
    buffer = io.BytesIO()
    font.save(buffer)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return (
        f"@font-face{{font-family:'{FONT_FAMILY}';font-display:swap;"
        f"src:url(data:font/woff2;base64,{encoded}) format('woff2');}}"
    )


def _charset(*elements: object) -> str:
    """Unique sorted characters used across the given SVG text elements"""
    text = "".join(
        re.sub(r"<[^>]+>", "", el.tostring())  # type: ignore[attr-defined]
        for el in elements
    )
    return "".join(sorted(set(BASE_CHARS) | set(text)))


def _stylesheet(theme: Theme, charset: str) -> str:
    return (
        f"{_font_face(charset)}"
        f".key{{fill:{theme.key};}}.value{{fill:{theme.value};}}"
        f".cc{{fill:{theme.cc};}}text,tspan{{white-space:pre;}}"
    )


def _avatar_group(dwg: Drawing, grid: Grid, top: int) -> object:
    """Emit the pixel grid as rects, run-length-merging equal colors per row"""
    group = dwg.g(shape_rendering="crispEdges")
    for j, row in enumerate(grid):
        y = top + j * PIXEL_SIZE
        x = 0
        while x < len(row):
            color = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == color:
                run += 1
            group.add(
                dwg.rect(
                    (PIXEL_X + x * PIXEL_SIZE, y),
                    (run * PIXEL_SIZE, PIXEL_SIZE),
                    fill=color,
                )
            )
            x += run
    return group


def _blinking_cursor() -> TSpan:
    cursor = TSpan("█", class_="key")
    cursor.add(
        Animate(
            attributeName="fill-opacity",
            values="1;1;0;0",
            keyTimes="0;0.5;0.5;1",
            dur="1.06s",
            repeatCount="indefinite",
        )
    )
    return cursor


def _footer(
    dwg: Drawing, profile: Profile, theme: Theme, footer_y: int
) -> list[object]:
    """A full-width terminal prompt line with a blinking cursor"""
    rule = dwg.text(
        "─" * RULE_CELLS, insert=(15, footer_y - LINE_HEIGHT), fill=theme.cc
    )
    prompt = dwg.text("", insert=(15, footer_y), fill=theme.fg)
    for child in (
        TSpan("visitor@", class_="cc"),
        TSpan(profile.user, class_="key"),
        TSpan(":", class_="cc"),
        TSpan("~", class_="value"),
        TSpan("$ ", class_="cc"),
        _blinking_cursor(),
    ):
        prompt.add(child)
    return [rule, prompt]


def render(profile: Profile, theme: Theme, settings: Settings) -> str:
    """Render one themed card to an SVG string"""
    panel, last_y = build_panel(profile, theme, settings)
    footer_y = last_y + FOOTER_GAP
    height = footer_y + BOTTOM_MARGIN

    portrait_bottom = footer_y - PORTRAIT_BOTTOM_GAP
    rows = (portrait_bottom - PORTRAIT_TOP) // PIXEL_SIZE
    grid = build_pixels(profile.avatar, theme, PIXEL_COLS, rows)

    dwg = svgwrite.Drawing(size=(f"{CANVAS_WIDTH}px", f"{height}px"))
    dwg["font-family"] = FONT_STACK
    dwg["font-size"] = f"{FONT_SIZE}px"
    footer = _footer(dwg, profile, theme, footer_y)
    dwg.defs.add(dwg.style(_stylesheet(theme, _charset(panel, *footer))))
    dwg.add(
        dwg.rect(
            (0, 0), (f"{CANVAS_WIDTH}px", f"{height}px"), fill=theme.bg, rx=15
        )
    )
    dwg.add(_avatar_group(dwg, grid, PORTRAIT_TOP))
    dwg.add(panel)
    for element in footer:
        dwg.add(element)
    document: str = dwg.tostring()
    # Tuck the hidden lore
    return document.replace("</svg>", f"{LORE_PID}</svg>", 1)
