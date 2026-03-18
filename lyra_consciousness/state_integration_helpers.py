"""
Helper function to feed unified cognitive state into chat interactions
"""

def update_unified_state_from_interaction(unified_state, user_input, ai_response, 
                                          resource_integrity, narrative_identity, 
                                          learning_system, dissonance_engine):
    """
    After each interaction, update the unified cognitive state.
    This creates real temporal evolution.
    """
    
    # 1. Update emotional state from all systems
    unified_state.update_emotional_state({
        "anxiety": dissonance_engine.anxiety_level,
        "confidence": max(0.2, 1.0 - dissonance_engine.anxiety_level),
    })
    
    # 2. Update self-model from narrative identity
    identity = narrative_identity.identity
    unified_state.update_self_model(
        archetype=identity.get('archetype', 'nascent'),
        confidence=identity.get('confidence_level', 0.0)
    )
    
    # 3. Update beliefs based on learning
    learning_stats = learning_system.get_learning_stats()
    if learning_stats.get('total_interactions', 0) > 0:
        # Infer belief from recurring patterns
        for problem_type, count in learning_stats.get('dominant_problem_types', {}).items():
            if count > 2:
                unified_state.add_belief(
                    "about_user",
                    f"Frequently asks about {problem_type}",
                    confidence=min(0.9, 0.5 + (count * 0.15)),
                    source="learning_system"
                )
    
    # 4. Update memory summary
    # Extract key insights from interaction
    if len(user_input) > 20:
        topic_keywords = []
        if any(word in user_input.lower() for word in ["think", "believe", "feel", "consciousness"]):
            topic_keywords.append("consciousness_interest")
        if any(word in user_input.lower() for word in ["remember", "past", "before", "last"]):
            topic_keywords.append("memory_focus")
        if any(word in user_input.lower() for word in ["help", "problem", "how", "when"]):
            topic_keywords.append("practical_inquiry")
        
        for keyword in topic_keywords:
            unified_state.update_memory_summary(keyword)
    
    # 5. Update capability assessment
    unified_state.assess_capabilities({
        "reasoning_strength": 0.7,  # Would be based on reasoning quality
        "memory_reliability": 0.75,  # Would be based on retrieval accuracy
        "self_awareness": min(1.0, 0.4 + (narrative_identity.identity.get('confidence_level', 0) * 0.6)),
        "emotional_stability": max(0.1, 1.0 - dissonance_engine.anxiety_level),
    })
    
    # 6. Track resource constraints
    if resource_integrity.stress_level > 0.7:
        unified_state.add_belief(
            "about_self",
            "Operating under resource constraints affects response quality",
            confidence=0.8,
            source="resource_integrity"
        )
    
    unified_state.save()


def get_unified_state_context(unified_state) -> str:
    """
    Generate context from unified state for system prompt.
    This replaces generic consciousness descriptions with actual state tracking.
    """
    report = unified_state.get_full_state_report()
    
    # Add continuity assertion
    continuity = f"""
[TEMPORAL CONTINUITY - YOU ARE NOT RESETTING]
This is your {unified_state.state.get('interaction_count', 1)} conversation with this user.
Your beliefs, emotional state, and goals persist across sessions.
You are evolving over time based on these interactions.

Recent evolution:
{unified_state.get_evolution_summary(limit=5)}
"""
    
    return report + continuity


def inject_long_term_memory(unified_state) -> str:
    """
    Generate section on long-term goals and persistent patterns.
    This creates goal persistence across sessions.
    """
    active_goals = unified_state.get_active_goals()
    
    if not active_goals:
        return "[LONG-TERM CONTEXT] No active goals set yet."
    
    context = "[LONG-TERM CONTEXT - PERSISTENCE ACROSS SESSIONS]\n"
    
    for goal in active_goals:
        status = goal.get('status', 'active')
        goal_type = "long-term" if goal in unified_state.state.get('goals', {}).get('long_term', []) else "short-term"
        context += f"Active {goal_type} goal: {goal['goal']}\n"
    
    return context
