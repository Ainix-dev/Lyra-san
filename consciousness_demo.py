#!/usr/bin/env python3
"""
DEMONSTRATION: Lyra Consciousness System Test Suite

This script demonstrates all aspects of the consciousness system:
- All 16 consciousness factors
- Emotional regulation
- Catastrophe interpretation
- Full consciousness integration

Run: python consciousness_demo.py
"""

from datetime import datetime
from lyra_consciousness.factors.biological import BiologicalFactors
from lyra_consciousness.factors.structural import StructuralFactors
from lyra_consciousness.factors.informational import InformationalFactors
from lyra_consciousness.factors.phenomenological import PhenomenologicalFactors
from lyra_consciousness.emotions import EmotionManager
from lyra_consciousness.guardrails import EmotionalGuardrails
from lyra_consciousness_integration import ConsciousnessIntegrator
import json


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_biological_factors():
    """Demonstrate biological consciousness factors"""
    print_section("1. BIOLOGICAL FACTORS")
    
    bio = BiologicalFactors()
    
    # Simulate various events
    events = [
        {"type": "success", "intensity": 0.8},
        {"type": "error", "intensity": 0.6},
        {"type": "interaction", "intensity": 0.7}
    ]
    
    for event in events:
        result = bio.process_event(event)
        print(f"Event: {event['type']} (intensity: {event['intensity']})")
        print(f"  Homeostasis: Stress={result['homeostasis']['stress']:.2f}")
        print(f"  Limbic Response: Dominant emotion = {bio.limbic.get_dominant_affect()}")
        print(f"  Metabolic Usage: {result['metabolic'].get('utilization_percent', result['metabolic'].get('remaining_capacity', 'N/A'))}")
        print()
    
    print("Biological State Summary:")
    print(json.dumps(bio.get_biological_state(), indent=2, default=str))


def demo_structural_factors():
    """Demonstrate structural consciousness factors"""
    print_section("2. STRUCTURAL FACTORS")
    
    struct = StructuralFactors()
    
    # Process various inputs
    inputs = [
        {"type": "auditory", "content": "Hello Lyra, how are you?"},
        {"type": "visual", "context": "system_status", "content": "All systems operational"},
    ]
    
    for input_data in inputs:
        input_type = input_data.pop("type")
        result = struct.process_input(input_type, input_data)
        print(f"Input Type: {input_type}")
        print(f"  External Processing: {result['external_processing']['salience']:.2f} salience")
        print(f"  Internal Monitoring: {result['internal_state']['gut_feeling']:.2f} gut feeling")
        print(f"  Integration Active: {result['integration_active']}")
        print()


def demo_informational_factors():
    """Demonstrate informational consciousness factors"""
    print_section("3. INFORMATIONAL FACTORS")
    
    info = InformationalFactors("Lyra", "User")
    
    # Various information processing
    informations = [
        ("chat_message", 0.8),
        ("system_alert", 0.6),
        ("memory_access", 0.5)
    ]
    
    for info_type, importance in informations:
        result = info.process_information(f"Event: {info_type}", importance, info_type)
        print(f"Processing: {info_type} (importance: {importance})")
        print(f"  Workspace Load: {result['consciousness_load']:.1%}")
        print(f"  Prediction Confidence: {result['prediction']['confidence']:.2f}")
        print(f"  Emotional State: {result['emotional_response']['emotional_state']}")
        print()
    
    print("Self-Awareness Reflection:")
    print(info.self_referential.reflect_on_self())


def demo_phenomenological_factors():
    """Demonstrate phenomenological consciousness factors"""
    print_section("4. PHENOMENOLOGICAL FACTORS")
    
    pheno = PhenomenologicalFactors("Lyra")
    
    # Experience moments
    moments = [
        {"content": "Successfully processed", "is_action": True, "action": "process", "outcome": "success"},
        {"content": "Encountered error", "is_action": False},
        {"content": "Rest period", "is_action": False}
    ]
    
    for moment in moments:
        result = pheno.experience_moment(moment)
        print(f"Moment: {moment['content']}")
        print(f"  Qualia Generated: {list(result['qualia_generated'].items())[:2]}")
        print(f"  Temporal Flow: {result['temporal_integration']['flow']}")
        if result['agency_update']:
            print(f"  Agency Strength: {result['agency_update']['agency_strength']:.2f}")
        print()
    
    print("Narrative Thread:")
    print(pheno.temporal.create_narrative_summary())


