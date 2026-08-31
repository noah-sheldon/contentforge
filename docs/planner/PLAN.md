# Content Planner — System Plan (v1 draft)

Date: 2026-08-09 · Status: awaiting sign-off
Goal: turn ANY YouTube video/playlist into short-form + long-form content ideas, researched briefs, scripts in Noah's voice, and 7/14-day publishing plans.

Funnel this serves: free tutorials → grow audience → paid courses · AI services · product demos · brand collabs.

---

## 1. The skill — pipeline

A Qwen Code skill (`content-planner`) that orchestrates sub-agents. One input: ANY URL or raw content — YouTube video, YouTube playlist, blog post, article, website, podcast/audio file, or pasted text.

```
ANY INPUT (URL or raw text)
   │
   ▼
[1] INGEST      auto-detect content type:
                · YouTube/playlist → yt-dlp inventory → youtube-transcript-api
                  (fast path) → mlx-whisper local transcription (fallback)
                · website/blog/article → fetch → readable markdown
                · audio file / podcast → mlx-whisper transcription
                · pasted text → as-is
                → normalized markdown in library/<slug>/ + metadata.json
   │
   ▼
[2] ANALYZE     agent reads transcripts → concepts, teaching structure, terms, gaps
   │
   ▼
[2b] MARKETING  platform strategy agent → per-platform playbook from skill/persona.yaml
                growth + goals: hook styles, captions, hashtags, CTA variants,
                cadence, series structure (one concept per short)
   │
   ▼
[3] IDEATE      short-form ideas (IG/TikTok/Shorts) + long-form ideas (YouTube
                tutorials/playlists) + course-seed + service/demo angles
                + per long-form: 3 TITLE options + 3 THUMBNAIL concepts
   │
   ▼
[4] RESEARCH    parallel agents per chosen idea → brief with facts, examples,
                code, stats, sources (no fabrication)
   │
   ▼
[5] SCRIPT      long-form script (hook → teach → demo → recap → CTA)
                + short-form scripts (hook ≤2s, one concept)
                Voice: Indian English, grade 5-6, short sentences, one idea per
                line, no jargon, no marketing voice, passes AI detection.
                Each beat tagged with visual: [EXCALIDRAW] [CODE] [SCREEN] [CAM]
                + teleprompter.txt export (breath-broken lines, mobile-ready)
   │
   ▼
[5b] DIRECTOR   scene-by-scene storyboard: shot list with timings, OBS scene
                switches, camera framing, and an EQUIPMENT CALL SHEET per scene
                (Mac screen / iPad+Excalidraw / iPhone webcam / mic / b-roll)
                + locks 1 title + 1 thumbnail concept + diagram_base.excalidraw
   │
   ▼
[6] PLAN        7-day and 14-day calendars — platform, format, idea, script ref,
                funnel tag. Every long-form auto-splits into 3-5 shorts.
                Grouped into BATCH FILMING days + lighter edit/distribute days
                + creates/updates GitHub Project cards (7=short / 8=long) via gh CLI
```

### Repo layout (at repo root — this IS `content-planner/`)

```
content-planner/
├── skill/                <-- SKILL.md + agent prompt templates + voice rules
├── scripts/              <-- ingest.py, diagram.py, board.py, workspace.py (deterministic glue only)
├── library/<slug>/       <-- ingested source: metadata.json, raw_transcript.md
├── outputs/<slug>/       <-- source-level: analysis, ideas, research, scripts, storyboard, diagram specs, code
├── calendar/             <-- 2026-W33_plan.md (7-day), 2026-W33-W34_plan.md (14-day)
└── workspace/            <-- per-video production folders (sync to iCloud — iPad opens 03_diagrams/)
```

### Platform profiles (one video → five platforms)

No per-platform skills/agents — one pipeline, platform *profiles*. The same cut goes everywhere, uploaded natively and watermark-free (a visible TikTok watermark costs ~5-15% of IG reach). Per-platform variants come from the MARKETING stage: caption, hashtags, CTA, aspect ratio. Priorities (from skill/persona.yaml `growth`): **IG Reels + TikTok + YT Shorts** = audience growth (9:16) · **LinkedIn** = professional credibility + AI services inbound (1:1/4:5 native video + carousels) · **Facebook** = passive repost only. Series ("one concept per short") is the primary follower-conversion mechanism.

### GitHub Projects = the production dashboard

Boards already exist (private, user-level): **7 = short-form** (7 items: Day 1-7 AI series, one issue per video, custom fields `Series`/`Week`/`Form`) · **8 = long-form** (empty, ready for series backlog).

