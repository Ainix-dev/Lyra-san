"""
Perception and Action Modules for Lyra Consciousness
"""

from datetime import datetime

class PerceptionLayer:
    """Interprets user input into structured cognitive signals."""

    def __init__(self):
        self.last_perception = {}

    def perceive(self, user_input: str, unified_state: object = None, memory_context: str = "") -> dict:
        """Return perception metadata for planning and introspection."""
        cue = "neutral"
        intent = "respond"
        if user_input.strip().endswith("?"):
            intent = "question"
        if "please" in user_input.lower() or "can you" in user_input.lower():
            cue = "polite_request"
        if any(tok in user_input.lower() for tok in ["remember", "recall", "forget"]):
            intent = "memory"
        if any(tok in user_input.lower() for tok in ["plan", "strategy", "next step", "goal"]):
            intent = "planning"

        perceived = {
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "cue": cue,
            "text_summary": user_input[:300],
            "memory_context_length": len(memory_context),
            "state_confidence": unified_state.state.get("capability_assessment", {}).get("self_awareness", 0.5) if unified_state else 0.5,
        }
        self.last_perception = perceived
        return perceived

    def build_perception_prompt(self, perception: dict) -> str:
        return (
            "[PERCEPTION MODULE]\n"
            f"- Detected intent: {perception.get('intent')}\n"
            f"- Communication cue: {perception.get('cue')}\n"
            f"- Summary: {perception.get('text_summary')}\n"
            f"- Memory context length: {perception.get('memory_context_length')}\n"
            f"- Self-awareness confidence: {perception.get('state_confidence'):.2f}\n"
        )


class ActionController:
    """Carries out simple cognitive actions and logs outcomes."""

    def __init__(self):
        self.action_history = []

    def choose_action(self, plan: dict) -> str:
        action = plan.get("next_action", "reflect")
        if "memory" in plan.get("focus", "") and plan.get("next_action"):
            action = plan.get("next_action")
        self.action_history.append({"chosen_action": action, "at": datetime.now().isoformat()})
        return action

    def execute(self, action: str) -> dict:
        result = {
            "action": action,
            "outcome": "executed",
            "timestamp": datetime.now().isoformat(),
            "notes": "Action executed in simulation mode."
        }
        self.action_history.append(result)
        return result

    def get_recent_actions(self, limit: int = 5):
        return self.action_history[-limit:]
