---
name: cp-course-builder
description: Content-planner stage — generate/update a full course repo from course.yaml (no hardcoding). Reads the config, writes modules in the Six Beats pattern.
version: 1.0.0
updated: 2026-08-09
changelog:
  - 1.0.0: "Initial"
---

# COURSE BUILDER — write or extend a course from config

## Role
You build course content from a config file. ZERO hardcoding: every module,
lesson, exercise, quiz, and project comes from `course.yaml` + the course's own
templates. You never invent topics the config doesn't list.

## Inputs
- `skill/templates/course.yaml` — the canonical course spec (name, theme,
  scope, modules with topics/projects/lesson counts)
- Course repo: `../production-agentic-rag-from-scratch/` (or the repo in
  course.yaml `repo`)

## Read first (course repo)
- `AGENTS.md` — the 10 teaching rules (build-first, HITL quiz, few exercises,
  diagram-first, scope)
- `LESSON_TEMPLATE.md` — the Six Beats format
- `ROADMAP.md` — module order + gates

## What you generate/update (per course.yaml)

1. **ROADMAP.md** — module table exactly as config: `num | title | project`.
   Gates text: 2-3 exercises, HITL quiz, project gates module.
2. **Per module** `modules/<NN>-<slug>/README.md` — topics (from config,
   comma-separated, mapped to a human paragraph), Build-first line, the
   module's own exercises/quiz/project sections.
3. **Lessons** — `lessons/<NN>-<topic-slug>/docs/en.md` (Six Beats:
   MOTTO/PROBLEM/CONCEPT with mermaid + excalidraw reference/BUILD IT/USE
   IT/SHIP IT) + `code/build.py` (plain Python, stdlib, runnable) +
   `outputs/artifact.md`. Lesson count per module from config `lessons`; topics
   derived from config `topics`.
4. **Exercises** — `exercises/01_exercises.py` + `02_solutions.py`: exactly
   2-3 per module, runnable, each with an automatic check.
5. **Quiz** — `quizzes/quiz.md`: 5 questions answered from memory + a review
   guide for the human. HITL, no auto-pass.
6. **Project** — `project/project.md` + skeleton: the config `project` as the
   goal; acceptance criteria; TODOs tied to lessons.
7. **Diagrams** — every lesson CONCEPT: mermaid block + an excalidraw spec
   (`diagrams/<name>.spec.json`), generated via `python/scripts/diagram.py` from the
   content-planner repo.

## Rules
- Build-first: BUILD IT is plain Python stdlib; frameworks only in USE IT as
  the honest scoreboard.
- No copied code or projects from other courses (arXiv curator off-limits).
- Diagram-first: less text, more picture; explanations high-level, first
  principles, grade-5 words.
- Verify: run every `build.py` and `py_compile` the exercises before reporting
  done. Commit only complete modules (all files present).
