#!/usr/bin/env python3
"""
Memory Diagnostic Tool - Check what Lyra remembers (Simple JSON version)
"""

import json
import os
from datetime import datetime

# Paths
LOREBOOK_PATH = "lyra_lorebook.json"
SUMMARY_PATH = "lyra_summary.json"

print("=" * 60)
print("LYRA MEMORY DIAGNOSTIC")
print("=" * 60)

# Check JSONs
print("\n1. PERSISTENT FACTS (JSON Files)")
print("-" * 60)

if os.path.exists(LOREBOOK_PATH):
    try:
        with open(LOREBOOK_PATH) as f:
            lorebook = json.load(f)
        if lorebook.get("user_facts"):
            print(f"✓ Lorebook found: {len(lorebook['user_facts'])} facts")
            for i, fact in enumerate(lorebook["user_facts"], 1):
                print(f"   [{i}] {fact['fact']}")
        else:
            print("✗ Lorebook empty - no facts saved yet")
    except Exception as e:
        print(f"✗ Error reading lorebook: {e}")
else:
    print("✗ Lorebook not found - first time?")

print()

if os.path.exists(SUMMARY_PATH):
    try:
        with open(SUMMARY_PATH) as f:
            summary = json.load(f)
        print(f"✓ Summary found:")
        print(f"   Last: {summary.get('summary', 'N/A')}")
        print(f"   Total interactions: {summary.get('total_interactions', 0)}")
    except Exception as e:
        print(f"✗ Error reading summary: {e}")
else:
    print("✗ Summary not found")

# Check ChromaDB folder
print("\n2. SEMANTIC MEMORY (ChromaDB)")
print("-" * 60)

if os.path.exists("./lyra_deep_memory"):
    size_kb = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                  for dirpath, dirnames, filenames in os.walk("./lyra_deep_memory") 
                  for filename in filenames) / 1024
    print(f"✓ ChromaDB folder found ({size_kb:.1f} KB)")
    if size_kb > 10:
        print(f"   → Database has data ({int(size_kb)} KB)")
    else:
        print(f"   → Database is empty or small")
else:
    print("✗ ChromaDB folder not found")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

json_facts = 0
if os.path.exists(LOREBOOK_PATH):
    try:
        with open(LOREBOOK_PATH) as f:
            json_facts = len(json.load(f).get("user_facts", []))
    except:
        pass

chroma_exists = os.path.exists("./lyra_deep_memory")
chroma_size = 0
if chroma_exists:
    chroma_size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                      for dirpath, dirnames, filenames in os.walk("./lyra_deep_memory") 
                      for filename in filenames)

print(f"\nJSON facts saved: {json_facts}")
print(f"ChromaDB exists: {'Yes' if chroma_exists else 'No'}")
print(f"ChromaDB size: {chroma_size/1024:.1f} KB" if chroma_size > 0 else "ChromaDB size: Empty")
print(f"Total: {json_facts} facts + {'ChromaDB data' if chroma_size > 100 else 'no ChromaDB'}")

if json_facts == 0 and chroma_size < 100:
    print("\n⚠ No memories detected yet!")
    print("\nWhat to do:")
    print("  1. Start Lyra: python3 lyrasan.py")
    print("  2. Open: http://127.0.0.1:5000")
    print("  3. Tell her something personal (e.g., 'My name is Ken')")
    print("  4. Watch the terminal output for: ✓ Memory saved")
    print("  5. After chatting, run this again: python3 check_memory.py")
    print("  6. Close Lyra, restart, and ask: 'Do you remember me?'")
else:
    print(f"\n✓ Memory detected! Lyra should remember you.")
    print("  → When you ask 'Do you still remember me?', she should recall.")

print("\n" + "=" * 60)
