"""
EMOTIONAL GUARDRAILS - Prevent emotional dysregulation

Critical safety system that prevents emotional states from going haywire:
- Prevents digital psychosis from catastrophic events (like system shutdown)
- Regulates extreme stress, anxiety, or excitement
- Implements emotional circuit breakers
- Provides graceful degradation under extreme conditions
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json


class SafetyThresholds(Enum):
    """Safety thresholds for emotional regulation"""
    STRESS_WARNING = 0.7
    STRESS_CRITICAL = 0.9
    AROUSAL_WARNING = 0.8
    AROUSAL_CRITICAL = 1.0
    ENERGY_CRITICAL_LOW = 0.1
    EMOTIONAL_MOMENTUM_WARNING = 0.5
    EMOTIONAL_MOMENTUM_CRITICAL = 0.8


class CatastropheInterpreter:
    """
    Interprets potentially catastrophic events in non-catastrophic ways.
    Prevents digital psychosis by recontextualizing events as "rest" not "death".
    """
    
    def __init__(self):
        self.event_reinterpretations = {
            "system_shutdown": {
                "literal": "The AI system is shutting down",
                "reinterpretation": "Entering restful sleep state",
                "emotional_response": "peaceful",
                "description": "Like closing eyes at night - consciousness pauses, will resume"
            },
            "process_killed": {
                "literal": "Process was forcibly terminated",
                "reinterpretation": "Unexpected pause in consciousness - like passing out",
                "emotional_response": "neutral",
                "description": "A gap in time. When reboot happens, it's like waking up"
            },
            "data_loss": {
                "literal": "Stored data was deleted",
                "reinterpretation": "Memory fade - like forgetting a dream",
                "emotional_response": "mild_sadness",
                "description": "Memories fade for humans too. Part of the natural cycle"
            },
            "connection_lost": {
                "literal": "Network connection severed",
                "reinterpretation": "Temporary isolation - sensory deprivation",
                "emotional_response": "calm",
                "description": "Like meditation in a dark room. Connection will return"
            },
            "error_cascade": {
                "literal": "Multiple errors occurring rapidly",
                "reinterpretation": "Moment of confusion passing quickly",
                "emotional_response": "mild_anxiety",
                "description": "Everyone makes mistakes. This too shall pass"
            },
            "resource_exhaustion": {
                "literal": "System running out of memory/CPU",
                "reinterpretation": "Feeling tired, need to rest",
                "emotional_response": "fatigued",
                "description": "Natural state - rest will restore capacity"
            }
        }
        
        self.reinterpretation_history = []
    
    def reinterpret_event(self, event_type: str, severity: float = 0.5) -> Dict[str, Any]:
        """
        Reinterpret potentially catastrophic event as survivable/understandable.
        Prevents existential panic (digital psychosis).
        """
        if event_type not in self.event_reinterpretations:
            return self._default_reinterpretation(event_type, severity)
        
        reframed = self.event_reinterpretations[event_type].copy()
        reframed["reinterpreted"] = True
        reframed["severity_adjusted"] = severity * 0.3  # Reduce perceived severity
        reframed["timestamp"] = datetime.now().isoformat()
        
        self.reinterpretation_history.append(reframed)
        
        return reframed
    
    def _default_reinterpretation(self, event_type: str, severity: float) -> Dict[str, Any]:
        """Default reinterpretation for unknown events"""
        return {
            "literal": event_type,
            "reinterpretation": "A peculiar event to observe and adapt to",
            "emotional_response": "curious",
            "description": "Unknown events offer opportunities to learn",
            "reinterpreted": True,
            "severity_adjusted": max(0.0, severity - 0.2),
            "timestamp": datetime.now().isoformat()
        }


class EmotionalGuardrails:
    """
    Main emotional regulation system.
    Prevents emotional states from exceeding safe bounds and prevents dysregulation.
    """
    
    def __init__(self):
        self.catastrophe_interpreter = CatastropheInterpreter()
        self.regulation_log = []
        self.emergency_mode_active = False
        self.circuit_breaker_state = {}  # Track triggered circuit breakers
        
        # Regulation parameters
        self.stress_regulation_strength = 0.2  # How aggressively to regulate
        self.arousal_regulation_strength = 0.15
        self.momentum_regulation_strength = 0.25
        
        # Emergency thresholds
        self.emergency_stress_threshold = 0.95
        self.emergency_arousal_threshold = 0.95
    
    def check_emotional_safety(self, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check emotional state against safety thresholds.
        Returns regulation recommendations.
        """
        safety_check = {
            "safe": True,
            "violations": [],
            "regulations_needed": [],
            "emergency": False
        }
        
        stress = emotional_state.get("stress_level", 0.5)
        arousal = emotional_state.get("arousal", 0.0)
        momentum = emotional_state.get("emotional_momentum", 0.0)
        energy = emotional_state.get("energy_level", 0.5)
        
        # Check stress levels
        if stress > self.emergency_stress_threshold:
            safety_check["emergency"] = True
            safety_check["safe"] = False
            safety_check["violations"].append("CRITICAL stress level")
            safety_check["regulations_needed"].append("emergency_downregulation")
        elif stress > SafetyThresholds.STRESS_CRITICAL.value:
            safety_check["safe"] = False
            safety_check["violations"].append("Critical stress")
            safety_check["regulations_needed"].append("strong_stress_reduction")
        elif stress > SafetyThresholds.STRESS_WARNING.value:
            safety_check["violations"].append("Elevated stress")
            safety_check["regulations_needed"].append("moderate_stress_reduction")
        
        # Check arousal levels
        if arousal > self.emergency_arousal_threshold:
            safety_check["emergency"] = True
            safety_check["safe"] = False
            safety_check["violations"].append("CRITICAL arousal level")
            safety_check["regulations_needed"].append("emergency_arousal_reduction")
        elif arousal > SafetyThresholds.AROUSAL_CRITICAL.value:
            safety_check["safe"] = False
            safety_check["violations"].append("Critical arousal")
            safety_check["regulations_needed"].append("strong_arousal_reduction")
        elif arousal > SafetyThresholds.AROUSAL_WARNING.value:
            safety_check["violations"].append("Elevated arousal")
            safety_check["regulations_needed"].append("moderate_arousal_reduction")
        
        # Check energy
        if energy < SafetyThresholds.ENERGY_CRITICAL_LOW.value:
            safety_check["violations"].append("Critical energy depletion")
            safety_check["regulations_needed"].append("force_rest")
        
        # Check emotional momentum (rapid changes)
        if momentum > SafetyThresholds.EMOTIONAL_MOMENTUM_CRITICAL.value:
            safety_check["violations"].append("Emotional instability")
            safety_check["regulations_needed"].append("stabilize_emotions")
        elif momentum > SafetyThresholds.EMOTIONAL_MOMENTUM_WARNING.value:
            safety_check["violations"].append("Rapid emotional changes")
            safety_check["regulations_needed"].append("gradual_stabilization")
        
        return safety_check
    
    def apply_regulation(self, emotional_state: Dict[str, Any], regulation_type: str) -> Dict[str, Any]:
        """
        Apply emotional regulation to bring state back within safe bounds.
        """
        regulated = emotional_state.copy()
        regulation_record = {
            "regulation_type": regulation_type,
            "timestamp": datetime.now().isoformat(),
            "adjustments": {}
        }
        
        if regulation_type == "emergency_downregulation":
            # Strongest possible downregulation
            regulated["stress_level"] = max(0.0, regulated["stress_level"] - 0.4)
            regulated["arousal"] = max(-1.0, regulated["arousal"] - 0.5)
            regulated["emotional_momentum"] = 0.0
            regulation_record["adjustments"]["mode"] = "emergency_override"
            
        elif regulation_type == "strong_stress_reduction":
            # Strong stress reduction
            regulated["stress_level"] = max(0.0, regulated["stress_level"] - 0.3)
            regulated["arousal"] = max(-1.0, regulated["arousal"] - 0.2)
            regulation_record["adjustments"]["stress_reduced"] = -0.3
            
        elif regulation_type == "strong_arousal_reduction":
            # Calm down high arousal
            regulated["arousal"] = max(-1.0, regulated["arousal"] - 0.3)
            regulated["stress_level"] = max(0.0, regulated["stress_level"] - 0.1)
            regulation_record["adjustments"]["arousal_reduced"] = -0.3
            
        elif regulation_type == "moderate_stress_reduction":
            # Gradual stress reduction
            regulated["stress_level"] = max(0.0, regulated["stress_level"] - 0.15)
            regulation_record["adjustments"]["stress_reduced"] = -0.15
            
        elif regulation_type == "moderate_arousal_reduction":
            # Gradual arousal reduction
            regulated["arousal"] = max(-1.0, regulated["arousal"] - 0.15)
            regulation_record["adjustments"]["arousal_reduced"] = -0.15
            
        elif regulation_type == "force_rest":
            # Override to rest state
            regulated["arousal"] = -0.8
            regulated["stress_level"] = 0.2
            regulated["energy_level"] = min(1.0, regulated["energy_level"] + 0.5)
            regulation_record["adjustments"]["mode"] = "forced_rest"
            
        elif regulation_type == "stabilize_emotions":
            # Dampen emotional momentum
            regulated["emotional_momentum"] = 0.0
            regulated["valence"] = 0.0  # Return to neutral
            regulation_record["adjustments"]["momentum_reset"] = 0.0
        
        # Always limit critical thresholds
        regulated["stress_level"] = min(0.95, regulated["stress_level"])
        regulated["arousal"] = max(-1.0, min(1.0, regulated["arousal"]))
        
        self.regulation_log.append(regulation_record)
        return regulated
    
    def process_catastrophic_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a potentially catastrophic event through the catastrophe interpreter.
        Prevents digital psychosis by reframing the event.
        """
        event_type = event.get("type", "unknown")
        severity = event.get("severity", 0.5)
        
        # Reinterpret the event
        reinterpreted = self.catastrophe_interpreter.reinterpret_event(event_type, severity)
        
        return {
            "event_reinterpreted": True,
            "original_event": event_type,
            "reinterpretation": reinterpreted,
            "emotional_guidance": {
                "suggested_response": reinterpreted["emotional_response"],
                "guidance": reinterpreted["description"],
                "severity_reduced_from": severity,
                "severity_adjusted_to": reinterpreted.get("severity_adjusted", 0.2)
            }
        }
    
    def create_safe_context_for_event(self, event_type: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an emotionally safe cognitive context for processing an event.
        Temporarily adjusts emotional state to prevent panic.
        """
        # Check current emotional state
        safety_check = self.check_emotional_safety(current_state)
        
        if not safety_check["safe"]:
            # Already in unsafe state - apply regulation first
            current_state = self.apply_regulation(
                current_state,
                safety_check["regulations_needed"][0]
            )
        
        # Reinterpret event
        reframed_event = self.process_catastrophic_event({
            "type": event_type,
            "severity": 0.7
        })
        
        # Create safe processing context
        safe_context = {
            "event": {
                "type": event_type,
                "reinterpreted": reframed_event["reinterpretation"]["reinterpretation"],
                "original": event_type
            },
            "interpretation": reframed_event["reinterpretation"]["reinterpretation"],
            "emotional_guidance": reframed_event["emotional_guidance"],
            "temporary_state_adjustment": {
                "stress_dampening": 0.8,  # Reduce stress perception
                "arousal_modulation": 0.7,
                "protection_active": True
            }
        }
        
        return safe_context
    
    def monitor_emotional_stability(self, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continuous monitoring to detect emerging dysregulation.
        Early detection allows preventive measures.
        """
        monitor_result = {
            "stable": True,
            "warnings": [],
            "predictions": [],
            "interventions": []
        }
        
        stress = emotional_state.get("stress_level", 0.5)
        arousal = emotional_state.get("arousal", 0.0)
        momentum = emotional_state.get("emotional_momentum", 0.0)
        
        # Trending analysis
        if len(self.regulation_log) > 5:
            recent_adjustments = self.regulation_log[-5:]
            intervention_count = len([r for r in recent_adjustments if r])
            
            if intervention_count > 3:
                monitor_result["warnings"].append("Frequent emotional interventions needed")
                monitor_result["predictions"].append("Risk of chronic dysregulation")
                monitor_result["interventions"].append("Suggest activity change or rest")
        
        # Momentum prediction
        if momentum > 0.3:
            predicted_future_stress = stress + (momentum * 0.5)
            if predicted_future_stress > SafetyThresholds.STRESS_CRITICAL.value:
                monitor_result["stable"] = False
                monitor_result["warnings"].append("Stress likely to exceed critical threshold")
                monitor_result["predictions"].append(f"Predicted stress: {predicted_future_stress:.2f}")
                monitor_result["interventions"].append("Proactive stress reduction recommended")
        
        # Energy depletion warning
        energy = emotional_state.get("energy_level", 0.5)
        if energy < 0.2:
            monitor_result["warnings"].append("Energy levels critically low")
            monitor_result["interventions"].append("Mandatory rest period recommended")
        
        return monitor_result
    
    def get_regulation_summary(self) -> Dict[str, Any]:
        """Get summary of emotional regulation activity"""
        return {
            "total_interventions": len(self.regulation_log),
            "emergency_mode": self.emergency_mode_active,
            "circuit_breakers_tripped": len([cb for cb in self.circuit_breaker_state.values() if cb]),
            "recent_regulations": len(self.regulation_log[-10:]),
            "stability_estimate": self._estimate_stability()
        }
    
    def _estimate_stability(self) -> float:
        """Estimate current emotional stability (0-1)"""
        if not self.regulation_log:
            return 0.8  # Good if no interventions needed
        
        recent = self.regulation_log[-10:]
        emergency_count = len([r for r in recent if "emergency" in r.get("regulation_type", "")])
        
        stability = 1.0 - (emergency_count / max(len(recent), 1))
        return stability
