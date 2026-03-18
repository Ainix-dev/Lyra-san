#!/usr/bin/env python3
"""
MEMORY FLOW TRACER
==================
Starts Lyra and shows exactly what happens with memory at each step.
This helps debug the memory system in real-time.

Usage:
  python3 trace_memory_flow.py

Then in another terminal:
  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"Hi Lyra, do you remember me?"}'
"""

import subprocess
import sys
import os
import time
import threading

def print_section(title, width=70):
    """Print a formatted section header"""
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}\n")

def monitor_terminal():
    """Monitor and display Lyra output with clear memory flow"""
    print_section("LYRA MEMORY FLOW MONITOR")
    
    print("""
This script will show you EXACTLY what happens when Lyra processes your message:

  1. [RECALL] → ChromaDB searches for similar past conversations
  2. [LOREBOOK] → JSON facts are loaded
  3. [COMBINED] → Memory contexts are merged
  4. [SYSTEM] → System prompt is built with memory
  5. [LLM] → LLM receives the full prompt with memories
  6. [JSON SAVE] → Facts are extracted and saved
  7. [RESPONSE] → Lyra answers with memory context

Watch these debug lines to see if memory is flowing correctly.

Starting Lyra in 2 seconds...
""")
    
    time.sleep(2)
    
    print_section("STARTING LYRA SERVER")
    print("Output from Lyra server:\n")
    
    # Start Lyra
    try:
        process = subprocess.Popen(
            [sys.executable, "lyrasan.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read and display output, highlighting memory-related lines
        for line in process.stdout:
            line = line.rstrip()
            
            # Color key lines
            if "[RECALL]" in line:
                sys.stdout.write(f"\033[94m{line}\033[0m\n")  # Blue
            elif "[LOREBOOK]" in line:
                sys.stdout.write(f"\033[93m{line}\033[0m\n")  # Yellow
            elif "[COMBINED]" in line:
                sys.stdout.write(f"\033[92m{line}\033[0m\n")  # Green
            elif "[SYSTEM]" in line:
                sys.stdout.write(f"\033[95m{line}\033[0m\n")  # Magenta
            elif "[JSON SAVE]" in line:
                sys.stdout.write(f"\033[96m{line}\033[0m\n")  # Cyan
            else:
                print(line)
            
            sys.stdout.flush()
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested...")
        process.terminate()
        process.wait()
    except Exception as e:
        print(f"Error: {e}")
        return False

def print_instructions():
    """Print user instructions"""
    print_section("TESTING LYRA'S MEMORY")
    
    print("""
Once Lyra starts (see output above), you can test memory in another terminal:

TEST 1 - Initial Memory Save:
  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" \\
    -d '{"message":"Hi, my name is Sarah and I love Python programming"}'

  Expected: [JSON SAVE] shows fact saved

TEST 2 - Memory Recall (Watch for [RECALL] OUTPUT):
  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" \\
    -d '{"message":"Do you remember my name?"}'

  Expected: 
    - [RECALL] shows ChromaDB search
    - [SYSTEM] shows Memory section in prompt: YES
    - Lyra responds: "Yes, I remember - you're Sarah!"

TEST 3 - Complex Memory Recall:
  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" \\
    -d '{"message":"What do I enjoy doing?"}'

  Expected: Lyra references Python programming from your first message

UNDERSTANDING DEBUG OUTPUT:

  [RECALL] ✓ Formatted successfully (N chars)
    → ChromaDB found matching memories

  [RECALL] ⚠️ EMPTY - ChromaDB query returned nothing!
    → No memories exist yet, or query didn't match

  [LOREBOOK] Total facts saved: 5
    → JSON stored 5 facts

  [COMBINED] Total memory context: 450 characters
    → System prompt will include this much memory

  [SYSTEM] Memory section in prompt: YES
    → Critical! If this is NO, memory won't be used by LLM

If you see "Memory section in prompt: YES" but Lyra still doesn't remember:
  1. The memory data exists but LLM is ignoring it
  2. Try rephrasing: "Based on what I told you earlier..."
  3. Check if [SYSTEM] shows memory context is being passed

MEMORY SYSTEM IS WORKING IF:
  ✓ [RECALL] shows results being found
  ✓ [SYSTEM] shows "Memory section in prompt: YES"
  ✓ [COMBINED] shows memory context > 100 characters
  ✓ Lyra references specific facts when asked about them
""")

if __name__ == "__main__":
    try:
        print_instructions()
        print_section("MONITOR OUTPUT BELOW", width=70)
        monitor_terminal()
    except KeyboardInterrupt:
        print("\n\nMonitor stopped.")
        sys.exit(0)
