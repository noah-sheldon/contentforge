---
description: "SOLID, KISS, DRY, YAGNI + design patterns + HLD/LLD + shadcn/ui"
---

# Engineering & Architecture Standards

## Core Principles (Ordered)

### 1. SOLID
| Principle | Rule | Example |
|---|---|---|
| **S**ingle Responsibility | One file, one job | `researcher.py` searches only. |
| **O**pen/Closed | New platform = new class. Never touch existing code. | Add Reddit: `RedditScraper(BaseScraper)`. Zero edits to YouTube/X. |
| **L**iskov Substitution | Every scraper implements `search(query)`. Swappable. | `InstagramPublisher` and `LinkedInPublisher` both implement `publish()`. |
| **I**nterface Segregation | Dont implement methods you dont use. | `TextAnimation.tsx` has no video logic. |
| **D**ependency Inversion | Depend on ABCs, not concretions. | Strategist depends on `SearchInterface`. Swap DuckDuckGo for Exa = one import change. |

### 2. KISS
- No Kubernetes. Docker Compose is enough.
- No microservices. One FastAPI app + Celery workers.
- No RabbitMQ. Redis is sufficient.
- No complex config. `persona.yaml` + `.env` covers everything.
- V1: one platform. Prove the loop before scaling.
- Junior test: can a junior engineer understand the file in 5 minutes?

### 3. DRY
| What | DRY solution |
|---|---|
| Retry logic | `@retry_on_failure` decorator on `BasePublisher` |
| LLM prompts | Individual `{domain}/{name}.yaml` files in `prompts/` |
| Credentials | `.env` only. Never scattered across files. |
| File paths | `Path` constants in `config/settings.py`. Never hardcoded. |
| API clients | `get_client()` in `search/web.py`. Shared DuckDuckGo client. |
| Schemas | All Pydantic models in `agents/schemas.py`. |

### 4. YAGNI (You Aint Gonna Need It)
- Never build V2 before V1 works.
- Never add a framework just in case.
- No database until JSON files become insufficient.
- No dashboard until CLI proves the pipeline works.
- No auto-publisher until manual posting is validated.
- If you are unsure whether you need it, you dont need it.
- Add abstraction only when you have three identical blocks, not before.

## Design Patterns

| Pattern | Where Used | Why |
|---|---|---|
| **Factory** | `get_expert(platform)` in `experts/__init__.py` | Creates right adapter without callers knowing subclasses |
| **Strategy** | All `SearchInterface` implementations | Swap YouTube for Reddit without changing research loop |
| **Template Method** | `PlatformExpert` base class with `adapt()` | Subclasses inherit shared logic, override only differences |
| **Decorator** | `@retry_on_failure()` in `base.py` | Adds retry to any function without modifying it |
| **Singleton** | `get_client()` in `search/web.py` | One DuckDuckGo client shared across all scrapers |
| **Registry** | HyperFrames template selection in `text_animator.py` | New block type = one template clause. No changes to the render loop |
| **Facade** | `run_research()` in `research/orchestrator.py` | Single function hiding scrape-filter-synthesise-generate-review cycle |
| **Value Object** | All Pydantic models in `schemas.py` | Immutable data contracts. No dicts floating around. |

## Naming Conventions (Mandatory)

### No underscore prefixes
- Do NOT use `_name` for "private" methods or variables.
- Python's `_` prefix convention is **not used** in this project.
- Methods: `def scrape()`, not `def _scrape()`
- Variables: `self.cache`, not `self._cache`
- Helpers: `def format_data()`, not `def _format_data()`

### Everything else follows standard Python
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- `self.thing` for instance attributes (no `self._thing`)

## Autonomous Agents (CrewAI)

Agents run sequentially in a Crew. Each has a role, goal, and backstory.

| Agent | Role | Output |
|---|---|---|
| Researcher | Senior Content Researcher | Raw scraped data + LLM trend synthesis |
| Strategist | Content Strategy Director | 3 topic proposals with platform-fit scores |
| Storyboard Director | Video Storyboard Director | Scene-by-scene shot list with timings |
| Producer | Content Production Director | Rendered video files + captions |

