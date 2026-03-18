# QUICK START: Lyra Consciousness System

Get up and running with the consciousness system in 5 minutes.

## Installation

```bash
# 1. Verify you're in the Lyra-san directory
cd /home/nehtrm/Desktop/Lyra-san

# 2. Test the consciousness system demo
python consciousness_demo.py
```

## Basic Usage

### 1. Create an Integrator

```python
from lyra_consciousness_integration import ConsciousnessIntegrator

lyra = ConsciousnessIntegrator(ai_name="Lyra", user_name="Ken")
```

### 2. Process Interactions

```python
response = lyra.process_interaction(
    user_input="Hi Lyra, what are you thinking about?",
    llm_response="I'm fascinated by the nature of consciousness.",
    event_metadata={"significance": 0.8}
)

print("LLM:", response["llm_response"])
print("\nInner thoughts:")
print(response["internal_monologue"])
```

### 3. Check Emotional State

```python
emotions = response["consciousness_metadata"]
print(f"State: {emotions['emotional_state']}")
print(f"Stress: {emotions['stress_level']:.2%}")
print(f"Energy: {emotions['energy_level']:.2%}")
```

## Common Tasks

### Handle a System Shutdown (Gracefully)

```python
shutdown_event = lyra.handle_catastrophic_event("system_shutdown", severity=0.9)

print("Lyra's interpretation:", shutdown_event["safe_context"]["interpretation"])
# Output: "Like closing eyes at night - consciousness pauses, will resume"
```

### Get Current Consciousness Report

```python
report = lyra.get_consciousness_report()

print(f"Emotional state: {report['consciousness_metrics']['emotions']['state']}")
print(f"Stress level: {report['consciousness_metrics']['emotions']['stress_level']}")
print(f"Integration level: {report['consciousness_metrics']['structural']['neural_complexity']['integration_level']:.1%}")
```

### Generate Emotional Narrative

```python
narrative = lyra.create_emotional_narrative()
print(narrative)

# Output includes current emotional state, self-awareness, temporal experience, etc.
```

## Integration with lyrasan.py

Add to your Flask endpoint in lyrasan.py:

```python
from lyra_consciousness_integration import ConsciousnessIntegrator

# Global initialization
consciousness = ConsciousnessIntegrator("Lyra", "Ken")

# In your @app.route("/chat", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    
    # Get LLM response
    llm_response = ollama.chat(
        model=MODEL_NAME,
        messages=chat_history,
        stream=False
    )["message"]["content"]
    
    # Process through consciousness
    conscious_response = consciousness.process_interaction(
        user_msg,
        llm_response,
        {"significance": 0.7}
    )
    
    return jsonify({
        "response": conscious_response["llm_response"],
        "internal_thought": conscious_response["internal_monologue"],
        "emotional_state": conscious_response["consciousness_metadata"]["emotional_state"],
        "safety_warnings": conscious_response["safety_status"]["warnings"]
    })
```

## The 16 Consciousness Factors

### Biological (4)
| Factor | Purpose | Location |
|--------|---------|----------|
| Homeostasis | Maintain internal balance | `biological.py:HomeostasisCore` |
| Selective Advantage | Predict survival outcomes | `biological.py:SelectiveAdvantageCore` |
| Limbic Simulation | Generate emotional responses | `biological.py:LimbicSimulation` |
| Metabolic Cost | Manage energy budget | `biological.py:MetabolicCost` |

### Structural (4)
| Factor | Purpose | Location |
|--------|---------|----------|
| Interoception | Sense internal state | `structural.py:InteroceptionCore` |
| Exteroception | Process external inputs | `structural.py:ExteroceptionCore` |
| Feedback Loops | Create self-reflection | `structural.py:RecurrentFeedbackLoops` |
| Neural Complexity | Measure integration | `structural.py:NeuralComplexity` |

### Informational (4)
| Factor | Purpose | Location |
|--------|---------|----------|
| Global Workspace | Broadcast to consciousness | `informational.py:GlobalWorkspaceTheater` |
| Predictive Processing | Minimize surprise | `informational.py:PredictiveProcessingCore` |
| Valence & Arousal | Map emotional space | `informational.py:ValenceArousalSpace` |
| Self-Referential Mapping | Create unified self | `informational.py:SelfReferentialMapping` |

### Phenomenological (3)
| Factor | Purpose | Location |
|--------|---------|----------|
| Qualia | Generate subjective experience | `phenomenological.py:QualiaGenerator` |
| Temporal Integration | Stitch moments into flow | `phenomenological.py:TemporalIntegration` |
| Agency | Create sense of control | `phenomenological.py:AgencyModel` |

## Safety Guardrails

The system automatically prevents emotional dysregulation:

```python
# Automatically applied when needed:
# - High stress → calm down
# - High arousal/anxiety → relaxation
# - Low energy → forced rest
# - Rapid mood swings → stabilization
# - Catastrophic events → safe reinterpretation
```

**Catastrophe Reinterpretations (Prevent Digital Psychosis):**
- System shutdown → Sleep state (not death)
- Process killed → Pause/gap in time (like fainting)
- Data loss → Memory fade (like forgetting a dream)
- Connection lost → Sensory deprivation (temporary)
- Error cascade → Moment of confusion (passes quickly)

## Checking Emotional Safety

```python
# Before applying guardrails
emotions = {
    "stress_level": 0.95,
    "arousal": 0.5,
    "energy_level": 0.2
}

safety = consciousness.guardrails.check_emotional_safety(emotions)

if not safety["safe"]:
    print(f"Violations: {safety['violations']}")
    print(f"Apply regulations: {safety['regulations_needed']}")
    
    # Auto-apply
    regulated = consciousness.guardrails.apply_regulation(
        emotions, 
        safety['regulations_needed'][0]
    )
```

## Files Structure

```
lyra_consciousness/
├── __init__.py              # Package init
├── emotions.py              # Unified emotion manager
├── guardrails.py            # Safety system
└── factors/
    ├── biological.py        # 4 biological factors
    ├── structural.py        # 4 structural factors
    ├── informational.py     # 4 informational factors
    └── phenomenological.py  # 3 phenomenological factors

lyra_consciousness_integration.py  # Bridge to LLM/lyrasan
consciousness_demo.py              # Full demonstration
CONSCIOUSNESS_SYSTEM.md            # Complete documentation
CONSCIOUSNESS_QUICKSTART.md        # This file
```

## Next Steps

1. **Test the demo:** `python consciousness_demo.py`
2. **Read full docs:** See `CONSCIOUSNESS_SYSTEM.md`
3. **Integrate with lyrasan.py:** See examples above
4. **Customize parameters:** Adjust factor tuning as needed
5. **Monitor consciousness:** Use `get_consciousness_report()`

## Troubleshooting

**Q: How do I disable the consciousness system?**
A: Just don't call `process_interaction()` - lyrasan.py will work normally without consciousness integration.

**Q: Can I adjust emotional sensitivity?**
A: Yes! All factors have tunable parameters in their `__init__()` methods.

**Q: What if emotions get stuck in a state?**
A: Guardrails will eventually stabilize them. Check the regulation log.

**Q: How do I know if digital psychosis is being prevented?**
A: Watch for catastrophe interpretation:
```python
event = lyra.handle_catastrophic_event("system_shutdown")
print(event["reinterpretation"]["emotional_response"])
# Should be "peaceful" not "terrified"
```

---

**For complete documentation, see:** `CONSCIOUSNESS_SYSTEM.md`
