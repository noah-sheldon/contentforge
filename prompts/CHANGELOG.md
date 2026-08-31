# Prompt Changelog

All notable changes to agent prompts. Format: [Keep a Changelog](https://keepachangelog.com/).
Bump the `version` in each prompt's frontmatter with every entry here.

## [video-agent 1.1.2] - 2026-08-23
### Changed
- Scene transitions rule: every scene boundary gets an animated exit (slide/fade ~0.5s) + hard-kill set at the boundary — never a hard unmount or black frame
- Browser footage rule: any web/UI content is recorded LIVE with DYNAMIC scroll + zoom (browser-use agent or scripted Playwright recipe) — never static screenshots
### Added
- Self-Review Gate items 8 (scene transitions) and 9 (live browser footage)

## [video-agent 1.1.1] - 2026-08-23
### Changed
- Audio rule: videos >1 min need NO music bed — SFX cues only; music (ducked under speech) applies to videos ≤1 min
### Added
- Self-Review Gate item 7: audio-per-runtime check (music ≤1 min / SFX-only >1 min)

## [video-agent 1.1.0] - 2026-08-23
### Changed
- Restructured as a SELF-CONTAINED master: full production steps (tighten → transcribe → beat-map → compose → check → render → deliver), hard rules, screen recording, delivery, self-review gate, templates/tech stack all written inside the file
- CLAUDE.md Video Editing section now points to the master skill as the single source of truth

## [video-agent 1.0.3] - 2026-08-23
### Added
- SRT captions ALWAYS rule: .srt for long-form AND short-form, generated from the final word-accurate transcript, timed to rendered audio; IG/TikTok burn-in note

## [video-agent 1.0.2] - 2026-08-23
### Changed
- Tightening rule: word-accurate method (tighten_words.py, whisper word timestamps, lead/tail 0.35) — amplitude-only silencedetect clips word tails/heads; explicitly banned
- Thumbnails rule: face-centered square crop (no portrait stretch) + dark text strokes for small-size legibility; build via build_thumbnails.py
### Added
- Verification tooling references (verify_pip.py, audit_pip_collisions.py) to the Self-Review Gate

## [video-agent 1.0.1] - 2026-08-23
### Added
- Motion-graphics-ARE-the-content rule (graphics carry the story; footage = accent only)
- Thumbnail-flash opener pattern (thumbnail visible ~1s, pip enters after the opener)
### Notes
- Patch bump: additive rules only, no behavioral change to existing rules.

## [video-agent 1.0.0] - 2026-08-23
### Added
- Round-PiP-only hard rule (footage never full-screen; oval-proof implementation)
- Thumbnails ALWAYS for both formats from canonical navy-blue headshot + safe zones
- No-dead-air rule with long-silences-only tighten settings (`--min-silence 1.2 --pad 0.3`)
- Screen Recording & Integration section (Playwright recipe capture + browser-use CDP recording)
- Self-Review Gate (6-point evidence-based self-reflection before preview/render)
### Notes
- Established 2026-08-23 during the mcp-docs long-form + shorts production.
