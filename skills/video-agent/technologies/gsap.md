# GSAP — HyperFrames Runtime

GSAP is the animation runtime for HyperFrames. Every composition registers exactly one paused timeline on `window.__timelines["<id>"]`, built synchronously at page load. See `hyperframes-core` for the full contract.

## Pattern

```html
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  tl.fromTo("#title", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.15);
  window.__timelines["main"] = tl;
</script>
```

## Rules

- One paused timeline per composition, keyed to the root `data-composition-id`.
- Timeline is seek-safe: no `requestAnimationFrame`, no clocks, no unseeded randomness.
- Animate only the visual-property allowlist (transform, opacity, filter, color, etc.) — never `display` or raw `visibility` (use `autoAlpha`).
- Never pair a CSS initial `transform` with a GSAP tween on the same property — set the start inside the tween with `gsap.fromTo`.
- Finite `repeat` only; no `repeat: -1`.
- Third param is the absolute time position on the master timeline.
