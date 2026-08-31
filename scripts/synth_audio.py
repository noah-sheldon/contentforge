#!/usr/bin/env python3
"""Synthesize a unique music bed + SFX palette per video preset.

Zero external assets: every preset generates its own chords, texture,
and sound effects. Outputs WAV files into <outdir>.

Usage: python3 scripts/synth_audio.py <preset> <outdir>
Presets: warm, upbeat, ambient, corporate, tense, funk, confident
"""

import math
import os
import random
import struct
import sys
import wave

RATE = 44100

PRESETS = {
    "warm": {
        "chords": [[110.0, 130.81, 164.81, 196.0], [87.31, 110.0, 130.81, 164.81],
                   [130.81, 164.81, 196.0, 246.94], [98.0, 123.47, 146.83, 196.0]],
        "chord_secs": 2.5, "wave": "sine", "arp": 0, "detune": 0.3,
        "attack": 0.5, "release": 0.8, "body": 0.35,
        "sfx": {"stamp": 85, "rip": 0.55, "sweep": (500, 3400), "tick": 3100,
                "chime": (1180, 1760), "boom": 68},
    },
    "upbeat": {
        "chords": [[220.0, 261.63, 329.63, 392.0], [174.61, 220.0, 261.63, 329.63],
                   [196.0, 246.94, 293.66, 392.0], [146.83, 196.0, 220.0, 293.66]],
        "chord_secs": 2.5, "wave": "sine", "arp": 4, "detune": 0.45,
        "attack": 0.3, "release": 0.6, "body": 0.13,
        "sfx": {"stamp": 130, "rip": 0.3, "sweep": (900, 5200), "tick": 4200,
                "chime": (1560, 2340), "boom": 95},
    },
    "ambient": {
        "chords": [[130.81, 196.0, 246.94, 293.66], [110.0, 164.81, 220.0, 261.63],
                   [98.0, 146.83, 196.0, 246.94], [87.31, 130.81, 174.61, 220.0]],
        "chord_secs": 2.5, "wave": "sine", "arp": 0, "detune": 0.9,
        "attack": 1.0, "release": 1.2, "body": 0.30,
        "sfx": {"stamp": 70, "rip": 0.7, "sweep": (300, 2200), "tick": 2600,
                "chime": (880, 1320), "boom": 55},
    },
    "corporate": {
        "chords": [[196.0, 246.94, 293.66, 392.0], [174.61, 220.0, 261.63, 349.23],
                   [146.83, 196.0, 246.94, 329.63], [164.81, 220.0, 261.63, 392.0]],
        "chord_secs": 2.5, "wave": "pulse", "arp": 4, "detune": 0.1,
        "attack": 0.02, "release": 0.12, "body": 0.20,
        "sfx": {"stamp": 115, "rip": 0.25, "sweep": (700, 4000), "tick": 3800,
                "chime": (1320, 1980), "boom": 80},
    },
    "tense": {
        "chords": [[110.0, 138.59, 164.81, 207.65], [103.83, 130.81, 155.56, 196.0],
                   [116.54, 146.83, 174.61, 220.0], [98.0, 123.47, 146.83, 185.0]],
        "chord_secs": 2.5, "wave": "sine", "arp": 0, "detune": 1.4,
        "attack": 0.8, "release": 1.0, "body": 0.28,
        "sfx": {"stamp": 62, "rip": 0.9, "sweep": (200, 1800), "tick": 2100,
                "chime": (740, 1110), "boom": 48},
    },
    "funk": {
        "chords": [[196.0, 293.66, 392.0, 493.88], [174.61, 261.63, 349.23, 440.0],
                   [164.81, 246.94, 329.63, 415.3], [146.83, 220.0, 293.66, 369.99]],
        "chord_secs": 2.5, "wave": "pulse", "arp": 12, "detune": 0.3,
        "attack": 0.01, "release": 0.1, "body": 0.24,
        "sfx": {"stamp": 140, "rip": 0.2, "sweep": (1100, 6000), "tick": 4600,
                "chime": (1750, 2625), "boom": 105},
    },
    "confident": {
        "chords": [[130.81, 196.0, 261.63, 329.63], [110.0, 164.81, 220.0, 277.18],
                   [98.0, 146.83, 196.0, 246.94], [123.47, 185.0, 246.94, 329.63]],
        "chord_secs": 2.5, "wave": "pulse", "arp": 6, "detune": 0.2,
        "attack": 0.03, "release": 0.18, "body": 0.26,
        "sfx": {"stamp": 105, "rip": 0.35, "sweep": (600, 4600), "tick": 3600,
                "chime": (1240, 1860), "boom": 75},
    },
}


