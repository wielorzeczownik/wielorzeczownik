from __future__ import annotations

import io
from typing import TYPE_CHECKING, cast

from PIL import Image, ImageEnhance, ImageOps

from .colors import clamp_lightness, hex_to_rgb
from .constants import PORTRAIT_COLORS

if TYPE_CHECKING:
    from .models import Theme

Grid = list[list[str]]


def build_pixels(avatar: bytes, theme: Theme, cols: int, rows: int) -> Grid:
    """Render the avatar as a cols by rows grid of hex colors"""
    img = ImageEnhance.Color(
        Image.open(io.BytesIO(avatar)).convert("RGB")
    ).enhance(1.4)
    # object-fit
    img = ImageOps.fit(img, (cols, rows), centering=(0.5, 0.5))
    pixels = img.load()
    if pixels is None:  # Pillow always returns an accessor for a loaded image
        raise RuntimeError("failed to load avatar pixels")
    grid: Grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            red, green, blue = cast("tuple[int, int, int]", pixels[x, y])
            hex_color = f"#{red:02x}{green:02x}{blue:02x}"
            row.append(
                clamp_lightness(
                    hex_color, theme.px_floor, theme.px_ceil, theme.sat
                )
            )
        grid.append(row)
    return grid


def encode_portrait(grid: Grid) -> bytes:
    """Pack the color grid into a lossless WebP, one image pixel per cell"""
    img = Image.new("RGB", (len(grid[0]), len(grid)))
    img.putdata([hex_to_rgb(color) for row in grid for color in row])
    snapped = img.quantize(
        colors=PORTRAIT_COLORS,
        method=Image.Quantize.FASTOCTREE,
        dither=Image.Dither.NONE,
    ).convert("RGB")
    buffer = io.BytesIO()
    snapped.save(buffer, "WEBP", lossless=True, quality=100, method=6)
    return buffer.getvalue()
