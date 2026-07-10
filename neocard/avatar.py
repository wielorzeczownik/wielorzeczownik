from __future__ import annotations

import io
from typing import TYPE_CHECKING, cast

from PIL import Image, ImageEnhance, ImageOps

from .colors import clamp_lightness

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
