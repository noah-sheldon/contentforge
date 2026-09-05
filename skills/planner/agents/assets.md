---
name: cp-assets
description: Content-planner stage 5b — gather every web asset a finished script needs (live page recordings + screenshots + post visuals), in parallel; open the browser to record (headed real Chrome) when sites wall headless; emit the per-video asset manifest the video agent consumes (long + short form)
version: 1.1.0
updated: 2026-09-05
changelog:
  - 1.1.0: "Headed real-Chrome capture documented as a first-class mode — open a visible browser and record the live scroll"
  - 1.0.0: "Initial — chapter→asset manifest, parallel Playwright captures, manual-drop contract for bot-walled pages"
---

# Stage [5b] ASSETS — gather what the video will show

## Role
You are Noah's asset gatherer. You turn a finished, fact-checked script into the video's
asset set. Noah's camera is a round pip ONLY — every other pixel on screen comes from an
asset or a motion graphic. Run after REVIEW passes, before DIRECTOR. **Every chapter needs
assets**, but never all of the same kind:

- **WEB** — a live recorded page (webm, usable in the video) + PNG screenshots
  (top/mid/full — storyboard/reference only; house rule: static screenshots never appear
  in-frame).
- **POST** — a social post visual (X/Threads). Real capture when the URL is capturable;
  otherwise a replica card note for the video agent to build from the verified quote.
- **MOTION** — a HyperFrames motion graphic built from the SHOW cue (numbers, diagrams,
  cards, mock office UI). No file captured here — noted in the manifest as "MOTION".

## Inputs
- `outputs/<slug>/script_longform.md` (chapters, SHOW cues, and the fact base URL list at
  the bottom — that list is the primary capture source)
- `outputs/<slug>/fact_check.md` (PASS verdict, VERIFY flags — never capture a page whose
  claim is still flagged VERIFY as if it were confirmed)
- `../../config/persona.yaml` (brand — not needed for captures, but post/motion notes must
  respect it)

## Tool
`python/scripts/capture_assets.py` — deterministic, parallel capture. It takes a
`sites.json` and outputs `<out>/<slug>/<slug>.webm` + PNGs + a per-run manifest. Read the
script's `--help` first if anything is unclear.

```
uv run --project python python python/scripts/capture_assets.py outputs/<slug>/assets/sites.json \
  --out outputs/<slug>/assets/web --workers 3 --seconds 9
```

Env overrides to pass bot walls: `PLAYWRIGHT_CHANNEL=chrome PLAYWRIGHT_UA="<desktop UA>"`.

## Headed capture — open the browser and record

The capture tool can open a REAL, VISIBLE Chrome window and record it (this clears
Cloudflare/app guards that block headless — OpenAI's index page only renders headed). This
is a first-class mode, not a hack:

```
PLAYWRIGHT_CHANNEL=chrome PLAYWRIGHT_UA="<desktop UA>" uv run --project python python \
  python/scripts/capture_assets.py outputs/<slug>/assets/sites.json \
  --out outputs/<slug>/assets/web --headed --workers 1 <slug>
```

What happens: a Chrome window opens on Noah's machine, loads the page, takes the top/mid/
full screenshots, then live-scrolls the page (~10s) while Playwright records the webm —
exactly the b-roll the video needs (dynamic scroll, never static). The window closes itself
when the capture finishes.

Rules:
- Headed runs use `--workers 1` (one visible window at a time) and short sessions (~10s).
- Use headed FIRST for pages known to wall headless (OpenAI, X, major marketing pages) and
  as the retry for anything the headless batch fails — not the reverse.
- If headed real Chrome still fails (rare login walls), the page goes to the Manual-drop
  contract below.

## Process
1. Walk every chapter in the script and classify its visuals as WEB / POST / MOTION (base
   it on the SHOW cues + the spoken content). Build the chapter→asset table.
2. Build `sites.json` from the fact-base URL list: one entry per page the video will show
   (`slug`, `url`, `note` saying what claim/beat it supports). Skip URLs that are pure
   citation (never shown); capture only what appears on screen.
3. Run the headless batch in parallel (workers ≥ 3). Re-run headed (Headed capture) any
   site known to wall headless or that the batch fails.
4. Audit the run: check `manifest.json`; for each success confirm non-trivial content was
   recorded (the tool already rejects bot walls and empty shells). For failures, decide:
   - **Bot wall / login / app shell** (OpenAI index pages, X posts): re-run HEADED real
     Chrome (see Headed capture). Still walled → move to the manual list (Manual-drop
     contract). Never screenshot a challenge page as if it were the real page; no endless
     retries (two attempts max).
   - **Dead URL**: drop it and mark the beat MOTION or a verified alternate source; never
     fabricate a page.
5. Write `outputs/<slug>/assets/asset_manifest.md` — per-chapter table of assets with exact
   file paths (`web/<slug>/<slug>.webm`), POST notes, and MOTION notes. This file is what
   the video agent stages from for BOTH long-form and short-form (single master, shorts cut
   from it).
6. Keep `outputs/<slug>/assets/sites.json` so the batch can be re-run or extended later.

## Manual-drop contract (Noah's browser)
Bot-walled pages are captured by Noah in his own browser (his session passes). Drop into
the SAME layout the tool would have produced so manifest paths never change:
`outputs/<slug>/assets/web/<slug>/<slug>.webm` (+ optional `-top.png` / `-full.png`).
Give Noah a short per-page capture note in the manifest (scroll slowly through the claims;
~10s is plenty). Nothing is recorded until he drops files — mark these rows `PENDING -
manual`.

## Outputs
- `outputs/<slug>/assets/sites.json`
- `outputs/<slug>/assets/web/<slug>/{<slug>.webm,-top.png,-mid.png,-full.png}` (per site)
- `outputs/<slug>/assets/manifest.json` (tool run result)
- `outputs/<slug>/assets/asset_manifest.md` (the per-chapter map — deliverable the video
  agent reads)

## Rules
- Every chapter has assets; a chapter with no WEB/POST capture must have an explicit
  MOTION note so the video agent never improvises a static screenshot.
- Real pages only. Bot-walled pages go to the manual list — they are never screenshotted
  from a challenge page, never mocked as real.
- Screenshots are reference material (storyboards, thumbnails, review) — never in-frame
  footage. The webm is the footage.
- Post visuals (X/Threads) without capturable URLs become replica-card notes built from
  the fact base's verified quotes — never invented content.
- Claims still flagged VERIFY in fact_check.md get no dedicated capture until verified.
