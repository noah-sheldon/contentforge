#!/usr/bin/env python3
"""Fetch a single weight of a Google Font as woff2 (latin subset).

Usage: python3 scripts/fetch_font.py "Space Grotesk" 900 out.woff2
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")


def main():
    family, weight, out = sys.argv[1], sys.argv[2], sys.argv[3]
    fam = family.replace(" ", "+")
    url = f"https://fonts.googleapis.com/css2?family={fam}:wght@{weight}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    # split into @font-face blocks, keep the last (latin) per matching weight
    blocks = re.findall(r"@font-face\s*{([^}]*)}", css)
    picked = None
    for b in blocks:
        w = re.search(r"font-weight:\s*(\d+)", b)
        u = re.search(r"url\(([^)]+)\) format\('woff2'\)", b)
        if w and u and w.group(1) == weight:
            picked = u.group(1)
    if not picked:
        sys.exit(f"no woff2 for {family} {weight}")
    data = urllib.request.urlopen(picked, timeout=30).read()
    with open(out, "wb") as f:
        f.write(data)
    print(f"{out}: {len(data)} bytes ({family} {weight})")


if __name__ == "__main__":
    main()
