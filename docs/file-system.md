# File Structure (Updated July 2026)

```
python/
  agents/
    base.py                    # ABCs: SearchInterface, SynthesizerInterface, @retry_on_failure
    copywriter.py              # Writes ~100-150 word master draft in Noah's voice
    review.py                  # Per-platform quality gate (pass/fail)
    search/
      youtube.py               # YouTube Data API v3 scraper
      x.py                     # X API v2 scraper (read-only, free tier)
      web.py                   # DuckDuckGo + RSS summarizer (for IG/TT/LI summaries)
    research/
      orchestrator.py          # Runs all scrapers + LLM synthesis
    strategy/
      strategist.py            # LLM proposes 3 topics with platform-fit scores
    storyboard/
      director.py              # Shot list generator (for video pipeline, V2)
      animation_director.py    # Block type selector (text_card, code_block, diagram, etc.)
    synthesis/
      openai.py                # OpenAI LLM wrapper
    experts/
      __init__.py              # LinkedInExpert, XExpert, ThreadsExpert adapters
    platforms/
      linkedin.yaml            # Platform rules + templates
      x.yaml
      threads.yaml
    prompts/
      research/                # synthesis.yaml, topic_selection.yaml
      copy/                    # copywriter.yaml, review.yaml
      experts/                 # linkedin.yaml, x.yaml, threads.yaml
      story/                   # storyboard.yaml, animation_director.yaml
  config/
    settings.py                # Paths, persona loader, prompt loader (DRY)
  services/
    text_animator.py           # AnimationDirector + HyperFrames render orchestration
    code_snapper.py            # Pillow code snippet images
  scripts/
    run_crew.py                # Main entry point (manual + auto flows)
    render_text.py             # Quick render from CLI args
  state/
    pipeline_manager.py        # JSON-based HITL pause/resume
  tests/                       # Placeholder
  requirements.txt
  .env.example

templates/short-form/        # Format templates (each a HyperFrames project)
  day-in-my-life/
    spec.md + index.html
  desk-setup/
    spec.md + index.html
  transformation/
    spec.md + index.html

workspace/shortform/         # Per-day HyperFrames projects (git-ignored)

output/
  week_N/                      # Generated renders
    linkedin.txt + .mp4
    x.txt + .mp4
    threads.txt + .mp4
