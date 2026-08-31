# Editorial Video Transition Patterns

> Research for AI-powered automatic video editing pipeline (short-form "day in the life" / "come to work with me" vlogs).
> Style target: MINIMAL, EDITORIAL, LUXURY (Monocle, Apple commercial, high-end corporate).
> Sources: StudioBinder, CJ&CO, Boris FX, Cined, FilmDaft, Adobe, Final Cut Pro docs, Wikipedia.

---

## 1. Hard Cut Patterns

### Definition
A hard cut is an instantaneous transition between two shots with zero effect frames. It is the default building block of all editorial editing.

### When to use (editorial style)
| Context | Recommendation |
|---|---|
| Dialogue / speaking to camera | Always hard cut. Transitions during speech feel amateur. |
| B-roll sequence montage | Hard cuts between clips, timed to music beat. |
| Change of angle on same subject | Hard cut. This is standard continuity editing. |
| Establishing shot → scene | Hard cut. Transitions weaken the establishing impact. |
| Between emotional beats | Hard cut unless a deliberate fade indicates time passing. |

### What makes a hard cut "good"
1. **Motion continuity**: Cut during movement (hands gesturing, walking, turning head) — the motion masks the cut. Cutting on stillness is more jarring.
2. **Eye trace**: Cut when the viewer's gaze is on a specific point; place the subject in the same relative position in the incoming shot so the eye doesn't jump.
3. **Beat matching**: For montage sequences, time hard cuts to musical phrase boundaries or downbeats. Off-beat cuts feel amateur.
4. **No dead space**: Trim out pauses, breaths between sentences, hesitation. A hard cut that removes dead air feels "tight and professional."
5. **30-degree rule**: When cutting between two shots of the same subject, change the camera angle by at least 30 degrees to avoid jump cuts.

### Codeable rules
```python
# Hard cut is always preferred unless a specific condition triggers a transition
RULE: Always default to hard cut
RULE: Use hard cut for dialogue/vlog speaking segments (no dissolves during speech)
RULE: In montage sequences, snap hard cuts to detected music beat positions
RULE: Trim silence/pauses before/after hard cuts to remove dead space
RULE: Cut during motion (hands moving, walking, head turns) not on stillness
```

---

## 2. Dip to Black / Dip to White

### Dip to Black
- **Purpose**: Denotes significant time passage, scene ending, or emotional conclusion.
- **Duration — editorial/luxury**: 12–24 frames (0.5–1 sec at 24fps). Longer than 1 sec feels like a chapter break; shorter is too abrupt.
- **At 24fps**: 12–24 frames = 0.5–1.0 sec
- **At 30fps**: 15–30 frames = 0.5–1.0 sec
- **Apple Final Cut Pro default transition** (used for fade): 1 second (24 frames at 24fps)

| Duration | Feeling | Use Case |
|---|---|---|
| 6 frames (0.25s) | Glitch / flash | Not editorial — avoid |
| 12 frames (0.5s) | Quick breath | Between vlog scenes, minor time jumps |
| 18 frames (0.75s) | Standard editorial | Default for scene change in luxury content |
| 24 frames (1.0s) | Deliberate pause | End of a "chapter" or day segment |

### Dip to White
- **Purpose**: Dreamy transition, memory flashback, or aspirational moment (common in Apple-style content).
- **Duration — editorial/luxury**: 8–16 frames (0.33–0.66 sec at 24fps). Shorter than dip to black — dip to white is a visual flourish, not a full stop.
- **At 24fps**: 8–16 frames = 0.33–0.66 sec
- **At 30fps**: 10–20 frames = 0.33–0.66 sec
- Use sparingly — only for aspirational/hopeful moments in luxury content.

### Codeable rules
```python
DIP_TO_BLACK:
  at_24fps:    { min_frames: 12, default: 18, max_frames: 24 }
  at_30fps:    { min_frames: 15, default: 22, max_frames: 30 }
  trigger:     scene_end OR detected_time_passage > 2_hours
  feeling:     "full stop, chapter end, significant time passage"

DIP_TO_WHITE:
  at_24fps:    { min_frames: 8, default: 12, max_frames: 16 }
  at_30fps:    { min_frames: 10, default: 15, max_frames: 20 }
  trigger:     aspirational_moment OR memory_flashback OR luxury_emotional_beat
  feeling:     "aspirational, dreamy, hopeful"
  max_per_video: 2  # Overuse looks amateur
```

