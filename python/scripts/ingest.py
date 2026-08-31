#!/usr/bin/env python3
"""Universal content ingester for the content-planner skill.

Usage:
  python3 scripts/ingest.py <URL|audio-file|-> [--slug NAME] [--model MODEL] [--chunk-min 45] [--force]
  echo "raw text" | python3 scripts/ingest.py -

Accepted inputs (auto-detected):
  - YouTube video URL      -> transcript-api fast path, mlx-whisper fallback
  - YouTube playlist URL   -> per-video ingest under library/<slug>/
  - audio/video file path  -> mlx-whisper (chunked if > chunk-min minutes)
  - website/blog URL       -> trafilatura readable-markdown extraction
  - raw text (stdin "-")   -> written as-is

Outputs (idempotent; finished items are skipped unless --force):
  library/<slug>/metadata.json
  library/<slug>/raw_transcript.md
  library/<slug>/per-video/<NN>-<title>/...   (playlists only)
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from common import CONFIG, LIBRARY, ensure_dirs, slugify, write_json

HAS_YT = False
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    HAS_YT = True
except ImportError:
    pass

_ing = CONFIG.get("ingest", {})
DOMAIN_PROMPT = _ing.get(
    "domain_prompt",
    "RAG, MLOps, LLM, LangGraph, data engineering, data science, Python, SQL, "
    "machine learning, AI agents, embeddings, vector database, production, "
    "LangChain, retrieval, fine-tuning",
)
WHISPER_MODEL = _ing.get("whisper_model", "mlx-community/whisper-large-v3-turbo")
CHUNK_MIN_DEFAULT = _ing.get("chunk_minutes", 45)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def tool(name):
    """Resolve a console script in the same venv first, else PATH."""
    venv_bin = Path(sys.executable).parent / name
    if venv_bin.exists():
        return str(venv_bin)
    return shutil.which(name) or name


def yt_video_id(url):
    if "youtu.be/" in url:
        return urlparse(url).path.split("/")[1][:11]
    m = re.search(r"[?&]v=([\w-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"/(?:shorts|live|embed)/([\w-]{11})", url)
    if m:
        return m.group(1)
    return None


def is_youtube(url):
    return "youtube.com" in url or "youtu.be" in url


def is_playlist_url(url):
    return "list=" in url or "playlist" in url.lower()


def fetch_transcript(video_id):
    if not HAS_YT:
        return None
    try:
        segs = YouTubeTranscriptApi().fetch(video_id)
        return "\n".join(s.text for s in segs)
    except Exception:
        return None


def audio_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)])
    try:
        return float(r.stdout.strip())
    except (ValueError, AttributeError):
        return 0.0


def split_audio(path, out_dir, chunk_min):
    out_dir.mkdir(parents=True, exist_ok=True)
    pat = str(out_dir / "part-%03d.m4a")
    r = run(["ffmpeg", "-y", "-i", str(path), "-f", "segment",
             "-segment_time", str(chunk_min * 60), "-c", "copy", pat])
    if r.returncode != 0:
        run(["ffmpeg", "-y", "-i", str(path), "-f", "segment",
             "-segment_time", str(chunk_min * 60), "-c", "aac", pat])
    return sorted(out_dir.glob("part-*.m4a"))


def transcribe_audio(path, model):
    """Return transcript text. Prefers mlx_whisper CLI, falls back to faster-whisper."""
    exe = tool("mlx_whisper")
    if exe != "mlx_whisper":
        out_dir = path.parent
        r = run([exe, "--model", model, "--output-format", "txt",
                 "--output-dir", str(out_dir),
                 "--initial-prompt", DOMAIN_PROMPT, str(path)])
        if r.returncode == 0:
            txt = out_dir / (path.stem + ".txt")
            if txt.exists():
                return txt.read_text(encoding="utf-8")
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(model, device="cpu", compute_type="int8")
        segs, _ = m.transcribe(str(path), initial_prompt=DOMAIN_PROMPT)
        return "".join(s.text for s in segs)
    except ImportError:
        pass
    raise RuntimeError("No working whisper backend (mlx_whisper or faster-whisper)")


def transcribe_file(path, out_dir, model, chunk_min):
    """Transcribe one audio/video file, chunking long sources. Returns text."""
    dur = audio_duration(path)
    if dur <= chunk_min * 60:
        return transcribe_audio(path, model)
    tmp = Path(tempfile.mkdtemp(prefix="cp-chunk-"))
    try:
        parts = split_audio(path, tmp, chunk_min)
        texts = []
        for p in parts:
            texts.append(transcribe_audio(p, model))
            p.unlink(missing_ok=True)
        return "\n\n".join(t.strip() for t in texts if t.strip())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def yt_title(video_id, fallback):
    r = run([tool("yt-dlp"), "--skip-download", "--print", "%(title)s",
             f"https://www.youtube.com/watch?v={video_id}"])
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    return fallback


def ingest_youtube_video(url, out_dir, model, chunk_min, force, title_hint=None):
    vid = yt_video_id(url)
    if not vid:
        raise RuntimeError(f"Cannot parse YouTube video id from: {url}")
    if not force and (out_dir / "raw_transcript.md").exists():
        return read_meta(out_dir, vid, title_hint or vid, "transcript-api")

    title = title_hint or yt_title(vid, vid)
    text = fetch_transcript(vid)
    source = "youtube-transcript-api"
    if not text:
        # Fallback: download audio -> whisper
        with tempfile.TemporaryDirectory(prefix="cp-yt-") as tmp:
            tmpd = Path(tmp)
            r = run([tool("yt-dlp"), "-f", "ba/b", "-x", "--audio-format", "m4a",
                     "-o", str(tmpd / "audio.%(ext)s"), url])
            if r.returncode != 0:
                raise RuntimeError(f"yt-dlp download failed: {r.stderr[:400]}")
            audio = next(tmpd.glob("audio.*"), None)
            if not audio:
                raise RuntimeError("yt-dlp produced no audio file")
            text = transcribe_file(audio, tmpd, model, chunk_min)
            source = "mlx-whisper"
    if not text.strip():
        raise RuntimeError(f"No transcript available for {vid}")

    (out_dir / "raw_transcript.md").write_text(text, encoding="utf-8")
    meta = {
        "type": "youtube_video",
        "video_id": vid,
        "url": url,
        "title": title,
        "transcript_source": source,
        "language": "en",
    }
    write_json(out_dir / "metadata.json", meta)
    return meta


def read_meta(out_dir, vid, title, source):
    try:
        return json.loads((out_dir / "metadata.json").read_text())
    except (OSError, json.JSONDecodeError):
        return {"video_id": vid, "url": "", "title": title, "transcript_source": source}


def ingest_playlist(url, out_dir, model, chunk_min, force):
    r = run([tool("yt-dlp"), "--flat-playlist", "-J", url])
    if r.returncode != 0:
        raise RuntimeError(f"yt-dlp playlist failed: {r.stderr[:400]}")
    data = json.loads(r.stdout)
    title = data.get("title") or slugify(url)
    entries = data.get("entries") or []
    meta = {
        "type": "youtube_playlist",
        "title": title,
        "url": url,
        "count": len(entries),
        "videos": [],
    }
    for i, e in enumerate(entries, 1):
        vurl = e.get("url")
        if not vurl:
            continue
        vtitle = e.get("title") or f"video-{i}"
        vdir = out_dir / "per-video" / f"{i:02d}-{slugify(vtitle)}"
        vdir.mkdir(parents=True, exist_ok=True)
        vmeta = ingest_youtube_video(vurl, vdir, model, chunk_min, force,
                                     title_hint=vtitle)
        meta["videos"].append(vmeta)
    write_json(out_dir / "metadata.json", meta)
    return meta


def ingest_web(url, out_dir, force):
    if (out_dir / "raw_transcript.md").exists() and not force:
        return {"type": "web", "url": url, "title": urlparse(url).netloc}
    import requests
    r = requests.get(url, timeout=30,
                     headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    r.raise_for_status()
    try:
        import trafilatura
        text = trafilatura.extract(r.text)
    except ImportError:
        text = re.sub(r"<[^>]+>", " ", r.text)
        text = re.sub(r"\s+", " ", text).strip()
    if not text or len(text) < 200:
        raise RuntimeError(f"Could not extract meaningful text from {url}")
    (out_dir / "raw_transcript.md").write_text(text, encoding="utf-8")
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.S | re.I)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
    meta = {"type": "web", "url": url, "title": title or urlparse(url).netloc}
    write_json(out_dir / "metadata.json", meta)
    return meta


def main():
    ap = argparse.ArgumentParser(description="Universal content ingester")
    ap.add_argument("input", help="URL, file path, or '-' for stdin raw text")
    ap.add_argument("--slug", help="library folder name (default: derived from title)")
    ap.add_argument("--model", default=WHISPER_MODEL)
    ap.add_argument("--chunk-min", type=int, default=CHUNK_MIN_DEFAULT,
                    help="split audio longer than N minutes before Whisper")
    ap.add_argument("--force", action="store_true", help="re-ingest finished items")
    args = ap.parse_args()
    ensure_dirs()

    inp = args.input

    if inp == "-":
        text = sys.stdin.read().strip()
        if not text:
            sys.exit("stdin empty")
        slug = args.slug or "raw-text"
        out = LIBRARY / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "raw_transcript.md").write_text(text, encoding="utf-8")
        write_json(out / "metadata.json",
                   {"type": "text", "title": slug, "chars": len(text)})
        print(f"ingested text -> {out}")
        return

    p = Path(inp).expanduser()
    if p.exists():
        slug = args.slug or slugify(p.stem)
        out = LIBRARY / slug
        out.mkdir(parents=True, exist_ok=True)
        text = transcribe_file(p, out / "audio", args.model, args.chunk_min)
        (out / "raw_transcript.md").write_text(text, encoding="utf-8")
        write_json(out / "metadata.json",
                   {"type": "audio", "file": str(p), "title": p.stem})
        print(f"ingested audio -> {out} ({len(text)} chars)")
        return

    if is_youtube(inp) and is_playlist_url(inp):
        r = run([tool("yt-dlp"), "--flat-playlist", "-J", inp])
        if r.returncode != 0:
            sys.exit(f"yt-dlp failed: {r.stderr[:400]}")
        ptitle = json.loads(r.stdout).get("title", "playlist")
        slug = args.slug or slugify(ptitle)
        out = LIBRARY / slug
        out.mkdir(parents=True, exist_ok=True)
        meta = ingest_playlist(inp, out, args.model, args.chunk_min, args.force)
        print(f"ingested playlist '{ptitle}' ({len(meta['videos'])} videos) -> {out}")
        return

    if is_youtube(inp):
        vid = yt_video_id(inp)
        if not vid:
            sys.exit(f"Cannot parse YouTube id: {inp}")
        title = yt_title(vid, vid)
        slug = args.slug or slugify(title)
        out = LIBRARY / slug
        out.mkdir(parents=True, exist_ok=True)
        meta = ingest_youtube_video(inp, out, args.model, args.chunk_min, args.force)
        print(f"ingested '{meta['title']}' [{meta['transcript_source']}] -> {out}")
        return

    if "://" in inp:
        slug = args.slug or slugify(urlparse(inp).netloc + "-" + urlparse(inp).path.strip("/"))
        out = LIBRARY / slug
        out.mkdir(parents=True, exist_ok=True)
        meta = ingest_web(inp, out, args.force)
        print(f"ingested web '{meta['title']}' -> {out}")
        return

    sys.exit(f"Unrecognized input: {inp}")


if __name__ == "__main__":
    main()
