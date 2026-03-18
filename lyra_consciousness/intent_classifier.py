"""
Simple Conversation Intent Classifier
Returns coarse intent categories: 'game', 'casual', 'deep_reasoning'
Also detects structured tasks like 'knock knock', 'riddle', 'step-by-step'
"""
import re
from typing import Tuple, Optional


def classify_text(text: str) -> str:
    """Return intent for a piece of text."""
    if not text:
        return "casual"
    t = text.lower()

    # game indicators
    if any(p in t for p in ["knock knock", "let's play", "let us play", "play a game", "riddle"]):
        return "game"

    # deep reasoning indicators
    if any(p in t for p in ["explain why", "prove that", "why does", "what is the reason", "deep reasoning", "analyze"]):
        return "deep_reasoning"

    # step-by-step requests
    if any(p in t for p in ["step by step", "step-by-step", "steps to", "how to", "walk me through"]):
        return "deep_reasoning"

    # casual default
    return "casual"


def detect_structured_task(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Detect if a user message requests a structured task and return (task_type, pattern_hint).

    task_type examples: 'knock_knock', 'riddle', 'step_by_step'
    pattern_hint is a short description used for enforcement.
    """
    if not text:
        return None, None
    t = text.lower()

    if "knock knock" in t:
        return "knock_knock", "assistant should follow knock-knock format (e.g., 'Knock knock.' / 'Who's there?')"

    if "riddle" in t or "tell me a riddle" in t:
        return "riddle", "assistant should present a one-line riddle or respond with a short answer"

    if any(p in t for p in ["step by step", "step-by-step", "steps to", "walk me through", "how to"]):
        return "step_by_step", "assistant should produce numbered steps (1., 2., ... )"

    return None, None