def tone(freq, dur, wave="sine", attack=0.01, release=0.05, detune=0.0):
    n = int(dur * RATE)
    out = []
    for i in range(n):
        t = i / RATE
        env = min(1.0, t / max(attack, 0.001))
        env = min(env, max(0.0, (dur - t) / max(release, 0.001)))
        f1 = freq * (1.0 + detune)
        f2 = freq * (1.0 - detune)
        if wave == "sine":
            s = (math.sin(2 * math.pi * f1 * t) + math.sin(2 * math.pi * f2 * t)) * 0.5
        else:  # pulse
            s = (math.sin(2 * math.pi * f1 * t) + 0.5 * math.sin(2 * math.pi * 2 * f1 * t)
                 + 0.25 * math.sin(2 * math.pi * 4 * f1 * t)) * 0.6
        out.append(s * env)
    return out


def noise(dur, seed=1):
    rng = random.Random(seed)
    return [rng.uniform(-1, 1) for _ in range(int(dur * RATE))]


def lowpass(sig, cutoff):
    rc = 1.0 / (2 * math.pi * cutoff)
    dt = 1.0 / RATE
    a = dt / (rc + dt)
    out = []
    prev = 0.0
    for s in sig:
        prev = prev + a * (s - prev)
        out.append(prev)
    return out


def adsr(sig, attack, release):
    n = len(sig)
    a = int(attack * RATE)
    r = int(release * RATE)
    out = []
    for i, s in enumerate(sig):
        env = min(1.0, i / max(a, 1))
        env = min(env, max(0.0, (n - i) / max(r, 1)))
        out.append(s * env)
    return out


def normalize(sig, peak=0.85):
    m = max(0.0001, max(abs(s) for s in sig))
    g = peak / m
    return [s * g for s in sig]


def write_wav(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        frames = b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in samples)
        w.writeframes(frames)


def lowpass_mix(sig, cutoff=3200):
    rc = 1.0 / (2 * math.pi * cutoff)
    dt = 1.0 / RATE
    a = dt / (rc + dt)
    out = []
    prev = 0.0
    for s in sig:
        prev = prev + a * (s - prev)
        out.append(prev)
    return out


def echo(sig, delay=0.38, feedback=0.32):
    n = len(sig)
    d = int(delay * RATE)
    out = list(sig)
    for i in range(d, n):
        out[i] += out[i - d] * feedback
    return out


def build_music(p, duration=10.0):
    total = int(duration * RATE)
    mix = [0.0] * total
    chord_secs = p["chord_secs"]
    arp = p["arp"]
    for ci, chord in enumerate(p["chords"]):
        start = int(ci * chord_secs * RATE)
        end = min(total, start + int(chord_secs * RATE))
        seg = [0.0] * (end - start)
        for vi, f in enumerate(chord):
            if arp and vi > 0:
                off = int((vi * 60.0 / arp) * RATE)
            else:
                off = 0
            s = tone(f, (end - start) / RATE, wave=p["wave"], attack=p["attack"],
                     release=p["release"], detune=p["detune"] * (0.3 + 0.12 * vi))
            pan = 0.72 + 0.28 * (vi % 2)
            for i in range(min(len(s), end - start)):
                if start + off + i < total:
                    seg[i] += s[i] * p["body"] / len(chord) * pan
        for i, v in enumerate(seg):
            mix[start + i] += v
    mix = lowpass_mix(mix, 3200)
    mix = echo(mix)
    return normalize(mix, 0.55)


def build_sfx(p):
    sfx = {}
    s = p["sfx"]
    boom = tone(s["boom"], 0.25, wave="sine", attack=0.002, release=0.2)
    click = tone(s["tick"], 0.035, wave="sine", attack=0.001, release=0.02)
    stamp = [a * 0.7 + b * 0.3 for a, b in zip(boom, click + [0.0] * max(0, len(boom) - len(click)))]
    sfx["stamp"] = normalize(stamp)
    n = noise(0.4, seed=int(s["rip"] * 1000))
    rip = lowpass(n, 6000)
    rip = adsr(rip, 0.005, 0.3)
    sfx["rip"] = normalize(rip)
    n2 = noise(0.5, seed=int(s["sweep"][0]))
    sw = lowpass(n2, s["sweep"][1])
    sw = [v * (0.4 + 0.6 * min(1.0, i / len(sw))) for i, v in enumerate(sw)]
    sw = adsr(sw, 0.05, 0.25)
    sfx["sweep"] = normalize(sw)
    tick = tone(s["tick"], 0.03, wave="sine", attack=0.001, release=0.02)
    sfx["tick"] = normalize(tick)
    c1 = tone(s["chime"][0], 0.9, wave="sine", attack=0.003, release=0.8)
    c2 = tone(s["chime"][1], 0.9, wave="sine", attack=0.003, release=0.8)
    chime = [a * 0.6 + b * 0.4 for a, b in zip(c1, c2)]
    sfx["chime"] = normalize(chime, 0.7)
    b = tone(s["boom"], 0.5, wave="sine", attack=0.004, release=0.45)
    sfx["boom"] = normalize(b)
    return sfx


def main():
    preset = sys.argv[1]
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    p = PRESETS[preset]
    write_wav(os.path.join(outdir, "music.wav"), build_music(p))
    for name, sig in build_sfx(p).items():
        write_wav(os.path.join(outdir, f"{name}.wav"), sig)
    print(f"generated {preset} palette -> {outdir}")


if __name__ == "__main__":
    main()
