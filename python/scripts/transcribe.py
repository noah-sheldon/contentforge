#!/usr/bin/env python3
"""Transcribe a video's audio with word-level timestamps using faster-whisper.

Writes segment + word timing JSON so downstream beat-sync work can find exactly
where each topic/sentence begins in the (tightened) footage.
"""
import argparse
import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with word timestamps")
    parser.add_argument("input", help="Path to video or audio file")
    parser.add_argument("output", help="Path to output JSON")
    parser.add_argument("--model", default="small", help="Whisper model size (default small)")
    parser.add_argument("--device", default="cpu", help="cpu or cuda (default cpu)")
    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"Error: input not found: {inp}")
        sys.exit(1)

    print(f"Loading whisper model '{args.model}' ...")
    model = WhisperModel(args.model, device=args.device, compute_type="int8")

    segments, info = model.transcribe(str(inp), word_timestamps=True, vad_filter=True)
    result = {
        "language": info.language,
        "duration": round(info.duration, 3),
        "segments": [],
    }
    for seg in segments:
        words = [
            {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (seg.words or [])
        ]
        result["segments"].append({
            "id": seg.id,
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "words": words,
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Wrote {len(result['segments'])} segments -> {out}")
    for seg in result["segments"]:
        print(f"[{seg['start']:7.2f}-{seg['end']:7.2f}] {seg['text']}")


if __name__ == "__main__":
    main()
