#!/usr/bin/env node
/* Teleprompter server (Express) — serves the prompter UI + all teleprompter.txt scripts.

Endpoints:
  GET /              -> script picker index (auto-generated)
  GET /prompter      -> the prompter UI
  GET /api/scripts   -> JSON list of scripts (newest-first ordering)
  GET /read?path=..  -> raw script text (path-traversal guarded to project root)

Usage:
  node server.js                     # 127.0.0.1:8000
  node server.js --host 0.0.0.0      # reachable on your LAN (phone/iPad)
  node server.js --port 9000
  node server.js --list              # print scripts and exit
*/
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import express from 'express';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');            // content-planner/
const PROMPTER = path.join(__dirname, 'index.html');

/* ---------- script discovery (newest-first) ---------- */
function rank(name) {
  const n = name.toLowerCase();
  if (n.includes('tech')) return 0;                          // time-sensitive first
  const lf = n.match(/m(\d)-longform/);
  if (lf) return 1 + (6 - parseInt(lf[1], 10));              // m6=1 … m1=6
  const sh = n.match(/m(\d)l(\d)/);
  if (sh) return 10 + (6 - parseInt(sh[1], 10));             // shorts after long-forms
  return 20;
}

function labelFor(rel) {
  const parts = rel.split(path.sep);
  const i = parts.indexOf('outputs');
  if (i !== -1 && parts[i + 1]) {
    return parts[i + 1].replace(/[-_]/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }
  return rel;
}

function collectScripts() {
  const found = [];
  const bases = [path.join(ROOT, 'outputs'), path.join(ROOT, 'workspace')];
  const walk = (dir) => {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile() && entry.name === 'teleprompter.txt') {
        const rel = path.relative(ROOT, full).split(path.sep).join('/');
        // Long-form only — skip per-lesson shorts (m#l# folders).
        if (!/longform/.test(rel) && !/^tech-/.test(rel)) continue;
        found.push({ name: rel, path: '/read?path=' + encodeURIComponent(rel), label: labelFor(rel) });
      }
    }
  };
  for (const b of bases) walk(b);
  found.sort((a, b) => rank(a.name) - rank(b.name) || a.label.localeCompare(b.label));
  return found;
}

/* ---------- index page ---------- */
function buildIndex(scripts) {
  const rows = scripts
    .map((s) => {
      const pathParam = encodeURIComponent(s.name);
      return `<a class="row" href="/prompter?path=${pathParam}"><span class="label">${s.label}</span>` +
        `<span class="mono">${s.name}</span></a>`;
    })
    .join('\n');
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teleprompter — Scripts</title>
<style>
  :root { --bg:#12141C; --text:#FAFAFA; --gold:#D4AF37; --muted:#6B7280; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Inter',system-ui,sans-serif; min-height:100vh; padding:48px 24px; }
  h1 { color:var(--gold); font-size:24px; margin-bottom:8px; }
  p.sub { color:var(--muted); font-size:14px; margin-bottom:32px; }
  .list { max-width:720px; margin:0 auto; display:flex; flex-direction:column; gap:10px; }
  .row { display:flex; justify-content:space-between; align-items:center; gap:16px; background:#1A1D27;
        border:1px solid rgba(212,175,55,.25); border-radius:12px; padding:16px 20px; color:var(--text); text-decoration:none; }
  .row:hover { border-color:var(--gold); box-shadow:0 0 16px rgba(212,175,55,.2); }
  .label { font-weight:600; } .mono { font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--muted); }
  .empty { color:var(--muted); text-align:center; }
</style></head><body>
  <h1>Teleprompter</h1>
  <p class="sub">Pick a script to open in the prompter</p>
  <div class="list">${rows || '<div class="empty">No teleprompter.txt files found.</div>'}</div>
</body></html>`;
}

/* ---------- server ---------- */
const app = express();
const args = process.argv.slice(2);
const host = args.includes('--host') ? args[args.indexOf('--host') + 1] : '127.0.0.1';
const portIdx = args.indexOf('--port');
const port = portIdx !== -1 ? parseInt(args[portIdx + 1], 10) : 8000;

app.disable('x-powered-by');

app.get('/api/scripts', (req, res) => res.json(collectScripts()));

app.get('/read', (req, res) => {
  const rel = req.query.path || '';
  const target = path.resolve(ROOT, rel);
  if (!target.startsWith(ROOT)) return res.status(403).send('forbidden');
  if (fs.existsSync(target) && fs.statSync(target).isFile() && /\.(txt|md)$/.test(target)) {
    return res.type('text/plain').send(fs.readFileSync(target));
  }
  res.status(404).send('not found');
});

app.get('/prompter', (req, res) => res.sendFile(PROMPTER));

app.get('/', (req, res) => res.type('html').send(buildIndex(collectScripts())));

const scripts = collectScripts();

if (args.includes('--list')) {
  for (const s of scripts) console.log(`${s.label.padEnd(40)} ${s.name}`);
  process.exit(0);
}

app.listen(port, host, () => {
  const display = host === '0.0.0.0' ? 'your LAN IP' : host;
  console.log('Teleprompter (Express) running:');
  console.log(`  -> http://${display}:${port}/         (pick a script)`);
  console.log(`  -> http://${display}:${port}/prompter  (direct prompter UI)`);
  console.log(`  ${scripts.length} script(s) available`);
});
