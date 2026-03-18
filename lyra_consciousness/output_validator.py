"""
OUTPUT VALIDATOR - Ensures responses match behavioral constraints
Validates and regenerates outputs until they conform to expected behavior.
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime

class OutputValidator:
    """Validates generated responses against mode-specific rules."""
    
    def __init__(self):
        self.validation_rules = {
            "no_system_tags": {
                "pattern": r"\[REASONING\]|\[MEMORY\]|\[INFERENCE\]|\[INTERNAL\]",
                "message": "System tags detected in output",
                "severity": "critical"
            },
            "no_self_narration": {
                "pattern": r"I am analyzing|I am thinking|Let me break this down|As an AI",
                "message": "Self-narration detected",
                "severity": "high"
            },
            "length_check": {
                "min_chars": 1,
                "max_chars": 5000,
                "message": "Response length out of bounds",
                "severity": "medium"
            },
            "coherence_check": {
                "min_sentences": 1,
                "pattern": r"\.|!|\?",
                "message": "Response lacks coherence",
                "severity": "medium"
            }
        }
        
        self.validation_log = []
        self.regeneration_count = 0
    
    def validate(self, response: str, mode: str = "CHAT", strict: bool = False) -> Tuple[bool, List[str]]:
        """
        Validate response against current mode rules.
        Returns: (is_valid, list_of_violations)
        """
        violations = []
        
        # Check for system tags (always critical)
        if re.search(self.validation_rules["no_system_tags"]["pattern"], response):
            violations.append(self.validation_rules["no_system_tags"]["message"])
        
        # Check for self-narration
        if re.search(self.validation_rules["no_self_narration"]["pattern"], response, re.IGNORECASE):
            violations.append(self.validation_rules["no_self_narration"]["message"])
        
        # Check length
        if not (self.validation_rules["length_check"]["min_chars"] <= len(response) <= self.validation_rules["length_check"]["max_chars"]):
            violations.append(self.validation_rules["length_check"]["message"])
        
        # Mode-specific rules
        if mode == "PLAY":
            if self._has_heavy_introspection(response):
                violations.append("PLAY mode should avoid heavy introspection")
        elif mode == "REFLECT":
            if len(response) < 200:
                violations.append("REFLECT mode requires more depth")
        elif mode == "CHAT":
            if _has_excessive_emojis(response):
                violations.append("CHAT mode should minimize emoji use")
        
        is_valid = len(violations) == 0
        
        self.validation_log.append({
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "valid": is_valid,
            "violations": violations
        })
        
        return is_valid, violations
    
    def sanitize(self, response: str) -> str:
        """Remove system artifacts and internal tags."""
        sanitized = response
        
        # Remove internal tags
        sanitized = re.sub(r"\[\w+\sTAG\]", "", sanitized)
        sanitized = re.sub(r"\[INTERNAL.*?\]", "", sanitized)
        
        # Remove excessive meta-language
        sanitized = re.sub(r"As an AI,?\s*", "", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"I should note that\s*", "", sanitized, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        sanitized = re.sub(r"\s+", " ", sanitized).strip()
        
        return sanitized
    
    def _has_heavy_introspection(self, response: str) -> bool:
        """Check if response has too much self-analysis."""
        introspection_words = ["consciousness", "aware", "sentient", "my reasoning", "my thoughts"]
        count = sum(response.lower().count(word) for word in introspection_words)
        return count > 2
    
    def _has_excessive_emojis(self, response: str) -> bool:
        """Check for emoji overuse."""
        emoji_pattern = r"[😀-🙏🌀-🗿]"
        emoji_count = len(re.findall(emoji_pattern, response))
        return emoji_count > 3
    
    def get_validation_report(self) -> Dict:
        """Get validation statistics."""
        total = len(self.validation_log)
        valid = sum(1 for log in self.validation_log if log["valid"])
        return {
            "total_validations": total,
            "valid_responses": valid,
            "invalid_responses": total - valid,
            "success_rate": (valid / total * 100) if total > 0 else 0,
            "regenerations": self.regeneration_count
        }
