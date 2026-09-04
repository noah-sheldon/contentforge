#!/usr/bin/env python3
"""Generate long-form (1280x720) and short-form (1080x1920) thumbnails.

Uses the canonical headshot (assets/noah-headshot.png), circular crop + gold
ring, bold gold title + server chips on a dark gradient — same visual language
as the round pip.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HEADSHOT = ROOT / "assets" / "noah-headshot.png"
OUT_LONG = ROOT / "assets" / "thumbnails" / "mcp-docs-thumb-16x9.png"
OUT_SHORT = ROOT / "assets" / "thumbnails" / "mcp-docs-thumb-9x16.png"

GOLD = (212, 175, 55, 255)
WHITE = (242, 245, 248, 255)
DIM = (174, 185, 196, 255)

# Cross-platform font resolution (audit A5). P0: remove macOS-only paths so
# thumbnails render on the Linux VM; P1.5 formalizes the font policy and
# bundles the brand fonts (Inter/Playfair/JetBrains Mono) by family name.
_FONT_DIRS = {
    "linux": [Path("/usr/share/fonts/truetype/dejavu")],
    "darwin": [
        Path("/System") / "Library" / "Fonts" / "Supplemental",
        Path("/Library") / "Fonts",
    ],
    "win32": [Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"],
}
_FONT_FILES = {
    True: ["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
    False: ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf"],
}


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    override = os.environ.get("CONTENTFORGE_FONT")
    candidates = [Path(override)] if override else []
    for directory in _FONT_DIRS.get(sys.platform, []):
        for name in _FONT_FILES[bold]:
            candidates.append(directory / name)
    for cand in candidates:
        if cand.is_file():
            try:
                return ImageFont.truetype(str(cand), size)
            except Exception:
                continue
    return ImageFont.load_default()


def dark_gradient(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    top = (11, 17, 25)
    bottom = (13, 10, 16)
    for y in range(h):
        t = y / max(1, h - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=color)
    return img


def circular_headshot(bg: Image.Image, cx: int, cy: int, diameter: int) -> None:
    """Face-centered square crop (no distortion) + circular crop + gold ring."""
    hs = Image.open(HEADSHOT).convert("RGB")
    w, h = hs.size
    # Face center in the navy photo (Vision detection, top-left origin): (0.514, 0.481)
    fc_x = int(w * 0.514)
    fc_y = int(h * 0.481)
    side = int(w * 0.80)  # square crop side — face + headroom, fits 872x1216 portrait
    left = max(0, min(w - side, fc_x - side // 2))
    top = max(0, min(h - side, fc_y - side // 2))
    sq = hs.crop((left, top, left + side, top + side)).resize(
        (diameter, diameter), Image.Resampling.LANCZOS
    )
    mask = Image.new("L", (diameter, diameter), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    bg.paste(sq, (cx - diameter // 2, cy - diameter // 2), mask)
    ring = ImageDraw.Draw(bg)
    ring_w = max(4, diameter // 90)
    ring.ellipse(
        (cx - diameter // 2, cy - diameter // 2, cx + diameter // 2, cy + diameter // 2),
        outline=GOLD,
        width=ring_w,
    )


def text_center(
    d: ImageDraw.ImageDraw, cx: int, y: int, txt: str, fnt, fill, anchor="ma", stroke: int = 0
) -> None:
    d.text(
        (cx, y),
        txt,
        font=fnt,
        fill=fill,
        anchor=anchor,
        stroke_width=stroke,
        stroke_fill=(10, 14, 19),
    )


def chip(d: ImageDraw.ImageDraw, cx: int, y: int, txt: str, fnt) -> None:
    bbox = d.textbbox((0, 0), txt, font=fnt)
    w = bbox[2] - bbox[0] + 48
    h = bbox[3] - bbox[1] + 28
    x0, y0 = cx - w // 2, y - h // 2
    d.rounded_rectangle(
        [x0, y0, x0 + w, y0 + h], radius=h // 2, outline=GOLD, width=3, fill=(17, 24, 35, 255)
    )
    d.text((cx, y), txt, font=fnt, fill=WHITE, anchor="mm")


def build_long() -> None:
    W, H = 1280, 720
    img = dark_gradient(W, H)
    d = ImageDraw.Draw(img)
    f_t1 = font(58)
    f_t2 = font(92)
    f_sub = font(30)
    f_chip = font(26)
    # headshot left
    circular_headshot(img, 300, H // 2, 430)
    # title right
    tx = 640
    sw = 8
    text_center(d, tx, 210, "STOP HALLUCINATING", f_t1, WHITE, stroke=sw)
    text_center(d, tx, 310, "LANGCHAIN", f_t2, GOLD, stroke=sw)
    text_center(d, tx, 420, "Official MCP Servers — connect in 60 seconds", f_sub, DIM, stroke=5)
    chip(d, tx, 530, "docs-langchain  ·  reference-langchain", f_chip)
    os.makedirs(os.path.dirname(OUT_LONG), exist_ok=True)
    img.save(OUT_LONG)
    print("saved", OUT_LONG)


def build_short() -> None:
    W, H = 1080, 1920
    img = dark_gradient(W, H)
    d = ImageDraw.Draw(img)
    f_t1 = font(78)
    f_t2 = font(122)
    f_sub = font(40)
    f_chip = font(34)
    circular_headshot(img, W // 2, 600, 620)
    sw = 10
    text_center(d, W // 2, 940, "STOP HALLUCINATING", f_t1, WHITE, stroke=sw)
    text_center(d, W // 2, 1090, "LANGCHAIN", f_t2, GOLD, stroke=sw)
    text_center(d, W // 2, 1260, "Official MCP Servers", f_sub, DIM, stroke=6)
    text_center(d, W // 2, 1320, "connect in 60 seconds", f_sub, DIM, stroke=6)
    chip(d, W // 2, 1480, "docs-langchain  ·  reference-langchain", f_chip)
    os.makedirs(os.path.dirname(OUT_SHORT), exist_ok=True)
    img.save(OUT_SHORT)
    print("saved", OUT_SHORT)


if __name__ == "__main__":
    build_long()
    build_short()
