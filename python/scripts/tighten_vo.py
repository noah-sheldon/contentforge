#!/usr/bin/env python3
"""Tighten VO pacing: cut long interior silences down to a natural breath.

Keeps pauses <= keep_ms as-is; pauses longer than cut_ms are trimmed to
keep_ms. Emits the kept-segment map so word timestamps can be re-mapped.

Usage:
    python scripts/tighten_vo.py <in.wav> --out <tight.wav> --map <map.json> [--keep 0.3] [--cut 0.6]

Defaults: keep 0.55s breath, cut pauses longer than 0.9s (natural pacing).
Aggressive (short-form): --keep 0.3 --cut 0.6.
"""

import argparse
import json
import re
import subprocess


def silencedetect(path: str, threshold: str = "-38dB") -> list[tuple[float, float]]:
    cmd = [
        "ffmpeg",
        "-i",
        path,
        "-af",
        f"silencedetect=noise={threshold}:d=0.35",
        "-f",
        "null",
        "-",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def duration(path: str) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        path,
    ]
    return float(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument(
        "--keep", type=float, default=0.55, help="seconds of silence left after a long pause"
    )
    ap.add_argument("--cut", type=float, default=0.9, help="pauses longer than this get trimmed")
    args = ap.parse_args()

    KEEP = args.keep
    CUT = args.cut
    total = duration(args.audio)
    silences = silencedetect(args.audio)

    # Cut regions = the tail of every long silence (keep a breath of it).
    # Kept = the complement of all cut regions. Short silences are kept whole.
    cuts = []
    for s, e in silences:
        if e - s > CUT:
            cuts.append((s + KEEP, e))

    kept = []  # (old_start, old_end)
    cursor = 0.0
    for cs, ce in cuts:
        if cs < cursor:
            continue
        kept.append((cursor, cs))
        cursor = ce
    if cursor < total:
        kept.append((cursor, total))

    # Cap trailing silence at ~0.5s.
    if kept:
        last = kept[-1]
        speech_tail = max(last[0], last[1] - 0.5)
        kept[-1] = (last[0], speech_tail)

    # ffmpeg concat of kept segments.
    parts = []
    for i, (s, e) in enumerate(kept):
        parts.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]")
    fc = (
        ";".join(parts)
        + ";"
        + "".join(f"[a{i}]" for i in range(len(kept)))
        + "concat=n="
        + str(len(kept))
        + ":v=0:a=1[out]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            args.audio,
            "-filter_complex",
            fc,
            "-map",
            "[out]",
            "-c:a",
            "pcm_s16le",
            args.out,
        ],
        check=True,
    )

    # Emit the old->new map.
    mapping = []
    new_cursor = 0.0
    for s, e in kept:
        mapping.append(
            {"old_start": s, "old_end": e, "new_start": new_cursor, "new_end": new_cursor + (e - s)}
        )
        new_cursor += e - s
    with open(args.map, "w") as f:
        json.dump({"duration": new_cursor, "segments": mapping}, f, indent=2)
    print(f"kept {len(kept)} segments, {total:.2f}s -> {new_cursor:.2f}s")


if __name__ == "__main__":
    main()
