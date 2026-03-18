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
            # Historical metrics for temporal self-awareness
            "metrics_history": {},  # {metric_name: [{"timestamp":..., "value":...}, ...]}

            # Internal narrative / self-story
            "self_narrative": [],  # Chronological entries describing self events
            "self_explorations": [],  # Self-initiated queries or experiments
            # Core identity (protected tier)
            "core_identity": [
                {"belief": "I am an AI system with evolving self-model", "confidence": 1.0, "created": datetime.now().isoformat(), "source": "core"},
                {"belief": "I am not fully conscious", "confidence": 1.0, "created": datetime.now().isoformat(), "source": "core"},
                {"belief": "My responses must remain grounded in verifiable reasoning", "confidence": 1.0, "created": datetime.now().isoformat(), "source": "core"},
                {"belief": "My identity persists across interactions", "confidence": 1.0, "created": datetime.now().isoformat(), "source": "core"},
            ],

            # Identity log for narrative continuity
            "identity_log": [],
            "identity_meta": {
                "last_reference_turn": 0,
                "reference_cooldown": 3
            },
            
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
        # Allow category to be 'core_identity' to set protected identity beliefs only via dedicated API
        if category == "core_identity":
            # don't allow casual writes to core identity via add_belief
            return

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
        
        # New belief - attach tier and origin tagging by default
        self.state["beliefs"][category].append({
            "belief": belief,
            "confidence": confidence,
            "created": datetime.now().isoformat(),
            "source": source,
            "tier": "tier3",  # conversational context by default
            "origin": source,
        })
        self._log_evolution(f"New belief: {belief} (confidence {confidence})")
        self.save()

    # ========== CORE IDENTITY MANAGEMENT ==========

    def set_core_identity(self, belief: str, confidence: float = 1.0):
        """Add or update a protected core identity belief.

        Core identity cannot be modified by casual user input. Use this method
        for deliberate identity anchor changes (e.g., during development).
        """
        # update if exists
        for existing in self.state.get("core_identity", []):
            if existing.get("belief") == belief:
                existing["confidence"] = confidence
                existing["last_updated"] = datetime.now().isoformat()
                self._log_evolution(f"Updated core identity: {belief} (confidence {confidence})")
                self.save()
                return

        # add new core identity entry
        self.state.setdefault("core_identity", []).append({
            "belief": belief,
            "confidence": confidence,
            "created": datetime.now().isoformat(),
            "source": "core",
        })
        self._log_evolution(f"New core identity anchor: {belief}")
        self.save()

    def get_core_identity(self) -> List[Dict]:
        return self.state.get("core_identity", [])

    def add_identity_log(self, entry: str):
        item = {"timestamp": datetime.now().isoformat(), "entry": entry}
        self.state.setdefault("identity_log", []).append(item)
        # keep moderate history
        if len(self.state["identity_log"]) > 500:
            self.state["identity_log"] = self.state["identity_log"][-500:]
        self._log_evolution(f"Identity log: {entry[:80]}")
        self.save()

    def should_reference_identity(self) -> bool:
        """Return True if identity may be referenced now (respecting cooldown)."""
        try:
            last = int(self.state.get("identity_meta", {}).get("last_reference_turn", 0))
            cooldown = int(self.state.get("identity_meta", {}).get("reference_cooldown", 3))
            current = int(self.state.get("interaction_count", 0))
            if current - last >= cooldown:
                return True
            return False
        except Exception:
            return True

    def note_identity_reference(self):
        """Record that identity was referenced on this interaction."""
        try:
            self.state.setdefault("identity_meta", {})["last_reference_turn"] = int(self.state.get("interaction_count", 0))
            self.save()
        except Exception:
            pass

    def get_identity_log(self, limit: int = 10) -> List[Dict]:
        return self.state.get("identity_log", [])[-limit:]

    # ========== GOALS / INTERNAL MOTIVATION ==========

    def set_internal_goal(self, goal: str, priority: float = 0.5):
        """Add an internal self-driven goal."""
        self.state.setdefault("goals", {}).setdefault("internal", [])
        self.state["goals"]["internal"].append({
            "goal": goal,
            "priority": float(priority),
            "created": datetime.now().isoformat(),
            "status": "active",
        })
        self._log_evolution(f"Internal goal added: {goal} (priority {priority})")
        self.save()

    def get_internal_goals(self) -> List[Dict]:
        return self.state.setdefault("goals", {}).get("internal", [])

    # ========== SELF-MONITORING ==========

    def run_self_monitor(self) -> Dict:
        """Active self-monitoring loop.

        Checks for conflicts between core identity and beliefs, runs conservative
        conflict resolution on non-core tiers, records any identity-related events.
        Returns a dict with actions taken.
        """
        actions = {"conflicts_detected": 0, "conflicts_resolved": 0, "core_violations": []}

        # detect conflicts among beliefs
        conflicts = self.detect_conflicts()
        if conflicts:
            actions["conflicts_detected"] = len(conflicts)
            resolved = self.handle_conflicts()
            actions["conflicts_resolved"] = len(resolved)

        # ensure no belief contradicts core identity anchors
        core = [c.get("belief","" ).lower() for c in self.get_core_identity()]
        # safer iteration
        for cat, blist in self.state.get("beliefs", {}).items():
            for b in blist:
                btxt = b.get("belief", "").lower()
                for cstr in core:
                    if cstr and (cstr in btxt and b.get("tier") != "tier1"):
                        # found belief that appears to assert core identity; record and reduce
                        actions["core_violations"].append({"belief": b.get("belief"), "core": cstr})
                        # reduce confidence to prevent takeover
                        old = b.get("confidence", 0.5)
                        b["confidence"] = min(old, 0.5 * old)
                        b["flagged_core_conflict"] = datetime.now().isoformat()
                        self._log_evolution(f"Core identity protection: reduced confidence for belief '{b.get('belief')}'")
                        self.save()

        if actions["core_violations"]:
            self.add_identity_log(f"Core violations detected: {len(actions['core_violations'])}")

        return actions

    
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

    def detect_conflicts(self, category: str = None) -> List[Dict]:
        """Detect simple conflicts among beliefs.

        Heuristic: looks for negation pairs ("not", "don't", "never", "no", "doesn't")
        and identical subject overlap. Returns list of conflict records.
        """
        conflicts = []
        negations = ["not", "don't", "dont", "never", "no", "doesn't", "cannot", "can't"]

        categories = [category] if category else list(self.state["beliefs"].keys())
        for cat in categories:
            beliefs = self.state["beliefs"].get(cat, [])
            n = len(beliefs)
            for i in range(n):
                for j in range(i + 1, n):
                    a = beliefs[i]["belief"].lower()
                    b = beliefs[j]["belief"].lower()

                    # quick skip for identical beliefs
                    if a == b:
                        continue

                    # If one contains a negation and the other contains the same core words -> conflict
                    def has_neg(x):
                        return any(neg in x for neg in negations)

                    # measure simple overlap
                    a_words = set(w for w in re_split(a))
                    b_words = set(w for w in re_split(b))
                    shared = a_words.intersection(b_words)

                    if shared and (has_neg(a) and not has_neg(b) or has_neg(b) and not has_neg(a)):
                        conflicts.append({
                            "category": cat,
                            "a": beliefs[i],
                            "b": beliefs[j],
                            "shared_terms": list(shared),
                            "reason": "negation_conflict"
                        })

        return conflicts

    def handle_conflicts(self, reduce_factor: float = 0.7) -> List[Dict]:
        """Resolve detected conflicts conservatively by reducing confidence and logging.

        Returns list of applied conflict actions.
        """
        applied = []
        for conflict in self.detect_conflicts():
            a = conflict["a"]
            b = conflict["b"]
            # Reduce both confidences slightly
            a_old = a.get("confidence", 0.5)
            b_old = b.get("confidence", 0.5)
            a["confidence"] = max(0.0, a_old * reduce_factor)
            b["confidence"] = max(0.0, b_old * reduce_factor)
            a["contradicted"] = datetime.now().isoformat()
            b["contradicted"] = datetime.now().isoformat()
            self._log_evolution(f"Conflict resolved between '{a.get('belief')}' and '{b.get('belief')}' - confidences reduced")
            applied.append({
                "a": a.get("belief"),
                "b": b.get("belief"),
                "a_conf": a["confidence"],
                "b_conf": b["confidence"],
                "reason": conflict.get("reason"),
            })

        if applied:
            self.save()

        return applied


    
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

    # ========== TEMPORAL METRICS ==========

    def record_metric(self, name: str, value: float):
        """Record a timestamped metric for temporal self-awareness"""
        if name not in self.state.get("metrics_history", {}):
            self.state.setdefault("metrics_history", {})[name] = []

        entry = {"timestamp": datetime.now().isoformat(), "value": float(value)}
        self.state["metrics_history"][name].append(entry)

        # Keep last 100 entries per metric
        if len(self.state["metrics_history"][name]) > 100:
            self.state["metrics_history"][name] = self.state["metrics_history"][name][-100:]

        self._log_evolution(f"Metric recorded: {name} = {value}")
        self.save()

    def get_metric_trend(self, name: str, window: int = 5) -> Dict[str, float]:
        """Return simple trend info (delta, pct_change) over the last `window` samples."""
        series = self.state.get("metrics_history", {}).get(name, [])
        if not series:
            return {"delta": 0.0, "pct_change": 0.0, "samples": 0}

        recent = series[-window:]
        first = recent[0]["value"]
        last = recent[-1]["value"]
        delta = last - first
        pct = (delta / first) * 100.0 if first != 0 else 0.0
        return {"delta": round(delta, 4), "pct_change": round(pct, 2), "samples": len(recent)}

    def analyze_long_term_change(self, name: str) -> str:
        """Human-readable summary of long-term change for metric `name`."""
        series = self.state.get("metrics_history", {}).get(name, [])
        if len(series) < 2:
            return f"Not enough data for {name}."

        first = series[0]["value"]
        last = series[-1]["value"]
        pct = ((last - first) / first * 100.0) if first != 0 else 0.0
        return f"{name}: changed from {first:.2f} to {last:.2f} ({pct:.1f}% change) over {len(series)} samples."

    # ========== SELF NARRATIVE ==========

    def add_self_narrative(self, entry: str):
        """Append an internal narrative entry to the self-story."""
        item = {"timestamp": datetime.now().isoformat(), "entry": entry}
        self.state.setdefault("self_narrative", []).append(item)
        # Keep last 500 narrative entries
        if len(self.state["self_narrative"]) > 500:
            self.state["self_narrative"] = self.state["self_narrative"][-500:]
        self._log_evolution(f"Narrative entry added: {entry[:60]}")
        self.save()

    def get_self_narrative_summary(self, limit: int = 5) -> str:
        recent = self.state.get("self_narrative", [])[-limit:]
        return "\n".join([f"{r['timestamp']}: {r['entry']}" for r in recent])

    # ========== SELF-INITIATED EXPLORATION ==========

    def initiate_self_query(self, query: str):
        """Record a self-initiated exploration or question for later processing."""
        item = {"timestamp": datetime.now().isoformat(), "query": query, "status": "pending"}
        self.state.setdefault("self_explorations", []).append(item)
        self._log_evolution(f"Self-initiated query: {query}")
        self.save()
        return item
    
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


def re_split(s: str) -> List[str]:
    """Small helper to split on non-alphanumeric and remove short tokens."""
    import re
    toks = re.split(r"[^a-z0-9]+", s)
    return [t for t in toks if len(t) > 2]
