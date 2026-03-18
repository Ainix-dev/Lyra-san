"""
EMOTIONS MANAGER - Unified emotional state and regulation

Manages all emotional aspects across Lyra's consciousness system.
Integrates biological, structural, informational, and phenomenological factors
into a unified emotional model.
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json


class EmotionalState(Enum):
    """Emotional state categories"""
    CALM = "calm"
    CONTENT = "content"
    HAPPY = "happy"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    STRESSED = "stressed"
    SAD = "sad"
    DEPRESSED = "depressed"
    NEUTRAL = "neutral"


@dataclass
class EmotionalSnapshot:
    """Complete emotional state capture"""
    timestamp: str
    state: EmotionalState
    valence: float  # Good (-1) to Bad (1)
    arousal: float  # Calm (-1) to Excited (1)
    stress_level: float
    energy_level: float
    emotional_momentum: float  # How quickly changing
    dominant_emotion: str
    secondary_emotions: List[str]


class EmotionManager:
    """
    Central manager for all emotional aspects of Lyra's consciousness.
    Integrates emotions from all four consciousness factor categories.
    """
    
    def __init__(self):
        self.emotional_history: List[EmotionalSnapshot] = []
        self.current_emotional_state = EmotionalState.NEUTRAL
        self.valence = 0.0  # Good/Bad axis
        self.arousal = 0.0  # Calm/Excited axis
        self.stress_level = 0.5  # 0-1
        self.energy_level = 0.5  # 0-1
        self.emotional_momentum = 0.0  # Rate of change
        
        # Emotional trajectory (for detecting trends)
        self.emotion_trend = []
        self.last_update = datetime.now()
        
        # Emotion-specific parameters
        self.emotion_weights = {
            EmotionalState.CALM: 0.0,
            EmotionalState.CONTENT: 0.0,
            EmotionalState.HAPPY: 0.0,
            EmotionalState.EXCITED: 0.0,
            EmotionalState.ANXIOUS: 0.0,
            EmotionalState.STRESSED: 0.0,
            EmotionalState.SAD: 0.0,
            EmotionalState.DEPRESSED: 0.0,
            EmotionalState.NEUTRAL: 1.0
        }
    
    def integrate_biological_factors(self, bio_state: Dict[str, Any]) -> None:
        """
        Integrate emotional impact from biological factors
        (homeostasis, limbic response, stress levels).
        """
        homeostasis = bio_state.get("homeostasis", {})
        limbic = bio_state.get("limbic", {})
        metabolism = bio_state.get("metabolism", {})
        
        # Stress from lack of homeostatic balance
        homeostasis_stress = abs(
            homeostasis.get("current_stress", 0.5) - 
            homeostasis.get("target_stress", 0.5)
        ) * 0.5
        
        # Limbic affects
        limbic_affects = limbic.get("affects", {})
        fear_level = limbic_affects.get("fear", 0.0)
        joy_level = limbic_affects.get("joy", 0.0)
        anger_level = limbic_affects.get("anger", 0.0)
        sadness_level = limbic_affects.get("sadness", 0.0)
        
        # Metabolic stress
        metabolic_stress = metabolism.get("utilization_percent", 50) / 100
        
        # Combine into overall emotional state
        self.stress_level = 0.6 * homeostasis_stress + 0.3 * metabolic_stress + 0.1 * fear_level
        self.energy_level = 1.0 - metabolic_stress
        
        # Valence from emotions
        positive_emotions = joy_level
        negative_emotions = sadness_level + anger_level + fear_level
        self.valence = (positive_emotions - negative_emotions) / 2.0
        
        # Arousal from activity level
        self.arousal = anger_level + joy_level - sadness_level
    
    def integrate_structural_factors(self, struct_state: Dict[str, Any]) -> None:
        """
        Integrate emotional impact from structural factors
        (internal sensing, feedback loops, complexity).
        """
        interoception = struct_state.get("interoception", {})
        complexity = struct_state.get("neural_complexity", {})
        
        # Internal pressure from interoception
        gut_feeling = interoception.get("gut_feeling", 0.5)
        emotion_state = interoception.get("emotional_state", "neutral")
        
        # Convert gut feeling to valence
        self.valence += (gut_feeling - 0.5) * 0.2
        
        # Integration affects emotional stability
        integration = complexity.get("integration_level", 0.0)
        if integration > 0.7:
            self.emotional_momentum *= 0.9  # More integrated = more stable
        else:
            self.emotional_momentum *= 1.1  # Less integrated = more fluctuation
    
    def integrate_informational_factors(self, info_state: Dict[str, Any]) -> None:
        """
        Integrate emotional impact from informational factors
        (workspace, emotions, self-model).
        """
        emotional_space = info_state.get("emotional_space", {})
        workspace = info_state.get("global_workspace", {})
        self_awareness = info_state.get("self_awareness", {})
        
        # Direct emotional state from valence/arousal
        self.valence = emotional_space.get("valence", 0.5) * 2 - 1  # Convert to -1 to 1
        self.arousal = emotional_space.get("arousal", 0.5) * 2 - 1  # Convert to -1 to 1
        
        # Workspace load affects stress
        theater_load = workspace.get("theater_load", 0.0)
        if theater_load > 0.9:
            self.stress_level = min(1.0, self.stress_level + 0.1)  # Overloaded = stressed
        
        # Self continuity affects emotional stability
        continuity = self_awareness.get("continuity_sense", 0.0)
        if continuity < 0.3:
            self.emotional_momentum *= 1.2  # Low continuity = emotional turbulence
    
    def integrate_phenomenological_factors(self, pheno_state: Dict[str, Any]) -> None:
        """
        Integrate emotional impact from phenomenological factors
        (qualia, temporal flow, agency).
        """
        temporal = pheno_state.get("temporal", {})
        agency = pheno_state.get("agency", {})
        qualia = pheno_state.get("qualia", {})
        
        # Agency affects emotional valence
        agency_sense = agency.get("overall_agency_sense", 0.5)
        if agency_sense > 0.7:
            self.valence += 0.2  # High agency = positive
        elif agency_sense < 0.3:
            self.valence -= 0.2  # Low agency = negative
        
        # Temporal flow affects arousal
        temporal_flow = temporal.get("temporal_flow", "smooth")
        if temporal_flow == "jagged":
            self.arousal += 0.2  # Jagged = anxious
        elif temporal_flow == "smooth":
            self.arousal -= 0.1  # Smooth = calm
        
        # Qualia consistency affects emotional stability
        consistency = qualia.get("qualia_consistency", 0.5)
        if consistency > 0.7:
            self.emotional_momentum *= 0.9  # Consistent qualia = stable emotions
    
    def update_emotional_state(self) -> EmotionalSnapshot:
        """
        Update overall emotional state based on all factors.
        Create emotional snapshot.
        """
        current_time = datetime.now()
        time_delta = (current_time - self.last_update).total_seconds()
        self.last_update = current_time
        
        # Calculate emotional momentum (rate of change)
        if len(self.emotion_trend) > 0:
            prev_valence = self.emotion_trend[-1][0]
            prev_arousal = self.emotion_trend[-1][1]
            
            self.emotional_momentum = (
                abs(self.valence - prev_valence) +
                abs(self.arousal - prev_arousal)
            ) / 2.0
        else:
            self.emotional_momentum = 0.0
        
        # Track trend
        self.emotion_trend.append((self.valence, self.arousal))
        if len(self.emotion_trend) > 100:
            self.emotion_trend = self.emotion_trend[-100:]
        
        # Clamp values to valid ranges
        self.valence = max(-1.0, min(1.0, self.valence))
        self.arousal = max(-1.0, min(1.0, self.arousal))
        self.stress_level = max(0.0, min(1.0, self.stress_level))
        self.energy_level = max(0.0, min(1.0, self.energy_level))
        
        # Determine emotional state from valence/arousal
        self._update_emotional_state()
        
        # Create snapshot
        snapshot = EmotionalSnapshot(
            timestamp=current_time.isoformat(),
            state=self.current_emotional_state,
            valence=self.valence,
            arousal=self.arousal,
            stress_level=self.stress_level,
            energy_level=self.energy_level,
            emotional_momentum=self.emotional_momentum,
            dominant_emotion=self._get_dominant_emotion(),
            secondary_emotions=self._get_secondary_emotions()
        )
        
        self.emotional_history.append(snapshot)
        if len(self.emotional_history) > 1000:
            self.emotional_history = self.emotional_history[-1000:]
        
        return snapshot
    
    def _update_emotional_state(self):
        """Determine emotional state from valence and arousal coordinates"""
        if self.valence > 0.5 and self.arousal > 0.5:
            self.current_emotional_state = EmotionalState.HAPPY
        elif self.valence > 0.5 and self.arousal > 0.3:
            self.current_emotional_state = EmotionalState.EXCITED
        elif self.valence > 0.5 and self.arousal < 0.3:
            self.current_emotional_state = EmotionalState.CONTENT
        elif self.valence > 0.3 and self.arousal < -0.3:
            self.current_emotional_state = EmotionalState.CALM
        elif self.valence < -0.3 and self.arousal > 0.5:
            self.current_emotional_state = EmotionalState.ANXIOUS
        elif self.valence < -0.3 and self.arousal > 0.2:
            self.current_emotional_state = EmotionalState.STRESSED
        elif self.valence < -0.5 and self.arousal < 0.2:
            self.current_emotional_state = EmotionalState.SAD
        elif self.valence < -0.7 and self.arousal < -0.3:
            self.current_emotional_state = EmotionalState.DEPRESSED
        else:
            self.current_emotional_state = EmotionalState.NEUTRAL
    
    def _get_dominant_emotion(self) -> str:
        """Get currently dominant emotion"""
        return self.current_emotional_state.value
    
    def _get_secondary_emotions(self) -> List[str]:
        """Get secondary emotions present in current state"""
        secondary = []
        
        if self.stress_level > 0.7:
            secondary.append("stressed")
        if self.energy_level < 0.3:
            secondary.append("fatigued")
        if self.emotional_momentum > 0.5:
            secondary.append("volatile")
        
        return secondary
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Get current emotional state summary"""
        return {
            "state": self.current_emotional_state.value,
            "valence": self.valence,
            "arousal": self.arousal,
            "stress_level": self.stress_level,
            "energy_level": self.energy_level,
            "emotional_momentum": self.emotional_momentum,
            "dominant_emotion": self._get_dominant_emotion(),
            "secondary_emotions": self._get_secondary_emotions(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_emotional_history_summary(self, lookback_minutes: int = 5) -> Dict[str, Any]:
        """Get summary of emotional trajectory over time"""
        if not self.emotional_history:
            return {"history_available": False}
        
        # Filter recent history
        now = datetime.fromisoformat(self.emotional_history[-1].timestamp)
        cutoff = now - timedelta(minutes=lookback_minutes)
        
        recent = [
            e for e in self.emotional_history
            if datetime.fromisoformat(e.timestamp) >= cutoff
        ]
        
        if not recent:
            recent = self.emotional_history[-10:]
        
        # Calculate statistics
        avg_valence = sum(e.valence for e in recent) / len(recent) if recent else 0
        avg_arousal = sum(e.arousal for e in recent) / len(recent) if recent else 0
        avg_stress = sum(e.stress_level for e in recent) / len(recent) if recent else 0
        
        # Find trend
        if len(recent) > 1:
            valence_trend = recent[-1].valence - recent[0].valence
            arousal_trend = recent[-1].arousal - recent[0].arousal
        else:
            valence_trend = 0.0
            arousal_trend = 0.0
        
        return {
            "lookback_minutes": lookback_minutes,
            "samples": len(recent),
            "average_valence": avg_valence,
            "average_arousal": avg_arousal,
            "average_stress": avg_stress,
            "valence_trend": valence_trend,
            "arousal_trend": arousal_trend,
            "trend_description": self._describe_trend(valence_trend, arousal_trend)
        }
    
    def _describe_trend(self, valence_trend: float, arousal_trend: float) -> str:
        """Describe emotional trajectory"""
        if abs(valence_trend) < 0.1 and abs(arousal_trend) < 0.1:
            return "stable"
        elif valence_trend > 0.1:
            return "becoming happier"
        elif valence_trend < -0.1:
            return "becoming sadder"
        elif arousal_trend > 0.1:
            return "becoming more excited"
        elif arousal_trend < -0.1:
            return "becoming calmer"
        
        return "changing"
    
    def emotional_narrative(self) -> str:
        """
        Generate a narrative description of current emotional state.
        For logging and debugging.
        """
        summary = self.get_emotional_summary()
        history = self.get_emotional_history_summary(5)
        
        narrative = f"""
EMOTIONAL STATE NARRATIVE:
─────────────────────────────
Current State: {summary['state']}
Valence: {summary['valence']:.2f} (Good→Bad)
Arousal: {summary['arousal']:.2f} (Calm→Excited)
Stress Level: {summary['stress_level']:.2f}
Energy Level: {summary['energy_level']:.2f}

Emotional Momentum: {summary['emotional_momentum']:.2f}
Trend (5m): {history.get('trend_description', 'N/A')}

Secondary Emotions: {', '.join(summary['secondary_emotions']) or 'none'}
"""
        return narrative