Agents are defined in `python/agents/` with CrewAI `Agent` + `Task` classes.
The Crew runs weekly. User reviews outputs at each checkpoint.

## KISS (Keep It Simple, Stupid)

- **No Kubernetes.** Docker Compose is enough.
- **No microservices.** One FastAPI app + Celery workers.
- **No RabbitMQ.** Redis is sufficient.
- **No complex config.** `persona.yaml` + `.env` covers everything.
- **V1: one platform.** Instagram Reels only. Prove the loop before scaling.
- **Junior test:** can a junior engineer understand the file in 5 minutes?

## DRY (Don't Repeat Yourself)

| What | DRY solution |
|---|---|
| Retry logic | `@retry_on_failure` decorator on `BasePublisher` |
| LLM prompts | `prompts.yaml` or `PromptRegistry` class. One place to edit. |
| Credentials | `.env` only. Never scattered across files. |
| File paths | `Path` constants in `config.py`. Never hardcoded strings. |
| API wrappers | `BaseScraper` with shared rate-limit handling, auth, error logging. |

## SOC (Separation of Concerns)

| Concern | File | Rule |
|---|---|---|
| Data contracts | `agents/schemas.py` | All Pydantic models. Every agent has typed input/output. |
| ABCs + decorators | `agents/base.py` | Interfaces and shared behavior. Never business logic. |
| Agent logic | `agents/{domain}/{agent}.py` | One job per file. Never inline prompts. |
| Prompts | `agents/prompts/{domain}/{name}.yaml` | Template text only. Never Python logic. |
| Config | `config/settings.py` | Paths, persona loader, prompt loader. Never agent code. |

## Naming Conventions (Mandatory)

### No underscore prefixes

## High-Level Design (HLD)

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────────┐
│  Researcher  │───▶│  Strategist  │───▶│  Storyboard  │───▶│   Producer     │
│              │    │              │    │              │    │                │
│ YouTube  API │    │ LLM proposes│    │ LLM generates│    │ HyperFrames  │
│ X       API  │    │ 3 topics    │    │ shot list     │    │ FFmpeg        │
│ DuckDuckGo   │    │ user picks 1│    │ scenes+timer  │    │ faster-whisper│
│ RSS feeds    │    │              │    │              │    │ Pillow        │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬─────────┘
       │                   │                   │                   │
       └───────────────────┴───────────────────┴───────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │  Object Store   │
                            │  (MinIO / S3)   │
                            │                 │
                            │  rendered/      │
                            │  captions/      │
                            │  raw/           │
                            │  images/        │
                            └─────────────────┘
```

### Data Flow

1. **Researcher** → scrapes YouTube + X directly, DuckDuckGo summarises IG/TT/LI/Threads → writes to MongoDB `weeks.research`
2. **Strategist** → reads research + `persona.yaml` → LLM proposes 3 topics with platform-fit scores → user picks 1
3. **Storyboard** → LLM reads script → generates scene-by-scene shot list with durations, camera angles, assets
4. **Producer** → branches on track:
   - **short_form**: faster-whisper → HyperFrames composition → FFmpeg composite → S3
   - **text_gen**: Pillow (code images) → HyperFrames TextAnimation → S3
5. **Output** → writes to MongoDB `renders` + `content_calendar`. User posts manually.

---

## Low-Level Design (LLD)

### Class Hierarchy

```
SearchInterface (ABC)
├── YouTubeScraper
├── XScraper
└── DuckDuckGoSummarizer

BasePublisher (ABC) — @retry_on_failure
├── InstagramPublisher
├── LinkedInPublisher
├── XPublisher
└── ThreadsPublisher

BaseRenderer (ABC)
├── OverlayRenderer   (HyperFrames, with A-Roll)
└── TextRenderer      (HyperFrames, no A-Roll)
```

### Key Interfaces

```python
class SearchInterface(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int) -> list[SearchResult]: ...

class BasePublisher(ABC):
    @retry_on_failure(max_retries=3, backoff=2)
    @abstractmethod
    def publish(self, content: PublishPayload) -> PublishResult: ...

class BaseRenderer(ABC):
    @abstractmethod
    def render(self, script: Script) -> RenderOutput: ...
