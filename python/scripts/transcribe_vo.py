#!/usr/bin/env python3
"""Transcribe a VO recording with word timestamps via faster-whisper.

Usage:
    python scripts/transcribe_vo.py <audio> --out <transcript.json> [--model small.en|medium.en]

Saves word-level timestamps (project data — preserve transcript.json) and
prints a readable segment transcript.
"""
import argparse
import json

from faster_whisper import WhisperModel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", help="input audio file (m4a/wav/mp3)")
    ap.add_argument("--out", required=True, help="output transcript.json path")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--compute-type", default="int8")
    args = ap.parse_args()

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(args.audio, word_timestamps=True, vad_filter=True)

    out = {
        "source": args.audio,
        "language": info.language,
        "duration": round(info.duration, 3),
        "segments": [],
    }
    for seg in segments:
        words = [
            {"w": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (seg.words or [])
        ]
        out["segments"].append(
            {
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip(),
                "words": words,
            }
        )

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    for seg in out["segments"]:
        print(f"[{seg['start']:7.2f}-{seg['end']:7.2f}] {seg['text']}")


if __name__ == "__main__":
    main()