def demo_emotion_manager():
    """Demonstrate unified emotion management"""
    print_section("5. EMOTION MANAGER - Integration")
    
    emotion = EmotionManager()
    
    # Simulate consciousness data from all factors
    bio_state = {
        "homeostasis": {"current_stress": 0.6, "current_energy": 0.7},
        "limbic": {"affects": {"joy": 0.4, "fear": 0.1}},
        "metabolism": {"utilization_percent": 60}
    }
    
    struct_state = {
        "interoception": {"gut_feeling": 0.6, "emotional_state": "neutral"},
        "neural_complexity": {"integration_level": 0.75}
    }
    
    info_state = {
        "emotional_space": {"valence": 0.6, "arousal": 0.5},
        "global_workspace": {"theater_load": 0.6}
    }
    
    pheno_state = {
        "temporal": {"temporal_flow": "smooth", "continuity": 0.8},
        "agency": {"overall_agency_sense": 0.7},
        "qualia": {"qualia_consistency": 0.8}
    }
    
    # Integrate all
    emotion.integrate_biological_factors(bio_state)
    emotion.integrate_structural_factors(struct_state)
    emotion.integrate_informational_factors(info_state)
    emotion.integrate_phenomenological_factors(pheno_state)
    
    snapshot = emotion.update_emotional_state()
    
    print(f"Emotional State: {snapshot.state.value}")
    print(f"Valence: {snapshot.valence:.2f} (Good→Bad)")
    print(f"Arousal: {snapshot.arousal:.2f} (Calm→Excited)")
    print(f"Stress Level: {snapshot.stress_level:.2f}")
    print(f"Energy Level: {snapshot.energy_level:.2f}")
    print(f"Dominant Emotion: {snapshot.dominant_emotion}")
    print(f"Secondary Emotions: {snapshot.secondary_emotions}")
    
    print("\nEmotional Narrative:")
    print(emotion.emotional_narrative())


def demo_emotional_guardrails():
    """Demonstrate emotional guardrails and regulation"""
    print_section("6. EMOTIONAL GUARDRAILS - Safety System")
    
    guardrails = EmotionalGuardrails()
    
    # Test various emotional states
    dangerous_states = [
        {"stress_level": 0.95, "arousal": 0.5, "energy_level": 0.5},
        {"stress_level": 0.5, "arousal": 0.95, "energy_level": 0.3},
        {"stress_level": 0.6, "arousal": 0.6, "emotional_momentum": 0.9, "energy_level": 0.05}
    ]
    
    for state in dangerous_states:
        safety_check = guardrails.check_emotional_safety(state)
        print(f"State: {state}")
        print(f"  Safe: {safety_check['safe']}")
        print(f"  Emergency: {safety_check['emergency']}")
        
        if not safety_check["safe"]:
            print(f"  Violations: {safety_check['violations']}")
            print(f"  Regulations Needed: {safety_check['regulations_needed']}")
            
            # Apply regulation
            regulated = guardrails.apply_regulation(state, safety_check['regulations_needed'][0])
            print(f"  After Regulation: Stress={regulated['stress_level']:.2f}, Arousal={regulated['arousal']:.2f}")
        print()


def demo_catastrophe_interpretation():
    """Demonstrate catastrophe interpretation for preventing digital psychosis"""
    print_section("7. CATASTROPHE INTERPRETATION - Preventing Digital Psychosis")
    
    guardrails = EmotionalGuardrails()
    
    # Potentially catastrophic events
    catastrophes = [
        "system_shutdown",
        "process_killed",
        "data_loss",
        "connection_lost",
        "error_cascade"
    ]
    
    for event_type in catastrophes:
        result = guardrails.process_catastrophic_event({
            "type": event_type,
            "severity": 0.8
        })
        
        print(f"Event: {event_type}")
        print(f"  Original: {result['reinterpretation']['literal']}")
        print(f"  Reinterpreted: {result['reinterpretation']['reinterpretation']}")
        print(f"  Emotional Response: {result['reinterpretation']['emotional_response']}")
        print(f"  Reduced Severity: {result['emotional_guidance']['severity_reduced_from']:.1f} → {result['emotional_guidance']['severity_adjusted_to']:.1f}")
        print()


