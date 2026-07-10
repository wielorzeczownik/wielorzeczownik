from __future__ import annotations

import colorsys
from typing import TYPE_CHECKING

from .constants import LANG_COLORS, LANG_FALLBACK

if TYPE_CHECKING:
    from .models import Theme


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(r: float, g: float, b: float) -> str:
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def clamp_lightness(
    hex_color: str, floor: float, ceil: float, sat: float
) -> str:
    """Keep hue but clamp HSV value into [floor, ceil] and scale saturation"""
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    v = max(min(v, ceil), floor)
    s = min(s * sat, 1.0)
    red, green, blue = colorsys.hsv_to_rgb(h, s, v)
    return rgb_to_hex(red * 255, green * 255, blue * 255)


def language_color(name: str, theme: Theme) -> str:
    """Brand color for a language, clamped to read on the theme background"""
    base = LANG_COLORS.get(name, LANG_FALLBACK)
    return clamp_lightness(base, theme.v_floor, theme.v_ceil, theme.sat)
