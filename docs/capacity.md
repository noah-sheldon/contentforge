# ContentForge — Capacity & Cost Envelope (back of the envelope)

> Working estimate, not a contract. Assumptions below must be corrected
> against **real P1.5 per-stage telemetry** at the P2 gate; the serving
> infra is deliberately re-decided with measurements, not guesses.
> Companion: docs/hld.md §7 (cost shape), docs/lld.md, PLAN.md Roadmap.

## 1. Assumptions (edit these, not the conclusions)

| # | Assumption | Value |
|---|---|---|
| A1 | Tenants at launch | 20 |
| A2 | Production volume (steady) | 30 videos/day |
| A3 | Media churn per run (capture + deliver) | ~1 GB raw, ~300 MB delivered MP4 |
| A4 | Serial render wall-clock (VM, one at a time) | ~6 min avg |
| A5 | API requests per run (polls, HITL, media, config) | ~100 |
| A6 | LLM tokens per generated video | ~200k total (research→script→edit passes) |
| A7 | Growth scenario | 5× launch = 150 videos/day |
| A8 | VM | Netcup VPS 1000 G12 — 4 vCPU / 8 GB (owned) |

## 2. Envelope calculations

### 2.1 VM render throughput (the real bottleneck)

```
Launch:   30 videos/day x 6 min = 3 h/day serial  ->  ~8x headroom on 24 h
Growth:  150 videos/day x 6 min = 15 h/day serial ->  ~1.6x headroom  -> busy
```

- Concurrency stays **1** on the VM (RAM: ~1-2 GB OpenHands-class tooling is
  not in the prod stack; prod = Chromium ~1 GB + whisper-tiny ~1 GB + ffmpeg
  per render) — one render at a time protects the 8 GB budget.
- Rule: if daily serial render time exceeds ~12 h, either raise concurrency
  to 2 (8 GB may not fit) or offload to the Cloudflare Containers burst path
  (same image, executor seam — architecture.md §8.2). Burst is a config swap.

### 2.2 API volume vs Workers free tier

```
Launch:  30 runs/day x 100 req = ~3-5k req/day + UI + HITL polling
         -> ~5% of Workers Free 100k req/day
Growth: 150 runs/day -> ~25k req/day -> ~25% of free tier  (still fine)
```

- Workers Free ceiling only becomes a constraint above ~1k runs/day; at that
  point Workers Paid ($5/mo, 10M req/mo incl.) is trivial.
- Workflows + Queues bill **per operation + GB-hour state**, not per request.
  **Re-verify current Workflows pricing at the P2 gate** — it is the one
  Cloudflare line that is not free-tier-zero.

### 2.3 Media storage + egress vs Hetzner OBJ (the first real limit)

```
Launch storage:  30 x 300 MB delivered = ~9 GB/day  -> ~270 GB/mo
                 -> 1 TB bucket lasts ~3-4 months (before cleanup policy)
Launch egress:   30 x ~1 GB churn   = ~30 GB/day -> ~900 GB/mo
                 -> close to the 1 TB/month INCLUDED egress
Growth:          5x volume -> ~4.5 TB/mo storage growth, ~4.5 TB/mo egress
                 -> far past included allowances
```

- **This is the constraint that bites first.** Mitigations (ordered by cost):
  1. Tenant + project retention policy (delete raw capture after N days;
     keep delivered MP4/SRT/thumb only) — cuts churn roughly in half.
  2. Per-tenant storage quotas + metering (P3) so one tenant cannot blow the
     bucket.
  3. Archive delivered masters to Hetzner *storage-only* class or lifecycle
     to cold storage; keep hot OBJ for active projects.
  4. Only then consider overage or a second bucket/region.

### 2.4 LLM cost (per day, worst case at launch)

```
Launch: 30 videos x ~200k tokens ≈ 6M tokens/day.
  Cheap model (DeepSeek-class via LiteLLM): single-digit $/day.
  Premium frontier model everywhere: would be 5-10x — do NOT default to it.
```

- Route heavy passes to the cheap model, reserve frontier for
  copy/editing-critical passes only. LiteLLM per-tenant budgets (P3) enforce
  this per customer. Meter from day one — P3 meters collection.

### 2.5 Database

- M0 (512 MB) is fine for dev and early launch; Flex / paid tier only when
  real usage arrives. Document-shaped run state keeps documents small
  (metadata only — media lives in OBJ, architecture.md §8.2).

## 3. Limits that bite first (ranked)

1. **OBJ egress allowance (~1 TB/mo)** — hit around ~33 videos/day at 1 GB
   churn, or immediately if a tenant re-renders/re-downloads heavily.
2. **OBJ storage growth** — ~3-4 months to 1 TB without retention.
3. **VM serial throughput** — busy above ~100-120 videos/day at 6 min avg.
4. **Workflows/Queues op cost** — cheap, but the least-understood number;
   verify pricing at P2 before locking orchestration volume.
5. **LLM spend** — only if premium model becomes the default.

## 4. When to re-run this sheet (re-verify triggers)

- **P2 gate**: replace A3-A6 with real P1.5 per-stage telemetry (capture
  size, render duration by `format_direction`, token counts, failure rate).
  Re-verify Workflows pricing + Atlas tier.
- Any tenant exceeding ~25% of a single limit (quota alert, P3).
- Before enabling the burst path or raising render concurrency.
