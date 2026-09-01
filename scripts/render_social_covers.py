#!/usr/bin/env python3
"""Render independent Editorial Life Notes cover layouts from one photo."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


SANS_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
KAI_FONT = (
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/"
    "54a2ad3dac6cac875ad675d7d273dc425010a877.asset/AssetData/Kaiti.ttc"
)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


def fit_photo(source: Image.Image, size: tuple[int, int], centering: tuple[float, float]) -> Image.Image:
    photo = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=centering)
    photo = ImageEnhance.Color(photo).enhance(0.86)
    photo = ImageEnhance.Contrast(photo).enhance(1.04)
    return photo


def right_vignette(image: Image.Image, start: float, opacity: int) -> Image.Image:
    width, height = image.size
    mask = Image.new("L", (width, 1))
    px = mask.load()
    start_x = int(width * start)
    for x in range(width):
        amount = max(0.0, min(1.0, (x - start_x) / max(1, width - start_x)))
        px[x, 0] = int(opacity * amount)
    mask = mask.resize((width, height)).filter(ImageFilter.GaussianBlur(max(8, width // 45)))
    shade = Image.new("RGBA", image.size, (10, 6, 3, 255))
    return Image.composite(shade, image.convert("RGBA"), mask)


def wrap(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and draw.textbbox((0, 0), candidate, font=text_font)[2] > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    box: tuple[int, int, int, int],
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    spacing: int,
) -> None:
    left, top, right, bottom = box
    heights = [draw.textbbox((0, 0), line, font=text_font)[3] for line in lines]
    total = sum(heights) + spacing * max(0, len(lines) - 1)
    y = top + max(0, (bottom - top - total) // 2)
    for line, height in zip(lines, heights):
        bounds = draw.textbbox((0, 0), line, font=text_font)
        x = left + (right - left - (bounds[2] - bounds[0])) // 2
        draw.text((x, y), line, font=text_font, fill=fill)
        y += height + spacing


def render_wide(source: Image.Image, lead: str, title: str, subtitle: str) -> Image.Image:
    canvas = fit_photo(source, (900, 383), (0.46, 0.39))
    canvas = right_vignette(canvas, 0.42, 120)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((345, 48, 900, 238), fill=(224, 142, 14, 178))
    lead_font = font(KAI_FONT, 24)
    title_font = font(SANS_FONT, 38, 2)
    subtitle_font = font(SANS_FONT, 20)
    draw_centered_lines(draw, wrap(draw, lead, lead_font, 500), (370, 70, 875, 126), lead_font, (255, 252, 244, 245), 3)
    draw_centered_lines(draw, wrap(draw, title, title_font, 500), (370, 125, 875, 220), title_font, (255, 255, 255, 255), 5)
    draw_centered_lines(draw, wrap(draw, subtitle, subtitle_font, 475), (385, 258, 875, 344), subtitle_font, (247, 239, 224, 245), 6)
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def render_square(source: Image.Image, lead: str, title: str, subtitle: str) -> Image.Image:
    canvas = fit_photo(source, (900, 900), (0.46, 0.50))
    canvas = right_vignette(canvas, 0.44, 125)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((360, 230, 900, 580), fill=(220, 139, 18, 178))
    lead_font = font(KAI_FONT, 31)
    title_font = font(SANS_FONT, 53, 2)
    subtitle_font = font(SANS_FONT, 27)
    draw_centered_lines(draw, wrap(draw, lead, lead_font, 475), (390, 270, 865, 370), lead_font, (255, 252, 244, 245), 6)
    draw_centered_lines(draw, wrap(draw, title, title_font, 470), (390, 375, 865, 545), title_font, (255, 255, 255, 255), 8)
    draw_centered_lines(draw, wrap(draw, subtitle, subtitle_font, 440), (415, 635, 865, 745), subtitle_font, (247, 239, 224, 245), 8)
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def render_portrait(source: Image.Image, lead: str, title: str, subtitle: str) -> Image.Image:
    canvas = fit_photo(source, (1080, 1440), (0.43, 0.50))
    dark = Image.new("RGBA", canvas.size, (8, 5, 3, 45))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), dark)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 610, 1080, 1005), fill=(220, 139, 18, 182))
    lead_font = font(KAI_FONT, 38)
    title_font = font(SANS_FONT, 68, 2)
    subtitle_font = font(SANS_FONT, 34)
    draw_centered_lines(draw, wrap(draw, lead, lead_font, 900), (90, 660, 990, 770), lead_font, (255, 252, 244, 248), 7)
    draw_centered_lines(draw, wrap(draw, title, title_font, 900), (90, 775, 990, 955), title_font, (255, 255, 255, 255), 10)
    draw.rectangle((0, 1005, 1080, 1260), fill=(18, 11, 6, 120))
    draw_centered_lines(draw, wrap(draw, subtitle, subtitle_font, 820), (130, 1050, 950, 1205), subtitle_font, (247, 239, 224, 248), 10)
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--lead", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(args.source).convert("RGB")
    source.resize((1440, 1440), Image.Resampling.LANCZOS).save(args.output_dir / "cover-master-1440.png", quality=95)
    render_portrait(source, args.lead, args.title, args.subtitle).save(args.output_dir / "cover-xiaohongshu.png", quality=95)
    render_wide(source, args.lead, args.title, args.subtitle).save(args.output_dir / "cover-wechat-wide.png", quality=95)
    render_square(source, args.lead, args.title, args.subtitle).save(args.output_dir / "cover-wechat-square.png", quality=95)


if __name__ == "__main__":
    main()
