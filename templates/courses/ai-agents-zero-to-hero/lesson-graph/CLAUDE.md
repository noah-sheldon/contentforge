# HyperFrames Composition Project — lesson-graph

Part of the AI Agents Zero→Hero course family. See the family README (`../README.md`) and this template's `spec.md` for the build recipe.

## Skills — USE THESE FIRST

Always invoke the relevant skill before writing or modifying compositions: `/hyperframes` (router), `/hyperframes-core` (composition contract), `/hyperframes-keyframes` (SVG paths, masks, draw-on), `/hyperframes-animation` (motion). Skipping them produces broken compositions.

## Commands

```bash
npm run dev          # preview server (long-running — background only)
npm run check        # lint + runtime + layout + motion + contrast
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
```

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, `data-track-index` and `class="clip"`.
2. Root composition element carries `data-composition-id`, `data-start="0"`, `data-width`, `data-height`, `data-duration`.
3. Exactly one paused timeline registered as `window.__timelines["main"]`, built synchronously.
4. Scene fills go on full-bleed children, never on the root.
5. Only deterministic logic — no `Date.now()`, no `Math.random()`, no `repeat: -1` (finite pulses only), no network at render time.
6. No CSS initial `transform` on any element that GSAP also tweens — use `fromTo` for initial states.
7. Edge markers: define one `<marker id>` per composition; ids must be unique across the page.
8. Every reveal is speech-timed: `at` values come from the VO transcript mapping.
9. Contrast: accent only for large text/decoratives; small text uses white ink or `--muted`.

## Kit sync

Tokens, brand blocks, and reveal engine are inlined from `../shared/`. Edit the canonical files there, then regenerate the inline blocks.

## Linting — ALWAYS RUN AFTER CHANGES

```bash
npm run check
```

Fix all errors before presenting the result. Review warnings before rendering.
