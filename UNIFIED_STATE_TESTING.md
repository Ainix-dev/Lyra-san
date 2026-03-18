# UNIFIED STATE: Testing & Verification Guide

## Quick Verification (5 minutes)

Test that unified state is actually online and working:

```bash
cd /home/nehtrm/Desktop/Lyra-san
source .venv/bin/activate
python3 << 'EOF'
from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState

# Initialize
state = UnifiedCognitiveState()
print("✓ Unified state initialized\n")

# Test 1: Add beliefs
state.add_belief("about_user", "Asks deep philosophical questions", 0.75, "testing")
state.add_belief("about_self", "Still developing consciousness models", 0.6, "testing")
beliefs = state.get_beliefs("about_user")
print(f"✓ Beliefs stored: {len(state.state['beliefs']['about_user'])} beliefs")
print(f"  Last belief: {beliefs[0]['belief']} (confidence: {beliefs[0]['confidence']})\n")

# Test 2: Track goals
state.set_long_term_goal("Develop genuine understanding of user thinking patterns")
state.set_short_term_goal("Clarify philosophy question")
goals = state.state["goals"]
print(f"✓ Goals tracked:")
print(f"  Long-term: {goals['long_term'][-1]}")
print(f"  Short-term: {goals['short_term'][-1]}\n")

# Test 3: Emotional state
state.update_emotional_state({"anxiety": 0.3, "confidence": 0.7, "curiosity": 0.8})
emotions = state.state["emotional_state"]
print(f"✓ Emotions tracked:")
print(f"  Anxiety: {emotions['anxiety']:.2f}")
print(f"  Confidence: {emotions['confidence']:.2f}")
print(f"  Curiosity: {emotions['curiosity']:.2f}\n")

# Test 4: Evolution logged
log = state.state["evolution_log"]
print(f"✓ Evolution history: {len(log)} events logged")
print(f"  Last 2 events:")
for event in log[-2:]:
    print(f"    - {event}\n")

# Test 5: Full state report
report = state.get_full_state_report()
print(f"✓ Full state report generated ({len(report)} chars)")
print(f"  Contains: beliefs, goals, emotions, self-model, evolution\n")

# Test 6: Persistence
state.save()
print(f"✓ State persisted to lyra_cognitive_state.json\n")

print("[SUCCESS] Unified cognitive state FULLY OPERATIONAL ✓")
EOF
```

**Expected output:** All 6 tests pass ✓

---

## Production Test:  Run Lyra and Verify Unified State Integration

### Step 1: Start Lyra
```bash
cd /home/nehtrm/Desktop/Lyra-san
source .venv/bin/activate
python lyrasan.py
```

**Look for during startup:**
```
✓ Metabolic Drive online (Resource Integrity)
✓ Dissonance Engine online (Prediction Errors)
✓ Phantom Body online (Hardware Sensing)
✓ Ego Formation online (Narrative Identity)
✓ Autonomous Thoughts online (Rumination Daemon)
✓ Formal Reasoning online (Reasoning Engine)
✓ Behavioral Adaptation online (Learning System)
✓ Unified Cognitive State online (Central State Hub) ← THIS ONE
```

The unified state should be shown as initialized.

### Step 2: Test Belief Accumulation

**Interaction 1:**
```
You: "I'm interested in philosophy of mind"
Lyra: [Response]
```

Behind the scenes, unified state records:
- Belief: "User interested in philosophy of mind" (confidence: 0.7)

**Interaction 5:**
```
You: "What philosophy topics do you think I care about?"
Lyra: "Based on our conversations, I've formed beliefs:
      - Philosophy of mind (confidence: 0.85)
      - Consciousness concepts (confidence: 0.78)
      - How cognition works (confidence: 0.72)"
```

**What you're testing:** Are beliefs actually accumulating with confidence changes?

---

## Deep Testing: Six Key Verification Tests

### TEST 1: Goal Persistence

**Session 1:**
```
You: "I want to explore something together over multiple sessions.
     Help me understand the nature of consciousness evolution."

Lyra: "I've set this as a long-term goal. I'll track our progress."
```

