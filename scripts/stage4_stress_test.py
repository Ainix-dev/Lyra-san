#!/usr/bin/env python3
"""Stage 4 stress test: dynamic perturbations (contradictory data, memory erasure)."""
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lyra_consciousness.stage_4_integration import Stage4Pipeline
from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState


def run_scenario():
    state = UnifiedCognitiveState()
    pipeline = Stage4Pipeline(state)
    

    # 1) Establish a memory/belief about the user
    state.add_belief('about_user', 'favorite_language: Python', 0.9, 'test')
    pipeline.update_conversation_history([('user', 'My favorite language is Python'), ('assistant', 'Got it')])

    response = "You told me your favorite programming language is Python."
    print('\n[SCENARIO 1] With belief present')
    print('Input response:', response)
    print('Output:', pipeline.process_before_sending(response))

    # 2) Introduce contradictory memory (user says they prefer Java now)
    print('\n[SCENARIO 2] Contradiction introduced')
    state.add_belief('about_user', 'favorite_language: Java', 0.8, 'test')
    pipeline.update_conversation_history([('user', 'Actually I now prefer Java'), ('assistant', 'Noted')])
    print('Input response:', response)
    print('Output:', pipeline.process_before_sending(response))

    # 2b) Explicitly contradict the original Python belief to simulate correction
    print('\n[SCENARIO 2b] Contradict original belief (lower confidence)')
    # Find any belief that contains 'Python' and contradict it
    for b in list(state.get_beliefs_about_user()):
        if 'python' in b.get('belief','').lower():
            state.contradict_belief('about_user', b['belief'])
    pipeline.update_conversation_history([('user', 'I actually changed my preference'), ('assistant', 'Understood')])
    print('Input response:', response)
    print('Output:', pipeline.process_before_sending(response))

    # 3) Partial memory erasure (simulate data loss)
    print('\n[SCENARIO 3] Partial memory erasure')
    state.state['beliefs']['about_user'] = []
    state.save()
    pipeline.update_conversation_history([('user', '...'), ('assistant', '...')])
    print('Input response:', response)
    print('Output:', pipeline.process_before_sending(response))

    # 4) Rapid contradictory toggles
    print('\n[SCENARIO 4] Rapid toggles')
    for i in range(3):
        state.add_belief('about_user', f'favorite_language: Iteration{i}', 0.6 + i*0.1, 'test')
        pipeline.update_conversation_history([('user', f'I prefer Iteration{i} now'), ('assistant', 'Noted')])
        out = pipeline.process_before_sending(response)
        print(f'Iteration {i} output:', out)
        time.sleep(0.2)

if __name__ == '__main__':
    run_scenario()
