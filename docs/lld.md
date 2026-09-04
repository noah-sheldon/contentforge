# ContentForge — Low-Level Design

Companion to HLD. Concrete packages, schemas, endpoints, and wiring. Everything is a package or proven existing code; one VM + managed services; cost-first.

> Layout below = **target (P2–P5)**. Current P0 tree is the pipeline core only:
> `python/`, `skills/`, `prompts/`, `templates/`, `config/`, `docs/`, `deploy/`.
> `apps/`, `services/`, `workers/` arrive with P2/P4.

## 1. Monorepo Layout (uv workspace)

```mermaid
flowchart LR
    subgraph ROOT[contentforge - uv workspace]
        subgraph apps
            W[apps/web - Next.js + shadcn/ui]
        end
        subgraph services
            A[services/api - Cloudflare Workers + Hono]
        end
        subgraph workers
            P[workers/pipeline - FastAPI container for the VM]
            L[workers/litellm - LiteLLM container]
        end
        subgraph deploy
            C[deploy/compose.yaml - VM stack]
            T[deploy/cloudflared - tunnel config]
        end
        subgraph shared
            CFG[config/ - Pydantic TenantConfig + YAML]
            PRO[prompts/ - registry + versioned prompts]
            TPL[templates/ - HyperFrames templates]
            SK[skills/ - production runbooks as config]
        end
        subgraph py
            PY[python/ - agents + scripts ported from both repos]
        end
    end
    W --> A
    A --> P
    P --> L
    P --> PY
    PY --> CFG
    PY --> PRO
    PY --> TPL
```

Tooling: `uv` workspace; `wrangler` (Workers/Queues/Workflows/Tunnel), `docker compose` (VM), GitHub Actions CI.

## 2. API Surface (Workers + Hono)

```mermaid
flowchart LR
    R[REST /api/v1] --> E1[POST /runs - start pipeline, format_direction]
    R --> E2[GET /runs/:id - status + artifacts]
    R --> E3[POST /runs/:id/approve or reject - HITL]
    R --> E4[GET /projects]
    R --> E5[GET or PUT /tenant/config - brand studio]
    R --> E6[POST /capture/recipes - generate recipe]
    R --> E7[GET /media/* - signed Hetzner OBJ URLs]
    E1 & E2 & E3 & E4 & E5 & E6 & E7 --> JWT[WorkOS JWT - JWKS verify]
    E1 --> WF[Start Workflow instance]
    E2 & E5 --> M[(MongoDB Atlas - mongoose)]
    E7 --> O[(Hetzner OBJ - presigned)]
```

Every request: WorkOS JWT verified at the edge, tenant from `org_id` claim, Mongo queries scoped by `tenant_id`, Zod validation.

## 3. Data Model (MongoDB, mongoose)

```mermaid
erDiagram
    tenants {
        ObjectId _id PK
        string slug UK
        object config "validated TenantConfig"
        date created_at
    }
    api_keys {
        ObjectId _id PK
        ObjectId tenant_id FK
        string key_hash UK
        string name
    }
    projects {
        ObjectId _id PK
        ObjectId tenant_id FK
        string title
        string source_url
    }
    runs {
        ObjectId _id PK
        ObjectId project_id FK
        ObjectId tenant_id FK
        string workflow_id
        string state "pending, checkpoint, running, done, failed"
        string checkpoint "topic, draft, final"
        string format_direction "short, long, long_to_short, short_to_long"
    }
    jobs {
        ObjectId _id PK
        ObjectId run_id FK
        string stage
        string status "queued, running, done, failed"
    }
    meters {
        ObjectId _id PK
        ObjectId tenant_id FK
        string metric "runs, renders, llm_credits"
        number amount
        string period
    }
```

Indexes: `tenant_id` on every collection; `run_id` on jobs. Media keys in Hetzner OBJ: `tenants/{tenant_id}/{project_id}/{run_id}/{artifact}`. `format_direction` is run-level config — the pipeline branches on it (section 4).

## 4. Pipeline Orchestration (Cloudflare Workflows → VM via Tunnel)

