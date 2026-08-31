#!/usr/bin/env python3
"""Short-form video editing pipeline with self-correction.

Usage:
    python scripts/edit_video.py /path/to/footage --title "Life as a 28yo AD"
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYTHON_ROOT = PROJECT_ROOT / "python"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PYTHON_ROOT))

FPS = 30
OUTPUT_W = 1080
OUTPUT_H = 1920
OUTPUT_DIR = PROJECT_ROOT / "output" / "short-form"

os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("edit")


def run_ffmpeg(cmd: list[str], timeout: int = 300) -> bool:
    """Run ffmpeg, return True on success, False on failure."""
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
        return True
    except subprocess.CalledProcessError as e:
        log.warning(f"ffmpeg failed: {e.stderr.decode()[:200] if e.stderr else 'no output'}")
        return False
    except FileNotFoundError:
        log.warning("ffmpeg not found")
        return False


def get_clip_duration(path: str) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=10
        )
        return float(r.stdout.strip() or 0)
    except (ValueError, subprocess.TimeoutExpired):
        return 0


def crop_clip(src: str, out: str, duration: float) -> bool:
    """Scale to 1080x1920 9:16. Lanczos for quality. CRF 18."""
    return run_ffmpeg([
        "ffmpeg", "-i", src, "-t", str(duration),
        "-vf", f"scale={OUTPUT_W}:{OUTPUT_H}:flags=lanczos",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", out
    ])


def build_edit(clips: list[Path], output_path: str, total_duration: float = 25) -> Optional[str]:
    """Build edit from cropped clips. Self-corrects: skips bad clips."""
    cropped_dir = OUTPUT_DIR / "clips"
    cropped_dir.mkdir(parents=True, exist_ok=True)
    cropped_paths = []

    per_clip = total_duration / max(len(clips), 1)

    for i, clip in enumerate(clips):
        dur = get_clip_duration(str(clip))
        if dur < 1:
            log.warning(f"  Skipping short/bad clip: {clip.name} ({dur:.1f}s)")
            continue
        out = cropped_dir / f"clip_{i:02d}.mp4"
        if crop_clip(str(clip), str(out), min(per_clip, dur)):
            cropped_paths.append(str(out))
        else:
            log.warning(f"  Skipping failed clip: {clip.name}")
            total_duration -= per_clip  # Adjust total

    if len(cropped_paths) < 1:
        log.error("No usable clips. Cannot build edit.")
        return None

    per_clip = total_duration / max(len(cropped_paths), 1)

    filter_parts = []
    inputs = []
    for i in range(len(cropped_paths)):
        inputs.extend(["-i", str(cropped_paths[i])])
        fade_out = per_clip - 0.5
        filter_parts.append(
            f"[{i}]fade=t=in:st=0:d=0.5,fade=t=out:st={fade_out}:d=0.5[v{i}]"
        )

    filter_str = ";".join(filter_parts)
    concat_str = "".join(f"[v{i}]" for i in range(len(cropped_paths)))
    filter_str += f";{concat_str}concat=n={len(cropped_paths)}:v=1:a=0[out]"

    if run_ffmpeg(
        ["ffmpeg"] + inputs + [
            "-filter_complex", filter_str,
            "-map", "[out]", "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", output_path
        ]
    ):
        return output_path
    return None


def render_overlay(scenes: list[dict], header: str, output_path: str) -> Optional[str]:
    """Retired — overlays are now authored inside HyperFrames compositions
    (see templates/short-form/), not rendered as a separate alpha layer."""
    log.warning("Overlay rendering retired: HUD overlays are built into HyperFrames compositions.")
    return None


def composite(video: str, output_path: str, overlay: Optional[str] = None, audio: Optional[str] = None) -> Optional[str]:
    """Composite video + optional overlay (blend average) + optional audio."""
    inputs = ["-i", video]

    if overlay and Path(overlay).exists():
        inputs.extend(["-i", overlay])
        filter_parts = [
            "[0:v]setpts=PTS-STARTPTS[bg]",
            f"[1:v]format=yuva444p10le,setpts=PTS-STARTPTS[fg]",
            "[bg][fg]blend=average[v]",
        ]
        video_map = "[v]"
    else:
        filter_parts = []
        video_map = "[0:v]"

    if audio and Path(audio).exists():
        inputs.extend(["-i", audio])
        cmd = ["ffmpeg"] + inputs + [
            "-filter_complex", ";".join(filter_parts),
            "-map", video_map, "-map", "2:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", output_path,
        ]
    else:
        cmd = ["ffmpeg"] + inputs + [
            "-filter_complex", ";".join(filter_parts),
            "-map", video_map,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            output_path,
        ]

    if run_ffmpeg(cmd):
        return output_path
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/edit_video.py /path/to/footage [--title 'Title']")
        sys.exit(1)

    src = Path(sys.argv[1])
    title = "LIFE AS A 28 YEAR OLD ASSOCIATE DIRECTOR"
    if "--title" in sys.argv:
        idx = sys.argv.index("--title")
        title = sys.argv[idx + 1]

    clips = sorted(src.glob("*.MP4")) + sorted(src.glob("*.mp4"))
    if not clips:
        log.error(f"No MP4 files found in {src}")
        sys.exit(1)

    log.info(f"Found {len(clips)} clips")
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Pick clips
    selected = []
    if len(clips) >= 6:
        indices = [0, len(clips)//4, len(clips)//2, 3*len(clips)//4, -1]
    elif len(clips) >= 3:
        indices = [0, len(clips)//2, -1]
    else:
        indices = list(range(len(clips)))
    for i in indices:
        selected.append(clips[i])
    log.info(f"Selected {len(selected)} clips")

    # Step 1: Build edit (self-corrects, skips bad clips)
    edit_path = str(run_dir / "edit.mp4")
    edit_result = build_edit(selected, edit_path)
    if not edit_result:
        log.error("Edit failed. No output.")
        sys.exit(1)
    log.info("Edit built")

    # Get edit duration
    edit_duration = get_clip_duration(edit_path)
    if edit_duration < 1:
        log.error("Edit has no duration. Aborting.")
        sys.exit(1)
    total_frames = int(edit_duration * FPS)

    # Step 2: Build scene list (overlay retired — captions live in the composition)
    per_scene = total_frames // max(len(selected), 1)
    scenes = []
    captions = [
        title.upper(),
        "COMMUTE  •  LONDON",
        "MODEL DESIGN  •  DESK",
        "TEAM STANDUP  •  CONFERENCE",
        "GOLDEN HOUR  •  FINISH",
    ]
    for i in range(min(len(selected), len(captions))):
        parts = captions[i].split("  •  ")
        scenes.append({
            "startFrame": i * per_scene,
            "endFrame": (i + 1) * per_scene,
            "title": parts[0],
            "subtitle": parts[1] if len(parts) > 1 else "",
        })

    # Step 3: Render overlay (self-corrects, skips if fails)
    header = f"CANARY WHARF  •  {datetime.now().strftime('%Y.%m.%d')}  •  WORK_DAY"
    overlay_path = str(run_dir / "overlay.mov")
    overlay_result = render_overlay(scenes, header, overlay_path)
    if overlay_result:
        log.info("Overlay rendered")
    else:
        log.info("No overlay -- continuing with text-free edit")

    # Step 4: Download music (optional, Pixabay handles its own failures)
    audio_path = None
    try:
        from services.pixabay import get_background_music
        audio_path = get_background_music(str(run_dir), mood="ambient")
        if audio_path:
            log.info(f"Audio: {audio_path}")
    except Exception as e:
        log.warning(f"Audio download failed: {e}")

    # Step 5: Composite (self-corrects, falls back gracefully)
    final = str(run_dir / "final.mp4")
    result = composite(edit_path, final, overlay_result, audio_path)
    if result:
        log.info(f"Done: {final}")
        subprocess.run(["ls", "-lh", final])
    else:
        # Fallback: copy edit without overlays
        log.warning("Composite failed. Copying raw edit as output.")
        import shutil
        shutil.copy2(edit_path, final)
        log.info(f"Fallback output: {final}")


if __name__ == "__main__":
    main()
