#!/usr/bin/env python3
"""Materialize the production workspace from board cards + pipeline outputs.

Layout (scales by date, one folder per video):
  workspace/
    short-form/<YYYY-MM-DD>/<video-slug>/
     00_script.md            (or TODO.md if not written yet)
     01_teleprompter.txt
     02_storyboard.md
     03_diagrams/*.excalidraw + *.spec.json
     04_research/*.md
     metadata.json           (title, form, series, status, dates, board card id)

Usage:
  python3 scripts/workspace.py [--slug <outputs slug>] [--week 2026-08-10]
Reads calendar/items_shorts.json + items_longs.json (board cards).
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from common import CONFIG, OUTPUTS, CALENDAR, ROOT, slugify

WORKSPACE = Path(__file__).resolve().parent.parent / \
    CONFIG.get("paths", {}).get("workspace", "workspace")

_DEF_WEEK = CONFIG.get("plan", {}).get("default_week", "2026-08-10")
_DEF_OWNER = CONFIG.get("boards", {}).get("shorts", {}).get("owner", "noah-sheldon")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def board_items(owner, project):
    """title -> item id, via gh project item-list --format json."""
    out = run(["gh", "project", "item-list", project, "--owner", owner,
               "--format", "json"])
    if not out:
        return {}
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return {}
    result = {}
    for it in data.get("items", []):
        content = it.get("content") or {}
        title = content.get("title")
        if title:
            result[title] = it.get("id")
    return result


def publish_date(title, week):
    """'Day N' -> week + (N-1) days; long-form -> week + 6 (Sunday)."""
    w = dt.date.fromisoformat(week)
    m = re.search(r"Day (\d+)", title)
    if m:
        return w + dt.timedelta(days=int(m.group(1)) - 1)
    return w + dt.timedelta(days=6)


def extract_short(text, idea_id):
    """Extract one short's section from the combined script_shorts.md."""
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        if re.match(rf"^##\s+{re.escape(idea_id)}\s+·", l):
            start = i
            break
    if start is None:
        return None
    out = [lines[start]]
    for l in lines[start + 1:]:
        if re.match(r"^##\s+s\d+\s+·", l):
            break
        out.append(l)
    return "\n".join(out)


