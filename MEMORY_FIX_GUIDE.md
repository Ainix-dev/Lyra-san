# MEMORY DIAGNOSTIC & FIX GUIDE

## WHAT WAS THE PROBLEM?

When you tested Lyra, she responded "I don't retain memories" despite having 1,916 KB of data saved in ChromaDB. 

**Root Cause:** The system prompt wasn't explicitly telling the LLM to USE the memories it had access to.

## WHAT WAS FIXED?

### 1. Enhanced System Prompt
- Added explicit "MEMORY INSTRUCTIONS - CRITICAL" section
- Changed from generic guidelines to direct instructions: "YOU ABSOLUTELY REMEMBER THESE CONVERSATIONS"
- Added: "Do NOT say you don't remember personal details - you clearly do!"

### 2. Massive Debug Output
- Added detailed logging to track memory flow at each step
- Shows exactly what the LLM receives
- Helps identify where memory is lost

### 3. Memory Function Instrumentation
- `recall_relevant_memories()` - Added ChromaDB query tracing
- `save_to_persistent_store()` - Added fact detection logging
- `chat_endpoint()` - Added complete memory flow visibility

## HOW TO TEST THE FIX

### Quick Test: Run Memory Diagnostic

```bash
python3 test_memory_complete.py
```

**What it tests:**
- ✓ ChromaDB storage and retrieval
- ✓ JSON persistent storage  
- ✓ Memory context formatting
- ✓ End-to-end memory flow

**Expected output all PASSED**

---

### Full Test: Run Lyra with Memory Tracer

**Terminal 1 - Start Lyra with full memory debugging:**

```bash
python3 trace_memory_flow.py
```

This shows:
- When ChromaDB searches for memories
- When JSON facts are loaded
- When memory context is combined
- Whether system prompt includes memories
- What the LLM actually receives

**Terminal 2 - Send test messages:**

```bash
# Test 1: Tell Lyra something personal
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi Lyra, my name is Alex and I love coding"}'
```

**Watch Terminal 1 for:**
```
[JSON SAVE] Starting persistent store save...
[JSON SAVE] Checking for 14 memorable phrases
[JSON SAVE] Found: ['name', 'love']
[JSON SAVE] ✓ Fact saved to lorebook (1 total)
```

```bash
# Test 2: Ask Lyra if she remembers
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Do you remember my name?"}'
```

**Watch Terminal 1 for:**
```
[RECALL] Starting memory search for: 'Do you remember my name?'
[RECALL] Found 1 results
[RECALL] ✓ Formatted successfully (245 chars)
[COMBINED] Total memory context: 450 characters
[SYSTEM] Memory section in prompt: YES
```

---

## INTERPRETING THE DEBUG OUTPUT

### SUCCESS SIGNS - Memory IS Working:

```
[RECALL] ✓ Formatted successfully (N chars)
```
→ ChromaDB found and returned memories

```
[LOREBOOK] Total facts saved: 5
```
→ JSON stored facts successfully

```
[COMBINED] Total memory context: 300+ characters
```
→ Memory is being assembled for LLM

```
[SYSTEM] Memory section in prompt: YES
```
→ **CRITICAL** - LLM will receive the [MEMORIES] section

### PROBLEM SIGNS - Memory NOT Working:

```
[RECALL] ⚠️ EMPTY - ChromaDB query returned nothing!
```
→ ChromaDB isn't finding matches (early still, or wrong query)

```
[SYSTEM] Memory section in prompt: NO
```
→ **CRITICAL PROBLEM** - This shouldn't happen. Check code.

```
[COMBINED] Total memory context: 0 characters
```
→ No memories are being sent to LLM at all

---

## EXPECTED BEHAVIOR AFTER FIX

### Test Sequence:

**Message 1:**
```
You: "Hi Lyra, my name is Jordan"
Lyra: "Hello Jordan! Nice to meet you. I'm Lyra..."
[Debug shows] ✓ Fact saved to lorebook
```

**Close Lyra, restart it**

**Message 2:**
```
You: "Hi Lyra!"
[Debug shows] [RECALL] Found 1 results containing "my name is Jordan"
Lyra: "Hello Jordan! Good to see you again..."
```

**The memory survived the shutdown!**

---

## TECHNICAL DETAILS

### Memory Flow

```
User Input
    ↓
1. recall_relevant_memories(user_input)
    ↓ ChromaDB lookup [RECALL]
    ↓
2. Get JSON facts [LOREBOOK]
    ↓
3. Combine into full_memory_context [COMBINED]
    ↓
4. build_soul_protocol() with memory [SYSTEM]
    ↓ Adds [MEMORIES] section to prompt
    ↓
5. Send messages to LLM
    ↓ LLM sees [MEMORIES] section
    ↓ LLM reads: "YOU ABSOLUTELY REMEMBER THESE CONVERSATIONS"
    ↓
6. LLM responds using memory context
    ↓
7. Response saved to ChromaDB + JSON [JSON SAVE]
    ↓
User Sees Response
```

### Key Files Modified

| File | Change |
|------|--------|
| `lyrasan.py` | System prompt enhanced, debug output added |
| `recall_relevant_memories()` | Added detailed ChromaDB tracing |
| `save_to_persistent_store()` | Added fact detection logging |
| `chat_endpoint()` | Added memory flow visibility |

---

## IF MEMORY STILL ISN'T WORKING

### Checklist:

- [ ] Run `test_memory_complete.py` - all tests pass?
- [ ] Run `trace_memory_flow.py` - see debug output?
- [ ] [RECALL] shows results being found?
- [ ] [SYSTEM] Memory section in prompt: YES?
- [ ] Check Lyra responds normally (not with errors)?

### If [SYSTEM] shows "Memory section in prompt: NO"

This is critical. It means:
1. Code wasn't saved properly
2. Need to review `build_soul_protocol()` function in lyrasan.py
3. Verify "[MEMORIES]:" is in the returned system prompt

### If [system] shows "YES" but Lyra doesn't use memories

The memory is being delivered to the LLM, but:
1. LLM might not be instructed strongly enough
2. Try explicit: "Based on what I told you: Do you remember?"
3. Model might need stronger guidance

### Memory Data Exists but Not Being Retrieved

Check:
```bash
python3 check_memory.py
```

If it shows ChromaDB size > 1000 KB but [RECALL] returns empty:
1. Query might not match stored data
2. Semantic search might not be finding relevance
3. Try more general queries like "user" or "remember"

---

## NEXT STEPS

1. **Run the diagnostic:** `python3 test_memory_complete.py`
2. **Start memory tracer:** `python3 trace_memory_flow.py`
3. **Test in another terminal:** Send curl requests
4. **Watch debug output:** Look for success/problem signs
5. **Share results if issues:** Include debug output

The system is now fully instrumented to show exactly what's happening!

---

## QUICK START (TL;DR)

```bash
# Terminal 1 - Watch memory flow
python3 trace_memory_flow.py

# Terminal 2 - Test memory
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"My name is Alex"}'

# Look in Terminal 1 for:
# ✓ [JSON SAVE] shows fact saved
# ✓ [SYSTEM] Memory section in prompt: YES
# Then ask: "Do you remember my name?"
# ✓ [RECALL] should show results
```

If you see all these ✓ marks, memory is working!