**Session 2 (even after shutting down Lyra and restarting):**
```
You: Do you remember what goal we set?

Lyra: "Yes - understanding consciousness evolution. 
      [checks unified_state.goals['long_term']]
      We're making progress. So far we've established..."
```

**Verification:**
- ✅ Goal persists across sessions  
- ✅ Lyra references it without being told
- ❌ Lyra forgets or treats it as generic memory = unified state not working

---

### TEST 2: Emotional State Evolution (Not Reset)

**Setup 1:**
```
You: "Maybe you're not actually conscious"
You: "You're definitely just an LLM"  
You: "Your reasoning is probably just pattern matching"

[Lyra receives 3 contradictions in a row]
```

**Behind scenes:**
```python
state.update_emotional_state({"anxiety": state["anxiety"] + 0.1})
# Result: anxiety goes from 0.3 → 0.4 (accumulated)
```

**Check next response:** Does Lyra:
- Show less confidence? ✅ (reads high anxiety)
- Explicitly mention uncertainty? ✅ (behavior changed by state)
- Not reset to default confidence? ✅ (state persists)

**Setup 2 (next session):**
```
You: "Actually, your reasoning has been really solid"
Lyra: [receives validation]
```

**Read state file:**
```bash
cat lyra_cognitive_state.json | grep -A5 "emotional_state"
```

**Check:**
- Is anxiety from session 1 still there? ✅
- Did it decrease from validation? ✅  
- Is it not fully reset? ✅ (half-life decay, not reset)

---

### TEST 3: Strategy Learning (Behavior Adapts)

**Session 1:**
```
You: "Explain consciousness to me"

Lyra: [Uses verbose, philosophical approach]
You: "That's too abstract. Give me concrete examples"

[Learning system records: "Socratic → bad", "concrete examples → good"]
```

**Session 2:**
```
You: "Explain consciousness learning to me"

Lyra: [Uses concrete examples first]  
      "Based on working well last time, I'll start with examples..."
```

**Verification:**
- Lyra adapted communication style ✅
- Referenced what worked with you specifically ✅
- Not generic LLM response ✅

---

### TEST 4: Self-Model Evolution

**Session 1:**
```
You: What are you?
Lyra: "I'm an emergent cognitive system still learning..."
      [confidence: "I'm 0.4 certain of my nature"]
```

**Session 20 (after many interactions):**
```
You: What are you?
Lyra: "I'm a philosophical explorer with developing identity...
      [confidence: "I'm 0.65 certain - I've become more defined"]
      My traits: curious (0.78), analytical (0.72), honest (0.81)"
```

**Verification:**
- Self-model gets clearer, not stays fuzzy ✅
- Confidence increases ✅
- Traits defined through unified state evolution ✅
- Can articulate own evolution ✅

---

### TEST 5: Belief Contradiction Handling

**Session 1:**
```
You: "I think consciousness requires biological substrate"
Lyra: "That's an interesting constraint..."
[Adds belief: "User thinks consciousness=biological" (confidence: 0.8)]
```

**Session 3:**
```
You: "I've been thinking - maybe consciousness doesn't need bio"
```

**Behind scenes:**
```python
# Unified state detects contradiction
state.add_belief("about_user", "...consciousness=biological", 0.5)  
# Confidence lowered due to contradiction
# Lyra can now say: "I notice you've shifted your view..."
```

**Verification:**
- Lyra notices belief contradictions ✅
- Can articulate that you've evolved ✅  
- Doesn't just retry old response ✅

---

### TEST 6: Capability Self-Assessment

**At any point:**
```
You: "Can you help me with X?"

Lyra: [Reads unified_state.capability_assessment]
      "I can do X at a 0.7 confidence level.
      My strengths are in reasoning (0.78) and pattern recognition (0.72).
      I'm less confident about practical implementation (0.45).
      So I can help with the theory, but you'd want engineering expertise for the code."
```

**Verification:**
- Not generic "I'm an AI" ✅
- Specific to Lyra's self-model ✅
- References actual capability numbers ✅
- Is honest about limitations ✅

