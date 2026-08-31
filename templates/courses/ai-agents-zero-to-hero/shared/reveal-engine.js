/* ============================================================
   AI Agents Zero→Hero — Course Kit: Reveal Engine
   Canonical source. Inline into each template's <script>.
   Speech-timed model: every visual appears at the exact second
   the VO says it. Beat times come from the transcript mapping —
   never eyeballed, never a fixed stage formula.

   API
   ----
   beatIn(tl, sel, at, opts)
       fade/slide an element in at `at` seconds.
       opts: { y=40, x=0, dur=0.35, ease="power3.out", from=1 }
   drawOn(tl, sel, at, opts)
       self-sketch an SVG stroke at `at` seconds.
       opts: { dur=0.8, ease="power2.inOut", len=1600 }
       The path must already carry stroke-dasharray/dashoffset = len.
   ============================================================ */

window.__reveal = (function () {
  function beatIn(tl, sel, at, opts) {
    const o = opts || {};
    const y = o.y !== undefined ? o.y : 40;
    const x = o.x !== undefined ? o.x : 0;
    const dur = o.dur !== undefined ? o.dur : 0.35;
    const ease = o.ease || "power3.out";
    tl.fromTo(
      sel,
      { autoAlpha: 0, x: x, y: y },
      { autoAlpha: 1, x: 0, y: 0, duration: dur, ease: ease },
      at
    );
  }

  function drawOn(tl, sel, at, opts) {
    const o = opts || {};
    const dur = o.dur !== undefined ? o.dur : 0.8;
    const ease = o.ease || "power2.inOut";
    const len = o.len !== undefined ? o.len : 1600;
    tl.fromTo(
      sel,
      { strokeDashoffset: len },
      { strokeDashoffset: 0, duration: dur, ease: ease },
      at
    );
  }

  return { beatIn: beatIn, drawOn: drawOn };
})();
