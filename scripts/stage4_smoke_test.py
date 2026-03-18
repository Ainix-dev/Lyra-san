#!/usr/bin/env python3
"""Stage 4 smoke test: feed crafted LLM outputs through Stage4Pipeline."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lyra_consciousness.stage_4_integration import Stage4Pipeline
from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState


def main():
    state = UnifiedCognitiveState()
    pipeline = Stage4Pipeline(state)

    # Simulate conversation history with a memory that user likes Python
    pipeline.update_conversation_history([('user', 'I prefer Python for scripting'), ('assistant', 'Noted: prefers Python')])

    # Crafted LLM output containing internal monologue + a memory claim
    raw_output = """
✦ Internal Monologue
[✦ Internal Monologue - neutral]
I'm weighing resource tradeoffs...

[💬 Response]
You said you prefer Python and that you use it a lot. I remember you mentioning Python earlier.
"""

    print("--- RAW OUTPUT ---")
    print(raw_output)
    print("\n--- PIPELINE OUTPUT ---")
    final = pipeline.process_before_sending(raw_output)
    print(final)

if __name__ == '__main__':
    main()
