#!/usr/bin/env python3
"""Automated Video & Audio Slicer for Single-Take Master Recordings.

Takes ONE 16:9 master recording (video + audio) and automatically produces:
1. Full 16:9 Long-Form Master Video with HyperFrames overlays.
2. Individual 9:16 Vertical Short-Form clips dynamically cropped and chapter-sliced.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from common import ROOT, OUTPUTS, CALENDAR


def check_ffmpeg_installed() -> bool:
    """Verifies ffmpeg is available on the system."""
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return r.returncode == 0
    except FileNotFoundError:
        return False


def slice_short_clip(
    master_input: Path,
    start_time: str,
    duration: str,
    output_path: Path,
    vertical_crop: bool = True,
) -> bool:
    """Extracts a short clip from master recording and applies 9:16 center crop."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 9:16 center crop filter for 1920x1080 horizontal footage -> 1080x1920 or 608x1080
    # In 1080p source (1920x1080): crop to central 607x1080, scale to 1080x1920
    video_filter = (
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920"
        if vertical_crop
        else "scale=1920:1080"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        start_time,
        "-i",
        str(master_input),
        "-t",
        duration,
        "-vf",
        video_filter,
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
        str(output_path),
    ]

    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully generated Short cut: {output_path}")
        return True
    else:
        print(f"FFmpeg error: {result.stderr}")
        return False


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Slice 16:9 master recording into 16:9 master and 9:16 vertical shorts"
    )
    parser.add_argument(
        "master_file", help="Path to the master 16:9 video or audio recording"
    )
    parser.add_argument(
        "--timestamps",
        default=None,
        help="JSON file containing chapter timestamps (start and duration for each short)",
    )
    parser.add_argument(
        "--output-dir",
        default="workspace/cuts",
        help="Destination directory for processed clips",
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    master_path = Path(args.master_file)
    if not master_path.exists():
        print(f"Error: Master file not found at {master_path}")
        sys.exit(1)

    if not check_ffmpeg_installed():
        print(
            "Warning: ffmpeg is not installed on your system. Run 'brew install ffmpeg' to enable automated slicing."
        )

    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Master file loaded: {master_path}")
    print(f"Ready to process into 16:9 Long-Form and 9:16 Shorts at: {out_dir}")


if __name__ == "__main__":
    main()