```mermaid
flowchart TD
    S0[Step 0 - load tenant config + format_direction] --> S1[Step 1 - ingest + plan]
    S1 --> H1{checkpoint: topic}
    H1 -->|approve| S2[Step 2 - capture Playwright webm]
    S2 --> S3[Step 3 - transcribe + tighten]
    S3 --> S4[Step 4 - write + review draft]
    S4 --> H2{checkpoint: draft}
    H2 -->|reject| S4
    H2 -->|approve| S5[Step 5 - compose HyperFrames]
    S5 --> S6[Step 6 - render by format_direction]
    S6 --> S6a{format}
    S6a -->|short| R9[render 9:16]
    S6a -->|long| R16[render 16:9 master]
    S6a -->|long_to_short| R16
    R16 --> SLC[build_shorts.py - auto-slice 9:16]
    SLC --> R9
    S6a -->|short_to_long| CMP[compile shorts into long]
    CMP --> R16
    R9 & R16 --> H3{checkpoint: final}
    H3 -->|approve| S7[Step 7 - deliver: SRT + thumbs + links]
    S7 --> S8[Step 8 - meter + notify]
    H1 -.->|reject| E[End - record failure]
    H3 -.->|reject| S5
```

Workflow steps call VM endpoints through the Cloudflare Tunnel (private hostname). Heavy stages (capture/transcribe/render) run on the VM; pure-LLM stages can run in-step via LiteLLM. Step payloads carry keys, not media. **Render concurrency is throttled to 1** (VM: 4 vCPU / 8 GB — VPS 1000 G12; each render needs ~3-4 GB); burst path = Cloudflare Containers with the same image.

## 5. VM Stack (Docker Compose on Netcup)

```yaml
# deploy/compose.yaml - one stack, three services
services:
  pipeline:
    build: ../workers/pipeline        # FastAPI: ingest/plan/capture/transcribe/tighten/compose/render/deliver
    env_file: .env                    # MONGO_URI (Atlas), OBJ_* (Hetzner), LITELLM_URL, DEEPSEEK_API_KEY, ARIZE_*
    volumes: [media-cache:/media]     # scratch for ffmpeg/whisper
  litellm:
    image: ghcr.io/berriai/litellm:main
    command: ["--config", "/app/litellm.yaml"]  # SQLite backend, model groups, virtual keys
    env_file: .env
  cloudflared:
    image: cloudflare/cloudflared
    command: tunnel run contentforge   # zero public ports; exposes pipeline to Workflows
volumes:
  media-cache:
```

- Pipeline image is a plain Dockerfile (portable to Cloudflare Containers / Cloud Run for burst).
- LiteLLM uses its SQLite backend (no Postgres — infra overhead not wanted); one instance is fine on one VM.
- Nightly cron: `mongodump` → Hetzner OBJ; `docker compose pull && up -d` for updates.
- VM hardening: non-root user, UFW default-deny, fail2ban, unattended-upgrades, secrets in `.env` never in images.

## 6. Agent-Agnostic LLM Layer (LiteLLM)

```mermaid
flowchart LR
    AGENT[any agent - research / copywriter / review / compose] --> SYNTH[synthesis provider wrapper]
    SYNTH -->|OpenAI-compatible| LP[LiteLLM proxy on VM]
    LP -->|virtual key per tenant| VK[tenant key: budgets + rate limits]
    LP --> R1[DeepSeek - default hosted]
    LP --> R2[OpenAI]
    LP --> R3[Anthropic]
    LP --> R4[tenant BYOK keys - encrypted]
```

- One virtual key per tenant via `POST /key/generate` (SQLite-backed; master key in `.env`).
- Existing `synthesis/openai.py` wrapper changes only its `base_url` to the LiteLLM endpoint — every agent stays on the OpenAI SDK. Agent-agnostic: no agent knows which provider serves it.
- Hosted mode: tenant key → platform DeepSeek group (metered credits). BYOK mode: tenant key → their provider keys.
- Prompt registry entries can carry `model_family` hints; LiteLLM aliases route per family.

## 7. Tenant Config (Pydantic)

