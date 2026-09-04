"""Pydantic models for all agent contracts.

S: Every agent has explicit input/output types. No dict passing.
O: New agent = new model. Existing models never change.
"""

from enum import Enum

from pydantic import BaseModel, Field

# ─── Enums ────────────────────────────────────────────────────────────


class Platform(str, Enum):
    linkedin = "linkedin"
    x = "x"
    threads = "threads"
    youtube = "youtube"


class Track(str, Enum):
    text_gen = "text_gen"
    short_form = "short_form"


class RunType(str, Enum):
    manual = "manual"
    auto = "auto"


class ReviewVerdict(str, Enum):
    passed = "passed"
    failed = "failed"


# ─── Persona / Brand ─────────────────────────────────────────────────


class BrandColors(BaseModel):
    obsidian: str = "#12141C"
    alabaster: str = "#FAFAFA"
    gold: str = "#D4AF37"
    silent_gray: str = "#6B7280"


class Persona(BaseModel):
    name: str
    title: str
    tagline: str
    niche: str
    audience: str
    tone: str
    brand: BrandColors = Field(default_factory=BrandColors)


# ─── Research Models ─────────────────────────────────────────────────


class ResearchRequest(BaseModel):
    query: str = "AI engineering machine learning production"
    max_results: int = 20


class ResearchResult(BaseModel):
    topics: list[dict] = Field(default_factory=list)
    synthesis: str = ""
    raw_count: dict = Field(default_factory=dict)


# ─── Topic Models ────────────────────────────────────────────────────


class TopicProposal(BaseModel):
    topic: str
    complexity_score: int = Field(ge=1, le=10)
    reason: str = ""


class TopicHistoryEntry(BaseModel):
    topic: str
    date: str
    platforms: list[str] = Field(default_factory=list)
    complexity_score: int = 3


# ─── Copywriter Models ───────────────────────────────────────────────


class CopywriterInput(BaseModel):
    topic: str
    persona: Persona


class CopywriterOutput(BaseModel):
    draft: str
    word_count: int = 0


# ─── Expert Models ───────────────────────────────────────────────────


class ExpertInput(BaseModel):
    draft: str
    platform: Platform
    persona: Persona


class ExpertOutput(BaseModel):
    text: str
    platform: Platform
    char_count: int = 0


# ─── Review Models ───────────────────────────────────────────────────


class ReviewInput(BaseModel):
    draft: str
    platform: Platform


class ReviewOutput(BaseModel):
    verdict: ReviewVerdict
    notes: str = ""
    score: int = Field(default=5, ge=1, le=10)


# ─── Animation Models ────────────────────────────────────────────────


class Block(BaseModel):
    type: str  # text_card, code_block, diagram, comparison, metric, quote
    duration_seconds: float = Field(gt=0)
    data: dict = Field(default_factory=dict)


class AnimationInput(BaseModel):
    hook: str
    body: str
    brand: BrandColors = Field(default_factory=BrandColors)


class AnimationOutput(BaseModel):
    blocks: list[Block] = Field(default_factory=list)
    total_duration: float = 15.0


# ─── Render Models ───────────────────────────────────────────────────


class RenderInput(BaseModel):
    hook: str
    body: str
    output_dir: str = "output"


class RenderOutput(BaseModel):
    video_path: str
    text_path: str
    platform: Platform


# ─── Pipeline State Models ───────────────────────────────────────────


class PipelineStep(BaseModel):
    data: str
    completed_at: str = ""


class PipelineState(BaseModel):
    run_id: str = ""
    run_type: RunType = RunType.manual
    topic: str = ""
    status: str = "started"
    steps: dict[str, PipelineStep] = Field(default_factory=dict)
    output: dict[str, dict] = Field(default_factory=dict)