- **One card per video** — an issue named `Day N · <hook>` (shorts, board 7) or `S<series>E<episode> · <title>` (long-form, board 8). Your existing pattern; the pipeline keeps it.
- **Status lifecycle** (set up as the Status field options): `Planned → Scripted → Storyboarded → Shot → Edited → Published`. The skill updates the card after each pipeline stage via `gh project item-edit`.
- **Batch filming:** `Week` iteration field + a `Batch` field (e.g. "A", "B"). Filter by Batch → see exactly the 5-7 cards to shoot in one session. Plan 7 reels → shoot them in one batch day → publish over the week.
- **Mass-production series (board 8):** create the whole series backlog upfront — e.g. 10 cards, `Series=RAG Zero→Hero`, `Episode=1..10`, `Status=Planned` — then produce in batches. The pipeline fills episodes in order; the board shows the queue.
- **Pipeline writes cards:** Phase 4 creates the cards (`gh issue create` in a designated repo → `gh project item-add`); stages update status. GitHub Projects becomes the live dashboard — open it and see exactly what's planned, shot, edited, published.

### Director / storyboard output (per video)

`storyboard.md` — one row per shot:

| # | Time | Visual | Action | Audio | Equipment | Framing |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:07 | [CAM] hook | "RAG fails on 100k docs..." | iPhone mic | iPhone webcam → OBS | eye-level, rule of thirds |
| 2 | 0:07-0:40 | [EXCALIDRAW] | draw doc-split diagram | voiceover | iPad+Pencil, QuickTime wired | full-canvas, zoom 120% |
| 3 | 0:40-2:10 | [CODE] | run the failing code | voiceover | Mac screen, VSCode 20pt font | fullscreen code |
| 4 | 2:10-2:30 | [CAM+WHITEBOARD] | PiP recap | voiceover | iPhone + iPad both in OBS | PiP 80/20 |

Rules the director enforces: one visual per shot, no dead air, b-roll list (hands on keyboard, desk, phone), **locks 1 of the 3 titles + 1 thumbnail concept**, CTA overlay placement. Each shot maps to an OBS scene preset so filming is switch-scene, not setup-per-shot.

**Diagrams: generated, not hand-drawn from scratch.** `.excalidraw` files are plain JSON — the skill emits ready diagram files (boxes, arrows, text) per storyboard shot into the video's `workspace/.../03_diagrams/`. On the iPad you open the base file and animate/trace on camera — no drawing from scratch. No MCP server required. (Verified Aug 2026: no *official* Excalidraw MCP exists on npm; several community servers exist — `excalidraw-mcp`, `excalidraw-mcp-server` — optional to wire later via `qwen mcp add --scope user` for live canvas control.)

## 2. Production setup (the "teach" part) — all free

| Element | Tool | Notes |
|---|---|---|
| Mac screen (VSCode) | OBS Studio | 1920×1080 canvas, Apple VT H.264 encoder, MKV → remux |
| Whiteboard | Excalidraw on iPad Safari | Apple Pencil pressure + palm rejection fixed (Jun 2026); free, live collab, PNG/SVG export |
| iPad screen into Mac | QuickTime (wired USB-C) | add as OBS window source; use Mac mic for audio |
| Webcam | iPhone via Continuity Camera | free, wireless, works as OBS video source; known restart bug → re-add source |
| Shorts | OBS 1080×1920 canvas (camera-led) OR record 16:9 + crop (code-led) | code is wide — crop, don't record vertical |
| Audio | Mac mic / iPhone mic via Continuity | — |

Scene presets: "Code" (VSCode, big font) · "Whiteboard" (Excalidraw) · "Camera+Code" (short-form) · **"Camera Offline / Code Only"** (fallback).

### Production mandates (non-negotiable)

1. **Dual-track audio:** OBS records Track 1 = Microphone (voice) and Track 2 = Desktop Audio as separate tracks inside the MKV. Editing out pauses/coughs never destroys background audio.
2. **Camera drop recovery:** Continuity Camera is wireless and *will* drop eventually — no USB "mode" exists. Always have the "Camera Offline / Code Only" fallback scene; on drop, switch scene, keep recording, fix the feed, continue. Never restart the recording.
3. **Diagram delivery:** every diagram lands in its video's `workspace/<form>/<date>/<video>/03_diagrams/` (iCloud-synced) before the filming day — iPad opens it directly, no drawing from scratch on camera.

### Recording budget — "14 shorts + 7 long-form in 2 hrs?"

No — not as fully-produced content. Realistic math (one-take, screencast-first):

