#!/usr/bin/env python3
"""Professional VO cleanup: noise reduction, breath softening, loudness.

Time-invariant — durations are preserved, so word timestamps stay valid.
Chain: highpass (rumble) -> anlmdn (speech noise reduction) -> agate
(gentle breath ducking) -> loudnorm (-14 LUFS).

Usage:
    python scripts/clean_vo.py <in.wav> --out <clean.wav>
"""

import argparse
import subprocess


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    chain = (
        "highpass=f=70,"
        "afftdn=nr=8:nf=-30,"
        "agate=threshold=-38dB:attack=8:release=180:ratio=3:makeup=1,"
        "loudnorm=I=-14:TP=-1.5:LRA=11"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            args.audio,
            "-af",
            chain,
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            args.out,
        ],
        check=True,
    )
    print("wrote", args.out)


if __name__ == "__main__":
    main()
