# ContentForge — Capacity & Cost Envelope (back of the envelope)

> Working estimate, not a contract. Every number below is derived from the
> **sample video sizes** in §2 and must be corrected against **real P1.5
> per-stage telemetry** at the P2 gate — golden outputs from P1.5 give the
> first true file sizes and render durations. Serving infra is deliberately
> re-decided with measurements, not guesses.
> Companion: docs/hld.md §7 (cost shape), docs/lld.md, PLAN.md Roadmap.

## 1. Assumptions (edit these, not the conclusions)

| # | Assumption | Value |
|---|---|---|
| A1 | Tenants at launch | 20 |
| A2 | Production volume (steady) | 30 videos/day |
| A3 | Media per run | sample-based, §2 (delivered 20-320 MB by format; raw/intermediates discarded after run by retention policy) |
| A4 | Serial render wall-clock (VM, one at a time) | short 2-4 min, long 4-8 min (4 vCPU, software encode); launch mix avg ~4 min |
| A5 | Launch product mix | 60% vertical shorts <= 60 s, 30% long-form 5-10 min, 10% assets-mode reels |
| A6 | API requests per run (polls, HITL, media, config) | ~100 |
| A7 | LLM tokens per generated video | ~200k total (research -> script -> edit passes) |
| A8 | Growth scenario | 5x launch = 150 videos/day |
| A9 | VM | Netcup VPS 1000 G12 - 4 vCPU / 8 GB (owned) |

## 2. Sample video sizes (reference deliverables)

Estimates for H.264 software encodes; replace with P1.5 golden-output
measurements. "Long -> short" reuses one long master to slice several shorts
(`format_direction` matrix).

### 2.1 Delivered artifact sizes

| # | Sample | Spec | Duration | Est. MP4 size | Notes |
|---|---|---|---|---|---|
| S1 | Vertical short (idea/url) | 1080x1920 @30, H.264 | 30 s | 20-45 MB | talking head + HyperFrames overlays, ~4-9 Mbps |
| S2 | Vertical short | same | 60 s | 40-90 MB | the common short; long_to_short slices land here |
| S3 | Horizontal long | 1280x720 @30, H.264 | 5 min | 90-160 MB | ~2.5-4.5 Mbps; talking-head + screencap |
| S4 | Horizontal long (master) | same | 10 min | 180-320 MB | source master for long_to_short |
| S5 | Sidecars (per deliverable) | SRT + captions + thumbnail + metadata | - | < 5 MB | thumbnails tens-hundreds KB |

### 2.2 Media processed per run (ingress + intermediates)

| Mode | Uploaded / captured | Intermediates (discarded post-run) | Delivered (kept) |
|---|---|---|---|
| idea / url (shorts) | screen/PiP capture ~20-80 MB | frames + wav + work files ~30-80 MB | 20-90 MB |
| idea / url (long) | screen/PiP capture ~80-250 MB | frames + wav + work files ~100-300 MB | 90-320 MB |
| script (visuals via capture) | same as above per format | same | same as above |
| assets (customer footage) | customer upload, typically 100 MB - 1 GB (one clip) | tightened/transcribed work files | 20-320 MB per output |

## 3. Envelope calculations

### 3.1 VM render throughput (the real bottleneck)

```
Launch mix:  30 runs/day, avg ~4 min serial  -> ~2 h/day  -> ~10x headroom
Growth:     150 runs/day, avg ~4 min serial  -> ~10 h/day -> ~2.4x (busy)
All-long:   150 x 6 min avg                  -> ~15 h/day -> 1.6x (burst path)
```

- Concurrency stays **1** on the VM (per render: Chromium ~1 GB, whisper
  ~1 GB, ffmpeg + ffprobe) - protects the 8 GB budget.
- Rule: if daily serial render time exceeds ~12 h, raise concurrency to 2
  (8 GB may not fit) or offload to the Cloudflare Containers burst path
  (same pipeline image, executor seam - architecture.md section 8.2). Burst
  is a config swap.

