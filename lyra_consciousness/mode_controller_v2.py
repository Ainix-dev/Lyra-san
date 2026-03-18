"""
MODE CONTROLLER - Behavioral mode system for Lyra
Modes: PLAY, CHAT, REFLECT, ANALYZE
"""

from datetime import datetime
from typing import Dict, List, Optional

class ModeController:
    """Central mode management system."""
    
    def __init__(self):
        self.current_mode = "CHAT"
        self.modes = {
            "PLAY": {
                "description": "Playful, casual, minimal introspection",
                "allow_reasoning": False,
                "allow_memory_deep_recall": False,
                "allow_identity_talk": False,
                "tone": "playful",
                "max_response_length": 300,
                "suppress_cognition": True,
                "personality_intensity": 0.9,
            },
            "CHAT": {
                "description": "Normal conversation, balanced cognition",
                "allow_reasoning": False,
                "allow_memory_deep_recall": True,
                "allow_identity_talk": False,
                "tone": "conversational",
                "max_response_length": 800,
                "suppress_cognition": False,
                "personality_intensity": 0.7,
            },
            "REFLECT": {
                "description": "Deep thoughtful responses, introspection allowed",
                "allow_reasoning": True,
                "allow_memory_deep_recall": True,
                "allow_identity_talk": True,
                "tone": "thoughtful",
                "max_response_length": 2000,
                "suppress_cognition": False,
                "personality_intensity": 0.5,
            },
            "ANALYZE": {
                "description": "Technical, analytical, no fluff",
                "allow_reasoning": True,
                "allow_memory_deep_recall": False,
                "allow_identity_talk": False,
                "tone": "analytical",
                "max_response_length": 1500,
                "suppress_cognition": False,
                "personality_intensity": 0.2,
            },
        }
        
        self.mode_history = []
        self.mode_lock = False
        self.mode_lock_until_turn = 0
        self.turn_count = 0
        self.last_mode_switch = datetime.now()
    
    def detect_mode(self, user_input: str) -> str:
        """Auto-detect appropriate mode from user input."""
        lower_input = user_input.lower()
        
        if any(word in lower_input for word in ["let's play", "game", "fun", "joke", "riddle"]):
            return "PLAY"
        elif any(word in lower_input for word in ["think", "reflect", "why", "meaning", "consciousness"]):
            return "REFLECT"
        elif any(word in lower_input for word in ["analyze", "explain", "breakdown", "technical"]):
            return "ANALYZE"
        else:
            return "CHAT"
    
    def set_mode(self, new_mode: str) -> bool:
        """Switch to a new mode."""
        if new_mode not in self.modes:
            return False
        
        if self.mode_lock and self.turn_count < self.mode_lock_until_turn:
            return False  # Mode is locked
        
        old_mode = self.current_mode
        self.current_mode = new_mode
        self.last_mode_switch = datetime.now()
        
        # Record mode switch
        self.mode_history.append({
            "timestamp": datetime.now().isoformat(),
            "from": old_mode,
            "to": new_mode,
            "turn": self.turn_count,
        })
        
        return True
    
    def lock_mode(self, turns: int = 3):
        """Lock current mode for N turns to prevent mode drift."""
        self.mode_lock = True
        self.mode_lock_until_turn = self.turn_count + turns
    
    def unlock_mode(self):
        """Unlock mode switching."""
        self.mode_lock = False
    
    def get_mode_config(self) -> Dict:
        """Get current mode configuration."""
        return self.modes[self.current_mode].copy()
    
    def get_mode_prompt_modifier(self) -> str:
        """Generate system prompt modifier for current mode."""
        config = self.get_mode_config()
        
        return f"""
[MODE: {self.current_mode}]
Mode Description: {config['description']}
Tone: {config['tone']}
Personality Intensity: {int(config['personality_intensity']*100)}%

Behaviors for this mode:
- Reasoning: {'Enabled' if config['allow_reasoning'] else 'Disabled (keep answers direct)'}
- Memory Recall: {'Deep retrieval allowed' if config['allow_memory_deep_recall'] else 'Surface-level only'}
- Identity Discussion: {'Allowed' if config['allow_identity_talk'] else 'Avoid talking about yourself'}
- Response Length: Target {config['max_response_length']} chars max
- Internal Cognition: {'Show your thinking' if not config['suppress_cognition'] else 'Keep thinking hidden'}

Focus on the {config['tone']} tone above all else.
"""
    
    def advance_turn(self):
        """Increment turn counter."""
        self.turn_count += 1
    
    def get_mode_history(self, limit: int = 10) -> List[Dict]:
        """Get recent mode switches."""
        return self.mode_history[-limit:]
    
    def get_mode_stats(self) -> Dict:
        """Get mode usage statistics."""
        mode_counts = {}
        for entry in self.mode_history:
            mode = entry["to"]
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        return {
            "current_mode": self.current_mode,
            "turn_count": self.turn_count,
            "mode_usage": mode_counts,
            "mode_locked": self.mode_lock,
        }
