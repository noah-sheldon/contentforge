"""Platform Expert Agents -- adapt master draft per platform rules.

S: Each expert handles ONE platform.
O: New platform = new expert file. Zero changes to existing code.
D: Reads platform rules from YAML, depends on SynthesizerInterface.
"""

import yaml

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import AGENTS_DIR, load_prompt

PLATFORMS_DIR = AGENTS_DIR / "platforms"


def load_platform_rules(name: str) -> str:
    with open(PLATFORMS_DIR / f"{name}.yaml") as f:
        data = yaml.safe_load(f)
    rules = []
    p = data["platform"]
    rules.append(f"Platform: {p['name']}")
    rules.append(f"Max chars: {p.get('max_chars', 'N/A')}")
    rules.append(f"Tone: {data['tone']['style']}")
    rules.append(f"Voice: {data['tone']['voice']}")
    rules.append("\nWhat works:")
    rules.extend(f"- {w}" for w in data.get("what_works", []))
    return "\n".join(rules)


def load_platform_checks(name: str) -> str:
    with open(PLATFORMS_DIR / f"{name}.yaml") as f:
        data = yaml.safe_load(f)
    checks = []
    p = data["platform"]
    checks.append(f"- Max {p.get('max_chars', 'N/A')} characters")
    hl = p.get("hashtag_limit")
    if hl:
        checks.append(f"- Max {hl} hashtags")
    checks.append(f"- Tone: {data['tone']['style']}")
    checks.extend(f"- Avoid: {a}" for a in data["tone"].get("avoid", []))
    return "\n".join(checks)


class PlatformExpert:
    """Base for platform experts. Each subclass adapts a master draft."""

    def __init__(self, platform: str, llm=None):
        self.platform = platform
        self.prompt_name = f"experts/{platform}"
        self.llm = llm or OpenAISynthesizer(thinking=False)

    def adapt(self, draft: str, persona: dict) -> str:
        rules = load_platform_rules(self.platform)
        prompt = load_prompt(
            self.prompt_name,
            platform_rules=rules,
            draft=draft,
            creator_name=persona["creator"]["name"],
            title=persona["creator"]["title"],
        )
        return self.llm.synthesize(prompt, temperature=0.6)


class LinkedInExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("linkedin", llm)


class XExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("x", llm)


class ThreadsExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("threads", llm)


class InstagramExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("instagram", llm)


class TikTokExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("tiktok", llm)


class YouTubeShortsExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("youtube_shorts", llm)


class YouTubeLongFormExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("youtube_long", llm)


class FacebookExpert(PlatformExpert):
    def __init__(self, llm=None):
        super().__init__("facebook", llm)


def get_expert(platform: str, llm=None) -> PlatformExpert:
    """Factory: returns the right expert for a platform name."""
    mapping = {
        "linkedin": LinkedInExpert,
        "x": XExpert,
        "threads": ThreadsExpert,
        "instagram": InstagramExpert,
        "tiktok": TikTokExpert,
        "youtube_shorts": YouTubeShortsExpert,
        "youtube_long": YouTubeLongFormExpert,
        "facebook": FacebookExpert,
    }
    cls = mapping.get(platform)
    if not cls:
        raise ValueError(f"Unknown platform: {platform}")
    return cls(llm)
