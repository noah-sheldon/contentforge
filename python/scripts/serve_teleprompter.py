#!/usr/bin/env python3
"""Teleprompter server — serves the prompter UI + all teleprompter.txt scripts.

Lets you browse and load any script in the project over your local network,
so you can read the prompter on your phone/iPad/desktop while you record.

Usage:
  python3 scripts/serve_teleprompter.py            # 127.0.0.1:8000
  python3 scripts/serve_teleprompter.py --host 0.0.0.0 --port 9000
  python3 scripts/serve_teleprompter.py --list-only

Open http://<host>:<port>/ in a browser.
"""
import argparse
import http.server
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from common import ROOT

PROMPTER_DIR = ROOT / "scripts" / "teleprompter"
PROMPTER_HTML = PROMPTER_DIR / "index.html"


def collect_scripts() -> list:
    """Finds every teleprompter.txt in outputs/ and workspace/ (with a label)."""
    found = []
    for base in (ROOT / "outputs", ROOT / "workspace"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("teleprompter.txt")):
            rel = path.relative_to(ROOT)
            found.append(
                {
                    "name": str(rel),
                    "path": "/read?path=" + str(rel),
                    "label": label_for(str(rel)),
                }
            )
    return found


def label_for(rel: str) -> str:
    """Build a short human label from a path like outputs/m3l1-what-is-langgraph/teleprompter.txt."""
    parts = Path(rel).parts
    if "outputs" in parts:
        idx = parts.index("outputs")
        slug = parts[idx + 1] if len(parts) > idx + 1 else rel
        slug = slug.replace("-", " ").replace("_", " ").title()
        return slug
    return rel


def build_index() -> str:
    """Minimal auto-advancing index page listing every available script."""
    scripts = collect_scripts()
    rows = "\n".join(
        f'<a class="row" href="{s["path"]}"><span class="label">{s["label"]}</span>'
        f'<span class="mono">{s["name"]}</span></a>'
        for s in scripts
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teleprompter — Scripts</title>
<style>
  :root {{ --bg:#12141C; --text:#FAFAFA; --gold:#D4AF37; --muted:#6B7280; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Inter',system-ui,sans-serif;
        min-height:100vh; padding:48px 24px; }}
  h1 {{ color:var(--gold); font-size:24px; margin-bottom:8px; }}
  p.sub {{ color:var(--muted); font-size:14px; margin-bottom:32px; }}
  .list {{ max-width:720px; margin:0 auto; display:flex; flex-direction:column; gap:10px; }}
  .row {{ display:flex; justify-content:space-between; align-items:center; gap:16px;
        background:#1A1D27; border:1px solid rgba(212,175,55,.25); border-radius:12px;
        padding:16px 20px; color:var(--text); text-decoration:none; }}
  .row:hover {{ border-color:var(--gold); box-shadow:0 0 16px rgba(212,175,55,.2); }}
  .label {{ font-weight:600; }}
  .mono {{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--muted); }}
  .empty {{ color:var(--muted); text-align:center; }}
</style></head><body>
  <h1>Teleprompter</h1>
  <p class="sub">Pick a script to open in the prompter</p>
  <div class="list">
    {rows if rows else '<div class="empty">No teleprompter.txt files found.</div>'}
  </div>
</body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", build_index().encode("utf-8"))
            return

        if parsed.path == "/scripts" or parsed.path == "/api/scripts":
            self._send(200, "application/json", json.dumps(collect_scripts()).encode("utf-8"))
            return

        if parsed.path == "/read":
            query = dict(x.split("=", 1) for x in parsed.query.split("&") if "=" in x)
            rel = query.get("path", "")
            target = (ROOT / rel).resolve()
            # Security: only allow paths inside the project root
            if not str(target).startswith(str(ROOT)):
                self._send(403, "text/plain", b"forbidden")
                return
            if target.is_file() and target.suffix in (".txt", ".md"):
                self._send(200, "text/plain; charset=utf-8", target.read_bytes())
                return
            self._send(404, "text/plain", b"not found")
            return

        if parsed.path == "/prompter":
            if PROMPTER_HTML.exists():
                self._send(200, "text/html; charset=utf-8", PROMPTER_HTML.read_bytes())
            else:
                self._send(404, "text/plain", b"prompter not found")
            return

        self._send(404, "text/plain", b"not found")

    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("[teleprompter] %s\n" % (fmt % args))


def main():
    ap = argparse.ArgumentParser(description="Serve the teleprompter + scripts over your local network")
    ap.add_argument("--host", default="127.0.0.1", help="Bind address (0.0.0.0 to reachable on LAN)")
    ap.add_argument("--port", type=int, default=8000, help="Port (default 8000)")
    ap.add_argument("--list-only", action="store_true", help="Print discovered scripts and exit")
    args = ap.parse_args()

    scripts = collect_scripts()

    if args.list_only:
        for s in scripts:
            print(f"{s['label']:40s} {s['name']}")
        return

    if not PROMPTER_HTML.exists():
        print(f"[warn] prompter UI not found at {PROMPTER_HTML}")
    if not scripts:
        print("[warn] no teleprompter.txt files found under outputs/ or workspace/")

    httpd = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    host_display = args.host if args.host != "0.0.0.0" else "your LAN IP"
    print(f"Teleprompter server running:")
    print(f"  -> http://{host_display}:{args.port}/        (pick a script)")
    print(f"  -> http://{host_display}:{args.port}/prompter (direct prompter UI)")
    print(f"  {len(scripts)} script(s) available")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.server_close()


if __name__ == "__main__":
    main()
