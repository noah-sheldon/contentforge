#!/usr/bin/env python3
"""Static audit: does any timed text element overlap the pip region during its window?"""
import argparse
import re
from pathlib import Path

parser = argparse.ArgumentParser(description="Audit timed text vs pip-region collisions")
parser.add_argument("mcp_dir", type=Path, help="MCP docs project root (contains project/ and project-short/)")
args = parser.parse_args()
MCP = args.mcp_dir

CASES = [
    ("LANDSCAPE", MCP / "project" / "index.html", 1920, 1080,
     # pip region (420px circle at right:80, bottom:70 -> square bbox)
     (1920 - 80 - 420, 1080 - 70 - 420, 1920 - 80, 1080 - 70),
     {"#walkCap1", "#walkCap2", "#term-window", "#json-card", ".scard", "#demo-strip", "#s60-stage", "#chipA-stage", "#cta-stage"}),
    ("SHORT", MCP / "project-short" / "index.html", 1080, 1920,
     # pip 320 at left:60, bottom:80
     (60, 1920 - 80 - 320, 60 + 320, 1920 - 80),
     {"#walkCap1", "#walkCap2", "#term-window", "#json-card", ".scard", "#demo-strip", "#s60-stage", "#chipA-stage", "#cta-stage"}),
]


def parse_clip(html, name, sel):
    """Return (start, end) for the first element matching name+sel, or None."""
    # find any tag containing the id
    m = re.search(r'<[^>]*\bid="' + re.escape(sel.lstrip("#")) + r'"[^>]*>', html)
    if not m:
        return None
    tag = m.group(0)
    ds = re.search(r'data-start="([\d.]+)"', tag)
    dd = re.search(r'data-duration="([\d.]+)"', tag)
    if not ds or not dd:
        return None
    return float(ds.group(1)), float(ds.group(1)) + float(dd.group(1))


def region_of(sel, W, H, name):
    """Approx region for known elements (from CSS/inline layout)."""
    # returns (x0, y0, x1, y1) or None
    R = {
        "#walkCap1": (90, 1080 - 84 - 90, 90 + 700, 1080 - 84),      # bottom-left caption
        "#walkCap2": (90, 1080 - 84 - 90, 90 + 700, 1080 - 84),
        "#term-window": (340, 160, 340 + 1240, 160 + 335),           # centered 1240 wide
        "#json-card": (430, 170, 430 + 940, 170 + 640),              # shifted left
        ".scard": (275, 280, 1645, 280 + 300),                       # split cards at top:280
        "#demo-strip": (90, 1080 - 70 - 170, 90 + 1210, 1080 - 70),  # left 90 right 620
        "#s60-stage": (0, 300, 1920, 600),                           # centered big num
        "#chipA-stage": (0, 300, 1920, 650),
        "#cta-stage": (0, 400, 1920, 700),
    }
    if name == "div":
        return None
    return R.get(sel)


def audit():
    for label, path, W, H, pip, sels in CASES:
        html = path.read_text()
        px0, py0, px1, py1 = pip
        # parse the pip's live window from the file
        m = re.search(r'<[^>]*\bid="pip"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"', html)
        pip_s, pip_dur = (float(m.group(1)), float(m.group(2))) if m else (20.7, 62.5)
        pip_e = pip_s + pip_dur
        print(f"=== {label} (pip bbox {pip}, live {pip_s:.1f}-{pip_e:.1f}s) ===")
        issues = 0
        for sel in sorted(sels):
            tag = sel.lstrip("#")
            m = re.search(r'<[^>]*\bid="' + re.escape(tag) + r'"[^>]*>', html)
            if not m:
                continue
            ds = re.search(r'data-start="([\d.]+)"', m.group(0))
            dd = re.search(r'data-duration="([\d.]+)"', m.group(0))
            if not ds or not dd:
                continue
            s, e = float(ds.group(1)), float(ds.group(1)) + float(dd.group(1))
            # skip full-screen layers (by design, pip overlays them)
            if tag in ("walk", "demo"):
                continue
            r = region_of(sel, W, H, "div")
            if r is None:
                continue
            x0, y0, x1, y1 = r
            overlap = not (x1 <= px0 or x0 >= px1 or y1 <= py0 or y0 >= py1)
            window_overlap = s < pip_e and e > pip_s
            if overlap and window_overlap:
                print(f"  COLLISION {sel}: window {s:.1f}-{e:.1f}s region {r} vs pip {pip}")
                issues += 1
        print(f"  -> {issues} collision(s)" if issues else "  -> clean")


if __name__ == "__main__":
    audit()
