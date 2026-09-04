#!/usr/bin/env python3
"""Measure the pip wrapper geometry in both compositions to verify it is a true circle."""

import argparse
import json

from playwright.sync_api import sync_playwright


def measure(path: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 2000, "height": 2000})
        page.goto(f"file://{path}", wait_until="load")
        page.wait_for_timeout(1500)
        result = page.evaluate(
            """() => {
                const el = document.getElementById('pip-anim');
                if (!el) return { error: 'no pip-anim' };
                const r = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                const v = document.getElementById('pip');
                const vr = v ? v.getBoundingClientRect() : null;
                return {
                    wrapper: { w: Math.round(r.width), h: Math.round(r.height), radius: cs.borderRadius, overflow: cs.overflow },
                    video: vr ? { w: Math.round(vr.width), h: Math.round(vr.height) } : null,
                    isSquare: Math.abs(r.width - r.height) < 1,
                };
            }"""
        )
        browser.close()
        return result


parser = argparse.ArgumentParser(description="Verify pip wrapper geometry is a true circle")
parser.add_argument("files", nargs="+", help="HTML composition files to measure")
args = parser.parse_args()

for f in args.files:
    print(f.split("/")[-2], "→", json.dumps(measure(f)))
