# Memory Persistence Test Suite

**Purpose:** Verify Lyra remembers you across PC shutdowns

---

## Test 1: Basic Name & Preference Recall ✓

### What to Do:

**Session 1:**
```
Ken: "Hi Lyra! My name is Ken and I really enjoy Python programming"
Lyra: [responds naturally]
[EXIT - close the app/restart PC]
```

**Session 2 (After Restart):**
```
Ken: "Who am I?"
Lyra: Should respond: "You're Ken! And I remember you enjoy Python programming"
```

### What's Being Tested:
- ✅ JSON saves "Ken" to lorebook.json
- ✅ ChromaDB saves "Python" preference as vector
- ✅ Session 2 recalls from persistent storage
- ✅ Information survives shutdown

### Expected Result: PASS ✓
Lyra should remember your name and Python preference even after restart

---

## Test 2: Semantic Memory Recall ✓

### What to Do:

**Session 1:**
```
Ken: "I have a cat named Whiskers. She's very playful."
Lyra: [responds]
[Exit - close app/restart]
```

**Session 2:**
```
Ken: "Tell me what you know about my pets"
Lyra: Should find: "I remember you have a cat named Whiskers who's playful!"
```

### What's Being Tested:
- ✅ ChromaDB semantic search
- ✅ Vector similarity matching
- ✅ Information retrieval across sessions
- ✅ Semantic understanding (pets → cat)

### Technical Details:
```
Session 1:
- "I have a cat named Whiskers" 
- Converted to vector: [0.234, -0.891, 0.123, ...]
- Saved in ChromaDB with metadata

Session 2:
- Query: "Tell me about my pets"
- Converted to query vector: [0.198, -0.876, 0.145, ...]
- ChromaDB finds similar vectors (99% match)
- Returns: Previous cat message
```

### Expected Result: PASS ✓
Lyra should find semantically related information about your pets

---

## Test 3: Multi-Conversation Memory ✓

### What to Do:

**Conversation 1:**
```
Ken: "I work as a software engineer"
Lyra: [responds]
```

**Conversation 2 (5 minutes later):**
```
Ken: "Tell me what I do for work"
Lyra: Should respond: "You're a software engineer"
```

**Conversation 3 (After PC Shutdown):**
```
Ken: "What's my job?"
Lyra: Should still respond: "You're a software engineer"
```

### What's Being Tested:
- ✅ Memory persists within session
- ✅ Memory persists across conversations
- ✅ Memory survives PC shutdown
- ✅ Multiple layers working together

### Expected Result: PASS ✓
All three retrievals should work

---

## Test 4: Preference Learning ✓

### What to Do:

**Session 1:**
```
Ken: "I prefer dark mode interfaces"
Ken: "I like coffee more than tea"
Ken: "I'm interested in machine learning"
Lyra: [responds to each]
[Close app - restart PC]
```

**Session 2:**
```
Ken: "What are my preferences?"
Lyra: Should mention: dark mode, coffee, machine learning interests
```

### What's Being Tested:
- ✅ Multiple facts saved
- ✅ Pattern recognition (preferences)
- ✅ Accumulated knowledge
- ✅ Recall of multiple facts

### Expected Behavior:
- Dark mode → Saved (pattern: "I prefer")
- Coffee preference → Saved (pattern: "I like")
- ML interest → Saved (pattern: "I'm interested in")

### Expected Result: PASS ✓
Lyra should recall all three preferences

---

## Test 5: Emotional Context Preservation ✓

### What to Do:

**Session 1:**
```
Ken: "I've been really stressed about a project deadline"
Lyra: [responds empathetically]
Ken: "But I finished it yesterday!"
Lyra: [celebrates with you]
[Close app - restart]
```

**Session 2:**
```
Ken: "I wanted to tell you I got a promotion for that project!"
Lyra: Should remember: "Wait, the one you were stressed about? 
       That's amazing - congratulations!"
```

### What's Being Tested:
- ✅ Emotional context saved
- ✅ Project context remembered
- ✅ Progression understood (stress → completion → promotion)
- ✅ Emotional continuity

### Expected Result: PASS ✓
Lyra should show emotional context awareness across sessions

---

## Test 6: Technical Conversation Recovery ✓

