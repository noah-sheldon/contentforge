---
name: engineering-standards
description: Engineering standards skill for contentforge. SOLID, DRY, SOC, KISS, YAGNI, laws of software engineering, small-file/folder structure, and the pre-commit review checklist. Load before designing, adding, or refactoring any module.
---

# ContentForge — Engineering & Architecture Standards

Current as of the P0 green baseline (2026-08-31). This is the "how we
write code" skill. It is binding together with the quality gates in the
root Makefile and the rules in `.openhands/microagents/repo.md`. When a
reviewer or agent disagrees with code, the principles below decide.

## 0. The system in one picture (know what you are coding against)

- `python/` = the pipeline (the only product code today): `agents/`
  (typed agents + research + copy), `services/` (text_animator, pixabay,
  arize), `scripts/` (one stage per script), config via `config/*.yaml`
  and `python/config/settings.py`.
- `skills/`, `prompts/`, `templates/`, `config/` = runbooks, prompt
  registry, HyperFrames templates, persona/voice/brand tokens.
- Serving track (Cloudflare + VM + MongoDB + Hetzner + apps/services/
  workers) is **deferred to P2-P5**. Do not build for it before the P1.5
  proof gate (PLAN.md Roadmap).
- No speculative frameworks were added (no Celery/Redis/CrewAI/DB yet);
  each was considered and rejected until a phase needs it (YAGNI).

## 1. SOLID (applied, with real anchors)

- **S — Single responsibility.** One file, one job. Split, don't grow
  (§6). `python/scripts/capture.py` only captures; `schemas.py` only
  declares contracts.
- **O — Open/closed.** A new platform/format/template is a new subclass or
  registry entry, not a new branch in existing code (experts/, platforms/,
  `text_animator.py` template selection).
- **L — Liskov.** Every implementation satisfies its base contract:
  scraper -> `list[SearchResult]`, publisher/expert -> its payload type
  from `agents/schemas.py`.
- **I — Interface segregation.** Typed, narrow interfaces
  (`agents/base.py` ABCs); no god-objects, no unused methods.
- **D — Dependency inversion.** Depend on the ABC/protocol, not on a
  concrete module: callers get clients via shared factories, never by
  importing deep internals.

## 2. DRY (applied)

- Rule of three: extract on the third repetition, not before — DRY is
  balanced by YAGNI.
- One home per concern: schemas in `agents/schemas.py`, shared
  behaviour/decorators in `agents/base.py`, config in `config/` +
  `python/config/settings.py`, prompts in the `prompts/` registry,
  clients via shared factory functions.
- Forbidden: per-video hardcoding (audit A6). Everything per run comes
  from config + registries at runtime, never pasted per video.
- Never copy a script between repos/tools; a missing capability is ported
  once into `python/`, then shared.

## 3. SOC (applied)

| Concern | Home | Rule |
|---|---|---|
| Data contracts | `python/agents/schemas.py` | Typed Pydantic models; no bare dicts across boundaries |
| ABCs + shared behaviour | `python/agents/base.py` | Interfaces only, no business logic |
| Agent logic | `python/agents/{domain}/*.py` | One job per file |
| Prompts | `prompts/` registry + `agents/prompts/` | Template text only, never Python logic |
| Config | `config/` YAML + settings loader | Persona/voice/brand/tokens as data |
| Stage orchestration | `python/scripts/*.py` | Thin CLI over services/agents |
| Reusable engines | `python/services/*.py` | No CLI, no per-run hardcoding |

Folders mirror bounded contexts; new context = new folder, never a loose
file at the repo root.

## 4. KISS

- Junior test: can a junior engineer understand the file in five minutes?
- Smallest change that satisfies the current phase's acceptance criteria.
- Stack stays small and proven (uv, ruff/pyrefly, OpenAI SDK, feedparser,
  playwright, faster-whisper, HyperFrames). Anything else needs a phase
  decision first.

## 5. YAGNI

- Build what the current phase's ACs need, nothing more. No DB before P2,
  no queue before P2, no dashboard before P4, no multi-tenant before P3,
  no billing before P5.
- No config knob, flag, or abstraction until a second concrete user of it
  exists. Don't future-proof public APIs against guesses.
- If unsure whether you need it, you don't need it yet.

## 6. Small files and folder structure (SRP as architecture)

- One responsibility per file; stay roughly under ~250 lines. When a file
  does a second job or grows unwieldy, it becomes a folder with
  subfolders — split, don't extend.
- Organize by bounded context (see §0/§3). P2+ adds `apps/`, `services/`,
  `workers/` as their own contexts.
- Never dump loose files at the repo root; a new top-level directory
  means a new bounded context, not tidiness.

## 7. Laws of software engineering (applied checklist)

1. Conway's law — structure follows the work: file/folder boundaries match
   stage boundaries (plan / produce / publish), and later the serving
   track, so teams and system can evolve together.
2. Gall's law — working complex systems evolve from working simple ones:
   P0-P1.5 make the pipeline correct first; the serving system is built on
   a proven core, never the other way around.
3. Law of Demeter — modules talk to immediate collaborators only
   (agent -> service/script -> config); no reaching through layers.
4. Brooks's law — late added effort is costly and pipeline work is
   serial: one render at a time (queue concurrency = 1); concurrency is a
   P2 decision, not a P1 invention.
5. Postel's law — be strict at the boundary: validate config input
   fail-fast (Pydantic), keep internal invariants tight and trusted.
6. Liskov + interface segregation — see SOLID §1.
7. Avoid bikeshedding — product decisions live in the PLAN.md decision
   register; resolve open items at phase gates, not in code review.

## 8. Pre-commit checklist (the "correct way" gate)

Before every commit or PR:

- [ ] `make verify` green — ruff lint + format, pyrefly types, biome,
      tsc (armed), pytest.
- [ ] Self-review against §1-§5: SOLID satisfied, no duplication (check
      `agents/base.py`, `schemas.py`, `services/` first), SOC respected,
      no speculative abstraction, nothing hardcoded that should come from
      config/registries.
- [ ] Small file / right folder; no loose files at root.
- [ ] No stale references to removed architecture (Cloud Run, CrewAI,
      Celery, Redis, MinIO, pre-P2 DB, hardcoded source paths).
- [ ] Non-trivial change: run the code-review checklist (code-review
      skill) before merging; P1.5+ behavioural changes add fixture
      coverage.

Principles are not ceremony. When two conflict, pick the reading that
keeps the pipeline simplest to reason about and change.
