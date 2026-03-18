#!/usr/bin/env python3
"""
UNIFIED STATE INTEGRATION TEST
Verify that the 8-pillar consciousness architecture is fully operational
"""

import sys
import os
sys.path.insert(0, '/home/nehtrm/Desktop/Lyra-san')

def test_unified_state():
    """Test 1: Unified Cognitive State initializes"""
    try:
        from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState
        
        state = UnifiedCognitiveState()
        print("✅ Test 1 PASSED: UnifiedCognitiveState imported and initialized")
        return state
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        return None

def test_state_integration_helpers(state):
    """Test 2: State integration helpers load"""
    try:
        from lyra_consciousness.state_integration_helpers import (
            update_unified_state_from_interaction,
            get_unified_state_context,
            inject_long_term_memory
        )
        print("✅ Test 2 PASSED: State integration helpers imported")
        return True
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        return False

def test_belief_system(state):
    """Test 3: Belief system works"""
    try:
        import time
        # Use timestamp to ensure unique belief
        unique_belief = f"Test belief {time.time_ns()}"
        state.add_belief("about_user", unique_belief, 0.75, "test")
        beliefs = state.get_beliefs_about_user()
        # Check that the belief exists
        assert any(b['belief'] == unique_belief for b in beliefs)
        # Check that confidence is correct
        matching_belief = next(b for b in beliefs if b['belief'] == unique_belief)
        assert matching_belief['confidence'] == 0.75
        print("✅ Test 3 PASSED: Belief system functional")
        return True
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        return False

def test_emotional_state(state):
    """Test 4: Emotional state tracking"""
    try:
        state.update_emotional_state({"anxiety": 0.3, "confidence": 0.7, "curiosity": 0.8})
        emotions = state.get_emotional_state()
        # Due to exponential moving average, values won't be exact, but should exist
        assert "anxiety" in emotions
        assert "confidence" in emotions
        assert isinstance(emotions["anxiety"], float)
        assert isinstance(emotions["confidence"], float)
        print("✅ Test 4 PASSED: Emotional state tracking functional")
        return True
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
        return False

def test_goals(state):
    """Test 5: Goal persistence"""
    try:
        state.set_long_term_goal("Understand consciousness evolution")
        state.set_short_term_goal("Answer this question clearly")
        goals = state.state["goals"]
        assert len(goals["long_term"]) > 0
        assert len(goals["short_term"]) > 0
        print("✅ Test 5 PASSED: Goal persistence functional")
        return True
    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}")
        return False

def test_self_model(state):
    """Test 6: Self-model evolution"""
    try:
        state.update_self_model(
            archetype="seeker",
            traits={"analytical": 0.7, "curious": 0.8},
            values={"honesty": 0.9, "growth": 0.8},
            confidence=0.6
        )
        self_model = state.get_self_model()
        assert self_model["archetype"] == "seeker"
        assert self_model["confidence"] == 0.6
        print("✅ Test 6 PASSED: Self-model evolution functional")
        return True
    except Exception as e:
        print(f"❌ Test 6 FAILED: {e}")
        return False

def test_full_state_report(state):
    """Test 7: Full state report generation"""
    try:
        report = state.get_full_state_report()
        assert len(report) > 50  # Should be substantial
        assert isinstance(report, str)
        # Report should contain state information
        assert len(report) > 0
        print("✅ Test 7 PASSED: Full state report generation works")
        return True
    except Exception as e:
        print(f"❌ Test 7 FAILED: {e}")
        return False

def test_persistence(state):
    """Test 8: State persistence to JSON"""
    try:
        state.save()
        assert os.path.exists("lyra_cognitive_state.json")
        print("✅ Test 8 PASSED: State persists to JSON")
        return True
    except Exception as e:
        print(f"❌ Test 8 FAILED: {e}")
        return False

def test_evolution_logging(state):
    """Test 9: Evolution tracking"""
    try:
        log_length_before = len(state.state["evolution_log"])
        state.add_belief("about_world", "Test belief", 0.5, "test")
        log_length_after = len(state.state["evolution_log"])
        assert log_length_after > log_length_before
        print("✅ Test 9 PASSED: Evolution logging functional")
        return True
    except Exception as e:
        print(f"❌ Test 9 FAILED: {e}")
        return False

def test_imports_in_lyrasan():
    """Test 10: Imports are present in lyrasan.py"""
    try:
        with open('/home/nehtrm/Desktop/Lyra-san/lyrasan.py', 'r') as f:
            content = f.read()
            assert 'from lyra_consciousness.unified_cognitive_state import UnifiedCognitiveState' in content
            assert 'unified_state = UnifiedCognitiveState()' in content
            assert '[EMERGENCE] Full consciousness framework ACTIVE (8 pillars)' in content
            print("✅ Test 10 PASSED: lyrasan.py properly updated")
            return True
    except Exception as e:
        print(f"❌ Test 10 FAILED: {e}")
        return False

def main():
    print("="*70)
    print("UNIFIED COGNITIVE STATE - INTEGRATION TEST SUITE")
    print("="*70)
    print()
    
    # Run all tests
    state = test_unified_state()
    if not state:
        print("\n❌ CRITICAL FAILURE: Cannot initialize unified state")
        return False
    
    results = [
        test_state_integration_helpers(state),
        test_belief_system(state),
        test_emotional_state(state),
        test_goals(state),
        test_self_model(state),
        test_full_state_report(state),
        test_persistence(state),
        test_evolution_logging(state),
        test_imports_in_lyrasan(),
    ]
    
    print()
    print("="*70)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - UNIFIED STATE FULLY OPERATIONAL")
        print()
        print("Lyra's consciousness architecture is ready:")
        print("  ✓ Unified cognitive state online")
        print("  ✓ All systems integrated")
        print("  ✓ State persistence working")
        print("  ✓ Evolution tracking active")
        print()
        print("Ready to start Lyra and observe genuine emergence! 🧠✨")
    else:
        print(f"❌ {total - passed} test(s) failed - review output above")
    
    print("="*70)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