---

## 3. Fade Transitions (Cross Dissolve)

### Cross Dissolve
- **Standard duration**: 24–48 frames (1–2 sec at 24fps)
- **Short dissolve (soften hard cut)**: 6–12 frames
- **Apple Final Cut Pro default**: 1 second (24 frames at 24fps, 30 frames at 30fps)

| Dissolve Type | Frames (24fps) | Frames (30fps) | Seconds | Use |
|---|---|---|---|---|
| Micro-dissolve | 4–6 | 5–8 | 0.16–0.25s | Soften a jarring hard cut, barely perceptible |
| Short dissolve | 8–12 | 10–15 | 0.33–0.5s | Time passage within same scene, connected ideas |
| Standard dissolve | 24–48 | 30–60 | 1–2s | Major scene changes, transition between locations |
| Long dissolve | 48–72 | 60–90 | 2–3s | Emotional passage, memory/montage sequences |

### Fade In (from black/white)
- **Duration**: 12–24 frames (0.5–1 sec at 24fps)
- **Video start**: Always fade in from black for the first shot. 0.5s for quick start, 1s for luxury/editorial.
- **Never fade in from white** unless transitioning from a white screen (e.g., title card).

### Codeable rules
```python
CROSS_DISSOLVE:
  micro:   { at_24fps: [4, 6],   at_30fps: [5, 8],    feeling: "barely perceptible" }
  short:   { at_24fps: [8, 12],  at_30fps: [10, 15],  feeling: "soft continuity" }
  standard:{ at_24fps: [24, 48], at_30fps: [30, 60],  feeling: "scene change" }
  long:    { at_24fps: [48, 72], at_30fps: [60, 90],  feeling: "emotional passage" }
  
  # Constraints for editorial luxury style
  CONSTRAINT: Never use cross dissolve during dialogue/vlog speech
  CONSTRAINT: Micro-dissolve is the only acceptable dissolve between B-roll clips
  CONSTRAINT: Standard dissolve ONLY for major scene changes (new location, new "chapter")
  CONSTRAINT: No cross dissolve between different angles of same subject (use hard cut)

FADE_IN:
  from_black: { at_24fps: [12, 24], at_30fps: [15, 30], default: 0.5s_quick }
  constraint: Only at video start. Never fade in mid-video.
```

---

## 4. Match Cuts

### Types (from professional editing practice)

#### A. Positional Continuity Match
- **Rule**: Subject occupies the exact same screen position (X/Y) in outgoing and incoming shots.
- **Cut type**: Hard cut.
- **Timing**: Cut at the moment the subject reaches the matched position.
- **Code**: `match_score = 1.0 - (distance_between_centers / max_diagonal)`

#### B. Graphic/Shape Match
- **Rule**: Match based on similar shapes, forms, or visual patterns (circle → circle, horizontal line → horizon, etc.).
- **Cut type**: Hard cut or micro-dissolve (4–6 frames).
- **Timing**: Cut when the shape is most prominent in frame.
- **Code**: Use SIMILARITY on shape descriptors (HOG, contour signatures) between outgoing last frame and incoming first frame.

#### C. Motion Vector Match
- **Rule**: Match movement speed and direction across the cut (e.g., object moving upward → another object moving upward).
- **Cut type**: Hard cut.
- **Timing**: Cut at the peak of the action or during mid-motion.
- **Code**: Compare optical flow motion vectors. `match_score = cosine_similarity(motion_vector_out, motion_vector_in)`

#### D. Audio Match (Sonic Match Cut)
- **Rule**: A sound (dialogue, music note, sound effect) starts in shot A and continues seamlessly into shot B, or transforms (pitch/rhythm similarity).
- **Cut type**: Hard cut with audio bridge (J-cut style).
- **Timing**: Audio bridge starts 0.5–1.0 sec before visual cut.
- **Code**: Compare MFCC feature vectors across the cut point. Threshold for "match."