```

### File Structure

```
python/
  agents/
    base.py                   # SearchInterface ABC + BasePublisher ABC
    search_youtube.py         # YouTubeScraper
    search_x.py               # XScraper
    search_web.py             # DuckDuckGoSummarizer + RSS
    strategist.py             # LLM topic proposer
    storyboard.py             # LLM shot list generator
    synthesizer_openai.py     # OpenAI LLM wrapper
  services/
    editor.py                 # faster-whisper + HyperFrames composition + FFmpeg
    text_animator.py          # Pillow + HyperFrames TextAnimation
    llm_service.py            # Shared LLM call logic
  main.py
  config.py                   # Path constants, env loader
  prompts.yaml                # All LLM prompts (DRY)
```

---

## UI/UX: Minimalist Modern + shadcn/ui

### Design Tokens

| Token | Value | Source |
|---|---|---|
| Primary font | Inter | `persona.yaml` |
| Heading font | Playfair Display | `persona.yaml` |
| Mono font | JetBrains Mono | `persona.yaml` |
| Accent | `#D4AF37` (gold) | CSS var `--gold` |
| Background (light) | `#FAFAFA` | CSS var `--alabaster` |
| Background (dark) | `#12141C` | CSS var `--obsidian` |
| Muted text | `#6B7280` | CSS var `--silent-gray` |

### Component Library

- **shadcn/ui** for all dashboard components (buttons, cards, dialogs, forms)
- **Tailwind CSS v4** for styling
- **tw-animate-css** for animations
- **Dark/light mode** via `.dark` class toggle

### Dashboard Layout

```
┌──────────────────────────────────────────┐
│  Header:  // BOREHAMWOOD • WORK_DAY      │
│  [Research] [Scripts] [Calendar]         │
├──────────────────────────────────────────┤
│                                          │
│  ┌─ Card: Topic 1 ──────────────────┐   │
│  │  Hook: "Building RAG at Scale"   │   │
│  │  Fit: LI:high  X:med  IG:low     │   │
│  │  [Select]                        │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌─ Card: Topic 2 ──────────────────┐   │
│  │  ...                              │   │
│  └──────────────────────────────────┘   │
│                                          │
└──────────────────────────────────────────┘
```

### Pages

| Route | Purpose | Components |
|---|---|---|
| `/research` | View 3 proposed topics, select one | `Card`, `Badge`, `Button` |
| `/scripts` | Review script + shot list, approve/reject | `Card`, `Separator`, `ScrollArea` |
| `/calendar` | Weekly content schedule | `Table`, `Badge`, `Switch` |
| `/renders` | Download finished output files | `Card`, `Button`, `Download` icon |

### UX Rules

- Every action is max 1 click. No multi-step wizards.
- Dark mode default (obsidian bg). Light mode toggle in header.
- Loading states = skeleton components (`<Skeleton />`).
- Errors = inline toast (`<Toast />`), not full-page errors.
- Mobile-first responsive. Single column on phone, 2-col on desktop.

---

## V1 Build Order

```
Week 1: BaseStrategyAgent → DuckDuckGoSearch → OpenAISynthesizer → Dashboard
        [Text-only loop. Prove the strategy layer works.]

Week 2: Storyboard agent → HyperFrames TextAnimation → Short-form video pipeline
        [One platform: Instagram Reels. One manual post.]

Week 3: Text animation pipeline → Pillow code images → 15s text posts
        [Add LinkedIn/X/Threads text-gen track.]

Week 4: YouTube Shorts + TikTok (same vertical.mp4)
        [Scale horizontally. No new pipeline code.]
```

## Pre-Commit Checklist

- [ ] Can I swap DuckDuckGo for Exa by changing ONE line? (Dependency Inversion)
- [ ] Does this file do ONE thing? (Single Responsibility)
- [ ] Am I copy-pasting anything? (DRY)
- [ ] Could a junior engineer understand this in 5 minutes? (KISS)
- [ ] Does adding a new platform require editing old code? (Open/Closed)
- [ ] Dark + light mode both work? (UI)
- [ ] Mobile responsive? (UI)
