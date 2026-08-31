"""Copywriter Agent -- writes master draft in Noah's voice from a topic.

S: Single responsibility -- writes one 100-150 word draft. Doesn't adapt per platform.
D: Depends on SynthesizerInterface, not concrete LLM.
O: New voice rules = edit the prompt. Agent code never changes.
"""

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona


class Copywriter:
    """Takes a topic, returns a master draft in Noah's voice."""

    def __init__(self, llm=None):
        self.llm = llm or OpenAISynthesizer(thinking=True)

    def write(self, topic: str) -> str:
        persona = load_persona()

        system = (
            f"You are {persona['creator']['name']}, {persona['creator']['title']}. "
            f"Write in your voice. Rules:"
            f" - Short sentences. Simple words. Grade 5-6 level."
            f" - Motivational tone. Focus on the opportunity, not the problem."
            f" - Use high-level terms for broad relevance. Dont name specific tools or acronyms."
            f" - One specific story. Real detail."
            f" - Messy structure. Like typed on a phone."
            f" - First person."
            f" - No transition phrases. No em dashes. No employer names."
            f" - Never write 'Here is the lesson', 'The takeaway', 'The moral of the story', or similar meta-commentary."
            f" - Never use a triple-structure closing ('Learn X. Understand Y. Know Z.'). End naturally."
            f" - Avoid narrative cliches: no one 'nodded', no 'bridge between ideas and reality', no generic metaphors."
            f" - Be specific and concrete. If someone approved something, say what happened. Not 'leaders nodded'."
            f" - ~100-150 words."
        )

        prompt = (
            f"Topic: {topic}\n\n"
            f"Step 1: Pick a post structure.\n"
            f" - hook -> story -> lesson: start bold, tell what happened, end with takeaway\n"
            f" - problem -> fix -> result: state the issue, share the solution, show outcome\n"
            f" - observation -> why it matters -> your take: notice something, explain impact, give opinion\n"
            f" - claim -> evidence -> invite: make a statement, back it up, ask a question\n\n"
            f"Step 2: Write the post. One specific story. Simple words. ~100-150 words."
        )

        return self.llm.synthesize(
            prompt,
            system=system,
            temperature=0.7,
            max_tokens=500,
        )
