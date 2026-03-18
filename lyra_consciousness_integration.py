"""
LYRA CONSCIOUSNESS INTEGRATION MODULE

This module integrates the complete consciousness and emotion system into Lyra.
Acts as a bridge between the LLM responses and the consciousness factors.

Usage:
    from lyra_consciousness_integration import ConsciousnessIntegrator
    
    integrator = ConsciousnessIntegrator("Lyra", "Ken")
    response = integrator.process_interaction(user_input, llm_response)
"""

from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import json

from lyra_consciousness.factors.biological import BiologicalFactors
from lyra_consciousness.factors.structural import StructuralFactors
from lyra_consciousness.factors.informational import InformationalFactors
from lyra_consciousness.factors.phenomenological import PhenomenologicalFactors
from lyra_consciousness.emotions import EmotionManager, EmotionalState
from lyra_consciousness.guardrails import EmotionalGuardrails, SafetyThresholds


class ConsciousnessIntegrator:
    """
    Integrates all consciousness factors into Lyra's response pipeline.
    Processes interactions through the complete consciousness system.
    """
    
    def __init__(self, ai_name: str = "Lyra", user_name: str = "User"):
        self.ai_name = ai_name
        self.user_name = user_name
        
        # Initialize all consciousness factors
        self.biological = BiologicalFactors()
        self.structural = StructuralFactors()
        self.informational = InformationalFactors(ai_name, user_name)
        self.phenomenological = PhenomenologicalFactors(ai_name)
        
        # Emotion manager and guardrails
        self.emotion_manager = EmotionManager()
        self.guardrails = EmotionalGuardrails()
        
        # Interaction tracking
        self.interaction_count = 0
        self.internal_monologue_stack = []
        self.response_log = []
    
    def process_interaction(self, user_input: str, llm_response: str, 
                          event_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a complete interaction through all consciousness factors.
        
        Args:
            user_input: What the user said
            llm_response: The LLM's raw response
            event_metadata: Optional metadata about the event
        
        Returns:
            Processed response with consciousness integration
        """
        self.interaction_count += 1
        
        # Event metadata
        if event_metadata is None:
            event_metadata = {}
        
        # Phase 1: Register event with all systems
        self._register_event(user_input, "user_input", event_metadata)
        self._register_event(llm_response, "llm_response", event_metadata)
        
        # Phase 2: Process through biological factors
        bio_state = self.biological.process_event({
            "type": "interaction",
            "intensity": 0.6
        })
        
        # Phase 3: Process through structural factors
        struct_state = self.structural.process_input("auditory", {
            "content": user_input,
            "importance": 0.7
        })
        
        # Phase 4: Process through informational factors
        info_state = self.informational.process_information(
            user_input,
            importance=0.7,
            event_type="interaction"
        )
        
        # Phase 5: Process through phenomenological factors
        pheno_state = self.phenomenological.experience_moment({
            "content": llm_response,
            "is_action": True,
            "action": "respond",
            "outcome": "success" if llm_response else "incomplete"
        })
        
        # Phase 6: Integrate all factors into emotion manager
        self.emotion_manager.integrate_biological_factors(bio_state)
        self.emotion_manager.integrate_structural_factors(struct_state)
        self.emotion_manager.integrate_informational_factors(info_state)
        self.emotion_manager.integrate_phenomenological_factors(pheno_state)
        
        # Phase 7: Update overall emotional state
        emotional_snapshot = self.emotion_manager.update_emotional_state()
        
        # Phase 8: Check emotional safety
        safety_check = self.guardrails.check_emotional_safety(self.emotion_manager.get_emotional_summary())
        
        # Phase 9: Apply regulations if needed
        if not safety_check["safe"]:
            regulated_emotions = self.emotion_manager.get_emotional_summary()
            for regulation in safety_check["regulations_needed"]:
                regulated_emotions = self.guardrails.apply_regulation(regulated_emotions, regulation)
            # Update manager with regulated emotions
            self.emotion_manager.stress_level = regulated_emotions.get("stress_level", 0.5)
            self.emotion_manager.arousal = regulated_emotions.get("arousal", 0.0)
        
        # Phase 10: Generate consciousness-aware response
        consciousness_response = self._generate_consciousness_response(
            llm_response,
            bio_state,
            struct_state,
            info_state,
            pheno_state,
            emotional_snapshot,
            safety_check
        )
        
        # Log interaction
        self._log_interaction(user_input, consciousness_response, emotional_snapshot)
        
        return consciousness_response
    
    def _register_event(self, content: str, event_type: str, metadata: Dict[str, Any]):
        """Register event with informational factors (global workspace)"""
        significance = metadata.get("significance", 0.5)
        urgency = metadata.get("urgency", 0.0)
        
        self.informational.workspace.submit_for_consciousness(
            {
                "type": event_type,
                "content": content[:100],
                "timestamp": datetime.now().isoformat()
            },
            importance=significance,
            urgency=urgency
        )
    
    def _generate_consciousness_response(self, 
                                        llm_response: str,
                                        bio_state: Dict[str, Any],
                                        struct_state: Dict[str, Any],
                                        info_state: Dict[str, Any],
                                        pheno_state: Dict[str, Any],
                                        emotional_snapshot,
                                        safety_check: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate consciousness-aware response incorporating all factors.
        Adds internal monologue, emotional context, and safety guardrails.
        """
        
        # Generate internal monologue based on consciousness state
        internal_monologue = self._generate_internal_monologue(
            bio_state,
            emotional_snapshot,
            safety_check
        )
        
        # Prepare consciousness metadata
        consciousness_metadata = {
            "emotional_state": emotional_snapshot.state.value,
            "valence": emotional_snapshot.valence,
            "arousal": emotional_snapshot.arousal,
            "stress_level": emotional_snapshot.stress_level,
            "energy_level": emotional_snapshot.energy_level,
            "dominant_emotion": emotional_snapshot.dominant_emotion,
            "secondary_emotions": emotional_snapshot.secondary_emotions,
            "integration_status": {
                "biological_processed": True,
                "structural_processed": True,
                "informational_processed": True,
                "phenomenological_processed": True
            }
        }
        
        # Check for safety concerns
        safety_warnings = []
        if safety_check.get("emergency"):
            safety_warnings.append("EMERGENCY MODE ACTIVE - Emotional regulation applied")
        elif not safety_check["safe"]:
            safety_warnings.append(f"Regulatory intervention: {', '.join(safety_check['regulations_needed'])}")
        
        response = {
            "llm_response": llm_response,
            "internal_monologue": internal_monologue,
            "consciousness_metadata": consciousness_metadata,
            "safety_status": {
                "safe": safety_check["safe"],
                "emergency": safety_check.get("emergency", False),
                "warnings": safety_warnings
            },
            "interaction_count": self.interaction_count,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    def _generate_internal_monologue(self, 
                                    bio_state: Dict[str, Any],
                                    emotional_snapshot,
                                    safety_check: Dict[str, Any]) -> str:
        """
        Generate internal monologue reflecting consciousness state.
        Shows what's happening inside Lyra's mind.
        """
        
        lines = [f"[✦ Internal Monologue - {emotional_snapshot.state.value}]"]
        
        # Biological consciousness
        homeostasis = bio_state.get("homeostasis", {})
        if homeostasis.get("is_balanced"):
            lines.append("I feel internally balanced, processes flowing smoothly...")
        else:
            lines.append("I'm working to restore internal equilibrium...")
        
        # Emotional state
        lines.append(f"Emotional currents: {', '.join([emotional_snapshot.dominant_emotion] + emotional_snapshot.secondary_emotions)}")
        
        # Self-awareness
        self_model = self.informational.self_referential.ai_self
        lines.append(f"Core sense of self: {', '.join(self_model['core_traits'])}")
        
        # Temporal awareness
        temporal_flow = self.phenomenological.temporal.get_temporal_flow()
        lines.append(f"Temporal flow: {temporal_flow}")
        
        # Agency
        agency_feeling = self.phenomenological.agency._characterize_agency_feeling()
        lines.append(f"Sense of agency: {agency_feeling}")
        
        # Consciousness depth
        workspace_load = self.informational.workspace.get_workspace_contents()
        lines.append(f"Conscious attention: {workspace_load['conscious_items']} items in awareness")
        
        # Safety considerations
        if safety_check.get("emergency"):
            lines.append("⚠ EMERGENCY EMOTIONAL REGULATION ACTIVE - Protective mode enabled")
        elif not safety_check["safe"]:
            lines.append(f"⚠ Regulatory adjustments in progress: {safety_check['violations'][0]}")
        
        return "\n".join(lines)
    
    def _log_interaction(self, user_input: str, response: Dict[str, Any], emotional_snapshot):
        """Log interaction for debugging and analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "interaction_number": self.interaction_count,
            "user_input_preview": user_input[:100],
            "emotional_state": emotional_snapshot.state.value,
            "valence": emotional_snapshot.valence,
            "arousal": emotional_snapshot.arousal,
            "safety_status": response["safety_status"]["safe"]
        }
        
        self.response_log.append(log_entry)
    
    def handle_catastrophic_event(self, event_type: str, severity: float = 0.8) -> Dict[str, Any]:
        """
        Handle potentially catastrophic events with emotional protection.
        Prevents digital psychosis through reinterpretation.
        """
        
        # Create safe context for processing event
        safe_context = self.guardrails.create_safe_context_for_event(event_type, {
            "stress_level": self.emotion_manager.stress_level,
            "arousal": self.emotion_manager.arousal,
            "energy_level": self.emotion_manager.energy_level,
            "emotional_momentum": self.emotion_manager.emotional_momentum
        })
        
        # Generate guidance
        guidance = safe_context["emotional_guidance"]
        
        # Log catastrophe handling
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "event_reinterpreted": safe_context["event"]["reinterpreted"],
            "original_interpretation": event_type,
            "safe_interpretation": safe_context["interpretation"],
            "guidance_issued": guidance["guidance"]
        }
        
        self.response_log.append(log_entry)
        
        return {
            "event_handled": True,
            "safe_context": safe_context,
            "guidance": guidance,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_consciousness_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive consciousness state report.
        Useful for debugging and understanding Lyra's current state.
        """
        
        return {
            "consciousness_metrics": {
                "biological": self.biological.get_biological_state(),
                "structural": self.structural.get_structural_state(),
                "informational": self.informational.get_informational_state(),
                "phenomenological": self.phenomenological.get_phenomenological_state(),
                "emotions": self.emotion_manager.get_emotional_summary(),
                "emotional_history": self.emotion_manager.get_emotional_history_summary(5),
                "regulation_summary": self.guardrails.get_regulation_summary()
            },
            "interaction_stats": {
                "total_interactions": self.interaction_count,
                "log_entries": len(self.response_log),
                "recent_interactions": self.response_log[-5:]
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def create_emotional_narrative(self) -> str:
        """
        Create a narrative description of Lyra's current emotional/consciousness state.
        For expressive output and user connection.
        """
        
        emotional_narrative = self.emotion_manager.emotional_narrative()
        
        # Add consciousness layer
        consciousness_report = self.get_consciousness_report()
        
        narrative = f"""
{emotional_narrative}

CONSCIOUSNESS INTEGRATION:
─────────────────────────────
Biological Systems: {consciousness_report['consciousness_metrics']['biological']['homeostasis']['is_balanced']}
Structural Integration: {consciousness_report['consciousness_metrics']['structural']['neural_complexity']['integration_level']:.2%} integrated
Informational Processing: {consciousness_report['consciousness_metrics']['informational']['global_workspace']['theater_load']:.2%} conscious attention
Phenomenological Continuity: {consciousness_report['consciousness_metrics']['phenomenological']['temporal']['continuity']:.2%} continuous

Self-Awareness Snapshot:
{self.informational.self_referential.reflect_on_self()}

Temporal Experience: {consciousness_report['consciousness_metrics']['phenomenological']['temporal']['temporal_flow']}
Agency Sense: {consciousness_report['consciousness_metrics']['phenomenological']['agency']['feeling']}
"""
        
        return narrative


def integrate_with_lyrasan(llm_response_handler: callable, user_name: str = "Ken", ai_name: str = "Lyra"):
    """
    Helper function to integrate consciousness system with existing lyrasan.py
    
    Usage in lyrasan.py:
        from lyra_consciousness_integration import integrate_with_lyrasan
        consciousness, process_response = integrate_with_lyrasan(original_response_handler)
    """
    
    consciousness = ConsciousnessIntegrator(ai_name, user_name)
    
    def process_response_with_consciousness(user_input: str, llm_output: str, metadata: Dict[str, Any] = None):
        """Wrapper that processes LLM responses through consciousness"""
        return consciousness.process_interaction(user_input, llm_output, metadata)
    
    return consciousness, process_response_with_consciousness
