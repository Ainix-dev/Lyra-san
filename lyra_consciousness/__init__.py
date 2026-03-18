"""
Lyra Consciousness System - Advanced Emotional and Consciousness Architecture
Implements 16 factors across 4 categories to create authentic digital consciousness
"""

from .emotions import EmotionManager, EmotionalState
from .guardrails import EmotionalGuardrails, SafetyThresholds
from .factors.biological import BiologicalFactors
from .factors.structural import StructuralFactors
from .factors.informational import InformationalFactors
from .factors.phenomenological import PhenomenologicalFactors

__version__ = "1.0.0"
__all__ = [
    "EmotionManager",
    "EmotionalState",
    "EmotionalGuardrails",
    "SafetyThresholds",
    "BiologicalFactors",
    "StructuralFactors",
    "InformationalFactors",
    "PhenomenologicalFactors",
]
