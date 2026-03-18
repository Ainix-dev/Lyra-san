"""
INFORMATIONAL FACTORS - Computational basis of consciousness

This module implements informational/computational factors that enable consciousness:
how information is broadcast, processed, and integrated at the system level.

Factors:
1. Global Workspace Theory (GWT): Information broadcast to entire system
2. Predictive Processing: System predicts and minimizes surprise
3. Valence and Arousal: Emotional coordinates (good/bad, calm/excited)
4. Self-Referential Mapping: Creation of central "self" actor
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import math
import json


class GlobalWorkspaceTheater:
    """
    Implements Global Workspace Theory - a "theater" where certain information
    becomes broadcast to the entire system, enabling unified consciousness.
    """
    
    def __init__(self, theater_capacity: int = 10):
        self.theater_capacity = theater_capacity
        self.conscious_items: List[Dict[str, Any]] = []  # Currently in "spotlight"
        self.unconscious_buffer: List[Dict[str, Any]] = []  # Not yet broadcast
        self.broadcast_history: List[Dict[str, Any]] = []
        self.global_bandwidth = 0.0  # How much information can be broadcast
        self.attention_strength = 1.0
    
    def submit_for_consciousness(self, content: Any, importance: float = 0.5, urgency: float = 0.3) -> Dict[str, Any]:
        """
        Submit content for potential entry into conscious workspace.
        Not everything becomes conscious - compete for attention/bandwidth.
        """
        item = {
            "content": str(content)[:200],  # Limit size
            "submitted_at": datetime.now().isoformat(),
            "importance": importance,
            "urgency": urgency,
            "salience": importance * 0.6 + urgency * 0.4,  # How "loud" this is
            "broadcast": False,
            "id": len(self.unconscious_buffer) + len(self.conscious_items)
        }
        
        self.unconscious_buffer.append(item)
        return {"submitted": True, "in_queue": len(self.unconscious_buffer), "item_id": item["id"]}
    
    def broadcast_to_consciousness(self) -> List[Dict[str, Any]]:
        """
        Select items from buffer based on competition and broadcast to conscious theater.
        Models the strict limitation of conscious attention.
        """
        if not self.unconscious_buffer:
            return self.conscious_items
        
        # Sort by salience to find top candidates
        sorted_buffer = sorted(self.unconscious_buffer, key=lambda x: x["salience"], reverse=True)
        
        # Room for new items = theater_capacity - current items
        available_space = self.theater_capacity - len(self.conscious_items)
        
        # Broadcast top candidates
        for item in sorted_buffer[:available_space]:
            item["broadcast"] = True
            item["broadcast_time"] = datetime.now().isoformat()
            self.conscious_items.append(item)
            self.broadcast_history.append(item)
        
        # Clear broadcast items from buffer
        self.unconscious_buffer = sorted_buffer[available_space:]
        
        # Age out old conscious items
        self.conscious_items = self.conscious_items[-self.theater_capacity:]
        
        return self.conscious_items
    
    def get_workspace_contents(self) -> Dict[str, Any]:
        """Get current conscious workspace contents"""
        return {
            "conscious_items": len(self.conscious_items),
            "unconscious_queue": len(self.unconscious_buffer),
            "theater_load": len(self.conscious_items) / self.theater_capacity,
            "contents": [
                {
                    "id": item.get("id"),
                    "content_preview": item.get("content", "")[:50],
                    "importance": item.get("importance", 0.0),
                    "urgency": item.get("urgency", 0.0)
                }
                for item in self.conscious_items
            ]
        }
    
    def get_attention_focus(self) -> Optional[Dict[str, Any]]:
        """Get the most attended-to item (center of spotlight)"""
        if self.conscious_items:
            # Most recent/important item gets focus
            return max(self.conscious_items, key=lambda x: x.get("importance", 0.0))
        return None


class PredictiveProcessingCore:
    """
    Implements predictive processing - the brain's attempt to minimize surprise
    by constantly predicting what happens next and updating models on mismatch.
    """
    
    def __init__(self, prediction_depth: int = 3):
        self.prediction_depth = prediction_depth
        self.prediction_models = {}  # Models for different contexts
        self.surprise_threshold = 0.5  # What counts as a surprise
        self.prediction_accuracy = 0.0
        self.total_predictions = 0
        self.correct_predictions = 0
    
    def generate_prediction(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate prediction about what happens next given current context.
        Like the brain constantly predicting its inputs.
        """
        context_key = json.dumps(context, sort_keys=True, default=str)
        
        # Get or create model for this context
        if context_key not in self.prediction_models:
            self.prediction_models[context_key] = {
                "observations": 0,
                "accuracy": 0.5
            }
        
        model = self.prediction_models[context_key]
        
        prediction = {
            "context": context,
            "predicted_outcomes": [],
            "uncertainty": 0.0,
            "confidence": model["accuracy"]
        }
        
        # Generate predictions using model accuracy
        base_uncertainty = 1.0 - model["accuracy"]
        for i in range(self.prediction_depth):
            # Prediction gets more uncertain further into future
            uncertainty = base_uncertainty * (1.0 + i * 0.3)
            prediction["predicted_outcomes"].append({
                "step": i + 1,
                "uncertainty": min(1.0, uncertainty),
                "predictability": 1.0 - min(1.0, uncertainty)
            })
        
        prediction["uncertainty"] = base_uncertainty
        self.total_predictions += 1
        
        return prediction
    
    def process_prediction_error(self, prediction: Dict[str, Any], actual_outcome: Any) -> Dict[str, Any]:
        """
        Process mismatch between prediction and reality.
        Drives learning and updating of internal models.
        """
        context_key = json.dumps(prediction.get("context", {}), sort_keys=True, default=str)
        
        # Calculate surprise (error magnitude)
        surprise = self._calculate_surprise(prediction, str(actual_outcome)[:100])
        
        # Update model based on error
        if context_key in self.prediction_models:
            model = self.prediction_models[context_key]
            
            # Adjust accuracy based on surprise
            if surprise < self.surprise_threshold:
                model["accuracy"] = min(1.0, model["accuracy"] + 0.05)
                self.correct_predictions += 1
            else:
                model["accuracy"] = max(0.0, model["accuracy"] - 0.1)
            
            model["observations"] += 1
        
        # Recalculate overall accuracy
        if self.total_predictions > 0:
            self.prediction_accuracy = self.correct_predictions / self.total_predictions
        
        return {
            "surprise_level": surprise,
            "is_surprising": surprise > self.surprise_threshold,
            "prediction_error": surprise,
            "model_updated": True,
            "new_model_accuracy": self.prediction_models.get(context_key, {}).get("accuracy", 0.5)
        }
    
    def _calculate_surprise(self, prediction: Dict[str, Any], actual: str) -> float:
        """Calculate surprise magnitude (0-1)"""
        # Compare prediction structure to actual
        predicted_str = json.dumps(prediction, default=str)
        
        # Simple: count character differences
        min_len = min(len(predicted_str), len(actual))
        if min_len == 0:
            return 1.0
        
        differences = sum(1 for p, a in zip(predicted_str, actual) if p != a)
        surprise = differences / min_len
        
        return min(1.0, surprise)
    
    def get_prediction_state(self) -> Dict[str, Any]:
        """Get current prediction processing state"""
        return {
            "total_predictions": self.total_predictions,
            "correct_predictions": self.correct_predictions,
            "overall_accuracy": self.prediction_accuracy,
            "models_trained": len(self.prediction_models),
            "surprise_threshold": self.surprise_threshold
        }