| Output | Finished runtime | Recording time |
|---|---|---|
| 7 long-form (12-15 min) | ~90-105 min | ~140-165 min (1.4-1.5× + setup) |
| 14 shorts (30-60s) | ~10 min | ~0 — auto-cut from the long-form raw |

So the honest budget is **~2.5-3 hrs of batch recording** for 7 long + 14 shorts — shorts are never filmed separately; the pipeline emits cut lists. Editing time ≈ 0 (auto cut lists, captions, overlays). Diagrams are pre-generated, so no whiteboard drawing time during recording.

If 2 hrs is a hard cap: 5 long-form (12 min) + 10 shorts, or 3 long-form (20 min) + 14 shorts.

## 3. Goal mapping

| Goal | How the pipeline feeds it |
|---|---|
| Paid tutorials/courses | Long-form tutorials = course modules; 5-8 tutorials → cohort course (persona Phase 3) |
| AI services for businesses | Tutorials prove capability → LLMOps/agent consulting inbound |
| AI product demos | Every tutorial tagged [DEMO] doubles as product showcase |
| Brand collabs | Reach goal — volume-first: 3-5 shorts + 1 long-form + 1 text post per week |
| Reach | 7/14-day plans prioritize consistent output; shorts repurposed from long-form |

## 4. Key decisions (researched Aug 2026)

- **Whisper stack:** `mlx-whisper` with `large-v3-turbo` — fastest local option on Apple Silicon (~3-8× realtime), free, runs on your M1 Pro. `small`/`medium` fallback for speed. `initial_prompt` with domain terms (RAG, MLOps, Jupyter) anchors technical jargon.
- **Fast path first:** `youtube-transcript-api` fetches auto-captions with no download, no key — free and instant. Whisper only when captions missing/poor (Indian-English ASR quality varies).
- **Playlists:** `yt-dlp --flat-playlist` lists titles/durations/URLs without downloading; active project, still maintained.
- **Excalidraw on iPad: works well now** — pressure + palm-rejection toggles shipped Jun 2026. No paid alternative needed.
- **Camera:** Continuity Camera into OBS is free and current; Camo/EpocCam not needed.
- **Universal input:** any URL or pasted content — YouTube/playlist (yt-dlp + transcript-api + whisper), website/blog (readable-markdown extraction), audio file (whisper), raw text.
- **Long-audio guard:** for sources >45-60 min, ffmpeg-split audio into ≤15-min segments before Whisper (bounds memory, gives resume points). Whisper windows internally at 30s, so this is insurance, not a correctness fix — and for long sources prefer transcript-api / Groq free tier first.
- **Optional speed-up:** Groq STT free tier (whisper-large-v3-turbo, ~8h audio/day) — skip local transcription when quota available.
- **Future hook:** scripts can feed existing HyperFrames 9:16 text pipeline for caption production (out of v1 scope).

## 5. Build phases

| Phase | Deliverable | Acceptance criteria |
|---|---|---|
| 0 | Scaffold: `skill/`, `scripts/`, `library/`, `outputs/`, `calendar/`, `workspace/` + voice rules (skill/persona.yaml + copywriter voice) | `content-planner` skill invocable |
| 1 | Universal ingester (`ingest.py`) | Ingests YouTube video + playlist + a blog URL + pasted text → normalized markdown in `library/`, resume on failure, >45-min sources chunked |
| 2 | Analyze + Marketing + ideate + research agents | 1 source → ≥10 short ideas, 3 long ideas + 3 titles + 3 thumbnail concepts each, research briefs with sources, per-platform playbook (hooks/captions/hashtags/CTAs/cadence) |
| 3 | Scriptwriter + Director | 1 long + 3 short scripts passing voice rules (grade 5-6, no jargon, visual tags) + `teleprompter.txt` + `storyboard.md` (shot list, equipment call sheet, title/thumbnail lock) + diagrams generated into the video's `workspace/.../03_diagrams/` |
| 4 | 7/14-day planner | Calendar markdown grouped into batch filming days + edit/distribute days, platform/format/funnel per day, + board cards created (7=short, 8=long) with Status/Series/Week/Batch fields via gh CLI |
| 5 | Production setup guide + first end-to-end test run | You record one tutorial from the plan (dual-track audio, fallback scene ready) |

## 6. Sign-off status

- Review feedback (2026-08-09) integrated: teleprompter export · dual-track audio · iCloud diagram delivery · long-audio chunk guard · batch filming days · titles/thumbnails at ideate · camera-drop fallback scene · repo layout
- Awaiting: your green light to build Phase 0 + 1
