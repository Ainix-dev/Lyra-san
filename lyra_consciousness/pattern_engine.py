"""
Pattern Engine: Handles deterministic pattern continuations (e.g., knock-knock jokes).
No reasoning, memory, identity, inference, or tone adaptation.
"""

class PatternEngine:
    def __init__(self):
        # Define supported patterns
        self.knock_knock_flow = [
            "Knock knock",
            "Who's there?",
            "<X>",
            "<X> who?",
            "<punchline>"
        ]

    def generate_knock_knock_response(self, context):
        # Determine which step we're on
        step = self._get_knock_knock_step(context)
        if step == 1:
            return "Who's there?"
        elif step == 2:
            # Expecting a name/word
            return f"{context[-1]} who?"
        elif step == 3:
            return "(punchline)"
        else:
            return "Knock knock"

    def _get_knock_knock_step(self, context):
        # Returns step number in knock-knock flow
        if not context:
            return 0
        if "knock knock" in context[-1].lower():
            return 1
        if len(context) >= 2 and "who's there" in context[-2].lower():
            return 2
        if len(context) >= 3 and context[-3].lower().startswith("knock knock"):
            return 3
        return 0

    def handle(self, context):
        # For now, only knock-knock supported
        return self.generate_knock_knock_response(context)
