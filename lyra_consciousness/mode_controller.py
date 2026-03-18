"""
Mode Controller
Selects operation mode from intent and adjusts cognitive parameters.

Modes: 'play', 'relaxed', 'focused'
"""
from typing import Dict


def select_mode(intent: str, unified_state) -> Dict:
    """Return a mode dict based on intent and optionally unified_state.

    mode dict keys: 'mode', 'cognition' (str), 'strict_blocking' (bool)
    """
    mode = "relaxed"
    cognition = "normal"
    strict_blocking = False

    if intent == "game":
        mode = "play"
        cognition = "low"
        strict_blocking = True  # enforce structured outputs for games

    elif intent == "deep_reasoning":
        mode = "focused"
        cognition = "high"
        strict_blocking = False

    else:
        mode = "relaxed"
        cognition = "normal"
        strict_blocking = False

    # Optionally bias based on internal capability assessment
    try:
        caps = unified_state.get_capability_assessment()
        if cognition == "high" and caps.get("reasoning_strength", 0.5) < 0.4:
            # if reasoning capacity is low, be more conservative
            cognition = "moderate"
    except Exception:
        pass

    return {"mode": mode, "cognition": cognition, "strict_blocking": strict_blocking}