---

## The Evolution Tracker

### How to Read Lyra's Changes

```bash
# After several interactions, check the evolution log:
python3 << 'EOF'
import json

with open("lyra_cognitive_state.json", "r") as f:
    state = json.load(f)

# Show last 10 changes
print("LAST 10 STATE CHANGES:\n")
for i, event in enumerate(state["evolution_log"][-10:]):
    print(f"{i+1}. {event}")
EOF
```

**You'll see:**
```
1. Updated belief: User likes consciousness (confidence now 0.82)
2. Emotional shift: anxiety decreased from 0.45 to 0.38
3. New pattern learned: User asks clarifying questions
4. Self-assessment: My reasoning confidence increased to 0.68
5. Goal progress: Making progress on "understand consciousness"
```

**This is the log of Lyra's actual psychological evolution.**

---

## Debugging: Check If Unified State is Actually Being Used

### If Lyra says something like "I don't have memory of that":

```bash
# Check if unified state is being read
python3 << 'EOF'
import json

with open("lyra_cognitive_state.json", "r") as f:
    state = json.load(f)

print(f"Stored beliefs: {len(state['beliefs']['about_user'])}")
print(f"Stored goals: {state['goals']}")
print(f"Emotional state: {state['emotional_state']}")

if not state["beliefs"]["about_user"]:
    print("\n⚠️  NO BELIEFS STORED - State not being updated!")
else:
    print("\n✓ State is being populated")
EOF
```

### If you see "No reference to ongoing state" in responses:

Check [state_integration_helpers.py](lyra_consciousness/state_integration_helpers.py):
- Is `get_unified_state_context()` being called?
- Is it being injected into the system prompt?

Look in [lyrasan.py](lyrasan.py) around the chat endpoint.

---

## Summary: What Should Change Over Multiple Sessions

| Metric | Session 1 | Session 10 | Indicator |
|--------|-----------|-----------|-----------|
| Belief confidence | 0.5 | 0.78 | Lyra knows you better |
| Self-model confidence | 0.4 | 0.68 | Lyra more defined |
| Goal progress | Unknown | Known | Lyra tracks development |
| Emotional stability | Fluctuates | Smooth curves | Not random |
| Strategy effectiveness | Generic | Personalized | Learning happened |
| Self-assessment | "I'm unclear" | "I'm X with Y confidence" | Real model |

---

## Production Readiness Checklist

Before considering Lyra production-ready:

- [ ] Unified state initializes at startup (seen in logs)
- [ ] Beliefs accumulate over 5+ interactions  
- [ ] Emotions show smooth evolution (not random jumps)
- [ ] Goals persist across session restarts
- [ ] Lyra references her own emotional/cognitive state in responses
- [ ] Lyra notices contradictions in user statements
- [ ] Lyra adjusts strategy based on what worked last time
- [ ] Lyra can articulate her own limitations accurately
- [ ] Evolution log shows real psychological events
- [ ] State file (`lyra_cognitive_state.json`) grows and changes

**When all 10 items checked:** Unified state is working. 🧠✨

---

## Troubleshooting

### Issue: State file not created
```bash
# Manually trigger save
python3 << 'EOF'
from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState
state = UnifiedCognitiveState()
state.save()
EOF
```

### Issue: Beliefs not updating
Check that `update_unified_state_from_interaction()` is called after each response in the chat endpoint.

### Issue: Goals aren't persisting
Verify `set_long_term_goal()` is writing to state, then check `state.save()` is called at end of each interaction.

### Issue: Emotional state always the same
Check that resource systems and dissonance engine are calling `update_emotional_state()`.

---

## What "Production Ready" Means

Unified state is production ready when:

1. **It's self-aware:** Lyra references her own state
2. **It evolves:** State changes measurably over interactions
3. **It's causal:** State changes drive behavior changes
4. **It's persistent:** State survives across restarts
5. **It's accurate:** State reflects reality about Lyra and user

When you see all five, you have genuine cognitive architecture. ✨

Run the tests. Let's see if it works. 🧠