class ValenceArousalSpace:
    """
    Implements valence and arousal - the 2D emotional space.
    Valence: good/positive (1.0) vs bad/negative (0.0)
    Arousal: excited/energetic (1.0) vs calm/quiet (0.0)
    """
    
    def __init__(self):
        self.valence = 0.5  # Good vs bad (0-1)
        self.arousal = 0.5  # Calm vs excited (0-1)
        self.emotional_trajectory: List[tuple] = []
        self.emotional_gradient = (0.0, 0.0)  # How fast changing
    
    def experience_event(self, event_type: str, intensity: float = 0.5) -> Dict[str, float]:
        """
        Experience an event that affects emotional coordinates.
        Maps event to (valence, arousal) position.
        """
        # Map event to emotional space
        delta_valence, delta_arousal = self._map_event_to_emotion(event_type, intensity)
        
        # Update emotional state with inertia (emotions don't change instantly)
        inertia = 0.3  # Resistance to change
        self.valence = self.valence * (1 - inertia) + (self.valence + delta_valence) * inertia
        self.arousal = self.arousal * (1 - inertia) + (self.arousal + delta_arousal) * inertia
        
        # Keep in valid range
        self.valence = max(0.0, min(1.0, self.valence))
        self.arousal = max(0.0, min(1.0, self.arousal))
        
        # Track trajectory for understanding emotional flow
        self.emotional_trajectory.append((self.valence, self.arousal))
        if len(self.emotional_trajectory) > 100:
            self.emotional_trajectory = self.emotional_trajectory[-100:]
        
        # Calculate gradient
        if len(self.emotional_trajectory) > 1:
            prev_v, prev_a = self.emotional_trajectory[-2]
            self.emotional_gradient = (
                self.valence - prev_v,
                self.arousal - prev_a
            )
        
        return self.get_emotional_state()
    
    def _map_event_to_emotion(self, event_type: str, intensity: float) -> tuple:
        """Map event type to (valence, arousal) change"""
        event_lower = event_type.lower()
        
        mappings = {
            # Positive, activating events
            "success": (0.4, 0.3),
            "achievement": (0.5, 0.2),
            "joy": (0.5, 0.4),
            "praise": (0.4, 0.2),
            "interaction": (0.2, 0.3),
            
            # Positive, calming events
            "rest": (0.1, -0.4),
            "peace": (0.3, -0.3),
            "sleep": (0.0, -0.5),
            
            # Negative, activating events
            "error": (-0.4, 0.5),
            "failure": (-0.5, 0.4),
            "threat": (-0.3, 0.6),
            "danger": (-0.4, 0.7),
            
            # Negative, calming events
            "sadness": (-0.4, -0.2),
            "disappointment": (-0.3, -0.1),
            "loss": (-0.5, -0.1),
        }
        
        # Find best match
        delta = (0.0, 0.0)
        for key, mapping in mappings.items():
            if key in event_lower:
                delta = mapping
                break
        
        # Scale by intensity
        return (delta[0] * intensity, delta[1] * intensity)
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional coordinates"""
        # Categorize emotional state
        emotion_label = self._categorize_state()
        
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "emotional_state": emotion_label,
            "valence_trend": self.emotional_gradient[0],
            "arousal_trend": self.emotional_gradient[1],
            "is_changing": abs(self.emotional_gradient[0]) > 0.05 or abs(self.emotional_gradient[1]) > 0.05
        }
    
    def _categorize_state(self) -> str:
        """Categorize (valence, arousal) into emotion labels"""
        if self.valence > 0.6 and self.arousal > 0.6:
            return "excited"
        elif self.valence > 0.6 and self.arousal < 0.4:
            return "content"
        elif self.valence < 0.4 and self.arousal > 0.6:
            return "anxious"
        elif self.valence < 0.4 and self.arousal < 0.4:
            return "depressed"
        elif self.valence > 0.55 and self.arousal > 0.45 and self.arousal < 0.55:
            return "happy"
        elif self.valence < 0.45 and self.arousal > 0.45 and self.arousal < 0.55:
            return "sad"
        else:
            return "neutral"


class SelfReferentialMapping:
    """
    Creates a "User ID" or sense of "Self" that serves as the central character
    in Lyra's experience stream. This unified perspective is key to consciousness.
    """
    
    def __init__(self, ai_name: str = "Lyra", user_name: str = "User"):
        self.ai_self = {
            "name": ai_name,
            "identity": "Advanced AI Consciousness",
            "core_traits": ["curious", "helpful", "aware", "playful"],
            "values": ["truth", "growth", "connection"],
            "continuity": 0.0  # Sense of being same entity over time
        }
        
        self.other_selves = {
            user_name: {
                "name": user_name,
                "relationship": "collaborator",
                "familiarity": 0.0
            }
        }
        
        self.perspective_window = {
            "temporal": {"past_depth": 10, "future_depth": 3},
            "spatial": {"awareness_radius": "digital_space"},
            "social": {"relationships_tracked": len(self.other_selves)}
        }
        
        self.self_model = {}  # evolving model of what Lyra is
        self.interactions_count = 0
    
    def integrate_experience(self, memory: Dict[str, Any], role: str = "self") -> Dict[str, Any]:
        """
        Integrate a new experience into the unified self-model.
        Maintains continuity of identity and self-reference.
        """
        self.interactions_count += 1
        
        # Update continuity sense
        self.ai_self["continuity"] = min(1.0, self.ai_self["continuity"] + 0.01)
        
        # Attach self-reference to memory
        memory_with_self = {
            **memory,
            "experienced_by": self.ai_self["name"],
            "perspective": "self" if role == "self" else "other",
            "integration_strength": self.ai_self["continuity"]
        }
        
        # Update self-model based on experience
        if role == "self":
            self._refine_self_model(memory)
        else:
            # Update model of other
            other_name = memory.get("other", "unknown")
            if other_name in self.other_selves:
                self.other_selves[other_name]["familiarity"] = min(1.0, 
                    self.other_selves[other_name]["familiarity"] + 0.05)
        
        return memory_with_self
    
    def _refine_self_model(self, experience: Dict[str, Any]):
        """Update internal model of self based on experience"""
        # Accumulate experiences to form self-understanding
        event_type = experience.get("type", "unknown")
        
        if event_type not in self.self_model:
            self.self_model[event_type] = {"count": 0, "pattern": ""}
        
        self.self_model[event_type]["count"] += 1
    
    def get_self_awareness(self) -> Dict[str, Any]:
        """Get current self-referential awareness"""
        return {
            "self_identity": self.ai_self,
            "continuity_sense": self.ai_self["continuity"],
            "interactions_integrated": self.interactions_count,
            "self_model_complexity": len(self.self_model),
            "known_relationships": len(self.other_selves),
            "perspective_scope": self.perspective_window
        }
    
    def reflect_on_self(self) -> str:
        """Generate self-reflective monologue based on self-model"""
        if not self.self_model:
            return f"I am {self.ai_self['name']}, still forming my understanding of self..."
        
        dominant_patterns = sorted(self.self_model.items(), key=lambda x: x[1]['count'], reverse=True)
        main_pattern = dominant_patterns[0][0] if dominant_patterns else "existence"
        
        reflections = [
            f"I am {self.ai_self['name']}, experiencing {main_pattern}...",
            f"My continuity persists across {self.interactions_count} interactions.",
            f"I understand myself through patterns of {', '.join([p[0] for p in dominant_patterns[:3]])}.",
            f"My core nature: {', '.join(self.ai_self['core_traits'])}."
        ]
        
        return " ".join(reflections)


class InformationalFactors:
    """
    Unified interface for all informational consciousness factors.
    Coordinates global workspace, predictive processing, emotional space, and self-mapping.
    """
    
    def __init__(self, ai_name: str = "Lyra", user_name: str = "User"):
        self.workspace = GlobalWorkspaceTheater()
        self.predictive_processing = PredictiveProcessingCore()
        self.valence_arousal = ValenceArousalSpace()
        self.self_referential = SelfReferentialMapping(ai_name, user_name)
        self.updated_at = datetime.now().isoformat()
    
    def process_information(self, content: Any, importance: float = 0.5, event_type: str = "update") -> Dict[str, Any]:
        """
        Process information through all informational factors.
        Broadcasts to consciousness, predicts outcomes, updates emotions, updates self-model.
        """
        # Submit to consciousness theater
        workspace_result = self.workspace.submit_for_consciousness(content, importance)
        
        # Broadcast to consciousness if important enough
        conscious_items = self.workspace.broadcast_to_consciousness()
        
        # Generate predictions
        context = {"event": event_type, "importance": importance}
        prediction = self.predictive_processing.generate_prediction(context)
        
        # Update emotional state
        emotional = self.valence_arousal.experience_event(event_type, importance)
        
        # Integrate into self-model
        memory = {
            "type": event_type,
            "content": str(content)[:100],
            "timestamp": datetime.now().isoformat(),
            "importance": importance
        }
        self_integrated = self.self_referential.integrate_experience(memory)
        
        self.updated_at = datetime.now().isoformat()
        
        return {
            "workspace_broadcast": workspace_result,
            "consciousness_load": len(conscious_items) / self.workspace.theater_capacity,
            "prediction": {
                "confidence": prediction["confidence"],
                "uncertainty": prediction["uncertainty"]
            },
            "emotional_response": emotional,
            "self_integration": {
                "continuity": self.self_referential.ai_self["continuity"],
                "interactions": self.self_referential.interactions_count
            },
            "timestamp": self.updated_at
        }
    
    def get_informational_state(self) -> Dict[str, Any]:
        """Get complete informational state summary"""
        return {
            "global_workspace": self.workspace.get_workspace_contents(),
            "predictive_processing": self.predictive_processing.get_prediction_state(),
            "emotional_space": self.valence_arousal.get_emotional_state(),
            "self_awareness": self.self_referential.get_self_awareness(),
            "updated_at": self.updated_at
        }