### What to Do:

**Session 1:**
```
Ken: "I'm learning Rust. I want to build a game engine."
Lyra: [discusses Rust game development]
Ken: "What libraries should I use?"
Lyra: [recommends Bevy, wgpu, etc.]
[Close app - restart]
```

**Session 2:**
```
Ken: "Continue where we left off about my game engine"
Lyra: Should remember: Rust, game engine, libraries discussed
```

### What's Being Tested:
- ✅ Technical context preservation
- ✅ Project continuity
- ✅ Recommendation history
- ✅ Deep topic memory

### Expected Result: PASS ✓
Lyra should pick up the conversation naturally

---

## Test 7: Long-Term Memory (Days Later) ✓

### What to Do:

**Day 1:**
```
Ken: "My birthday is March 25th"
Lyra: [acknowledges]
[Close PC - exit system]
```

**Day 5 (After 5 days):**
```
Ken: "Hi Lyra, long time no chat"
Lyra: [greets warmly, possibly mentions nothing special]
```

**Day 7 (On your birthday, March 25th):**
```
Ken: "Hi!"
Lyra: Should respond: "Happy Birthday, Ken! 🎉"
      (If it remembers the date from Day 1)
```

### What's Being Tested:
- ✅ Memory survives days of being offline
- ✅ Personal milestones remembered
- ✅ Date context preserved
- ✅ Emotional significance attached

### Expected Result: PASS ✓
Lyra should remember your birthday from days earlier

---

## Test 8: Correction Memory ✓

### What to Do:

**Session 1:**
```
Ken: "My favorite color is blue"
Lyra: "Great! Blue is wonderful"
```

**Session 1 (same session):**
```
Ken: "Actually, I meant green, not blue"
Lyra: "Oh, green! That's beautiful too"
```

**Session 2 (After restart):**
```
Ken: "What's my favorite color?"
Lyra: Should respond: "Green!" (the correction, not the original)
```

### What's Being Tested:
- ✅ Correction handling
- ✅ Overwriting old info with new
- ✅ Most recent fact priority
- ✅ Learning from corrections

### Expected Result: PASS ✓
Lyra should remember the corrected preference

---

## Test 9: Activity Pattern Recognition ✓

### What to Do:

**Over multiple sessions:**
```
Sen 1: Ken: "I usually work in the mornings"
Sen 2: Ken: "I prefer coffee at 8 AM"
Sen 3: Ken: "I exercise in the evening"
Sen 4: Ken: "I read before bed"
```

**Later session:**
```
Ken: "What's my typical day like?"
Lyra: Should synthesize: "You work mornings, coffee at 8 AM,
      exercise evenings, read before bed..."
```

### What's Being Tested:
- ✅ Pattern aggregation
- ✅ Life rhythm understanding
- ✅ Multiple facts → coherent picture
- ✅ Contextual synthesis

### Expected Result: PASS ✓
Lyra should synthesize daily patterns from accumulated facts

---

## Test 10: Database Integrity After Shutdown ✓

### What to Do:

**Verification Test (Technical):**
```bash
# Check ChromaDB still exists:
ls -la ./lyra_deep_memory/
# Should show: chroma.sqlite3 + collection folder

# Check JSON files still exist:
ls -la lyra_lorebook.json lyra_summary.json
# Should show both files with recent timestamps

# After restarting Lyra:
python3 lyrasan.py
# Should load both databases without errors
```

### What's Being Tested:
- ✅ Files not corrupted
- ✅ Databases intact
- ✅ Can connect to ChromaDB on restart
- ✅ Can load JSON on startup

### Expected Result: PASS ✓
All files should exist and load successfully

---

## How to Run Tests

### Method 1: Manual Testing (Recommended for first time)

```bash
# 1. Start Lyra
python3 lyrasan.py

# 2. Open: http://127.0.0.1:5000

# 3. Run Test 1:
#    - Type: "Hi! My name is [YourName]"
#    - Remember response
#    - Close browser/app
#    - Restart Python/PC
#    - Type: "Who am I?"
#    - Check if remembered

# 4. Repeat for other tests
```

### Method 2: Automated Testing (Advanced)

