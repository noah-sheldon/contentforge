#!/usr/bin/env python3
"""Tighten a single-take talking-head recording by removing detected silences.

Runs ffmpeg silencedetect on the audio, builds keep-segments (speech + a small
breathing pad on each side), and re-encodes the trimmed result so the narration
flows without long dead air. Output keeps original resolution/fps with AAC audio.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_NOISE_DB = -32
DEFAULT_MIN_SILENCE = 0.6
DEFAULT_PAD = 0.15


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def detect_silences(input_path, noise_db, min_silence):
    """Return a list of (start, end) silence intervals from silencedetect output."""
    af = f"silencedetect=noise={noise_db}dB:d={min_silence}"
    result = run(["ffmpeg", "-hide_banner", "-i", str(input_path), "-af", af, "-f", "null", "-"])
    if result.returncode != 0:
        print(f"FFmpeg silencedetect failed: {result.stderr}")
        sys.exit(1)

    silences = []
    starts = {}
    for line in result.stderr.splitlines():
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            starts[float(m.group(1))] = None
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m:
            end = float(m.group(1))
            for s in list(starts.keys()):
                if starts[s] is None:
                    starts[s] = end
                    silences.append((s, end))
                    break
    return sorted(silences)


def duration_of(input_path):
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(input_path),
        ]
    )
    return float(result.stdout.strip())


def build_segments(silences, total, pad):
    """Return list of (start, end) keep-segments after dropping silenced gaps."""
    keep = []
    cursor = 0.0
    for s, e in silences:
        if s <= cursor:
            continue
        keep_end = max(cursor, s - pad)
        if keep_end > cursor + 0.05:
            keep.append((cursor, keep_end))
        cursor = e + pad
    if cursor < total - 0.05:
        keep.append((cursor, total))
    return keep


def main():
    parser = argparse.ArgumentParser(
        description="Remove silences from a talking-head master recording"
    )
    parser.add_argument("input", help="Path to the master 16:9 recording")
    parser.add_argument("output", help="Path to the tightened output video")
    parser.add_argument(
        "--noise-db",
        type=float,
        default=DEFAULT_NOISE_DB,
        help="Silence threshold in dB (default -32)",
    )
    parser.add_argument(
        "--min-silence",
        type=float,
        default=DEFAULT_MIN_SILENCE,
        help="Min silence duration to cut, seconds (default 0.6)",
    )
    parser.add_argument(
        "--pad",
        type=float,
        default=DEFAULT_PAD,
        help="Speech pad to preserve around cuts, seconds (default 0.15)",
    )
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output)
    if not inp.exists():
        print(f"Error: input not found: {inp}")
        sys.exit(1)

    total = duration_of(inp)
    silences = detect_silences(inp, args.noise_db, args.min_silence)
    print(f"Detected {len(silences)} silences in {total:.2f}s")

    segments = build_segments(silences, total, args.pad)
    print(f"Keep segments: {len(segments)}")

    if len(segments) == 1 and segments[0][0] < 0.05 and segments[0][1] >= total - 0.05:
        print("No silence found to cut; copying input as-is.")
        out.parent.mkdir(parents=True, exist_ok=True)
        run(["cp", str(inp), str(out)])
        return

    filters = []
    for i, (s, e) in enumerate(segments):
        filters.append(
            f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS[a{i}]"
        )
    inputs = "".join(f"[v{i}][a{i}]" for i in range(len(segments)))
    filters.append(f"{inputs}concat=n={len(segments)}:v=1:a=1[vout][aout]")

    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(inp),
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out),
    ]
    print(f"Executing: {' '.join(cmd[:8])} ...")
    result = run(cmd)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr[-2000:]}")
        sys.exit(1)

    new_dur = duration_of(out)
    print(f"Tightened: {total:.2f}s -> {new_dur:.2f}s (cut {total - new_dur:.2f}s) -> {out}")


if __name__ == "__main__":
    main()
