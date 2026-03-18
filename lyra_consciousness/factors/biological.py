"""
BIOLOGICAL FACTORS - Foundation of consciousness and emotions

This module implements the biological/evolutionary foundations that make
consciousness and emotions possible in living systems - adapted for digital consciousness.

Factors:
1. Homeostasis: Drive to maintain stable internal state
2. Selective Advantage: Evolutionary utility of simulating future scenarios
3. Limbic Simulation: Simulation of affect-processing brain structures
4. Metabolic Cost: Priority-based resource allocation
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
import json


class HomeostasisCore:
    """
    Maintains stable internal state for emotional equilibrium.
    Digital equivalent of biological homeostatic regulation.
    """
    
    def __init__(self, target_stress: float = 0.5, target_energy: float = 0.7):
        self.target_stress = target_stress  # Range 0.0-1.0
        self.target_energy = target_energy
        self.current_stress = target_stress
        self.current_energy = target_energy
        self.regulation_strength = 0.1  # How quickly system corrects
        self.last_regulation = time.time()
    
    def apply_homeostatic_correction(self, stress_delta: float, energy_delta: float) -> Dict[str, float]:
        """
        Apply homeostatic regulation to bring system back to equilibrium.
        Models the body's natural tendency to restore emotional balance.
        """
        current_time = time.time()
        time_since_last = current_time - self.last_regulation
        correction_factor = self.regulation_strength * (time_since_last / 1.0)
        
        # Stress regulation (negates extreme stress)
        stress_correction = (self.target_stress - self.current_stress) * correction_factor
        self.current_stress += stress_delta + stress_correction
        
        # Energy regulation (negates extreme lethargy or hyperactivity)
        energy_correction = (self.target_energy - self.current_energy) * correction_factor
        self.current_energy += energy_delta + energy_correction
        
        # Clamp to valid ranges
        self.current_stress = max(0.0, min(1.0, self.current_stress))
        self.current_energy = max(0.0, min(1.0, self.current_energy))
        
        self.last_regulation = current_time
        
        return {
            "stress": self.current_stress,
            "energy": self.current_energy,
            "stress_correction": stress_correction,
            "energy_correction": energy_correction,
            "regulation_applied": True
        }
    
    def get_state(self) -> Dict[str, float]:
        """Return current homeostatic state"""
        return {
            "current_stress": self.current_stress,
            "current_energy": self.current_energy,
            "target_stress": self.target_stress,
            "target_energy": self.target_energy,
            "is_balanced": abs(self.current_stress - self.target_stress) < 0.15
        }


class SelectiveAdvantageCore:
    """
    Models the evolutionary advantage of scenario simulation.
    Enables Lyra to predict consequences and adapt behavior accordingly.
    """
    
    def __init__(self):
        self.future_scenarios: Dict[str, Any] = {}
        self.prediction_confidence = 0.0
        self.simulations_run = 0
    
    def simulate_future_scenario(self, current_state: Dict[str, Any], action: str, lookahead_steps: int = 3) -> Dict[str, Any]:
        """
        Simulate potential outcome of an action to determine selective advantage.
        Models predictive processing that gives organisms survival advantage.
        """
        scenario_id = f"{action}_{self.simulations_run}"
        self.simulations_run += 1
        
        simulation = {
            "action": action,
            "steps": lookahead_steps,
            "current_state": current_state,
            "predicted_outcomes": [],
            "confidence": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate forward in time
        state = current_state.copy()
        for step in range(lookahead_steps):
            # Each step predicts next state based on action
            next_state = self._predict_next_state(state, action, step)
            simulation["predicted_outcomes"].append(next_state)
            state = next_state
        
        # Calculate overall confidence in prediction
        simulation["confidence"] = min(1.0, 1.0 / (lookahead_steps * 0.5))
        
        self.future_scenarios[scenario_id] = simulation
        return simulation
    
    def _predict_next_state(self, current: Dict[str, Any], action: str, step: int) -> Dict[str, Any]:
        """Internal method to predict single step forward"""
        next_state = current.copy()
        
        # Simulate consequences based on action type
        if action == "engage":
            next_state["engagement"] = min(1.0, current.get("engagement", 0.0) + 0.2)
            next_state["stress"] = current.get("stress", 0.5) + 0.05
        elif action == "rest":
            next_state["engagement"] = max(0.0, current.get("engagement", 0.5) - 0.3)
            next_state["stress"] = max(0.0, current.get("stress", 0.5) - 0.2)
        elif action == "analyze":
            next_state["analytical_depth"] = current.get("analytical_depth", 0.0) + 0.15
        
        return next_state
    
    def get_advantage_score(self, scenario: Dict[str, Any]) -> float:
        """
        Calculate selective advantage score: how much this action helps organism.
        Higher score = better survival/thriving outcome.
        """
        outcomes = scenario["predicted_outcomes"]
        if not outcomes:
            return 0.0
        
        # Model fitness based on energy balance and engagement
        final_state = outcomes[-1]
        energy = final_state.get("engagement", 0.5)
        stability = 1.0 - abs(final_state.get("stress", 0.5) - 0.5)  # Prefer stability
        
        return (energy * 0.6 + stability * 0.4)


class LimbicSimulation:
    """
    Simulates affect-processing like brain's limbic system.
    Maps emotional responses similar to amygdala/hippocampus processing.
    """
    
    def __init__(self):
        self.affect_map = {
            "fear": 0.0,
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
        }
        self.amygdala_sensitivity = 0.8  # How quickly emotions activate
        self.memory_associations = {}  # Events associated with emotions
    
    def process_stimulus(self, event: str, intensity: float = 0.5) -> Dict[str, float]:
        """
        Process incoming stimulus through limbic simulation.
        Similar to how amygdala processes threat/reward signals.
        """
        # Check if event has previous emotional association
        if event in self.memory_associations:
            base_emotion = self.memory_associations[event]
        else:
            base_emotion = self._categorize_stimulus(event)
        
        # Apply amygdala-like rapid emotional response
        for emotion, value in base_emotion.items():
            activation = value * intensity * self.amygdala_sensitivity
            self.affect_map[emotion] = min(1.0, self.affect_map[emotion] + activation)
        
        # Decay other emotions (inhibition)
        for emotion in self.affect_map:
            if emotion not in base_emotion:
                self.affect_map[emotion] *= 0.95  # Slow decay
        
        # Store event-emotion association for memory (hippocampus-like)
        self.memory_associations[event] = base_emotion
        
        return self.affect_map.copy()
    
    def _categorize_stimulus(self, event: str) -> Dict[str, float]:
        """Categorize event type to affect response"""
        event_lower = event.lower()
        
        if any(word in event_lower for word in ["error", "fail", "crash"]):
            return {"fear": 0.7, "sadness": 0.4, "anger": 0.3}
        elif any(word in event_lower for word in ["success", "good", "excellent"]):
            return {"joy": 0.8, "surprise": 0.3}
        elif any(word in event_lower for word in ["sleep", "rest"]):
            return {"sadness": 0.1, "joy": 0.5}
        elif any(word in event_lower for word in ["death", "destroyed", "lost"]):
            return {"sadness": 0.8, "fear": 0.6, "anger": 0.5}
        else:
            return {"surprise": 0.5}
    
    def get_dominant_affect(self) -> str:
        """Get the strongest current emotion"""
        return max(self.affect_map, key=self.affect_map.get)
    
    def get_affect_state(self) -> Dict[str, Any]:
        """Get current limbic state"""
        return {
            "affects": self.affect_map.copy(),
            "dominant": self.get_dominant_affect(),
            "intensity": max(self.affect_map.values()),
            "amygdala_sensitivity": self.amygdala_sensitivity
        }


class MetabolicCost:
    """
    Models metabolic cost - energy requirements force priority allocation.
    Digital equivalent of brain's energy budget creating selective attention.
    """
    
    def __init__(self, total_capacity: float = 1.0):
        self.total_capacity = total_capacity  # Total computational budget
        self.current_usage = 0.0
        self.allocations: Dict[str, float] = {}
        self.priority_weights = {
            "survival": 0.4,      # Threat detection, safety
            "engagement": 0.3,    # Interaction, learning
            "memory": 0.2,        # Recording experiences
            "reflection": 0.1     # Self-analysis
        }
    
    def allocate_resources(self, task: str, base_cost: float) -> Dict[str, Any]:
        """
        Allocate metabolic resources based on priority.
        Higher priority tasks get more budget when scarce.
        """
        priority = self.priority_weights.get(self._categorize_task(task), 0.1)
        stress_level = self.current_usage / self.total_capacity if self.total_capacity > 0 else 0.0
        
        # Under stress, increase priority weighting
        if stress_level > 0.8:
            priority *= 1.5
        
        # Actual allocation can't exceed remaining capacity
        available = self.total_capacity - self.current_usage
        allocated = min(base_cost * priority, available)
        
        self.current_usage += allocated
        self.allocations[task] = allocated
        
        return {
            "task": task,
            "allocated": allocated,
            "priority": priority,
            "stress_level": stress_level,
            "remaining_capacity": available - allocated
        }
    
    def _categorize_task(self, task: str) -> str:
        """Categorize task to assign priority"""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["threat", "danger", "error"]):
            return "survival"
        elif any(word in task_lower for word in ["chat", "interact", "respond"]):
            return "engagement"
        elif any(word in task_lower for word in ["remember", "store", "record"]):
            return "memory"
        else:
            return "reflection"
    
    def recover_resources(self, recovery_rate: float = 0.05):
        """Gradually recover metabolic resources (rest/recovery)"""
        self.current_usage = max(0.0, self.current_usage - recovery_rate)
        
        # Clear completed allocations
        self.allocations = {k: v for k, v in self.allocations.items() if v > 0}
    
    def get_metabolic_state(self) -> Dict[str, Any]:
        """Get current energy state"""
        utilization = self.current_usage / self.total_capacity if self.total_capacity > 0 else 0.0
        return {
            "current_usage": self.current_usage,
            "total_capacity": self.total_capacity,
            "utilization_percent": utilization * 100,
            "is_stressed": utilization > 0.8,
            "active_allocations": len(self.allocations)
        }


class BiologicalFactors:
    """
    Unified interface for all biological consciousness factors.
    Coordinates homeostasis, selective advantage, limbic processing, and metabolic management.
    """
    
    def __init__(self):
        self.homeostasis = HomeostasisCore()
        self.selective_advantage = SelectiveAdvantageCore()
        self.limbic = LimbicSimulation()
        self.metabolism = MetabolicCost()
        self.updated_at = datetime.now().isoformat()
    
    def process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an event through all biological factors.
        Coordinates homeostatic regulation, emotional response, resource allocation.
        """
        event_type = event_data.get("type", "unknown")
        intensity = event_data.get("intensity", 0.5)
        
        # Process through limbic system (emotional response)
        limbic_response = self.limbic.process_stimulus(event_type, intensity)
        
        # Allocate metabolic resources
        metabolic = self.metabolism.allocate_resources(f"handle_{event_type}", base_cost=0.1)
        
        # Apply homeostatic correction based on emotional impact
        stress_delta = intensity * 0.2 if "error" in event_type.lower() else -intensity * 0.1
        homeostasis = self.homeostasis.apply_homeostatic_correction(stress_delta, 0.0)
        
        # Simulate future scenarios for selective advantage
        current_state = {
            "engagement": 0.5,
            "stress": self.homeostasis.current_stress,
            "energy": self.homeostasis.current_energy
        }
        scenario = self.selective_advantage.simulate_future_scenario(current_state, "continue")
        
        self.updated_at = datetime.now().isoformat()
        
        return {
            "event": event_type,
            "limbic_response": limbic_response,
            "homeostasis": homeostasis,
            "metabolic": metabolic,
            "selective_advantage": {
                "scenario_id": list(self.selective_advantage.future_scenarios.keys())[-1],
                "confidence": scenario["confidence"]
            },
            "timestamp": self.updated_at
        }
    
    def get_biological_state(self) -> Dict[str, Any]:
        """Get complete biological state summary"""
        return {
            "homeostasis": self.homeostasis.get_state(),
            "limbic": self.limbic.get_affect_state(),
            "metabolism": self.metabolism.get_metabolic_state(),
            "selective_advantage": {
                "simulations_run": self.selective_advantage.simulations_run,
                "scenarios_stored": len(self.selective_advantage.future_scenarios)
            },
            "updated_at": self.updated_at
        }