### 3.2 API volume vs Workers free tier

```
Launch:  30 runs/day x 100 req = ~3-5k req/day + UI + HITL polling
         -> ~5% of Workers Free 100k req/day
Growth: 150 runs/day -> ~25k req/day -> ~25% of free tier  (still fine)
```

- Workers Free ceiling becomes a constraint only above ~1k runs/day; at
  that point Workers Paid ($5/mo, 10M req/mo incl.) is trivial.
- Workflows + Queues bill **per operation + GB-hour of state**, not per
  request. **Re-verify current Workflows pricing at the P2 gate** - it is
  the one Cloudflare line that is not free-tier-zero.

### 3.3 Storage + egress vs Hetzner OBJ, from section 2 samples

```
Delivered, per day (launch mix):
  shorts 60%: 18 x ~60 MB  = ~1.1 GB
  longs  30%:  9 x ~200 MB = ~1.8 GB
  assets 10%:  3 x ~100 MB = ~0.3 GB
  -> ~3.2 GB/day delivered  -> ~95 GB/month
Egress: customer downloads + presigned pulls ~1-2x delivered
  -> ~3-6 GB/day -> ~100-180 GB/month  (comfortably inside 1 TB included)
Assets-mode uploads are INGRESS (Hetzner ingress is free), but add to
storage while kept.
```

- **Delivered-only storage ~95 GB/mo.** With a retention policy (keep
  delivered 90 days, discard raw/intermediates after run): steady-state ~3
  months of delivered ~ **~285 GB** -> the 1 TB bucket lasts ~3+ months to a
  plateau, then lifecycle to cold/archive.
- Without retention, 1 TB fills in ~10 months at launch and ~2 months at 5x
  growth - retention is not optional.
- Per-tenant quotas (P3) protect the bucket from a single heavy tenant
  (assets mode is the biggest single upload).

### 3.4 LLM cost (per day, worst case at launch)

```
Launch: 30 videos x ~200k tokens ~ 6M tokens/day.
  Cheap model (DeepSeek-class via LiteLLM): single-digit $/day.
  Premium frontier model everywhere: 5-10x - do NOT default to it.
```

- Route heavy passes to the cheap model; reserve frontier for copy and
  editing-critical passes. LiteLLM per-tenant budgets (P3) enforce per
  customer. Meter from day one (P3 meters collection).

### 3.5 Database

- M0 (512 MB) is fine for dev and early launch; Atlas Flex when real usage
  arrives. Run state is metadata-only (documents stay small - media lives
  in OBJ, architecture.md section 8.2).

## 4. Limits that bite first (ranked)

1. **OBJ storage growth from delivered artifacts** - ~95 GB/mo at launch;
   retention is the control, per-tenant quotas (P3) the guard.
2. **Assets-mode uploads** - biggest single files (up to ~1 GB per clip);
   quota + resumable presigned PUT at P2.
3. **VM serial throughput** - busy above ~100-150 videos/day at the launch
   mix; burst path is the release valve.
4. **Workflows/Queues op cost** - cheap, but the least-understood number;
   verify pricing at P2 before locking orchestration volume.
5. **LLM spend** - only if a premium model becomes the default.
6. **OBJ egress** - NOT a launch limit under the section 2 samples
   (~100-180 GB/mo of 1 TB); revisit only if re-renders or heavy download
   patterns appear.

## 5. When to re-run this sheet (re-verify triggers)

- **P1.5 gate**: replace section 2 sample sizes with golden-output
  measurements (per `format_direction` + input mode) and A4 render
  durations with real stage telemetry.
- **P2 gate**: re-decide infra with measured numbers; re-verify Workflows
  pricing and the Atlas tier; confirm retention policy constants.
- Any tenant exceeding ~25% of a single limit (quota alert, P3).
- Before enabling the burst path or raising render concurrency.
