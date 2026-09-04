#!/usr/bin/env python3
"""Generate the seven 9:16 short-form compositions (m1l1-m1l7).

Each short plays its corresponding beat segment of the tightened master
footage in portrait, with a top talking-head video band, narration audio
(HyperFrames <audio>), and a speech-synced motion-graphics screen.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "outputs"
MASTER_DIR = "m1-longform-what-is-an-ai-agent"
TIGHT = "short.mp4"

# (compId, segStart, segDur, title, accentSub, cards)
SHORTS = [
    {
        "id": "m1l1-what-are-ai-agents",
        "seg_start": 0.85,
        "seg_dur": 42.86,
        "title": "What Are AI Agents?",
        "sub": "Chatbots answer. Agents finish.",
        "type": "equation",
        "reveals": [
            ("#card-chatbot", 10.21),
            ("#card-agent", 12.0),
        ],
    },
    {
        "id": "m1l2-why-do-we-need-ai-agents",
        "seg_start": 43.71,
        "seg_dur": 29.54,
        "title": "Why We Need Agents",
        "sub": "Close the execution gap",
        "type": "gap",
        "reveals": [
            ("#manual-step1", 56.15),
            ("#manual-step2", 57.77),
            ("#manual-step3", 59.3),
            ("#agent-card", 61.87),
            ("#agent-step1", 66.67),
            ("#agent-step2", 68.5),
            ("#agent-step3", 70.5),
        ],
    },
    {
        "id": "m1l3-applications-of-ai-agents",
        "seg_start": 73.25,
        "seg_dur": 15.50,
        "title": "You Already Use Agents",
        "sub": "Running in production today",
        "type": "apps",
        "reveals": [
            ("#app1", 75.33),
            ("#app2", 79.05),
            ("#app3", 84.0),
        ],
    },
    {
        "id": "m1l4-reasoning-llm-decisions",
        "seg_start": 88.75,
        "seg_dur": 16.64,
        "title": "Reasoning Is a Prompt",
        "sub": "No magic — just structure",
        "type": "compare",
        "reveals": [
            ("#unstruct", 88.75),
            ("#struct", 92.45),
        ],
    },
    {
        "id": "m1l5-action-tools-with-llms",
        "seg_start": 105.39,
        "seg_dur": 33.32,
        "title": "Tools & MCP",
        "sub": "The model's hands",
        "type": "mcp",
        "reveals": [
            ("#host", 116.79),
            ("#client", 129.65),
            ("#server", 130.5),
        ],
    },
    {
        "id": "m1l6-react-pattern",
        "seg_start": 138.71,
        "seg_dur": 15.64,
        "title": "ReAct",
        "sub": "Reason and Act",
        "type": "react",
        "reveals": [
            ("#l-think", 142.57),
            ("#l-act", 144.91),
            ("#l-observe", 148.47),
            ("#l-repeat", 150.71),
        ],
    },
    {
        "id": "m1l7-single-vs-multi-agent",
        "seg_start": 154.35,
        "seg_dur": 13.28,
        "title": "One Agent or a Team?",
        "sub": "Pick by the job",
        "type": "team",
        "reveals": [
            ("#team1", 158.17),
            ("#team2", 160.11),
        ],
    },
]

# Per-type content HTML (cards go inside .content)
CONTENT = {
    "equation": """
        <div class="eyebrow">The One Difference</div>
        <div class="row">
          <div class="card bad" id="card-chatbot">
            <div class="card-label">CHATBOT</div>
            <div class="card-title">Waits for you</div>
            <div class="card-body">Answers one question. You drive every turn.</div>
          </div>
          <div class="card good" id="card-agent">
            <div class="card-label">AGENT</div>
            <div class="card-title">Drives itself</div>
            <div class="card-body">Thinks, acts, observes, loops until done.</div>
          </div>
        </div>
        <div class="equation">Agent = LLM <span>+</span> Loop <span>+</span> Tools</div>
    """,
    "gap": """
        <div class="eyebrow">Why We Need Agents</div>
        <div class="card bad" id="manual-card">
          <div class="card-label">CHATGPT · YOU DRIVE</div>
          <div class="card-title">Three pages of advice</div>
          <div class="steps">
            <div class="step" id="manual-step1">01 · Run the Python script</div>
            <div class="step" id="manual-step2">02 · Query the database</div>
            <div class="step" id="manual-step3">03 · Attach the PDF</div>
          </div>
        </div>
        <div class="arrow">→</div>
        <div class="card good" id="agent-card">
          <div class="card-label">AGENT · IT DRIVES</div>
          <div class="card-title">Autonomous pipeline</div>
          <div class="steps">
            <div class="step" id="agent-step1">01 · Executes the tools</div>
            <div class="step" id="agent-step2">02 · Handles errors</div>
            <div class="step" id="agent-step3">03 · Finishes the job</div>
          </div>
        </div>
    """,
    "apps": """
        <div class="eyebrow">Already In Production</div>
        <div class="app-card" id="app1">
          <div class="app-label">SEARCH</div>
          <div class="app-body">Plans multi-step queries</div>
        </div>
        <div class="app-card" id="app2">
          <div class="app-label">CODING ASSISTANT</div>
          <div class="app-body">Edits files, runs tests, fixes bugs</div>
        </div>
        <div class="app-card" id="app3">
          <div class="app-label">FINANCE</div>
          <div class="app-body">Reconciles transactions</div>
        </div>
    """,
    "compare": """
        <div class="eyebrow">Reasoning Is A Prompt</div>
        <div class="card bad" id="unstruct">
          <div class="card-label">UNSTRUCTURED</div>
          <div class="card-title">"Help me analyze this"</div>
          <div class="card-body">Wanders. No plan, no guardrails.</div>
        </div>
        <div class="card good" id="struct">
          <div class="card-label">STRUCTURED</div>
          <div class="card-title">Inspect → choose → act</div>
          <div class="card-body">Reads state, weighs tools, picks the next action.</div>
        </div>
    """,
    "mcp": """
        <div class="eyebrow">Tools Are The Hands</div>
        <div class="mcp-row">
          <div class="mcp-node" id="host"><div class="mcp-name">HOST</div><div class="mcp-sub">Your agent</div></div>
          <div class="mcp-link">⇄</div>
          <div class="mcp-node" id="client"><div class="mcp-name">CLIENT</div><div class="mcp-sub">Protocol</div></div>
          <div class="mcp-link">⇄</div>
          <div class="mcp-node" id="server"><div class="mcp-name">SERVER</div><div class="mcp-sub">DBs · files · APIs</div></div>
        </div>
    """,
    "react": """
        <div class="eyebrow">The Core Engine</div>
        <div class="react-grid">
          <div class="react-node" id="l-think"><div class="rn-name">THINK</div><div class="rn-sub">pick the action</div></div>
          <div class="react-node" id="l-act"><div class="rn-name">ACT</div><div class="rn-sub">call the tool</div></div>
          <div class="react-node" id="l-observe"><div class="rn-name">OBSERVE</div><div class="rn-sub">read the result</div></div>
          <div class="react-node" id="l-repeat"><div class="rn-name">REPEAT</div><div class="rn-sub">until done</div></div>
        </div>
    """,
    "team": """
        <div class="eyebrow">One Brain or a Team?</div>
        <div class="team-card" id="team1">
          <div class="team-title">Single agent</div>
          <div class="team-body">One clear job. Start here.</div>
        </div>
        <div class="team-card" id="team2">
          <div class="team-title">Multi-agent</div>
          <div class="team-body">Split for separate permissions or contexts.</div>
        </div>
    """,
}

REVEAL_JS = {
    "equation": """
      tl.fromTo("#card-chatbot", { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, {0});
      tl.fromTo("#card-agent", { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, {1});
      tl.fromTo(".equation", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, 32.85);
    """,
    "gap": """
      tl.from("#manual-card", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.3);
      tl.fromTo("#manual-step1", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {0});
      tl.fromTo("#manual-step2", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {1});
      tl.fromTo("#manual-step3", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {2});
      tl.from(".arrow", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, 18.09);
      tl.fromTo("#agent-card", { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, {3});
      tl.fromTo("#agent-step1", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {4});
      tl.fromTo("#agent-step2", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {5});
      tl.fromTo("#agent-step3", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, {6});
    """,
    "apps": """
      gsap.utils.toArray(".app-card").forEach(function (el, i) {
        tl.set(el, { opacity: 0, y: 70 }, [0,1,2][i]);
        tl.to(el, { y: 0, duration: 0.45, ease: "power4.out" }, [0,1,2][i]);
        tl.to(el, { opacity: 1, duration: 0.1 }, [0,1,2][i]);
      });
    """,
    "compare": """
      tl.from(".eyebrow", { opacity: 0, y: 14, duration: 0.4, ease: "power2.out" }, 0.2);
      tl.fromTo("#unstruct", { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, {0});
      tl.fromTo("#struct", { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, {1});
    """,
    "mcp": """
      tl.from(".eyebrow", { opacity: 0, y: 14, duration: 0.4, ease: "power2.out" }, 0.2);
      tl.fromTo("#host", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power3.out" }, {0});
      tl.fromTo("#client", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power3.out" }, {1});
      tl.fromTo("#server", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power3.out" }, {2});
      tl.from(".mcp-link", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 26.61);
    """,
    "react": """
      tl.from(".eyebrow", { opacity: 0, y: 14, duration: 0.4, ease: "power2.out" }, 0.2);
      gsap.utils.toArray(".react-node").forEach(function (el, i) {
        tl.fromTo(el, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, [0,1,2,3][i]);
      });
    """,
    "team": """
      tl.from(".eyebrow", { opacity: 0, y: 14, duration: 0.4, ease: "power2.out" }, 0.2);
      tl.fromTo("#team1", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, {0});
      tl.fromTo("#team2", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, {1});
    """,
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>@TITLE@ — Short</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    :root {
      --obsidian: #12141C; --alabaster: #FAFAFA; --gold: #D4AF37;
      --gold-glow: rgba(212, 175, 55, 0.25); --silent-gray: #9AA3B2;
      --surface-dark: #1A1D27; --glass-border: rgba(212, 175, 55, 0.25);
      --red: #E65055; --green: #46A758;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body { background: var(--obsidian); color: var(--alabaster); font-family: 'Inter', sans-serif; overflow: hidden; width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; }
    .stage { position: relative; width: 1080px; height: 1920px; background: radial-gradient(circle at 50% 22%, #1A1D2B 0%, #12141C 100%); overflow: hidden; }
    .ambient-glow { position: absolute; inset: 0; z-index: 0; background: radial-gradient(circle at 50% 30%, rgba(212,175,55,0.20) 0%, rgba(212,175,55,0.0) 55%); opacity: 0.5; pointer-events: none; }
    .pip { position: absolute; top: 80px; left: 50%; transform: translateX(-50%); width: 460px; height: 460px; border-radius: 50%; border: 3px solid var(--gold); box-shadow: 0 0 44px var(--gold-glow); overflow: hidden; background: #000; z-index: 4; }
    .pip video { width: 100%; height: 100%; object-fit: cover; object-position: center; }
    .hud-pill { position: absolute; top: 40px; left: 40px; z-index: 5; font-family: 'JetBrains Mono', monospace; font-size: 20px; letter-spacing: 0.12em; color: var(--gold); background: rgba(18,20,28,0.85); border: 1px solid var(--glass-border); padding: 10px 24px; border-radius: 999px; text-transform: uppercase; }
    .content { position: absolute; top: 620px; left: 60px; right: 60px; bottom: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; z-index: 2; }
    .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 22px; letter-spacing: 0.12em; color: var(--gold); text-transform: uppercase; }
    .headline { font-family: 'Playfair Display', serif; font-size: 58px; font-weight: 700; line-height: 1.05; text-align: center; }
    .headline .accent { color: var(--gold); }
    .sub { font-size: 26px; color: var(--silent-gray); text-align: center; }
    .card { background: var(--surface-dark); border: 1px solid var(--glass-border); border-radius: 24px; padding: 34px 36px; width: 100%; box-shadow: 0 16px 40px rgba(0,0,0,0.8); }
    .card.bad { border-color: rgba(229,72,77,0.55); } .card.bad .card-label { color: var(--red); }
    .card.good { border-color: rgba(70,167,88,0.55); box-shadow: 0 0 30px rgba(70,167,88,0.18); } .card.good .card-label { color: var(--green); }
    .card-label { font-family: 'JetBrains Mono', monospace; font-size: 18px; letter-spacing: 0.1em; color: var(--gold); text-transform: uppercase; margin-bottom: 12px; }
    .card-title { font-family: 'Playfair Display', serif; font-size: 40px; font-weight: 700; margin-bottom: 10px; }
    .card-body { font-size: 24px; line-height: 1.5; color: var(--silent-gray); }
    .steps { display: flex; flex-direction: column; gap: 14px; margin-top: 16px; }
    .step { font-size: 24px; color: var(--alabaster); background: rgba(26,29,39,0.7); border: 1px solid var(--glass-border); border-radius: 14px; padding: 16px 22px; }
    .arrow { font-family: 'Playfair Display', serif; font-size: 52px; color: var(--gold); }
    .equation { font-family: 'JetBrains Mono', monospace; font-size: 40px; color: var(--alabaster); text-align: center; }
    .equation span { color: var(--gold); }
    .app-card { background: var(--surface-dark); border: 1px solid var(--glass-border); border-radius: 22px; padding: 30px 34px; width: 100%; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,0.8); }
    .app-label { font-family: 'JetBrains Mono', monospace; font-size: 22px; color: var(--gold); margin-bottom: 10px; }
    .app-body { font-size: 24px; color: var(--silent-gray); }
    .mcp-row { display: flex; align-items: center; gap: 20px; }
    .mcp-node { background: var(--surface-dark); border: 1px solid var(--glass-border); border-radius: 18px; padding: 24px; text-align: center; width: 260px; }
    .mcp-name { font-family: 'JetBrains Mono', monospace; font-size: 26px; color: var(--gold); margin-bottom: 8px; }
    .mcp-sub { font-size: 20px; color: var(--silent-gray); }
    .mcp-link { font-family: 'JetBrains Mono', monospace; font-size: 26px; color: var(--alabaster); }
    .react-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; width: 100%; }
    .react-node { background: var(--surface-dark); border: 1px solid var(--gold); border-radius: 20px; padding: 28px; text-align: center; box-shadow: 0 0 26px var(--gold-glow); }
    .rn-name { font-family: 'JetBrains Mono', monospace; font-size: 28px; color: var(--gold); margin-bottom: 8px; }
    .rn-sub { font-size: 20px; color: var(--silent-gray); }
    .team-card { background: var(--surface-dark); border: 1px solid var(--glass-border); border-radius: 24px; padding: 34px; width: 100%; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,0.8); }
    .team-title { font-family: 'Playfair Display', serif; font-size: 40px; font-weight: 700; margin-bottom: 10px; }
    .team-body { font-size: 24px; color: var(--silent-gray); }
    .progress-bar-container { width: 100%; height: 6px; background: rgba(255,255,255,0.15); position: absolute; bottom: 0; left: 0; z-index: 10; }
    .progress-fill { height: 100%; width: 0%; background: var(--gold); box-shadow: 0 0 16px var(--gold); }
  </style>
</head>
<body>
  <div class="stage" id="stage" data-composition-id="@CID@" data-start="0" data-duration="@DUR@" data-width="1080" data-height="1920">
    <div class="ambient-glow" id="ambient-glow" data-track-index="0"></div>
    <div class="hud-pill" id="hud">// AI AGENTS ZERO→HERO • @BADGE@</div>
    <div class="pip" id="pip" data-track-index="4">
      <video id="talking-head" class="clip" src="short.mp4" playsinline muted data-start="0" data-duration="@SEGDUR@" data-track-index="1"></video>
    </div>
    <audio id="narration" src="short.mp4" data-start="0" data-duration="@SEGDUR@" data-volume="1" data-track-index="10"></audio>
    <div class="content" id="content">
      <div class="headline" id="headline">@TITLE@</div>
      <div class="sub" id="sub">@SUB@</div>
      @CONTENT@
    </div>
    <div class="progress-bar-container" id="progress-bar" data-track-index="10">
      <div class="progress-fill" id="progress-line"></div>
    </div>
  </div>
  <script>
    const D = @DUR@;
    const tl = gsap.timeline({ paused: true });
    tl.to("#progress-line", { width: "100%", ease: "none", duration: D }, 0);
    tl.from("#headline", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.2);
    tl.from("#sub", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 0.6);
@REVEALS@
    // ---- IDLE LAYER : never a static frame ----
    tl.fromTo("#ambient-glow", { opacity: 0.3 }, { opacity: 0.7, duration: 3, ease: "sine.inOut", yoyo: true, repeat: Math.floor(D / 6) - 1 }, 0);
    function float(sel, start, amp, cycle) {
      var reps = Math.max(0, Math.floor((D - start) / cycle) - 1);
      gsap.utils.toArray(sel).forEach(function (el) {
        tl.fromTo(el, { y: 0 }, { y: amp, duration: cycle / 2, ease: "sine.inOut", yoyo: true, repeat: reps }, start);
      });
    }
    float("#content", 1.0, 8, 3.4);
    float("#pip", 1.0, -6, 3.8);
    window.__timelines = window.__timelines || @@LBRACE@@@@RBRACE@@;
    window.__timelines["@CID@"] = tl;
  </script>
</body>
</html>
"""


def local(t, seg_start):
    return round(t - seg_start, 2)


def build_reveals(short):
    seg = short["seg_start"]
    locals = [local(t, seg) for _, t in short["reveals"]]
    js = REVEAL_JS[short["type"]]
    for i, v in enumerate(locals):
        js = js.replace("{" + str(i) + "}", str(v))
    # Replace remaining bracket placeholders in apps/react types
    return (
        js.replace("[0]", str(locals[0]) if len(locals) > 0 else "0")
        .replace("[1]", str(locals[1]) if len(locals) > 1 else "0")
        .replace("[2]", str(locals[2]) if len(locals) > 2 else "0")
        .replace("[3]", str(locals[3]) if len(locals) > 3 else "0")
    )


def render(short):
    out_dir = ROOT / short["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    # Slice this short's segment out of the tightened footage into short.mp4.
    # (data-start>0 media extraction is unreliable, so each short gets its own
    # file starting at 0; the HyperFrames render stays fully deterministic.)
    src_tight = ROOT / MASTER_DIR / "tight.mp4"
    dst_short = out_dir / "short.mp4"
    if not dst_short.exists():
        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{short['seg_start']:.3f}",
            "-i",
            str(src_tight),
            "-t",
            f"{short['seg_dur']:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(dst_short),
        ]
        subprocess.run(cmd, capture_output=True)
    badge = short["id"].split("-")[0].upper()
    html = TEMPLATE
    tokens = {
        "@CID@": short["id"],
        "@TITLE@": short["title"],
        "@SUB@": short["sub"],
        "@DUR@": f"{short['seg_dur']:.2f}",
        "@BADGE@": badge,
        "@TIGHT@": TIGHT,
        "@SEGSTART@": f"{short['seg_start']:.3f}",
        "@SEGDUR@": f"{short['seg_dur']:.3f}",
        "@CONTENT@": CONTENT[short["type"]].strip("\n"),
        "@REVEALS@": build_reveals(short),
    }
    for k, v in tokens.items():
        html = html.replace(k, v)
    # restore literal braces used for the timelines registry
    html = html.replace("@@LBRACE@@", "{").replace("@@RBRACE@@", "}")
    (out_dir / "index.html").write_text(html)
    print(f"Wrote {out_dir / 'index.html'}")


def main():
    for short in SHORTS:
        render(short)


if __name__ == "__main__":
    main()