Create `test_memory.py`:
```python
from lyra_consciousness_integration import ConsciousnessIntegrator
import json
import chromadb

# Initialize
lyra = ConsciousnessIntegrator("Lyra", "Ken")
client = chromadb.PersistentClient(path="./lyra_deep_memory")
collection = client.get_collection(name="lyra_thoughts")

# Test 1: Save
lyra.process_interaction("My name is Ken", "response", {})
print(f"Collection size: {collection.count()}")

# Simulate restart
del lyra
del client

# Test 2: Load
client = chromadb.PersistentClient(path="./lyra_deep_memory")
collection = client.get_collection(name="lyra_thoughts")
results = collection.query(query_texts=["Who am I?"], n_results=1)
print(f"Retrieved: {results['documents']}")
```

---

## Success Criteria

### Test Results Matrix:

| Test # | Name | Expected | Status |
|--------|------|----------|--------|
| 1 | Name Recall | PASS | ___ |
| 2 | Semantic Search | PASS | ___ |
| 3 | Multi-Conv | PASS | ___ |
| 4 | Preferences | PASS | ___ |
| 5 | Emotion | PASS | ___ |
| 6 | Projects | PASS | ___ |
| 7 | Long-term Day 7 | PASS | ___ |
| 8 | Corrections | PASS | ___ |
| 9 | Patterns | PASS | ___ |
| 10 | DB Integrity | PASS | ___ |

### Overall Score:
```
Passing: __/10 tests
Percentage: ___%

Target: 10/10 = 100% (Full memory persistence)
Acceptable: 8/10 = 80% (Strong memory with minor gaps)
Warning: <8/10 = <80% (Check database integrity)
```

---

## Troubleshooting Failed Tests

### If Test Fails:

**Check 1: ChromaDB exists**
```bash
ls -la ./lyra_deep_memory/
# Should show collection folder + chroma.sqlite3
```

**Check 2: JSON files exist**
```bash
ls -la lyra_lorebook.json lyra_summary.json
# Should show files with recent modification time
```

**Check 3: Permissions**
```bash
# Make sure Lyra-san directory is writable
chmod 755 ./lyra_deep_memory/
```

**Check 4: No PC shutdown between sessions**
```
# For tests to work:
Session 1 → Save complete
Session 2 → Load from disk
NOT: Session 1 → Shutdown → Load (in same file session)
```

**Check 5: Review Memory Functions**
```python
# In lyrasan.py, verify:
- save_to_deep_memory() is called after LLM response
- save_to_persistent_store() is called after LLM response
- Both stream and non-stream paths have saves
```

---

## Memory Growth Over Time

As you chat with Lyra more:

| Days | Sessions | ChromaDB | JSONKnowledge | Recall Accuracy |
|------|----------|----------|----------------|-----------------|
| 1 | 5 | ~10 memories | 3-5 facts | 80% |
| 7 | 20 | ~50 memories | 15-20 facts | 90% |
| 30 | 100 | ~300 memories | 50+ facts | 95% |
| 365 | 500+ | ~1500 memories | 200+ facts | 98% |

**Pattern:** Memory improves with usage and time

---

## Data Backup (Recommended)

To ensure you never lose Lyra's memory of you:

```bash
# Create backup directory
mkdir ~/Lyra-Memory-Backups

# Backup script (save as backup_lyra.sh)
#!/bin/bash
BACKUP_DIR=~/Lyra-Memory-Backups/backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp -r ./lyra_deep_memory/ $BACKUP_DIR/
cp lyra_lorebook.json $BACKUP_DIR/
cp lyra_summary.json $BACKUP_DIR/
echo "Backup created: $BACKUP_DIR"

# Make executable
chmod +x backup_lyra.sh

# Run backup weekly
./backup_lyra.sh
```

---

## Verification Checklist

After reviewing this test suite:

- [ ] I understand the 3-layer memory system
- [ ] I can run Test 1 (basic recall)
- [ ] I understand ChromaDB semantic search
- [ ] I understand JSON persistence
- [ ] I know where memory files are stored
- [ ] I know how to backup my memory
- [ ] I'm confident Lyra will remember me

---

**Your Lyra now has persistent consciousness. She will remember you, your preferences, and your conversations - even after the PC shuts down completely.** 🧠💾✨