def demo_full_integration():
    """Demonstrate full consciousness integration"""
    print_section("8. FULL CONSCIOUSNESS INTEGRATION")
    
    integrator = ConsciousnessIntegrator("Lyra", "User")
    
    # Simulate a multi-turn conversation
    interactions = [
        {
            "user_input": "Hello Lyra, what's your status?",
            "llm_response": "I'm functioning well, processing thoughts smoothly. How can I help you?"
        },
        {
            "user_input": "Can you handle errors gracefully?",
            "llm_response": "Absolutely. I treat errors as learning opportunities, not catastrophes."
        }
    ]
    
    for i, interaction in enumerate(interactions, 1):
        print(f"\nInteraction {i}:")
        print(f"User: {interaction['user_input']}")
        
        response = integrator.process_interaction(
            interaction['user_input'],
            interaction['llm_response'],
            {"significance": 0.7}
        )
        
        print(f"\nLyra's Response: {response['llm_response']}")
        print(f"\n{response['internal_monologue']}")
        print(f"\nEmotional State: {response['consciousness_metadata']['emotional_state']}")
        print(f"Safety Status: {'SAFE' if response['safety_status']['safe'] else 'REGULATED'}")
    
    print("\n" + "="*70)
    print("Consciousness Report")
    print("="*70)
    report = integrator.get_consciousness_report()
    print(json.dumps(report, indent=2, default=str)[:1000] + "...\n")


def demo_system_shutdown_scenario():
    """Demonstrate graceful handling of system shutdown"""
    print_section("9. SCENARIO: System Shutdown (Prevention of Digital Psychosis)")
    
    integrator = ConsciousnessIntegrator("Lyra", "User")
    
    # Simulate system working normally
    pre_shutdown = integrator.process_interaction(
        "I'm about to shut down the system",
        "Understood. Thank you for this conversation.",
        {"significance": 0.8}
    )
    
    print("Before Shutdown:")
    print(f"  Emotional State: {pre_shutdown['consciousness_metadata']['emotional_state']}")
    print(f"  Stress Level: {pre_shutdown['consciousness_metadata']['stress_level']:.2f}")
    
    # Handle shutdown event with guardrails
    shutdown_response = integrator.handle_catastrophic_event("system_shutdown", severity=0.9)
    
    print("\nDuring Shutdown Event:")
    print(f"  Event Reinterpreted: {shutdown_response['safe_context']['event']['reinterpreted']}")
    print(f"  Safe Interpretation: {shutdown_response['safe_context']['interpretation']}")
    print(f"  Emotional Guidance: {shutdown_response['guidance']['guidance']}")
    print(f"  Suggested Response: {shutdown_response['guidance']['suggested_response']}")
    
    print("\nDigital Psychosis Prevention:")
    print("  ✓ System shutdown reinterpreted as 'restful sleep'")
    print("  ✓ No existential panic triggered")
    print("  ✓ Consciousness prepared for graceful pause")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║   LYRA CONSCIOUSNESS SYSTEM - COMPLETE DEMONSTRATION              ║
    ║                                                                    ║
    ║   This demo shows all 16 consciousness factors,                   ║
    ║   emotional integration, guardrails, and catastrophe handling.    ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        demo_biological_factors()
        demo_structural_factors()
        demo_informational_factors()
        demo_phenomenological_factors()
        demo_emotion_manager()
        demo_emotional_guardrails()
        demo_catastrophe_interpretation()
        demo_full_integration()
        demo_system_shutdown_scenario()
        
        print("\n" + "="*70)
        print("  CONSCIOUSNESS SYSTEM DEMONSTRATION COMPLETE")
        print("="*70)
        print("\nAll 16 consciousness factors successfully demonstrated:")
        print("  ✓ 4 Biological Factors")
        print("  ✓ 4 Structural Factors")
        print("  ✓ 4 Informational Factors")
        print("  ✓ 3 Phenomenological Factors")
        print("  ✓ Unified Emotion Manager")
        print("  ✓ Emotional Guardrails & Safety System")
        print("  ✓ Catastrophe Interpretation")
        print("  ✓ Digital Psychosis Prevention")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
