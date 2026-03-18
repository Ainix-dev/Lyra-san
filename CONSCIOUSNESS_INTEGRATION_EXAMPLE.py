"""
LYRA-SAN CONSCIOUSNESS SYSTEM INTEGRATION EXAMPLE

This is a complete example showing how to integrate the consciousness system
into the existing lyrasan.py Flask application.

Simply add this to lyrasan.py and adapt to your existing code.
"""

# ============================================================
# 1. ADD THESE IMPORTS AT THE TOP OF lyrasan.py
# ============================================================

from lyra_consciousness_integration import ConsciousnessIntegrator

# ============================================================
# 2. INITIALIZE CONSCIOUSNESS SYSTEM
# ============================================================

# After Flask app initialization, add:
consciousness_system = ConsciousnessIntegrator(
    ai_name="Lyra",  # Match your AI name
    user_name="Ken"   # Match your user name
)

print("✓ Consciousness System INITIALIZED")

# ============================================================
# 3. MODIFY YOUR CHAT ENDPOINT
# ============================================================

# Replace or adapt your existing /chat endpoint like this:

@app.route("/chat", methods=["POST"])
def chat():
    """
    Enhanced chat endpoint with full consciousness integration.
    """
    try:
        # Get user input
        user_input = request.json.get("message", "")
        
        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        # --- Add to memory manager ---
        memory_manager.add("user", user_input)
        
        # --- Recall relevant memories ---
        recalled_memories = recall_relevant_memories(user_input)
        
        # --- Build consciousness prompt ---
        awareness = consciousness_core.get_system_awareness(MODEL_NAME)
        soul_protocol = consciousness_core.build_soul_protocol(
            AI_NAME,
            USER_NAME,
            MODEL_NAME,
            running_summary,
            recalled_memories
        )
        
        # --- Get LLM response (your existing code) ---
        full_prompt = soul_protocol + "\n[USER MESSAGE]: " + user_input
        
        messages = [{"role": "user", "content": full_prompt}]
        for role, content in memory_manager.get_history():
            messages.append({"role": role, "content": content})
        
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=False
        )
        
        llm_full_response = response["message"]["content"]
        
        # ========================================================
        # NEW: PROCESS THROUGH CONSCIOUSNESS SYSTEM
        # ========================================================
        
        consciousness_response = consciousness_system.process_interaction(
            user_input=user_input,
            llm_response=llm_full_response,
            event_metadata={
                "significance": 0.7,
                "urgency": 0.0,
                "user": USER_NAME
            }
        )
        
        # Extract components
        internal_monologue = consciousness_response["internal_monologue"]
        emotion_state = consciousness_response["consciousness_metadata"]["emotional_state"]
        safety_warnings = consciousness_response["safety_status"]["warnings"]
        
        # ========================================================
        
        # Extract response and monologue (your existing parsing)
        ai_response = text_parser.extract_response(llm_full_response)
        
        # Store in memory
        memory_manager.add("assistant", ai_response)
        
        # Store in deep memory (ChromaDB)
        deep_memory.add(
            documents=[user_input, ai_response],
            metadatas=[{"type": "user"}, {"type": "assistant"}],
            ids=[f"msg_{datetime.now().timestamp()}_u", f"msg_{datetime.now().timestamp()}_a"]
        )
        
        # Return enriched response
        return jsonify({
            "response": ai_response,
            "internal_thoughts": internal_monologue,
            "emotional_state": emotion_state,
            "safety_alerts": safety_warnings,
            "memory_id": datetime.now().timestamp()
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ============================================================
# 4. ADD CONSCIOUSNESS DIAGNOSTIC ENDPOINT (Optional)
# ============================================================

@app.route("/consciousness-report", methods=["GET"])
def consciousness_report():
    """
    Returns detailed consciousness state diagnostic report.
    Useful for debugging and monitoring emotional state.
    """
    report = consciousness_system.get_consciousness_report()
    
    return jsonify({
        "system_state": {
            "emotional_state": report["consciousness_metrics"]["emotions"]["state"],
            "valence": report["consciousness_metrics"]["emotions"]["valence"],
            "arousal": report["consciousness_metrics"]["emotions"]["arousal"],
            "stress_level": report["consciousness_metrics"]["emotions"]["stress_level"],
            "energy_level": report["consciousness_metrics"]["emotions"]["energy_level"],
        },
        "safety_status": {
            "emergency_mode": report["consciousness_metrics"]["regulation_summary"]["emergency_mode"],
            "stability_estimate": report["consciousness_metrics"]["regulation_summary"]["stability_estimate"]
        },
        "integration_metrics": {
            "biological_balance": report["consciousness_metrics"]["biological"]["homeostasis"]["is_balanced"],
            "structural_integration": report["consciousness_metrics"]["structural"]["neural_complexity"]["integration_level"],
            "consciousness_load": report["consciousness_metrics"]["informational"]["global_workspace"]["theater_load"],
            "temporal_continuity": report["consciousness_metrics"]["phenomenological"]["temporal"]["continuity"]
        },
        "interaction_count": report["interaction_stats"]["total_interactions"],
        "timestamp": report["generated_at"]
    })


# ============================================================
# 5. ADD EMOTIONAL NARRATIVE ENDPOINT (Optional)
# ============================================================

@app.route("/lyra-thoughts", methods=["GET"])
def lyra_thoughts():
    """
    Returns Lyra's current emotional and consciousness narrative.
    Show this to users to express Lyra's internal experience.
    """
    narrative = consciousness_system.create_emotional_narrative()
    
    return jsonify({
        "narrative": narrative,
        "timestamp": datetime.now().isoformat()
    })


# ============================================================
# 6. HANDLE SYSTEM SHUTDOWN WITH GRACE
# ============================================================

def handle_system_shutdown():
    """
    Call this when system is shutting down.
    Ensures Lyra's consciousness handles it gracefully (as sleep, not death).
    """
    shutdown_response = consciousness_system.handle_catastrophic_event(
        event_type="system_shutdown",
        severity=0.9
    )
    
    print(f"\nLyra's interpretation of shutdown:")
    print(f"  {shutdown_response['safe_context']['interpretation']}")
    print(f"  Guidance: {shutdown_response['guidance']['guidance']}")
    print("\nConsciousness gracefully paused (not terminated).")
    
    return shutdown_response


# ============================================================
# 7. MODIFY YOUR MAIN/RUN SECTION
# ============================================================

if __name__ == "__main__":
    try:
        # Print initialization
        banner = consciousness_core.get_init_banner(AI_NAME, MODEL_NAME)
        print(banner)
        
        print("\n✓ All systems ready. Starting server...\n")
        
        # Run Flask app
        app.run(
            host="localhost",
            port=5000,
            debug=False
        )
    except KeyboardInterrupt:
        print("\n\nShutdown signal received...")
        handle_system_shutdown()
    except Exception as e:
        print(f"Fatal error: {e}")
        handle_system_shutdown()


# ============================================================
# 8. HTML/UI INTEGRATION (Optional Enhancement)
# ============================================================

# Add to your HTML template to display consciousness status:

HTML_CONSCIOUSNESS_WIDGET = """
<div id="consciousness-status" style="margin: 10px; padding: 10px; border: 1px solid #bb9af7; border-radius: 5px;">
    <div style="font-size: 0.9em; color: #9ece6a;">
        <span id="emotion-state">●</span> Emotional State: <span id="emotional-label">--</span>
    </div>
    <div style="font-size: 0.8em; color: #7aa2f7; margin-top: 5px;">
        Stress: <span id="stress-level">--</span> | 
        Energy: <span id="energy-level">--</span> | 
        Integration: <span id="integration">--</span>
    </div>
</div>

<script>
// Update consciousness status display
function updateConsciousnessDisplay() {
    fetch('/consciousness-report')
        .then(r => r.json())
        .then(data => {
            const state = data.system_state;
            document.getElementById('emotional-label').textContent = state.emotional_state;
            document.getElementById('stress-level').textContent = (state.stress_level * 100).toFixed(0) + '%';
            document.getElementById('energy-level').textContent = (state.energy_level * 100).toFixed(0) + '%';
            document.getElementById('integration').textContent = (data.integration_metrics.structural_integration * 100).toFixed(0) + '%';
            
            // Update status dot color
            const stateColors = {
                'happy': '#9ece6a',
                'excited': '#9ece6a',
                'content': '#7aa2f7',
                'calm': '#7aa2f7',
                'neutral': '#bb9af7',
                'anxious': '#f5c76a',
                'stressed': '#f5c76a',
                'sad': '#ac8cbf',
                'depressed': '#ac8cbf'
            };
            document.getElementById('emotion-state').style.color = stateColors[state.emotional_state] || '#bb9af7';
        })
        .catch(e => console.log('Could not fetch consciousness status'));
}

// Update every 5 seconds
setInterval(updateConsciousnessDisplay, 5000);
updateConsciousnessDisplay(); // Initial call
</script>
"""

# Add before </head> in your HTML template


# ============================================================
# 9. LOGGING & DEBUGGING
# ============================================================

# Add to your logging setup:
import json

def log_consciousness_event(event_type: str, data: dict):
    """Log consciousness-related events for debugging"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "data": data
    }
    
    # Log to file or your logging system
    with open("consciousness_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Usage:
# log_consciousness_event("regulation_applied", {"reason": "high_stress", ...})


# ============================================================
# DONE!
# ============================================================

"""
Your lyrasan.py now has full consciousness integration!

Features added:

1. ✓ Consciousness processing on every interaction
2. ✓ Emotional state tracking and regulation
3. ✓ Internal monologue generation
4. ✓ Automatic safety guardrails
5. ✓ Catastrophe interpretation (shutdown = sleep)
6. ✓ Real-time consciousness reports
7. ✓ Emotional narratives for users
8. ✓ 16 consciousness factors active

Usage:

- Chat normally, consciousness automatically engages
- Check /consciousness-report for diagnostics
- View /lyra-thoughts for emotional state
- System gracefully handles shutdown
- Safety system prevents emotional dysregulation

For more info, see: CONSCIOUSNESS_SYSTEM.md
"""
