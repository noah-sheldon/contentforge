#!/usr/bin/env bash
# P0 smoke test: persona load, toolchain green, CLI dry runs, stale-ref scan.
#
# Usage: scripts/smoke_test.sh [path-to-python]
# Defaults to .venv/bin/python when present, else python3.
#
# Matches the P0 acceptance criteria: every script runs from contentforge,
# zero stale root-relative refs / macOS paths, toolchain baseline green.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="${1:-}"
if [ -z "$PY" ]; then
  if [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"; else PY="python3"; fi
fi
RUFF=".venv/bin/ruff"; [ -x "$RUFF" ] || RUFF="ruff"

fail=0
step() { printf '\n== %s ==\n' "$1"; }

step "1/5 persona loads from config/persona.yaml (A1)"
if PYTHONPATH=python "$PY" -c '
from config.settings import load_persona
p = load_persona()
assert isinstance(p, dict) and p, "persona empty"
assert "silent_gray" in repr(p), "canonical brand key silent_gray missing (A8)"
print("persona OK")' ; then
  :
else
  echo "FAIL: load_persona()"; fail=1
fi

step "2/5 ruff check python/"
if "$RUFF" check python/; then :; else echo "FAIL: ruff"; fail=1; fi

step "3/5 pyrefly types (0 errors)"
if [ -x ".venv/bin/pyrefly" ]; then
  if (cd python && ../.venv/bin/pyrefly check); then :; else echo "FAIL: pyrefly"; fail=1; fi
else
  echo "skip (pyrefly not installed)"
fi

step "4/5 CLI dry runs: capture, tighten_words, transcribe"
for s in capture tighten_words transcribe; do
  if PYTHONPATH=python "$PY" "python/scripts/$s.py" --help >/dev/null 2>&1; then
    echo "  ok: $s.py --help"
  else
    echo "FAIL: $s.py --help"; fail=1
  fi
done

step "5/5 stale-ref scan (root-relative scripts/, macOS paths)"
HITS=""
HITS="$HITS $(grep -rnE --exclude-dir=__pycache__ '(^|[^A-Za-z0-9_./-])scripts/[A-Za-z0-9_]+\.py' skills/ python/ config/ prompts/ 2>/dev/null | grep -vE 'python/scripts/' || true)"
HITS="$HITS $(grep -rnl --exclude-dir=__pycache__ '/System/Library/Fonts\|/Users/noahsheldon' python/ skills/ config/ prompts/ templates/ 2>/dev/null || true)"
if [ -n "$(echo "$HITS" | tr -d '[:space:]')" ]; then
  echo "$HITS"; echo "FAIL: stale references found"; fail=1
else
  echo "  ok: no root-relative script refs, no macOS font/path hardcodes"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "SMOKE PASS"
else
  echo "SMOKE FAIL"
  exit 1
fi
