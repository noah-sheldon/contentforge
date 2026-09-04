#!/usr/bin/env python3
"""Remap HyperFrames composition timing through a tighten_video segment map.

Reads a map JSON (segments: [{old_start, old_end, new_start, new_end}]) and an
index.html, maps every GSAP timeline position (the trailing numeric arg before
");") and every data-duration / data-start through the old->new map, and
rewrites the file.

Usage:
    python scripts/remap_timeline.py <map.json> <index.html> [--origin OLD_W0] [--new-origin NEW_W0]
      --origin      for shorts: the old absolute slice start (times are relative to it)
      --new-origin  for shorts: the mapped slice start (subtracted from remapped times)
"""

import argparse
import json
import re


def load_map(path):
    with open(path) as f:
        return json.load(f)


def build_fn(m):
    segs = m["segments"]
    if not segs:
        return lambda t: t

    def f(t):
        if t <= segs[0]["old_start"]:
            return segs[0]["new_start"]
        if t >= segs[-1]["old_end"]:
            return segs[-1]["new_end"]
        for s in segs:
            if s["old_start"] <= t <= s["old_end"]:
                return s["new_start"] + (t - s["old_start"])
        # inside a cut region: map to the end of the previous kept segment
        prev = segs[0]
        for s in segs:
            if t < s["old_start"]:
                return prev["new_end"]
            prev = s
        return prev["new_end"]

    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map")
    ap.add_argument("html")
    ap.add_argument("--origin", type=float, default=0.0)
    ap.add_argument("--new-origin", type=float, default=None)
    args = ap.parse_args()

    m = load_map(args.map)
    f = build_fn(m)
    new_total = m["duration"]
    if args.new_origin is None:
        new_origin = f(args.origin)
    else:
        new_origin = args.new_origin

    with open(args.html) as fh:
        src = fh.read()

    def remap(t):
        return f(args.origin + t) - new_origin

    # 1. Timeline positions: ", NUM);" at statement ends.
    def pos_repl(mo):
        old = float(mo.group(1))
        new = remap(old)
        return f", {new:.3f});"

    src = re.sub(r",\s*([0-9]+\.[0-9]+)\);", pos_repl, src)

    # 2. data-start + data-duration pairs (duration is a LENGTH: map the span).
    def sd_repl(mo):
        s = float(mo.group(1))
        d = float(mo.group(2))
        ns = remap(s)
        nd = remap(s + d) - ns
        return f'data-start="{ns:.3f}" data-duration="{nd:.3f}"'

    src = re.sub(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', sd_repl, src)

    # 3. Any remaining bare data-duration (root/composition total).
    def dur_repl(mo):
        old = float(mo.group(1))
        new = remap(old)
        return f'data-duration="{new:.3f}"'

    src = re.sub(r'data-duration="([0-9.]+)"', dur_repl, src)

    # 4. Progress bar tween duration = new total.
    src = re.sub(
        r'(tl\.fromTo\("#progress-line".*?duration: )[\d.]+', rf"\g<1>{new_total:.3f}", src
    )

    with open(args.html, "w") as fh:
        fh.write(src)

    print(
        f"remapped {args.html}: timeline positions through map; new total duration = {new_total:.2f}s"
    )


if __name__ == "__main__":
    main()
