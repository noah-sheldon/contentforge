"""Review Agent — per-platform quality gate.

S: Each review checks ONE platform draft. Independent retry per platform.
O: New platform = new expert + new platform YAML adds checks automatically.
"""

from agents.experts import load_platform_checks
from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_prompt


class PlatformReview:
    """Reviews a platform-specific draft. Returns (passed, notes).

    Usage:
        review = PlatformReview("linkedin")
        passed, notes = review.check(draft_text)
        if not passed:
            print(f"Fix: {notes}")
    """

    def __init__(self, platform: str, llm=None):
        self.platform = platform
        self.llm = llm or OpenAISynthesizer(thinking=False)

    def check(self, draft: str) -> tuple[bool, str]:
        checks = load_platform_checks(self.platform)
        prompt = load_prompt(
            "copy/review",
            platform=self.platform,
            draft=draft,
            platform_checks=checks,
        )
        result = self.llm.synthesize(prompt, temperature=0.2, max_tokens=120)
        if not result or not result.strip():
            return True, ""  # Empty = assume pass (lenient)

        upper = result.upper()

        if "VERDICT: PASS" in upper:
            return True, ""
        if "VERDICT: FAIL" in upper:
            if "NOTES:" in result:
                notes = result.split("NOTES:")[-1].strip()
            else:
                notes = result.replace("VERDICT:", "").replace("FAIL", "").strip()
            return False, notes
        if "PASS" in upper and "FAIL" not in upper:
            return True, ""

        return False, result.strip()


def run_review(platform: str, draft: str) -> tuple[bool, str]:
    """Shorthand: create review, run check."""
    return PlatformReview(platform).check(draft)
