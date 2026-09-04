#!/usr/bin/env python3
"""Tighten talking-head pacing: cut long interior silences from VIDEO + AUDIO
together (the PiP must stay synced with the voice).

Policy mirrors tighten_vo.py: pauses longer than `--cut` are trimmed to
`--keep` seconds; short silences stay whole; lead silence is trimmed to ~0.3s;
trailing silence capped at ~0.5s. Emits the old->new segment map so word
timestamps and composition anchors can be re-mapped.

Usage:
    python scripts/tighten_video.py <in.mp4> --out <tight.mp4> --map <map.json> [--keep 0.55] [--cut 0.9]
"""

import argparse
import json
import re
import subprocess


def silencedetect(
    path: str, threshold: str = "-35dB", min_dur: float = 0.35
) -> list[tuple[float, float]]:
    cmd = [
        "ffmpeg",
        "-i",
        path,
        "-af",
        f"silencedetect=noise={threshold}:d={min_dur}",
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
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--keep", type=float, default=0.55)
    ap.add_argument("--cut", type=float, default=0.9)
    args = ap.parse_args()

    KEEP = args.keep
    CUT = args.cut
    total = duration(args.video)
    silences = silencedetect(args.video)

    # Cut regions = the tail of every long silence (keep a breath of it).
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

    # Trim the LEAD-IN silence (first silence starting at ~0) to ~0.3s.
    if silences and silences[0][0] <= 0.1 and kept:
        lead_end = silences[0][1]
        kept[0] = (max(kept[0][0], lead_end - 0.3), kept[0][1])

    # Cap TRAILING silence (last silence ending at ~total) at ~0.5s.
    if silences and kept:
        last_sil = silences[-1]
        if abs(last_sil[1] - total) < 0.1:
            kept[-1] = (kept[-1][0], min(kept[-1][1], last_sil[0] + 0.5))

    # ffmpeg: concat the same kept segments across video + audio.
    parts_v, parts_a = [], []
    for i, (s, e) in enumerate(kept):
        parts_v.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}]")
        parts_a.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}]")
    n = len(kept)
    fc = (
        ";".join(parts_v + parts_a)
        + ";"
        + "".join(f"[v{i}]" for i in range(n))
        + f"concat=n={n}:v=1:a=0[vout]"
        + ";"
        + "".join(f"[a{i}]" for i in range(n))
        + f"concat=n={n}:v=0:a=1[aout]"
    )
    r = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            args.video,
            "-filter_complex",
            fc,
            "-map",
            "[vout]",
            "-map",
            "[aout]",
            "-c:v",
            "libx264",
            "-crf",
            "16",
            "-preset",
            "medium",
            "-g",
            "30",
            "-keyint_min",
            "30",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            args.out,
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"ffmpeg failed ({r.returncode})")

    mapping = []
    new_cursor = 0.0
    for s, e in kept:
        mapping.append(
            {"old_start": s, "old_end": e, "new_start": new_cursor, "new_end": new_cursor + (e - s)}
        )
        new_cursor += e - s
    with open(args.map, "w") as f:
        json.dump({"old_duration": total, "duration": new_cursor, "segments": mapping}, f, indent=2)
    print(f"kept {len(kept)} segments, {total:.2f}s -> {new_cursor:.2f}s")


if __name__ == "__main__":
    main()
