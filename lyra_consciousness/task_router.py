"""
Task Router: Decides if input is a structured pattern (e.g., knock-knock joke) or open conversation.
Routes to either full cognition or pattern engine.
"""

import re

class TaskRouter:
    def __init__(self):
        pass

    def detect_task(self, context):
        # Simple knock-knock pattern detection
        if self.is_knock_knock_sequence(context):
            return "PATTERN"
        return "OPEN"

    def is_knock_knock_sequence(self, context):
        # Look for knock-knock pattern in last 2-3 turns
        if not context or len(context) < 1:
            return False
        last = context[-1].lower()
        if "knock knock" in last:
            return True
        if len(context) >= 2 and "who's there" in context[-2].lower():
            return True
        return False
