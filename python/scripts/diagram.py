#!/usr/bin/env python3
"""Generate a valid .excalidraw file from a simple JSON spec.

Spec file:
{
  "title": "doc-split",
  "elements": [
    {"type": "text",      "x": 100, "y": 50,  "w": 300, "h": 40, "text": "RAG pipeline"},
    {"type": "rectangle", "x": 100, "y": 100, "w": 200, "h": 80, "text": "Embed", "fill": "#a5d8ff"},
    {"type": "ellipse",   "x": 400, "y": 100, "w": 160, "h": 80, "text": "Vector DB", "fill": "#ffc9c9"},
    {"type": "arrow",     "x1": 300, "y1": 140, "x2": 400, "y2": 140},
    {"type": "line",      "x1": 100, "y1": 220, "x2": 560, "y2": 220}
  ]
}

Usage:
  python3 scripts/diagram.py spec.json -o workspace/long-form/<date>/<video>/03_diagrams/diagram.excalidraw
"""
import argparse
import hashlib
import json
from pathlib import Path


def _seed(t):
    return int(hashlib.md5(t.encode()).hexdigest()[:8], 16)


def _ver(t):
    return _seed(t) & 0xFFFF


def _common(spec, uid, text):
    x, y = spec.get("x", 0), spec.get("y", 0)
    w, h = spec.get("w", 200), spec.get("h", 100)
    return {
        "id": uid,
        "type": spec.get("type", "rectangle"),
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": spec.get("stroke", "#1e1e1e"),
        "backgroundColor": spec.get("fill", "transparent"),
        "fillStyle": "solid" if spec.get("fill") else "hachure",
        "strokeWidth": spec.get("strokeWidth", 2),
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": _seed(uid + text),
        "version": _ver(uid + text),
        "versionNonce": _ver(uid + text + str(x)),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "customData": {"content-planner": True},
    }


def build_element(spec, uid):
    t = spec.get("type", "rectangle")
    text = spec.get("text", "")
    el = _common(spec, uid, text)

    if t in ("rectangle", "ellipse"):
        el["roundness"] = {"type": 3} if t == "rectangle" else {"type": 2}
        if text:
            el["boundElements"] = [{"id": f"{uid}-t", "type": "text"}]
        return [el, _text_el(spec, f"{uid}-t", text, uid)]

    if t == "text":
        el.update({
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": None,
            "originalText": text,
            "fontSize": spec.get("fontSize", 28),
            "fontFamily": spec.get("fontFamily", 1),
            "text": text,
        })
        return [el]

    if t == "arrow":
        x2, y2 = spec.get("x2", spec.get("x", 0) + spec.get("w", 200)), \
                 spec.get("y2", spec.get("y", 0) + spec.get("h", 100))
        el.update({
            "points": [[0, 0], [x2 - spec.get("x", 0), y2 - spec.get("y", 0)]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": spec.get("endArrowhead", "arrow"),
        })
        return [el]

    if t == "line":
        x2 = spec.get("x2", spec.get("x", 0) + spec.get("w", 200))
        y2 = spec.get("y2", spec.get("y", 0) + spec.get("h", 100))
        el.update({
            "points": [[0, 0], [x2 - spec.get("x", 0), y2 - spec.get("y", 0)]],
            "lastCommittedPoint": None,
        })
        return [el]

    raise ValueError(f"unknown element type: {t}")


def _text_el(shape_spec, uid, text, container_id):
    x = shape_spec.get("x", 0)
    y = shape_spec.get("y", 0)
    w = shape_spec.get("w", 200)
    h = shape_spec.get("h", 100)
    el = _common({"type": "text", "x": x + w / 2 - w / 2, "y": y + h / 2 - 14,
                  "w": w, "h": 28, "fontSize": shape_spec.get("fontSize", 20)},
                 uid, text)
    el.update({
        "type": "text",
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": container_id,
        "originalText": text,
        "fontSize": shape_spec.get("fontSize", 20),
        "fontFamily": 1,
        "text": text,
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
    })
    return el


def build(spec):
    elements = []
    for i, s in enumerate(spec.get("elements", [])):
        elements.extend(build_element(s, f"el-{i}"))
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": spec.get("background", "#ffffff"),
        },
        "files": {},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="path to spec JSON")
    ap.add_argument("-o", "--output", default="diagram_base.excalidraw")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build(spec), indent=1), encoding="utf-8")
    print(f"wrote {out} ({len(spec.get('elements', []))} elements)")


if __name__ == "__main__":
    main()
