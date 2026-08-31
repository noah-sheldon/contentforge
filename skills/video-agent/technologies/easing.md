# Motion Design — AE-Quality Easing

Mandatory for every animation. No linear motion — linear = amateur.

## Easing Presets (GSAP)

```js
const EE = {
  out: "power3.out",                     // smooth deceleration
  inOut: "power2.inOut",                 // smooth both ends
  bounce: "back.out(1.6)",               // overshoot + settle
  snap: "back.out(2.5)",                 // snap into place
  elastic: "elastic.out(0.8, 0.3)",      // rubber band
};
```

## Usage Rules

```js
// GOOD — AE-quality
tl.fromTo("#el", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.2);

// BAD — no ease = linear = amateur
tl.fromTo("#el", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.2);
```

## Physics

- Punch-ins (gear items, stat cards): `back.out(1.6)` — fast-in, settle.
- Slow pushes (aesthetic shots, reveals): `"none"` (linear drift is intentional for Ken Burns) — that is the one sanctioned linear use.
- Reveals that should feel weighty: `"power3.out"` with longer duration.
