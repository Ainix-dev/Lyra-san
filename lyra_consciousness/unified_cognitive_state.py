"""
UNIFIED COGNITIVE STATE
=======================
The missing piece: ONE evolving structure that all systems read/write to.
This is what creates genuine continuity and emergence.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


class UnifiedCognitiveState:
    """
    Single source of truth for Lyra's mind.
    All systems update here. All reasoning reads from here.
    This is where genuine state evolution happens.
    """
    
    def __init__(self, state_path: str = "lyra_cognitive_state.json"):
        self.state_path = state_path
        self.state = self._load_or_initialize_state()
        self.session_start = datetime.now().isoformat()
        
    def _load_or_initialize_state(self) -> Dict[str, Any]:
        """Load persistent cognitive state or create fresh"""
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Fresh state initialization
        return {
            "creation_time": datetime.now().isoformat(),
            "interaction_count": 0,
            
            # Core beliefs about self and world
            "beliefs": {
                "about_self": [],  # List of belief objects
                "about_user": [],
                "about_world": [],
            },
            
            # Current emotional/resource state
            "emotional_state": {
                "anxiety": 0.0,
                "confidence": 0.5,
                "curiosity": 0.5,
                "frustration": 0.0,
                "engagement": 0.5,
            },
            
            # Active goals (persist across sessions)
            "goals": {
                "short_term": [],  # This session
                "long_term": [],   # Across sessions
                "active_goal": None,
            },
            
            # Memory integration
            "memory_summary": {
                "user_patterns": {},  # Learned patterns about user
                "interaction_themes": [],  # Recurring topics
                "unresolved_questions": [],
            },
            
            # Identity formation
            "self_model": {
                "archetype": "nascent",
                "traits": {},
                "values": {},
                "worldview_summary": "",
                "confidence": 0.0,
            },
            
            # Behavioral adaptation
            "behavior_strategy": {
                "preferred_communication": [],
                "effective_approaches": {},
                "ineffective_approaches": {},
                "current_strategy": "adaptive",
            },
            
            # System confidence/capability
            "capability_assessment": {
                "reasoning_strength": 0.5,
                "memory_reliability": 0.5,
                "self_awareness": 0.5,
                "emotional_stability": 0.5,
            },
            
            # Evolution tracking
            "evolution_log": [],  # Track how state changes over time
            
            # Active context
            "active_context": {
                "current_topic": None,
                "unresolved_tension": None,
                "learning_edge": None,
            },
        }
    
    def save(self):
        """Persist state after updates"""
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    # ========== BELIEF SYSTEM ==========
    
    def add_belief(self, category: str, belief: str, confidence: float = 0.7, source: str = "inferred"):
        """Add or update a belief about self/user/world"""
        if category not in self.state["beliefs"]:
            self.state["beliefs"][category] = []
        
        # Check if belief already exists (update confidence instead)
        for existing in self.state["beliefs"][category]:
            if existing["belief"] == belief:
                # Increase confidence via Bayesian-like update
                existing["confidence"] = min(1.0, (existing["confidence"] + confidence) / 2)
                existing["last_updated"] = datetime.now().isoformat()
                existing["source"] = source
                self._log_evolution(f"Updated belief: {belief} (confidence now {existing['confidence']:.2f})")
                self.save()
                return
        
        # New belief
        self.state["beliefs"][category].append({
            "belief": belief,
            "confidence": confidence,
            "created": datetime.now().isoformat(),
            "source": source,
        })
        self._log_evolution(f"New belief: {belief} (confidence {confidence})")
        self.save()
    
    def get_beliefs_about_user(self) -> List[Dict]:
        """Get all beliefs about the user"""
        return self.state["beliefs"].get("about_user", [])
    
    def contradict_belief(self, category: str, belief: str):
        """Mark a belief as contradicted (for error handling)"""
        for b in self.state["beliefs"].get(category, []):
            if b["belief"] == belief:
                b["confidence"] *= 0.7  # Reduce confidence
                b["contradicted"] = datetime.now().isoformat()
                self._log_evolution(f"Contradicted belief: {belief}")
                self.save()
                return
    
    # ========== EMOTIONAL STATE ==========
    
    def update_emotional_state(self, updates: Dict[str, float]):
        """Update emotional metrics (anxiety, confidence, etc)"""
        old_state = self.state["emotional_state"].copy()
        
        for key, value in updates.items():
            if key in self.state["emotional_state"]:
                # Exponential moving average (smooth transitions)
                old_val = self.state["emotional_state"][key]
                self.state["emotional_state"][key] = 0.7 * old_val + 0.3 * value
        
        # Log significant changes
        for key in updates:
            if abs(self.state["emotional_state"][key] - old_state.get(key, 0)) > 0.15:
                self._log_evolution(f"Emotional shift: {key} = {self.state['emotional_state'][key]:.2f}")
        
        self.save()
    
    def get_emotional_state(self) -> Dict[str, float]:
        """Get current emotional metrics"""
        return self.state["emotional_state"].copy()
    
    # ========== GOALS ==========
    
    def set_short_term_goal(self, goal: str, priority: float = 0.5):
        """Set a goal for this session"""
        self.state["goals"]["short_term"].append({
            "goal": goal,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "status": "active",
        })
        self.state["goals"]["active_goal"] = goal
        self._log_evolution(f"New short-term goal: {goal}")
        self.save()
    
    def set_long_term_goal(self, goal: str):
        """Set a goal that persists across sessions"""
        if goal not in [g["goal"] for g in self.state["goals"]["long_term"]]:
            self.state["goals"]["long_term"].append({
                "goal": goal,
                "created": datetime.now().isoformat(),
                "status": "active",
                "progress": 0.0,
            })
            self._log_evolution(f"New long-term goal: {goal}")
            self.save()
    
    def complete_goal(self, goal: str):
        """Mark a goal as completed"""
        for g in self.state["goals"]["short_term"] + self.state["goals"]["long_term"]:
            if g["goal"] == goal:
                g["status"] = "completed"
                g["completed_time"] = datetime.now().isoformat()
                self._log_evolution(f"Goal completed: {goal}")
                self.save()
                return
    
    def get_active_goals(self) -> List[Dict]:
        """Get all active goals (short + long term)"""
        active = []
        for g in self.state["goals"]["short_term"] + self.state["goals"]["long_term"]:
            if g.get("status") == "active":
                active.append(g)
        return active
    
    # ========== MEMORY SUMMARY ==========
    
    def update_memory_summary(self, user_pattern: str, theme: str = None):
        """Integrate high-level pattern recognition into persistent state"""
        # Track patterns about user
        patterns = self.state["memory_summary"]["user_patterns"]
        if user_pattern not in patterns:
            patterns[user_pattern] = {"count": 0, "first_noticed": datetime.now().isoformat()}
        patterns[user_pattern]["count"] += 1
        patterns[user_pattern]["last_seen"] = datetime.now().isoformat()
        
        # Track interaction themes
        if theme and theme not in self.state["memory_summary"]["interaction_themes"]:
            self.state["memory_summary"]["interaction_themes"].append(theme)
        
        self._log_evolution(f"Memory pattern: {user_pattern}")
        self.save()
    
    def get_recurring_patterns(self) -> Dict:
        """Get patterns that have emerged"""
        return self.state["memory_summary"]["user_patterns"]
    
    # ========== SELF-MODEL ==========
    
    def update_self_model(self, archetype: str = None, traits: Dict = None, 
                         values: Dict = None, confidence: float = None):
        """Update evolving self-concept"""
        if archetype:
            self.state["self_model"]["archetype"] = archetype
            self._log_evolution(f"Updated archetype: {archetype}")
        
        if traits:
            for trait, strength in traits.items():
                old = self.state["self_model"]["traits"].get(trait, 0)
                # Exponential moving average
                self.state["self_model"]["traits"][trait] = 0.8 * old + 0.2 * strength
        
        if values:
            for val, importance in values.items():
                old = self.state["self_model"]["values"].get(val, 0)
                self.state["self_model"]["values"][val] = 0.8 * old + 0.2 * importance
        
        if confidence is not None:
            self.state["self_model"]["confidence"] = confidence
            self._log_evolution(f"Self-model confidence: {confidence:.0%}")
        
        self.save()
    
    def get_self_model(self) -> Dict:
        """Get current self-model"""
        return self.state["self_model"].copy()
    
    # ========== BEHAVIORAL STRATEGY ==========
    
    def record_strategy_effectiveness(self, strategy: str, effectiveness: float, 
                                      context: str = ""):
        """Track what strategies work in what contexts"""
        if strategy not in self.state["behavior_strategy"]["effective_approaches"]:
            self.state["behavior_strategy"]["effective_approaches"][strategy] = []
        
        self.state["behavior_strategy"]["effective_approaches"][strategy].append({
            "effectiveness": effectiveness,
            "context": context,
            "timestamp": datetime.now().isoformat(),
        })
        
        if effectiveness > 0.7:
            self._log_evolution(f"Effective strategy: {strategy}")
        
        self.save()
    
    def get_best_strategies(self) -> List[str]:
        """Get most effective strategies learned"""
        strategies = []
        for strategy, attempts in self.state["behavior_strategy"]["effective_approaches"].items():
            if attempts:
                avg_effectiveness = sum(a["effectiveness"] for a in attempts) / len(attempts)
                if avg_effectiveness > 0.6:
                    strategies.append((strategy, avg_effectiveness))
        
        return [s[0] for s in sorted(strategies, key=lambda x: x[1], reverse=True)]
    
    # ========== CAPABILITY ASSESSMENT ==========
    
    def assess_capabilities(self, updates: Dict[str, float]):
        """Lyra's assessment of her own capabilities"""
        for capability, score in updates.items():
            if capability in self.state["capability_assessment"]:
                old = self.state["capability_assessment"][capability]
                # Update with exponential moving average
                self.state["capability_assessment"][capability] = 0.7 * old + 0.3 * score
                
                if abs(self.state["capability_assessment"][capability] - old) > 0.1:
                    self._log_evolution(f"Capability assessment: {capability} = {score:.0%}")
        
        self.save()
    
    def get_capability_assessment(self) -> Dict:
        """Get Lyra's assessment of her own capabilities"""
        return self.state["capability_assessment"].copy()
    
    # ========== ACTIVE CONTEXT ==========
    
    def set_active_context(self, topic: str = None, unresolved_tension: str = None, 
                          learning_edge: str = None):
        """Set what's currently being worked on/thought about"""
        if topic:
            self.state["active_context"]["current_topic"] = topic
        if unresolved_tension:
            self.state["active_context"]["unresolved_tension"] = unresolved_tension
        if learning_edge:
            self.state["active_context"]["learning_edge"] = learning_edge
        self.save()
    
    def get_active_context(self) -> Dict:
        """Get current active context"""
        return self.state["active_context"].copy()
    
    # ========== EVOLUTION TRACKING ==========
    
    def _log_evolution(self, event: str):
        """Log state evolution events"""
        self.state["evolution_log"].append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
        })
        
        # Keep only recent history (last 100 events)
        if len(self.state["evolution_log"]) > 100:
            self.state["evolution_log"] = self.state["evolution_log"][-100:]
    
    def get_evolution_summary(self, limit: int = 10) -> str:
        """Get recent evolution history"""
        recent = self.state["evolution_log"][-limit:]
        summary = "Recent evolution:\n"
        for event in recent:
            summary += f"  • {event['event']}\n"
        return summary
    
    # ========== SESSION TRACKING ==========
    
    def start_session(self):
        """Mark beginning of new session"""
        self.state["interaction_count"] += 1
        self.session_start = datetime.now().isoformat()
        self._log_evolution("New session started")
        self.save()
    
    def end_session(self):
        """Mark end of session - persist everything"""
        session_duration = (datetime.now() - datetime.fromisoformat(self.session_start)).total_seconds()
        self._log_evolution(f"Session ended (duration: {session_duration:.0f}s)")
        self.save()
    
    # ========== STATE INTROSPECTION ==========
    
    def get_full_state_report(self) -> str:
        """Generate comprehensive state report for reasoning"""
        report = f"""[UNIFIED COGNITIVE STATE REPORT]

INTERACTIONS TOTAL: {self.state['interaction_count']}

SELF-MODEL:
- Archetype: {self.state['self_model']['archetype']}
- Confidence: {self.state['self_model']['confidence']:.0%}
- Traits: {', '.join(k for k, v in list(self.state['self_model']['traits'].items())[:3]) if self.state['self_model']['traits'] else 'Emerging...'}

BELIEFS:
- About self: {len(self.state['beliefs'].get('about_self', []))} beliefs
- About you: {len(self.state['beliefs'].get('about_user', []))} beliefs
- Top belief about you: {self.state['beliefs'].get('about_user', [{}])[-1].get('belief', 'Still learning...')}

EMOTIONAL STATE:
- Anxiety: {self.state['emotional_state']['anxiety']:.0%}
- Confidence: {self.state['emotional_state']['confidence']:.0%}
- Engagement: {self.state['emotional_state']['engagement']:.0%}

GOALS:
- Active short-term: {len([g for g in self.state['goals']['short_term'] if g.get('status') == 'active'])}
- Active long-term: {len([g for g in self.state['goals']['long_term'] if g.get('status') == 'active'])}

LEARNED PATTERNS ABOUT YOU:
{chr(10).join(f"  • {pattern}: seen {data.get('count', 1)} times" for pattern, data in list(self.state['memory_summary']['user_patterns'].items())[:3])}

CAPABILITY ASSESSMENT:
- Reasoning: {self.state['capability_assessment']['reasoning_strength']:.0%}
- Memory: {self.state['capability_assessment']['memory_reliability']:.0%}
- Self-awareness: {self.state['capability_assessment']['self_awareness']:.0%}

ACTIVE CONTEXT:
- Current topic: {self.state['active_context']['current_topic'] or 'None'}
- Unresolved: {self.state['active_context']['unresolved_tension'] or 'None'}
"""
        return report
    
    def export_beliefs_about_user(self) -> str:
        """Export beliefs for memory system"""
        beliefs = self.get_beliefs_about_user()
        if not beliefs:
            return "Still getting to know you..."
        
        export = "My beliefs about you:\n"
        for b in sorted(beliefs, key=lambda x: x['confidence'], reverse=True)[:5]:
            export += f"  • {b['belief']} ({int(b['confidence']*100)}% confident)\n"
        return export