def materialize(items, form, slug, week, owner, cards, research_map=None):
    for it in items:
        title = it["title"]
        date = publish_date(title, week)
        folder = WORKSPACE / form / date.isoformat() / slugify(title)
        folder.mkdir(parents=True, exist_ok=True)

        src = OUTPUTS / slug
        present = []
        missing = []

        # Match the card to its idea (ideas.json title -> id) once, for both
        # research and per-short script extraction.
        idea_id = None
        if research_map:
            norm = title.split(" · ", 1)[-1].strip()
            idea_id = research_map.get(norm)

        def copy(rel_name, target_name):
            f = src / rel_name
            if f.exists():
                shutil.copy2(f, folder / target_name)
                present.append(target_name)
            else:
                missing.append(rel_name)

        # Teleprompter + storyboard belong to the long-form only.
        # Short scripts: extract ONLY this video's section from the combined file.
        if form == "long-form":
            copy("script_longform.md", "00_script.md")
            copy("teleprompter.txt", "01_teleprompter.txt")
            copy("storyboard.md", "02_storyboard.md")
        else:
            sf = src / "script_shorts.md"
            if sf.exists() and idea_id:
                section = extract_short(sf.read_text(encoding="utf-8"), idea_id)
                if section:
                    (folder / "00_script.md").write_text(section, encoding="utf-8")
                    present.append("00_script.md")
                else:
                    missing.append(f"script_shorts.md (section {idea_id})")
            else:
                missing.append("script_shorts.md")

        # Per-video research: copy the brief for this idea only.
        rdir = folder / "04_research"
        n_res = 0
        if idea_id:
            f = src / "research" / f"{idea_id}.md"
            if f.exists():
                rdir.mkdir(exist_ok=True)
                shutil.copy2(f, rdir / f.name)
                n_res += 1
        if n_res:
            present.append(f"04_research ({n_res} file)")

        # Code (demo .py) — belongs with the long-form that teaches it.
        cdir = folder / "05_code"
        n_code = 0
        if form == "long-form":
            cdir.mkdir(exist_ok=True)
            for p in sorted((src / "code").glob("*.py")):
                shutil.copy2(p, cdir / p.name)
                n_code += 1
        if n_code:
            present.append(f"05_code ({n_code} files)")

        # Diagrams: canonical home is THIS video's 03_diagrams/ (per-video).
        # Specs come from outputs/<slug>/diagrams/; .excalidraw is generated here.
        ddir = folder / "03_diagrams"
        n_diag = 0
        if form == "long-form" and (src / "diagrams").exists():
            ddir.mkdir(exist_ok=True)
            for p in sorted((src / "diagrams").glob("*.spec.json")):
                shutil.copy2(p, ddir / p.name)
                base = p.name[: -len(".spec.json")]
                out = ddir / (base + ".excalidraw")
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "diagram.py"),
                     str(p), "-o", str(out)],
                    capture_output=True, text=True)
                if out.exists():
                    n_diag += 1
        if n_diag:
            present.append(f"03_diagrams ({n_diag} files)")

        if not present:
            missing.append("script")
        if not (folder / "00_script.md").exists():
            (folder / "TODO.md").write_text(
                "# TODO — no script yet\n\n"
                f"Run the SCRIPT stage for: {title}\n"
                f"Source: outputs/{slug}/\n", encoding="utf-8")

        meta = {
            "title": title,
            "form": form,
            "series": it.get("series"),
            "status": it.get("status"),
            "week": week,
            "publish_date": date.isoformat(),
            "source_slug": slug,
            "board_card_id": cards.get(title),
            "files_present": present,
            "files_missing": missing,
        }
        (folder / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        flag = "OK " if (folder / "00_script.md").exists() else "TODO"
        print(f"[{flag}] {form}/{date} {title}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default=None,
                    help="outputs/<slug> to pull assets from")
    ap.add_argument("--week", default=_DEF_WEEK,
                    help="plan week Monday (ISO date)")
    ap.add_argument("--owner", default=_DEF_OWNER)
    a = ap.parse_args()

    shorts = json.loads((CALENDAR / "items_shorts.json").read_text())
    longs = json.loads((CALENDAR / "items_longs.json").read_text())

    # Resolve slug from outputs if not given (skip hidden dirs like .smoke;
    # prefer a slug that already has scripts)
    slug = a.slug
    if not slug and OUTPUTS.exists():
        cands = sorted(d.name for d in OUTPUTS.iterdir()
                       if d.is_dir() and not d.name.startswith("."))
        scripted = [c for c in cands
                    if (OUTPUTS / c / "script_longform.md").exists()
                    or (OUTPUTS / c / "script_shorts.md").exists()]
        slug = (scripted or cands)[0] if (scripted or cands) else None
    if not slug or not (OUTPUTS / slug).exists():
        print("[warn] no outputs/<slug> found — workspace will be TODO-only")

    cards7 = board_items(a.owner, "7")
    cards8 = board_items(a.owner, "8")

    # Per-video research: map idea titles (from ideas.json) -> research file id.
    research_map = {}
    ideas_path = OUTPUTS / slug / "ideas.json" if slug else None
    if ideas_path and ideas_path.exists():
        ideas = json.loads(ideas_path.read_text(encoding="utf-8"))
        for s in ideas.get("shorts", []):
            research_map[re.sub(r"^Day\s*\d+\s*·\s*", "", s["title"]).strip()] = s["id"]
        for l in ideas.get("longs", []):
            research_map[l["title"]] = l["id"]

    materialize(shorts, "short-form", slug, a.week, a.owner, cards7, research_map)
    materialize(longs, "long-form", slug, a.week, a.owner, cards8, research_map)

    (WORKSPACE / "README.md").write_text(
        "# Workspace — per-video production\n\n"
        "One folder per video. Film from:\n"
        "- `00_script.md` — beat outline (WHAT/HOW/SHOW/WHEN)\n"
        "- `01_teleprompter.txt` — prompt cards (long-form)\n"
        "- `02_storyboard.md` — shot list + OBS scenes\n"
        "- `03_diagrams/` — .excalidraw files for the iPad\n"
        "- `04_research/` — this video's verified brief\n"
        "- `05_code/` — demo code (long-form)\n\n"
        "Rebuild anytime: `rm -rf workspace && .venv/bin/python scripts/workspace.py`\n"
        "Boards: https://github.com/users/noah-sheldon/projects/7 (short) · "
        "https://github.com/users/noah-sheldon/projects/8 (long)\n",
        encoding="utf-8")

    print(f"\nworkspace ready: {WORKSPACE}")


if __name__ == "__main__":
    main()
