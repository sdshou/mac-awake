#!/usr/bin/env python3
"""Generate icon.icns for mac-awake (coffee cup icon)."""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw

ICONSET_DIR = "mac-awake.iconset"
SIZES = [16, 32, 64, 128, 256, 512]


def draw_coffee_cup(size: int) -> Image.Image:
    """Draw a simple coffee cup icon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size  # shorthand
    pad = s * 0.1

    # Cup body (rounded rectangle)
    cup_left = pad + s * 0.05
    cup_top = s * 0.35
    cup_right = s * 0.7
    cup_bottom = s - pad
    r = s * 0.08  # corner radius
    draw.rounded_rectangle(
        [cup_left, cup_top, cup_right, cup_bottom],
        radius=r,
        fill="#6F4E37",  # coffee brown
    )

    # Coffee surface
    coffee_top = cup_top + s * 0.08
    draw.rounded_rectangle(
        [cup_left + s * 0.03, cup_top, cup_right - s * 0.03, coffee_top + s * 0.05],
        radius=r * 0.5,
        fill="#3E2723",  # dark coffee
    )

    # Handle (arc on the right side)
    handle_left = cup_right - s * 0.04
    handle_top = cup_top + s * 0.08
    handle_right = cup_right + s * 0.18
    handle_bottom = cup_bottom - s * 0.12
    # outer arc
    draw.ellipse(
        [handle_left, handle_top, handle_right, handle_bottom],
        fill="#6F4E37",
    )
    # inner arc (cut out)
    inset = s * 0.06
    draw.ellipse(
        [handle_left + inset * 0.3, handle_top + inset, handle_right - inset, handle_bottom - inset],
        fill=(0, 0, 0, 0),
    )

    # Steam wisps
    steam_color = (180, 180, 180, 180)
    for i, x_offset in enumerate([0.25, 0.40, 0.55]):
        x = cup_left + (cup_right - cup_left) * x_offset
        y_base = cup_top - s * 0.02
        wisp_w = s * 0.025
        for j in range(3):
            y = y_base - s * 0.06 * (j + 1)
            shift = s * 0.03 * (1 if (j + i) % 2 == 0 else -1)
            draw.ellipse(
                [x + shift - wisp_w, y - wisp_w * 1.5,
                 x + shift + wisp_w, y + wisp_w * 1.5],
                fill=steam_color,
            )

    return img


def main():
    # Clean up any previous iconset
    if os.path.exists(ICONSET_DIR):
        shutil.rmtree(ICONSET_DIR)
    os.makedirs(ICONSET_DIR)

    # Generate all required sizes
    for size in SIZES:
        icon = draw_coffee_cup(size)
        icon.save(os.path.join(ICONSET_DIR, f"icon_{size}x{size}.png"))
        # @2x variant (double resolution for Retina)
        icon_2x = draw_coffee_cup(size * 2)
        icon_2x.save(os.path.join(ICONSET_DIR, f"icon_{size}x{size}@2x.png"))

    # Convert to .icns using macOS iconutil
    subprocess.run(
        ["iconutil", "-c", "icns", ICONSET_DIR, "-o", "icon.icns"],
        check=True,
    )

    # Clean up iconset directory
    shutil.rmtree(ICONSET_DIR)
    print("Created icon.icns")


if __name__ == "__main__":
    main()
