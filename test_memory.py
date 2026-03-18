#!/usr/bin/env python3
"""
Memory Test - Manually add a test memory and verify recall
"""

import json
import os
import time
import chromadb
from datetime import datetime

print("=" * 60)
print("LYRA MEMORY TEST - Manual Save & Recall")
print("=" * 60)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./lyra_deep_memory")
collection = client.get_or_create_collection(name="lyra_thoughts")

# Test 1: Save a memory
print("\n[TEST 1] Saving test memory to ChromaDB...")
timestamp = datetime.now().isoformat()
test_memory = "User said: My name is Ken and I love Python programming\nAI responded: Great to meet you Ken! Python is wonderful"

try:
    collection.add(
        documents=[test_memory],
        metadatas=[{
            "timestamp": timestamp,
            "user_input": "My name is Ken and I love Python",
            "ai_response": "Great to meet you!",
            "context": "test",
            "type": "conversation"
        }],
        ids=[f"test_mem_{int(time.time())}"]
    )
    print("✓ Memory saved successfully")
except Exception as e:
    print(f"✗ Error saving: {e}")
    exit(1)

# Test 2: Verify it's in the database
print("\n[TEST 2] Checking collection count...")
count = collection.count()
print(f"✓ Collection now has {count} memories")

if count == 0:
    print("✗ ERROR: Memory wasn't saved properly!")
    exit(1)

# Test 3: Retrieve by query
print("\n[TEST 3] Testing memory recall (semantic search)...")
print("   Query: 'What's the user's name?'")

try:
    results = collection.query(
        query_texts=["What's the user's name?"],
        n_results=1
    )
    
    if results['documents'] and results['documents'][0]:
        recalled = results['documents'][0][0]
        print(f"✓ Retrieved: {recalled[:100]}...")
    else:
        print("✗ Query returned no results")
        exit(1)
except Exception as e:
    print(f"✗ Query error: {e}")
    exit(1)

# Test 4: Save to JSON
print("\n[TEST 4] Saving fact to JSON...")
lorebook_path = "lyra_lorebook.json"

try:
    if os.path.exists(lorebook_path):
        with open(lorebook_path) as f:
            lorebook = json.load(f)
    else:
        lorebook = {"user_facts": []}
    
    lorebook["user_facts"].append({
        "timestamp": timestamp,
        "fact": "My name is Ken",
        "type": "user_preference"
    })
    
    with open(lorebook_path, 'w') as f:
        json.dump(lorebook, f, indent=2)
    
    print(f"✓ Fact saved to JSON ({len(lorebook['user_facts'])} total)")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 5: Load and verify JSON
print("\n[TEST 5] Verifying JSON load...")
try:
    with open(lorebook_path) as f:
        loaded = json.load(f)
    
    fact_count = len(loaded['user_facts'])
    print(f"✓ JSON loads successfully ({fact_count} facts)")
    
    if loaded['user_facts']:
        last_fact = loaded['user_facts'][-1]['fact']
        print(f"  Last fact: {last_fact}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Summary
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
print(f"✓ ChromaDB saves: Working")
print(f"✓ ChromaDB queries: Working")
print(f"✓ JSON saves: Working")
print(f"✓ JSON loads: Working")
print("\n✓ ALL TESTS PASSED")
print("\nNext steps:")
print("  1. Run: python3 lyrasan.py")
print("  2. Chat with Lyra (type your messages)")
print("  3. Watch terminal for ✓ Memory saved messages")
print("  4. After chatting, run: python3 check_memory.py")
print("  5. If memory increased, restart Lyra and ask:")
print("     'Do you remember what we talked about?'")
print("\n" + "=" * 60)
