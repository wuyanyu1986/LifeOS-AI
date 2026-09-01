#!/usr/bin/env python3
"""Render restrained Microsoft YaHei editorial covers for LifeOS entries."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


FONT_REGULAR = "/Applications/Microsoft Word.app/Contents/Resources/DFonts/msyh.ttc"
FONT_BOLD = "/Applications/Microsoft Word.app/Contents/Resources/DFonts/msyhbd.ttc"
PAPER = (244, 242, 236)
INK = (31, 31, 29)
GRAY = (105, 103, 98)
LIGHT = (205, 201, 191)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def fit_photo(source: Image.Image, size: tuple[int, int], centering=(0.62, 0.52)) -> Image.Image:
    photo = ImageOps.fit(source, size, Image.Resampling.LANCZOS, centering=centering)
    photo = ImageEnhance.Color(photo).enhance(0.78)
    photo = ImageEnhance.Contrast(photo).enhance(0.96)
    return photo


def text_width(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=text_font)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and text_width(draw, candidate, text_font) > width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    xy: tuple[int, int],
    text_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    spacing: int,
) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=text_font, fill=fill)
        box = draw.textbbox((x, y), line, font=text_font)
        y = box[3] + spacing
    return y


def draw_contours(draw: ImageDraw.ImageDraw, size: tuple[int, int], opacity_color=(218, 214, 204)) -> None:
    width, height = size
    for inset in range(0, 420, 56):
        draw.arc(
            (width - 360 - inset, -180 - inset, width + 300 + inset, 500 + inset),
            start=96,
            end=264,
            fill=opacity_color,
            width=2,
        )


def render_xiaohongshu(source: Image.Image, context: str, title: str, subtitle: str) -> Image.Image:
    canvas = Image.new("RGB", (1080, 1440), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_contours(draw, canvas.size)
    context_font = font(FONT_REGULAR, 27)
    title_font = font(FONT_BOLD, 70)
    subtitle_font = font(FONT_REGULAR, 29)
    draw.text((82, 82), "生活里  /  2026.08.28", font=font(FONT_REGULAR, 21), fill=GRAY)
    draw.line((82, 132, 998, 132), fill=LIGHT, width=2)
    draw.text((82, 180), context, font=context_font, fill=GRAY)
    title_lines = wrap(draw, title, title_font, 870)
    y = draw_lines(draw, title_lines, (82, 244), title_font, INK, 18)
    y += 24
    draw.line((82, y, 168, y), fill=INK, width=3)
    y += 30
    draw_lines(draw, wrap(draw, subtitle, subtitle_font, 890), (82, y), subtitle_font, GRAY, 12)
    photo = fit_photo(source, (916, 620), (0.64, 0.52))
    canvas.paste(photo, (82, 742))
    draw.rectangle((82, 742, 998, 1362), outline=(225, 222, 214), width=2)
    return canvas


def render_wide(source: Image.Image, context: str, short_title: str, subtitle: str) -> Image.Image:
    canvas = Image.new("RGB", (900, 383), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.text((46, 34), "生活里  /  2026.08.28", font=font(FONT_REGULAR, 16), fill=GRAY)
    draw.line((46, 69, 464, 69), fill=LIGHT, width=1)
    draw.text((46, 91), context, font=font(FONT_REGULAR, 19), fill=GRAY)
    title_font = font(FONT_BOLD, 47)
    y = draw_lines(draw, wrap(draw, short_title, title_font, 395), (46, 138), title_font, INK, 8)
    y += 11
    draw.line((46, y, 108, y), fill=INK, width=2)
    draw_lines(draw, wrap(draw, subtitle, font(FONT_REGULAR, 17), 395), (46, y + 17), font(FONT_REGULAR, 17), GRAY, 6)
    photo = fit_photo(source, (390, 383), (0.68, 0.52))
    canvas.paste(photo, (510, 0))
    draw.line((490, 30, 490, 353), fill=LIGHT, width=1)
    return canvas


def render_square(context: str, short_title: str, subtitle: str) -> Image.Image:
    canvas = Image.new("RGB", (900, 900), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_contours(draw, canvas.size, (222, 218, 208))
    draw.text((76, 66), "生活里  /  2026.08.28", font=font(FONT_REGULAR, 20), fill=GRAY)
    draw.line((76, 112, 824, 112), fill=LIGHT, width=2)
    draw.text((76, 170), context, font=font(FONT_REGULAR, 26), fill=GRAY)
    title_font = font(FONT_BOLD, 82)
    y = draw_lines(draw, wrap(draw, short_title, title_font, 680), (76, 252), title_font, INK, 18)
    y += 28
    draw.line((76, y, 168, y), fill=INK, width=3)
    y += 34
    draw_lines(draw, wrap(draw, subtitle, font(FONT_REGULAR, 29), 700), (76, y), font(FONT_REGULAR, 29), GRAY, 12)
    draw.line((76, 758, 824, 758), fill=LIGHT, width=2)
    draw.text((76, 793), "只要你回头，我还在身后。", font=font(FONT_REGULAR, 25), fill=INK)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--context", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--short-title", required=True)
    parser.add_argument("--subtitle", required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(args.source).convert("RGB")
    source.resize((1440, 1440), Image.Resampling.LANCZOS).save(args.output_dir / "cover-master-1440.png")
    render_xiaohongshu(source, args.context, args.title, args.subtitle).save(args.output_dir / "cover-xiaohongshu.png")
    render_wide(source, args.context, args.short_title, args.subtitle).save(args.output_dir / "cover-wechat-wide.png")
    render_square(args.context, args.short_title, args.subtitle).save(args.output_dir / "cover-wechat-square.png")


if __name__ == "__main__":
    main()
