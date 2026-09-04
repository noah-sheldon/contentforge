#!/usr/bin/env python3
"""Audio engineering pass for a talking-head narration track.

Applies cleanup (high-pass, noise reduction), voice EQ (presence lift),
dynamic control (compression + limiter), and loudness normalization
(YouTube target: -14 LUFS, true peak <= -1.0 dBTP). Writes a processed
audio file ready to mux onto the rendered overlay.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(
        description="Engineer narration audio (cleanup -> EQ -> dynamics -> loudness)"
    )
    parser.add_argument("input", help="Source video (or audio) with the narration")
    parser.add_argument("output", help="Output engineered audio file (e.g. master_audio.m4a)")
    parser.add_argument(
        "--lufs", default=-14, help="Integrated loudness target in LUFS (default -14 for YouTube)"
    )
    parser.add_argument(
        "--true-peak", default=-1.0, help="True peak ceiling in dBTP (default -1.0)"
    )
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output)
    if not inp.exists():
        print(f"Error: input not found: {inp}")
        sys.exit(1)

    out.parent.mkdir(parents=True, exist_ok=True)

    # ------- ffmpeg audio filter chain -------
    # 1. Cleanup: rumble removal + adaptive denoise
    # 2. EQ: presence lift around 3kHz for intelligibility
    # 3. Dynamics: gentle compression then a hard limiter
    # 4. Loudness: normalize to target, clamp true peak
    afilter = (
        "highpass=f=90:t=q,"
        "afftdn=nr=12:nf=-40,"
        "equalizer=f=3000:t=q:w=1:g=3,"
        "equalizer=f=120:t=q:w=1.2:g=1.5,"
        f"acompressor=threshold=-20dB:ratio=3:attack=15:release=120:makeup=2dB,"
        f"alimiter=limit={args.true_peak:.1f}dB,"
        f"loudnorm=I={args.lufs}:TP={args.true_peak}:LRA=11"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(inp),
        "-vn",
        "-af",
        afilter,
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out),
    ]
    print("Running audio engineering pass...")
    result = run(cmd)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr[-2000:]}")
        sys.exit(1)

    probe = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_name",
            "-of",
            "json",
            str(out),
        ]
    )
    print(f"Engineered audio -> {out} ({probe.stdout.strip()})")


if __name__ == "__main__":
    main()
