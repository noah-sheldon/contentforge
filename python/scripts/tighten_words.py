#!/usr/bin/env python3
"""Word-accurate silence tightening using whisper word timestamps.

Cuts ONLY between words — never into a word. Each keep segment spans
[word.start - LEAD, word.end + TAIL], so word tails/heads are always
preserved. A cut happens only where the inter-word gap exceeds LEAD+TAIL
(genuinely long dead air), and the result keeps LEAD+TAIL breathing room.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration_of(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description="Word-accurate silence tightening")
    ap.add_argument("transcript", help="whisper transcript.json (word timestamps required)")
    ap.add_argument("input", help="original video/audio")
    ap.add_argument("output", help="tightened output")
    ap.add_argument("--lead", type=float, default=0.35, help="breathing pad before each word (s)")
    ap.add_argument("--tail", type=float, default=0.35, help="breathing pad after each word (s)")
    args = ap.parse_args()

    t = json.load(open(args.transcript))
    words = []
    for seg in t.get("segments", []):
        for w in seg.get("words", []):
            words.append((float(w["start"]), float(w["end"])))
    words.sort()
    if not words:
        print("Error: no word timestamps in transcript")
        sys.exit(1)

    keeps = []
    cs, ce = None, None
    for s, e in words:
        ks, ke = s - args.lead, e + args.tail
        if cs is None:
            cs, ce = ks, ke
        elif ks <= ce:
            ce = max(ce, ke)
        else:
            keeps.append((cs, ce))
            cs, ce = ks, ke
    if cs is not None:
        keeps.append((cs, ce))

    total = duration_of(args.input)
    keeps = [(max(0.0, s), min(total, e)) for s, e in keeps if e > s + 0.05]
    cut = total - sum(e - s for s, e in keeps)
    print(f"Words: {len(words)} | keep segments: {len(keeps)} | {total:.2f}s -> {total - cut:.2f}s (cut {cut:.2f}s)")

    filters = []
    for i, (s, e) in enumerate(keeps):
        filters.append(
            f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS[a{i}]"
        )
    inputs = "".join(f"[v{i}][a{i}]" for i in range(len(keeps)))
    filters.append(f"{inputs}concat=n={len(keeps)}:v=1:a=1[vout][aout]")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", args.input,
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        args.output,
    ]
    r = run(cmd)
    if r.returncode != 0:
        print(f"ffmpeg error: {r.stderr[-1500:]}")
        sys.exit(1)
    new = duration_of(args.output)
    print(f"Tightened: {total:.2f}s -> {new:.2f}s (cut {total - new:.2f}s) -> {args.output}")


if __name__ == "__main__":
    main()
