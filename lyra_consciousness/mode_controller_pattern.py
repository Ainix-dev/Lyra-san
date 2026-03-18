# Add PATTERN mode to mode controller
from lyra_consciousness.mode_controller_v2 import ModeController

class ModeControllerV2(ModeController):
    def __init__(self):
        super().__init__()
        self.modes["PATTERN"] = {
            "max_length": 80,
            "tone": "neutral",
            "personality_intensity": 0.0,
            "description": "Deterministic pattern continuation only. No reasoning, memory, or personality.",
        }

    def detect_mode(self, user_input: str):
        # If task router says pattern, force PATTERN mode
        from lyra_consciousness.task_router import TaskRouter
        router = TaskRouter()
        # For now, context is just [user_input]
        if router.detect_task([user_input]) == "PATTERN":
            return "PATTERN"
        return super().detect_mode(user_input)
