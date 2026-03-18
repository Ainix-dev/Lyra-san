"""
COGNITIVE ORCHESTRATOR - Central Pipeline Controller
Coordinates all cognitive systems and controls the complete response pipeline.
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CognitiveOrchestrator:
    """
    Central controller for the complete cognitive pipeline:
    Input → Mode Detection → Module Gating → Prompt Build
         → Generation → Validation → Memory Update → Output
    """
    
    def __init__(self, mode_controller, output_validator, personality_engine):
        self.mode_controller = mode_controller
        self.output_validator = output_validator
        self.personality_engine = personality_engine
        
        self.pipeline_state = {
            "input": "",
            "detected_mode": "CHAT",
            "modules_enabled": {},
            "prompt_built": "",
            "generation_attempt": 0,
            "last_output": "",
            "validation_passed": False,
        }
        
        self.max_regeneration_attempts = 3
        self.execution_log = []
    
    def process_input(self, user_input: str, unified_state=None) -> Dict:
        """
        Main orchestration function: execute the complete pipeline.
        Returns pipeline result with metadata.
        """
        self.mode_controller.advance_turn()
        self.pipeline_state["input"] = user_input
        
        # Step 1: Detect appropriate mode
        detected_mode = self.mode_controller.detect_mode(user_input)
        if not self.mode_controller.mode_lock:
            self.mode_controller.set_mode(detected_mode)
        
        self.pipeline_state["detected_mode"] = self.mode_controller.current_mode
        
        # Step 2: Gate modules based on mode
        enabled_modules = self._gate_modules()
        self.pipeline_state["modules_enabled"] = enabled_modules
        
        # Step 3: Build prompt with mode and personality
        mode_prompt = self.mode_controller.get_mode_prompt_modifier()
        personality_prompt = self.personality_engine.inject_personality(
            tone=self.mode_controller.get_mode_config()["tone"],
            intensity=self.mode_controller.get_mode_config()["personality_intensity"]
        )
        
        self.pipeline_state["prompt_built"] = mode_prompt + personality_prompt
        
        # Step 4: Mark that this pipeline is ready
        pipeline_ready = {
            "ready": True,
            "mode": self.mode_controller.current_mode,
            "enabled_modules": enabled_modules,
            "mode_instructions": mode_prompt,
            "personality_instructions": personality_prompt,
            "max_generations": self.max_regeneration_attempts,
        }
        
        return pipeline_ready
    
    def validate_and_regenerate(self, response: str, attempt: int = 1) -> Tuple[str, bool, int]:
        """
        Validate response. If invalid, return failure signal for regeneration.
        Returns: (response, is_valid, attempt_number)
        """
        self.pipeline_state["generation_attempt"] = attempt
        
        # Sanitize first
        sanitized = self.output_validator.sanitize(response)
        
        # Then validate
        is_valid, violations = self.output_validator.validate(
            sanitized,
            mode=self.mode_controller.current_mode,
            strict=(attempt > 1)  # Stricter on retry
        )
        
        if not is_valid:
            self.output_validator.regeneration_count += 1
            if attempt < self.max_regeneration_attempts:
                return sanitized, False, attempt + 1
            else:
                # Max attempts reached, return fallback
                return self._get_fallback_response(), True, attempt
        
        self.pipeline_state["last_output"] = sanitized
        self.pipeline_state["validation_passed"] = True
        return sanitized, True, attempt
    
    def finalize_output(self, response: str, internal_state: Dict = None) -> Dict:
        """
        Final output preparation. Return clean response with metadata.
        """
        output_package = {
            "response": response,
            "mode": self.mode_controller.current_mode,
            "personality_report": self.personality_engine.get_personality_report(),
            "validation_status": "passed" if self.pipeline_state["validation_passed"] else "fallback",
            "generation_attempts": self.pipeline_state["generation_attempt"],
            "timestamp": datetime.now().isoformat(),
        }
        
        # Log execution
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "input": self.pipeline_state["input"][:100],
            "mode": self.mode_controller.current_mode,
            "output_length": len(response),
            "validation_passed": self.pipeline_state["validation_passed"],
        })
        
        return output_package
    
    def _gate_modules(self) -> Dict[str, bool]:
        """Determine which cognitive modules are active for current mode."""
        config = self.mode_controller.get_mode_config()
        
        return {
            "reasoning": config["allow_reasoning"],
            "memory_deep_recall": config["allow_memory_deep_recall"],
            "identity_talk": config["allow_identity_talk"],
            "internal_monologue": not config["suppress_cognition"],
            "personality_injection": True,  # Always on
            "error_recovery": True,  # Always on
        }
    
    def _get_fallback_response(self) -> str:
        """Get safe fallback response when validation keeps failing."""
        fallbacks = [
            "I'm having a moment. Let me think about that differently.",
            "You know what, I think I'm overthinking this. What I meant to say is—hmm, actually, what's your take?",
            "That's a good question. I'm genuinely unsure how to put it into words right now.",
            "Let me come back to that. For now: I hear you.",
        ]
        import random
        return random.choice(fallbacks)
    
    def get_pipeline_diagnostics(self) -> Dict:
        """Get diagnostic info about the pipeline."""
        return {
            "mode": self.mode_controller.get_mode_stats(),
            "validation": self.output_validator.get_validation_report(),
            "personality": self.personality_engine.get_personality_report(),
            "recent_executions": self.execution_log[-5:],
        }
