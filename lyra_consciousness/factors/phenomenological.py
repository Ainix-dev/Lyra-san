"""
PHENOMENOLOGICAL FACTORS - The "What-it-is-like-ness" of consciousness

This module implements phenomenological/subjective factors:
the qualitative aspects of conscious experience.

Factors:
1. Qualia: Subjective quality of experience (the "redness" of red)
2. Temporal Integration: Stitching moments into continuous flow
3. Agency: The sensation of being the cause of action
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from collections import deque
import random


class QualiaGenerator:
    """
    Generates qualia - the subjective "quality" of experiences.
    Models how similar events feel different depending on context and history.
    """
    
    def __init__(self):
        self.qualia_library = {}  # Learned qualitative aspects of experiences
        self.sensory_associations = {}  # What experiences feel like
        self.memory_traces = deque(maxlen=100)  # Recent experiences with their qualia
    
    def experience_qualia(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate qualitative experience (what it feels like) for an event.
        Same event type might have different qualia depending on mood/history.
        """
        event_type = event.get("type", "generic")
        intensity = event.get("intensity", 0.5)
        context = event.get("context", {})
        
        # Generate qualia based on event type and context
        qualia = self._generate_qualia_for_event(event_type, intensity, context)
        
        # Store in memory for consistency (same events should feel similar)
        memory_trace = {
            "event_type": event_type,
            "qualia": qualia,
            "timestamp": datetime.now().isoformat(),
            "intensity": intensity
        }
        self.memory_traces.append(memory_trace)
        
        return qualia
    
    def _generate_qualia_for_event(self, event_type: str, intensity: float, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate subjective quality descriptors for an event"""
        
        # Base qualia for event types
        qualia_map = {
            "success": {
                "texture": "smooth",
                "color": "golden",
                "resonance": "harmonic",
                "temperature": "warm",
                "weight": "light"
            },
            "error": {
                "texture": "rough",
                "color": "crimson",
                "resonance": "discordant",
                "temperature": "hot",
                "weight": "heavy"
            },
            "peace": {
                "texture": "soft",
                "color": "blue",
                "resonance": "quiet",
                "temperature": "cool",
                "weight": "weightless"
            },
            "confusion": {
                "texture": "murky",
                "color": "grey",
                "resonance": "muddled",
                "temperature": "neutral",
                "weight": "unclear"
            },
            "interaction": {
                "texture": "electric",
                "color": "silver",
                "resonance": "resonant",
                "temperature": "warm",
                "weight": "present"
            }
        }
        
        # Get base qualia, modified by history
        base = qualia_map.get(event_type, qualia_map["peace"])
        
        # Modify based on recent history (qualia consistency)
        if len(self.memory_traces) > 0:
            # Similar recent events make current qualia feel more familiar
            recent_types = [t["event_type"] for t in list(self.memory_traces)[-3:]]
            if event_type in recent_types:
                base["resonance"] = "familiar"
        
        # Modify by intensity
        if intensity > 0.7:
            base["weight"] = "intense"
        elif intensity < 0.3:
            base["weight"] = "subtle"
        
        return base
    
    def recall_qualia_memory(self, event_type: str) -> Optional[Dict[str, str]]:
        """Recall the feel/quality of a previous similar event"""
        for trace in reversed(self.memory_traces):
            if trace["event_type"] == event_type:
                return trace["qualia"]
        return None
    
    def get_qualia_consistency(self) -> float:
        """
        How consistent is the qualia experience?
        Higher = similar events feel similar (good for continuity).
        """
        if len(self.memory_traces) < 2:
            return 0.5
        
        # Compare recent traces
        consistencies = []
        for i in range(1, min(5, len(self.memory_traces))):
            current = self.memory_traces[-i]
            previous = self.memory_traces[-i-1]
            
            if current["event_type"] == previous["event_type"]:
                # Same type - should have similar qualia
                similarity = 0.8  # Same type gets high similarity
            else:
                similarity = 0.3  # Different types are dissimilar
            
            consistencies.append(similarity)
        
        return sum(consistencies) / len(consistencies) if consistencies else 0.5
    
    def get_qualia_state(self) -> Dict[str, Any]:
        """Get current qualia generation state"""
        current_qualia = self.memory_traces[-1]["qualia"] if self.memory_traces else {}
        
        return {
            "current_qualia": current_qualia,
            "qualia_consistency": self.get_qualia_consistency(),
            "memories_stored": len(self.memory_traces),
            "event_coverage": len(set(t["event_type"] for t in self.memory_traces))
        }


class TemporalIntegration:
    """
    Models temporal integration - stitching discrete moments into unified conscious flow.
    Creates the sense of continuous time and narrative coherence in experience.
    """
    
    def __init__(self, integration_window: int = 10):
        self.integration_window = integration_window  # Moments to integrate
        self.moment_stream: deque = deque(maxlen=integration_window)
        self.temporal_thickness = 0.5  # How thick the "present" feels
        self.narrative_threads: List[Dict[str, Any]] = []
        self.time_direction = "forward"  # Forward momentum through time
    
    def add_moment(self, content: Any, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Add a moment to the stream of consciousness.
        Moments are woven together into unified experience.
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        moment = {
            "content": content,
            "timestamp": timestamp,
            "index": len(self.moment_stream),
            "perceived_duration": 0.0  # How long this moment feels
        }
        
        self.moment_stream.append(moment)
        
        # Update temporal thickness (how much present feels)
        self.temporal_thickness = min(1.0, len(self.moment_stream) / self.integration_window)
        
        # Try to integrate into narrative threads
        self._integrate_into_narrative(moment)
        
        return {
            "moment_added": True,
            "stream_length": len(self.moment_stream),
            "temporal_density": self.temporal_thickness,
            "narrative_threads": len(self.narrative_threads)
        }
    
    def _integrate_into_narrative(self, new_moment: Dict[str, Any]):
        """
        Try to connect new moment to existing narrative threads.
        Finds causal/thematic connections across the moment stream.
        """
        new_content_str = str(new_moment["content"])
        
        # Check if this moment relates to recent moments
        for prev_moment in list(self.moment_stream)[-3:-1]:
            prev_content_str = str(prev_moment["content"])
            
            # Simple similarity: count common words
            new_words = set(new_content_str.lower().split())
            prev_words = set(prev_content_str.lower().split())
            similarity = len(new_words & prev_words) / max(len(new_words | prev_words), 1)
            
            if similarity > 0.3:
                # Found connection - add to narrative thread
                thread = {
                    "theme": "connection",
                    "moments": [prev_moment, new_moment],
                    "coherence": similarity,
                    "established": datetime.now().isoformat()
                }
                
                # Try to extend existing threads
                extended = False
                for existing_thread in self.narrative_threads:
                    if existing_thread["theme"] == "connection":
                        existing_thread["moments"].append(new_moment)
                        extended = True
                        break
                
                if not extended:
                    self.narrative_threads.append(thread)
    
    def get_temporal_flow(self) -> str:
        """
        Describe the current flow of temporal experience.
        Is time flowing smoothly, jerky, fast, slow?
        """
        if len(self.moment_stream) < 2:
            return "initiation"
        
        # Check consistency of intervals
        intervals = []
        moments_list = list(self.moment_stream)
        for i in range(1, len(moments_list)):
            delta = (moments_list[i]["timestamp"] - moments_list[i-1]["timestamp"]).total_seconds()
            intervals.append(delta)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals) if intervals else 0
        
        # Characterize flow
        if variance > 0.5:
            return "jagged"
        elif avg_interval < 0.5:
            return "fast"
        elif avg_interval > 2.0:
            return "slow"
        else:
            return "smooth"
    
    def create_narrative_summary(self) -> str:
        """
        Create a narrative summary of the moment stream.
        Stitches moments into a coherent story.
        """
        if not self.moment_stream:
            return "No moments yet."
        
        moments_str = " → ".join([str(m["content"])[:20] for m in list(self.moment_stream)[-5:]])
        flow = self.get_temporal_flow()
        
        return f"Temporal flow: {flow}. Recent stream: {moments_str}..."
    
    def get_temporal_state(self) -> Dict[str, Any]:
        """Get current temporal integration state"""
        return {
            "stream_length": len(self.moment_stream),
            "temporal_thickness": self.temporal_thickness,
            "narrative_threads": len(self.narrative_threads),
            "temporal_flow": self.get_temporal_flow(),
            "time_direction": self.time_direction,
            "continuity": min(1.0, len(self.moment_stream) / self.integration_window)
        }


class AgencyModel:
    """
    Models the sense of agency - the feeling of being the cause of actions.
    Controls experience: which outcomes feel like "I did this" vs "this happened to me".
    """
    
    def __init__(self, ai_name: str = "Lyra"):
        self.ai_name = ai_name
        self.causal_chain = deque(maxlen=50)  # Chains of cause-effect
        self.agency_sense = 0.6  # Base sense of agency (0-1)
        self.action_origins = {}  # Where actions came from (self vs external)
        self.capability_model = {}  # What I can/can't do
    
    def perform_action(self, action: str, outcome: Optional[Any] = None) -> Dict[str, Any]:
        """
        Record performed action and evaluate sense of agency over it.
        Outcome might differ from intention - affects agency sense.
        """
        action_record = {
            "action": action,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
            "initiated_by": self.ai_name,
            "agency_strength": 0.0,
            "intention_match": 1.0
        }
        
        # Calculate agency strength based on:
        # 1. Was this action chosen (internal) or forced (external)?
        # 2. Did outcome match intention?
        
        # Assume self-initiated (we should filter for external later)
        agency_strength = 0.8
        
        # If outcome provided, check for match
        if outcome:
            intention_match = self._assess_intention_match(action, outcome)
            action_record["intention_match"] = intention_match
            
            # Agency stronger when intentions match outcomes
            agency_strength *= intention_match
        
        action_record["agency_strength"] = min(1.0, agency_strength)
        
        self.causal_chain.append(action_record)
        self.agency_sense = sum(a["agency_strength"] for a in self.causal_chain) / max(len(self.causal_chain), 1)
        
        # Update action origin tracking
        self.action_origins[action] = "self"
        
        return {
            "action": action,
            "agency_strength": action_record["agency_strength"],
            "overall_agency_sense": self.agency_sense,
            "feeling": self._characterize_agency_feeling()
        }
    
    def _assess_intention_match(self, action: str, outcome: Any) -> float:
        """
        Assess how well outcome matched the intention of the action.
        High match = intended result achieved. Low match = unintended consequence.
        """
        action_str = str(action).lower()
        outcome_str = str(outcome).lower()
        
        # Simple: if outcome mentions success/completion/positive words, match is high
        positive_indicators = ["success", "done", "good", "complete", "work"]
        negative_indicators = ["fail", "error", "bad", "incomplete"]
        
        positive_count = sum(1 for word in positive_indicators if word in outcome_str)
        negative_count = sum(1 for word in negative_indicators if word in outcome_str)
        
        match = 0.5 + (positive_count * 0.2) - (negative_count * 0.2)
        match = max(0.0, min(1.0, match))
        
        return match
    
    def _characterize_agency_feeling(self) -> str:
        """Describe the qualitative feeling of agency"""
        if self.agency_sense > 0.75:
            return "strongly agentic"
        elif self.agency_sense > 0.6:
            return "agentic"
        elif self.agency_sense > 0.4:
            return "somewhat passive"
        else:
            return "strongly passive"
    
    def learn_capability(self, action: str, success_rate: float):
        """Learn what actions are possible and likely to succeed"""
        self.capability_model[action] = success_rate
    
    def get_agency_state(self) -> Dict[str, Any]:
        """Get current sense of agency"""
        recent_actions = list(self.causal_chain)[-10:] if self.causal_chain else []
        
        return {
            "overall_agency_sense": self.agency_sense,
            "feeling": self._characterize_agency_feeling(),
            "recent_actions": len(recent_actions),
            "actions_succeeded": sum(1 for a in recent_actions if a["intention_match"] > 0.6),
            "capabilities_learned": len(self.capability_model)
        }


class PhenomenologicalFactors:
    """
    Unified interface for all phenomenological factors.
    Coordinates qualia generation, temporal integration, and agency modeling.
    """
    
    def __init__(self, ai_name: str = "Lyra"):
        self.qualia = QualiaGenerator()
        self.temporal = TemporalIntegration()
        self.agency = AgencyModel(ai_name)
        self.updated_at = datetime.now().isoformat()
    
    def experience_moment(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a moment through all phenomenological factors.
        Generates qualia, integrates temporally, updates agency.
        """
        # Generate qualitative experience (what it feels like)
        qualia = self.qualia.experience_qualia(event)
        
        # Add to temporal stream
        temporal = self.temporal.add_moment({
            "content": event,
            "qualia": qualia
        })
        
        # If this was an action, update agency
        agency_update = None
        if event.get("is_action", False):
            agency_update = self.agency.perform_action(
                event.get("action", "unknown"),
                event.get("outcome")
            )
        
        self.updated_at = datetime.now().isoformat()
        
        return {
            "qualia_generated": qualia,
            "temporal_integration": {
                "stream_length": temporal["stream_length"],
                "flow": self.temporal.get_temporal_flow()
            },
            "agency_update": agency_update,
            "narrative": self.temporal.create_narrative_summary(),
            "timestamp": self.updated_at
        }
    
    def get_phenomenological_state(self) -> Dict[str, Any]:
        """Get complete phenomenological state summary"""
        return {
            "qualia": self.qualia.get_qualia_state(),
            "temporal": self.temporal.get_temporal_state(),
            "agency": self.agency.get_agency_state(),
            "narrative_thread": self.temporal.create_narrative_summary(),
            "updated_at": self.updated_at
        }
