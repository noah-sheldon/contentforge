#!/usr/bin/env python3
"""Create GitHub Projects v2 draft cards and set their fields.

Usage:
  python3 scripts/board.py --project 7 --owner noah-sheldon items.json [--dry-run]

items.json:
[
  {"title": "Day 1 · Hook", "status": "To Do", "form": "Short",
   "series": "Build RAG from scratch", "week": "2026-08-10"}
]

Field mapping (resolved against the live board, not hardcoded):
  status -> Status single-select   form -> Form single-select
  series -> Series single-select   week -> Week iteration (matched by start date)
Unknown option names are warned and skipped, never fatal.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import CONFIG

FIELD_QUERY = """
query {
  node(id: "%s") {
    ... on ProjectV2 {
      fields(first: 50) {
        nodes {
          ... on ProjectV2SingleSelectField { id name options { id name } }
          ... on ProjectV2IterationField { id name configuration { iterations { id startDate } } }
        }
      }
    }
  }
}
"""

_BOARDS = CONFIG.get("boards", {})
_FIELDS = CONFIG.get("board_fields", {})


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[warn] gh failed: {' '.join(args)}\n{r.stderr.strip()[:300]}", file=sys.stderr)
        return None
    return r.stdout.strip()


def project_id(owner, number):
    out = run(["gh", "project", "view", number, "--owner", owner, "--format", "json"])
    if not out:
        return None
    return json.loads(out)["id"]


def field_map(project_id_val):
    """Return {field_name: {"id":..., "options": {name: id}, "iterations": {startDate: id}}}"""
    out = run(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            "query=" + FIELD_QUERY % project_id_val,
            "--jq",
            ".data.node.fields.nodes",
        ]
    )
    if not out:
        return {}
    nodes = json.loads(out)
    m = {}
    for n in nodes:
        name = n.get("name")
        if not name:
            continue
        entry = {"id": n.get("id")}
        if "options" in n:
            entry["options"] = {o["name"]: o["id"] for o in (n.get("options") or [])}
        if n.get("configuration"):
            entry["iterations"] = {
                i["startDate"]: i["id"] for i in n["configuration"].get("iterations") or []
            }
        m[name] = entry
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--project",
        default=str(_BOARDS.get("shorts", {}).get("number", "")),
        help="GitHub project number (default: config boards.shorts)",
    )
    ap.add_argument(
        "--owner", default=_BOARDS.get("shorts", {}).get("owner", ""), help="project owner"
    )
    ap.add_argument("items", help="JSON file with the card list")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    items = json.loads(Path(a.items).read_text(encoding="utf-8"))
    pid = project_id(a.owner, a.project)
    if not pid:
        sys.exit(f"cannot resolve project {a.project}")
    fields = field_map(pid)

    for it in items:
        base = [
            "gh",
            "project",
            "item-create",
            a.project,
            "--owner",
            a.owner,
            "--title",
            it["title"],
            "--format",
            "json",
        ]
        if a.dry_run:
            print("DRY:", " ".join(base))
            continue
        out = run(base)
        if not out:
            continue
        try:
            item_id = json.loads(out)["id"]
        except (json.JSONDecodeError, KeyError):
            print(f"[warn] cannot parse item id: {out[:200]}", file=sys.stderr)
            continue
        print(f"created {it['title']!r}")

        for key, fkey in (
            ("status", "status"),
            ("form", "form"),
            ("series", "series"),
            ("week", "week"),
        ):
            value = it.get(key)
            if not value:
                continue
            field_name = _FIELDS.get(fkey) or fkey.title()
            f = fields.get(field_name)
            if not f:
                print(f"[warn] no {field_name} field on project {a.project}")
                continue
            cmd = [
                "gh",
                "project",
                "item-edit",
                "--id",
                item_id,
                "--project-id",
                pid,
                "--field-id",
                f["id"],
                "--format",
                "json",
            ]
            if key == "week":
                iid = (f.get("iterations") or {}).get(value)
                if not iid:
                    print(f"[warn] no iteration starting {value} on {field_name}")
                    continue
                cmd += ["--iteration-id", iid]
            else:
                oid = (f.get("options") or {}).get(value)
                if not oid:
                    print(f"[warn] no option '{value}' on {field_name}")
                    continue
                cmd += ["--single-select-option-id", oid]
            if run(cmd):
                print(f"  {field_name}={value}")

    print(f"\n{len(items)} card(s) -> project {a.project}")


if __name__ == "__main__":
    main()