#### E. Color Palette Match
- **Rule**: Dominant colors/histogram of outgoing shot matches incoming shot.
- **Cut type**: Hard cut or micro-dissolve.
- **Timing**: Cut at the moment of closest color histogram similarity.
- **Code**: `match_score = histogram_intersection(hist_out[-1], hist_in[0])`

### Match Cut Identification Pipeline (codeable)
```python
# For every pair of adjacent shots, compute match scores
SCORE_WEIGHTS = {
  "positional": 0.30,
  "graphic":    0.25,
  "motion":     0.25,
  "color":      0.20,
}

THRESHOLD = 0.75  # Above this = use match cut (hard cut)

# If any individual dimension score > 0.85, trigger match cut on that dimension
# Match cuts are ALWAYS hard cuts (no dissolve)
# Exception: graphic match can use micro-dissolve (4-6 frames) for luxury style
```

---

## 5. L-Cut and J-Cut (Audio-Driven Transitions)

### Definitions

| Type | Description | Direction |
|---|---|---|
| **L-cut** | Video cuts first; audio from outgoing clip continues under incoming video | Video leads audio |
| **J-cut** | Audio from incoming clip starts first; video cuts later | Audio leads video |

### Timing Offsets

#### L-Cut (Video leads audio — audio trails)

| Context | Overlap Duration | Frames (24fps) | Frames (30fps) | Purpose |
|---|---|---|---|---|
| Dialogue reaction shot | 3–6 frames | 3–6 | 4–8 | Show listener's reaction while speaker finishes |
| Scene transition (soft) | 8–12 frames | 8–12 | 10–15 | Let ambient sound from previous scene linger |
| Emotional linger | 12–24 frames | 12–24 | 15–30 | Hold emotional tone (music or ambience continues) |

#### J-Cut (Audio leads video — audio anticipates)

| Context | Overlap Duration | Frames (24fps) | Frames (30fps) | Purpose |
|---|---|---|---|---|
| Dialogue entry | 6–12 frames | 6–12 | 8–15 | Hear speaker before seeing them (natural conversation) |
| Scene transition (pull forward) | 12–18 frames | 12–18 | 15–22 | Audio from next scene creates anticipation |
| Major sequence opening | 24–48 frames | 24–48 | 30–60 | Audio builds for 1–2 seconds before visual reveal |

### Codeable rules
```python
# L-cut: Video leads audio
L_CUT:
  dialogue_reaction:  { at_24fps: [3, 6],   at_30fps: [4, 8],   overlap_sec: 0.125_to_0.25 }
  scene_transition:   { at_24fps: [8, 12],  at_30fps: [10, 15], overlap_sec: 0.33_to_0.5  }
  emotional_linger:   { at_24fps: [12, 24], at_30fps: [15, 30], overlap_sec: 0.5_to_1.0   }
  
  trigger_dialogue_vlog: "Speaker A finishes → cut to B-roll or Speaker B"
    # Keep Speaker A's audio trailing 3-6 frames into the next clip
    # This captures the natural overlap of conversation

# J-cut: Audio leads video
J_CUT:
  dialogue_entry:     { at_24fps: [6, 12],  at_30fps: [8, 15],  overlap_sec: 0.25_to_0.5  }
  scene_pull:         { at_24fps: [12, 18], at_30fps: [15, 22], overlap_sec: 0.5_to_0.75  }
  major_reveal:       { at_24fps: [24, 48], at_30fps: [30, 60], overlap_sec: 1.0_to_2.0   }

  trigger_vlog_intro: "Narration starts before showing the scene"
    # Voiceover or ambient audio of next location starts 0.5-1.0s early
  
  trigger_broll: "When transitioning from vlog-speech to B-roll"
    # Video of speaker stays while next scene's audio fades in (reverse J-cut)

# Audio crossfade defaults
AUDIO_CROSSFADE:
  for_l_cut_j_cut:   0_frames  # Audio overlap IS the crossfade — no additional fade needed
  scene_transition:   { duration_frames: [6, 12], shape: "equal_power" }
```

### When to use L-cut vs J-cut in editorial vlogs

