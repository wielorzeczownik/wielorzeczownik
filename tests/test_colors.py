from __future__ import annotations

import colorsys
from typing import TYPE_CHECKING

import pytest

from neocard.colors import clamp_lightness, hex_to_rgb, language_color
from neocard.constants import DARK, LIGHT

if TYPE_CHECKING:
    from neocard.models import Theme

THEMES = [DARK, LIGHT]


def _value(hex_color: str) -> float:
    red, green, blue = hex_to_rgb(hex_color)
    return colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)[2]


def _hue(hex_color: str) -> float:
    red, green, blue = hex_to_rgb(hex_color)
    return colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)[0]


@pytest.mark.parametrize("value", ["#ff0000", "ff0000", "#FF0000"])
def test_hex_to_rgb_accepts_the_forms_the_tables_use(value: str) -> None:
    assert hex_to_rgb(value) == (255, 0, 0)


@pytest.mark.parametrize(
    "hex_color", ["#000000", "#ffffff", "#3572a5", "#8b949e"]
)
@pytest.mark.parametrize("theme", THEMES)
def test_clamp_lightness_lands_inside_the_theme_window(
    hex_color: str, theme: Theme
) -> None:
    """A colour outside the window is what makes text unreadable on the bg."""
    clamped = clamp_lightness(hex_color, theme.v_floor, theme.v_ceil, theme.sat)
    tolerance = 1 / 255
    assert (
        theme.v_floor - tolerance
        <= _value(clamped)
        <= (theme.v_ceil + tolerance)
    )


@pytest.mark.parametrize("theme", THEMES)
def test_clamp_lightness_keeps_the_hue(theme: Theme) -> None:
    """Clamping brightness must not turn one language's colour into another."""
    source = "#3572a5"
    clamped = clamp_lightness(source, theme.v_floor, theme.v_ceil, theme.sat)
    assert _hue(clamped) == pytest.approx(_hue(source), abs=0.01)


@pytest.mark.parametrize("theme", THEMES)
def test_language_color_falls_back_for_an_unknown_language(
    theme: Theme,
) -> None:
    unknown = language_color("Not A Real Language", theme)
    assert unknown == language_color("Другой", theme)
    assert unknown.startswith("#")
    assert len(unknown) == 7
