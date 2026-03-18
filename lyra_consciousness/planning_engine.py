"""
Planning Engine for Hierarchical Internal Goals and Task Execution
"""

from datetime import datetime

class Planner:
    """Create and manage plans from perception and goals."""

    def __init__(self):
        self.long_term_goals = []
        self.current_plan = None
        self.plan_history = []

    def set_long_term_goal(self, goal: str, priority: float = 0.5):
        self.long_term_goals.append({
            "goal": goal,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "status": "active",
        })

    def generate_plan(self, user_input: str, perception: dict, unified_state: object = None) -> dict:
        """Map user intent into a short-term plan."""
        if perception.get("intent") == "memory":
            next_action = "retrieve_relevant_memories"
            focus = "memory_recall"
        elif perception.get("intent") == "planning":
            next_action = "create_stepwise_plan"
            focus = "planning"
        elif perception.get("intent") == "question":
            next_action = "answer_with_clarity"
            focus = "clarity"
        else:
            next_action = "respond_with_context"
            focus = "contextual"

        if unified_state:
            active_goals = unified_state.get_active_goals() if hasattr(unified_state, 'get_active_goals') else []
        else:
            active_goals = []

        plan = {
            "created": datetime.now().isoformat(),
            "user_intent": perception.get("intent"),
            "next_action": next_action,
            "focus": focus,
            "active_goals": active_goals,
            "plan_text": f"Based on intent [{perception.get('intent')}], the next step is {next_action}."
        }
        self.current_plan = plan
        self.plan_history.append(plan)
        return plan

    def refine_plan(self, plan: dict, outcome: dict) -> dict:
        plan["last_outcome"] = outcome
        plan["refined_at"] = datetime.now().isoformat()
        plan["confidence"] = 0.5
        self.plan_history.append(plan)
        return plan

    def get_plan_summary(self, limit: int = 3):
        return self.plan_history[-limit:]