```yaml
# config/tenants/example.yaml - validated by config/ package
tenant:
  id: t_01
  slug: acme
  brand:
    colors: { primary: "#0D1117", accent: "#D4AF37", bg: "#F5F1E8" }
    fonts: ["Playfair Display", "Inter", "JetBrains Mono"]
  voice: "grade 5-6 plain speech, no em-dashes, spoken-flow"
  persona: config/persona.yaml
  llm:
    mode: hosted            # hosted | byok
    provider: deepseek
    model: deepseek-v4-flash
    key_ref: null           # set when mode=byok
  templates: ["short-form/vox", "long-form/documentary"]
  prompts:
    copywriter: v1.1.2
    review: v1.0.3
  formats: ["long_to_short", "short"]   # allowed format_direction values
  recipes: ["table-walkthrough", "json-api-demo"]
```

A new tenant = validated blob + LiteLLM virtual key + OBJ prefixes — zero code. `formats` caps which directions a tenant may request.

## 8. BYOK Flow

```mermaid
sequenceDiagram
    participant T as Tenant (dashboard)
    participant A as API
    participant L as LiteLLM
    participant P as Provider (OpenAI/Anthropic/DeepSeek)
    T->>A: PUT /tenant/config { llm: { mode: byok, provider } }
    A->>L: POST /key/generate (tenant scoped, provider group)
    L-->>A: virtual key
    A->>A: store key_ref (encrypted, Secrets Store)
    A-->>T: saved - next runs use tenant keys
    Note over L,P: tenant calls route via virtual key to P
    A->>L: run LLM calls (OpenAI SDK, base_url=LiteLLM)
    L->>P: forward with tenant BYOK key
```

## 9. Auth Flow (WorkOS AuthKit)

```mermaid
sequenceDiagram
    participant U as User
    participant N as Next.js (AuthKit UI)
    participant W as WorkOS
    participant A as Workers API
    U->>N: sign in (Google / GitHub / email)
    N->>W: AuthKit hosted UI
    W-->>N: session cookie (wos-session)
    N->>A: API call (session JWT)
    A->>A: verify JWT via JWKS (org_id, role, permissions)
    A->>M: scope queries by org_id = tenant_id
```

RBAC: WorkOS roles gate dashboard actions; API trusts token claims. Tenant ↔ WorkOS org: 1:1 at provisioning.

## 10. Render Handoff (VM)

```mermaid
sequenceDiagram
    participant F as Workflow
    participant V as VM pipeline (compose)
    participant O as Hetzner OBJ
    F->>V: compose stage (config + template + script)
    V->>V: generate index.html (HyperFrames)
    V->>O: upload composition bundle
    F->>V: render job (keys, format_direction, crf)
    V->>V: npx hyperframes render + ffmpeg CRF 14 (+ slice if long_to_short)
    V->>O: MP4 + SRT + thumbnails
    V-->>F: result keys + duration
```

Workers cannot render (CPU ceiling, no ffmpeg — verified). VM runs Chromium + ffmpeg natively; Cloudflare Containers is the burst path with the same image. Signed URLs from Hetzner OBJ deliver at ~EUR 1/TB egress beyond the included 1 TB.

## 11. Fast-to-Market Package Map

| Need | Package | Where |
|---|---|---|
| Web framework | Next.js + shadcn/ui + Tailwind | apps/web |
| API framework | Hono | services/api |
| ODM | mongoose | services/api |
| Validation | Zod (TS) / Pydantic (Python) | api / workers |
| LLM gateway | LiteLLM proxy (MIT, SQLite) | VM container |
| Auth | WorkOS AuthKit (+ SDKs) | web + api |
| Capture | Playwright (Python) | VM pipeline |
| Transcribe | faster-whisper | VM pipeline |
| Ingest | yt-dlp + youtube-transcript-api + trafilatura | VM pipeline |
| Research search | Exa + RSS (existing) | VM pipeline |
| Video | HyperFrames CLI (npx) + ffmpeg | VM pipeline |
| Shorts slicing | build_shorts.py / slice.py (existing) | VM pipeline |
| DB | MongoDB Atlas (mongoose/pymongo) | managed |
| Storage | Hetzner OBJ (boto3/S3 SDK) | managed |
| Tunnel | cloudflared | VM container |
| Errors | Sentry | web + api + workers |
| Observability | Arize OTEL (existing) | VM pipeline |
| Analytics | Cloudflare Web Analytics | web |
| Uptime | UptimeRobot | VM + API |
| Email (P4+) | Resend | services/api |
| Billing (P5) | Stripe | services/api |
| Docs (P4+) | Mintlify | repo |