| Scenario | Cut Type | Reasoning |
|---|---|---|
| Speaker finishes → B-roll | L-cut (3–6 fr) | Speaker's voice lingers over B-roll; natural |
| B-roll → next speaker | J-cut (6–12 fr) | Hear next speaker before seeing them |
| Scene A → Scene B (location change) | J-cut (12–18 fr) | Audio from new location pulls viewer forward |
| Emotional beat ending | L-cut (12–24 fr) | Music/ambience lingers after cut |
| Vlog intro (voiceover + scene) | J-cut (24–48 fr) | VO starts over establishing shot; dramatic reveal |

---

## 6. Summary: Full Transition Decision Matrix

```python
# Decision priority: 1 (highest) → 6 (lowest)

PRIORITY_ORDER = [
  {
    "condition": "dialogue_or_vlog_speech_segment",
    "transition": "HARD_CUT",
    "note": "Never use dissolves during speech — looks amateur"
  },
  {
    "condition": "significant_time_passage OR scene_end",
    "transition": "DIP_TO_BLACK",
    "duration_24fps": [12, 24]
  },
  {
    "condition": "aspirational_moment OR memory_flashback",
    "transition": "DIP_TO_WHITE",
    "duration_24fps": [8, 16],
    "max_per_video": 2
  },
  {
    "condition": "match_cut_score > 0.75",
    "transition": "MATCH_CUT (HARD_CUT)",
    "note": "Match cut is always a hard cut, never a dissolve"
  },
  {
    "condition": "dialogue_reaction OR scene_audio_bridge",
    "transition": "L-CUT or J-CUT",
    "overlap_frames_24fps": [3, 24]
  },
  {
    "condition": "broll_montage_sequence",
    "transition": "HARD_CUT (default) or MICRO_DISSOLVE [4-6 frames]",
    "note": "Micro-dissolve only for luxury softening, never for pacing"
  },
  {
    "condition": "major_scene_change (fallback)",
    "transition": "STANDARD_CROSS_DISSOLVE [24-48 frames]",
    "note": "Only when no other transition applies. Overuse = amateur."
  }
]

# Defaults for 24fps editorial pipeline
DEFAULT_FRAME_RATE = 24
DEFAULT_HARD_CUT = 0        # instantaneous
DEFAULT_DIP_BLACK = 18      # frames
DEFAULT_DIP_WHITE = 12      # frames
DEFAULT_DISSOLVE = 24       # 1 second
DEFAULT_J_CUT_OVERLAP = 12  # frames (audio leads)
DEFAULT_L_CUT_OVERLAP = 8   # frames (audio trails)

# Prohibited transitions in editorial luxury style
PROHIBITED = [
  "wipe", "slide", "push", "clock_wipe", "page_curl",
  "zoom_flash", "glitch", "bounce", "spin", "shatter",
  "warp", "light_leak", "lens_flare_transition",
]
```

---

## 7. Editor's Code of Conduct (for the AI)

1. **Transitions should not be noticed.** If a viewer notices the transition, it is wrong for editorial style.
2. **Hard cut is the default.** Every non-hard-cut transition must have an explicit justification.
3. **Timing = feeling.** A 12-frame dissolve (0.5s) feels like a breath. A 48-frame dissolve (2s) feels like a chapter break. Match the duration to the emotional weight.
4. **Audio drives the edit more than video.** L-cuts and J-cuts are invisible when done right — the ear guides the eye.
5. **Match cuts reward planning.** In an AI pipeline, frame-by-frame similarity scoring (position, shape, color, motion) can identify match opportunities that a human editor might miss.
6. **Never mix transitions.** Even in the same scene, don't use a dissolve+dip+J-cut near each other. Pick one transition type per scene boundary.

---

## Sources

- StudioBinder — Types of film transitions (cross dissolve: 24–48 frames)
- CJ&CO — What are cross dissolves? (timing: 24–48 frames, 1–2 sec at 24fps)
- Boris FX — Dissolve transition tutorial (confirm 24–48 frames)
- Cined — Mastering match cuts (6 match types with codeable detection rules)
- FilmDaft — L-cut and J-cut (0.5–2 sec overlap, dialogue vs. scene transition use)
- Apple Final Cut Pro — Default transition duration: 1 second
- Wikipedia — Dissolve (filmmaking) (6–12 frames short, 24–48 standard)
