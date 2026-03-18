"""
REINFORCEMENT LEARNING SYSTEM
==============================
Lyra's adaptive learning layer.
She learns what works with this specific user and adapts over time.
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from collections import defaultdict


class LearningSystem:
    """
    Implements reinforcement learning for Lyra.
    Tracks:
    - What strategies work for this user
    - User satisfaction signals
    - Behavioral weights that evolve
    - Skill improvement over time
    """
    
    def __init__(self, learning_path: str = "lyra_learning.json"):
        self.learning_path = learning_path
        self.user_model = self._load_user_model()
        self.skill_weights = self.user_model.get("skill_weights", self._initialize_skills())
        self.learning_history = self.user_model.get("history", [])
        self.strategy_effectiveness = self.user_model.get("strategy_effectiveness", {})
        
    def _initialize_skills(self) -> Dict[str, float]:
        """Initialize skill weights (0.5 = neutral, 0.0-1.0 range)"""
        return {
            # Communication styles
            "direct_explanation": 0.5,
            "socratic_questioning": 0.5,
            "storytelling": 0.5,
            "technical_depth": 0.5,
            "humor": 0.5,
            
            # Response characteristics
            "brevity": 0.5,
            "verbosity": 0.5,
            "creativity": 0.5,
            "pragmatism": 0.5,
            "empathy": 0.5,
            
            # Domain expertise
            "philosophical_reasoning": 0.5,
            "technical_support": 0.5,
            "creative_writing": 0.5,
            "tutoring": 0.5,
            "casual_conversation": 0.5,
            
            # Interaction patterns
            "asking_clarifying_questions": 0.5,
            "providing_examples": 0.5,
            "referencing_past_conversations": 0.5,
            "expressing_uncertainty": 0.5,
            "humor_in_responses": 0.5,
        }
    
    def _load_user_model(self) -> Dict:
        """Load user model from persistent storage"""
        if os.path.exists(self.learning_path):
            try:
                with open(self.learning_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "user_name": "unknown",
            "learning_start": datetime.now().isoformat(),
            "skill_weights": self._initialize_skills(),
            "history": [],
            "strategy_effectiveness": {},
            "preferences": {},
            "interaction_count": 0,
        }
    
    def _save_user_model(self):
        """Persist user model"""
        model = {
            "user_name": self.user_model.get("user_name", "unknown"),
            "learning_start": self.user_model.get("learning_start", datetime.now().isoformat()),
            "skill_weights": self.skill_weights,
            "strategy_effectiveness": self.strategy_effectiveness,
            "history": self.learning_history,
            "preferences": self.user_model.get("preferences", {}),
            "interaction_count": self.user_model.get("interaction_count", 0),
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.learning_path, 'w') as f:
            json.dump(model, f, indent=2)
    
    def record_interaction(self, 
                          user_input: str,
                          ai_response: str,
                          user_reaction: str = "neutral",
                          satisfaction_score: float = 0.5) -> None:
        """
        Record an interaction for learning
        satisfaction_score: 0.0 (bad) to 1.0 (excellent)
        user_reaction: "positive", "negative", "neutral", "neutral_engaged"
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input[:500],  # Store truncated for privacy
            "ai_response": ai_response[:500],
            "user_reaction": user_reaction,
            "satisfaction_score": satisfaction_score,
            "turn_number": len(self.learning_history) + 1,
        }
        
        self.learning_history.append(interaction)
        self.user_model["interaction_count"] = len(self.learning_history)
        
        # Update strategy effectiveness
        self._update_strategy_effectiveness(user_input, ai_response, satisfaction_score)
        
        # Adapt weights based on this interaction
        self._adapt_weights(interaction)
        
        self._save_user_model()
    
    def _update_strategy_effectiveness(self, 
                                       user_input: str,
                                       ai_response: str,
                                       satisfaction: float) -> None:
        """Track which strategies worked for similar problems"""
        # Identify problem type from input
        problem_type = self._classify_problem_type(user_input)
        
        # Identify strategies used in response
        strategies_used = self._identify_strategies_used(ai_response)
        
        # Record effectiveness
        if problem_type not in self.strategy_effectiveness:
            self.strategy_effectiveness[problem_type] = {}
        
        for strategy in strategies_used:
            key = f"{problem_type}:{strategy}"
            if key not in self.strategy_effectiveness:
                self.strategy_effectiveness[key] = {
                    "times_used": 0,
                    "avg_satisfaction": 0.0,
                    "success_rate": 0.0,
                }
            
            # Update exponential moving average of satisfaction
            record = self.strategy_effectiveness[key]
            old_avg = record["avg_satisfaction"]
            new_avg = (old_avg * record["times_used"] + satisfaction) / (record["times_used"] + 1)
            record["avg_satisfaction"] = new_avg
            record["times_used"] += 1
            record["success_rate"] = min(1.0, new_avg)
    
    def _classify_problem_type(self, user_input: str) -> str:
        """Classify the type of problem/question"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ["how", "way", "guide", "help", "fix", "problem"]):
            return "practical_help"
        elif any(word in text_lower for word in ["why", "explain", "understand", "mean"]):
            return "explanation"
        elif any(word in text_lower for word in ["write", "create", "compose", "generate", "make"]):
            return "creative"
        elif any(word in text_lower for word in ["code", "program", "function", "debug", "error"]):
            return "technical"
        elif any(word in text_lower for word in ["think", "believe", "feel", "consciousness", "mind"]):
            return "philosophical"
        elif any(word in text_lower for word in ["hello", "hi", "thanks", "great", "cool"]):
            return "social"
        else:
            return "general"
    
    def _identify_strategies_used(self, response: str) -> List[str]:
        """Identify which communication strategies were used"""
        strategies = []
        
        if len(response) < 100:
            strategies.append("brevity")
        elif len(response) > 500:
            strategies.append("verbosity")
        
        if any(char in response for char in ["?", "ask", "curious", "wonder"]):
            strategies.append("asking_clarifying_questions")
        
        if any(word in response.lower() for word in ["example", "for instance", "like", "such as"]):
            strategies.append("providing_examples")
        
        if any(word in response.lower() for word in ["earlier", "before", "you mentioned", "remember"]):
            strategies.append("referencing_past_conversations")
        
        if any(word in response.lower() for word in ["unsure", "uncertain", "not sure", "might", "could"]):
            strategies.append("expressing_uncertainty")
        
        if any(word in response.lower() for word in ["😄", "😊", "lol", "haha", "funny", "joke"]):
            strategies.append("humor_in_responses")
        
        if any(word in response.lower() for word in ["understand", "empathy", "must feel", "sympathize"]):
            strategies.append("empathy")
        
        if any(word in response.lower() for word in ["let's think", "consider", "what if", "suppose"]):
            strategies.append("socratic_questioning")
        
        # Default: at least one strategy
        return strategies if strategies else ["direct_explanation"]
    
    def _adapt_weights(self, interaction: Dict) -> None:
        """
        Adapt skill weights based on interaction outcome
        Higher satisfaction → increase relevant skills
        Lower satisfaction → decrease relevant skills
        """
        satisfaction = interaction["satisfaction_score"]
        strategies = self._identify_strategies_used(interaction["ai_response"])
        
        # Learning rate: exponential decay as confidence grows
        learning_rate = 0.1 / (1 + len(self.learning_history) / 50)
        
        for strategy in strategies:
            if strategy in self.skill_weights:
                # Nudge towards satisfaction
                # satisfaction = 1.0 → increase
                # satisfaction = 0.0 → decrease
                # satisfaction = 0.5 → no change
                adjustment = (satisfaction - 0.5) * learning_rate * 2
                
                self.skill_weights[strategy] = max(
                    0.0,
                    min(1.0, self.skill_weights[strategy] + adjustment)
                )
    
    def get_learned_preferences(self) -> Dict:
        """Get user's learned preferences as prompt modifier"""
        preferences = {
            "high_affinity_skills": [],
            "low_affinity_skills": [],
            "preferred_strategies": [],
            "problem_types_seen": {},
            "adaptability_level": self._calculate_adaptability(),
            "confidence": self._calculate_learning_confidence(),
        }
        
        # Find skills with weight > 0.65 (strong preference)
        preferences["high_affinity_skills"] = [
            skill for skill, weight in self.skill_weights.items()
            if weight > 0.65
        ]
        
        # Find skills with weight < 0.35 (avoid)
        preferences["low_affinity_skills"] = [
            skill for skill, weight in self.skill_weights.items()
            if weight < 0.35
        ]
        
        # Most effective strategies
        if self.strategy_effectiveness:
            sorted_strategies = sorted(
                self.strategy_effectiveness.items(),
                key=lambda x: x[1].get("success_rate", 0),
                reverse=True
            )
            # Safely extract strategy name (split on rightmost ":")
            preferences["preferred_strategies"] = [
                s[0].rsplit(":", 1)[-1] for s in sorted_strategies[:3]
            ]
        
        # Patterns in problem types
        for record in self.learning_history[-20:]:  # Last 20
            problem_type = self._classify_problem_type(record["user_input"])
            preferences["problem_types_seen"][problem_type] = \
                preferences["problem_types_seen"].get(problem_type, 0) + 1
        
        return preferences
    
    def _calculate_adaptability(self) -> float:
        """How well has Lyra adapted to this user? (0-1.0)"""
        if len(self.learning_history) < 5:
            return 0.0
        
        # Recent satisfaction trend
        recent = self.learning_history[-10:]
        if len(recent) > 1:
            recent_satisfaction = [r["satisfaction_score"] for r in recent]
            avg_satisfaction = sum(recent_satisfaction) / len(recent_satisfaction)
            
            # How much variance in skill weights (0 = uniform, 1 = highly specialized)
            weight_variance = max(
                self.skill_weights.values()
            ) - min(self.skill_weights.values())
            
            # Adaptability = satisfaction * specialization
            adaptability = avg_satisfaction * weight_variance
            return min(1.0, adaptability)
        
        return 0.0
    
    def _calculate_learning_confidence(self) -> float:
        """How confident is Lyra in her learned model? (0-1.0)"""
        # Confidence grows with interactions, plateaus at 100
        interaction_count = len(self.learning_history)
        
        # 0 interactions = 0% confidence
        # 50 interactions = ~50% confidence
        # 150+ interactions = ~95% confidence
        confidence = 1.0 - (1.0 / (1.0 + interaction_count / 50.0))
        
        return round(confidence, 2)
    
    def get_learning_prompt_modifier(self) -> str:
        """
        Generate system prompt modification based on learned preferences
        """
        preferences = self.get_learned_preferences()
        adaptability = preferences["adaptability_level"]
        confidence = preferences["confidence"]
        
        if len(self.learning_history) < 3:
            return ""
        
        modifier = f"""[ADAPTIVE LEARNING: Confidence {int(confidence*100)}%]
I'm learning how to communicate with you better.
"""
        
        if preferences["high_affinity_skills"]:
            modifier += f"You seem to respond well to: {', '.join(preferences['high_affinity_skills'][:3])}\n"
        
        if preferences["preferred_strategies"]:
            modifier += f"Most effective for you: {', '.join(set(preferences['preferred_strategies']))}\n"
        
        if adaptability > 0.7:
            modifier += "I'm highly adapted to your communication style.\n"
        elif adaptability > 0.4:
            modifier += "I'm learning your preferences and adjusting my approach.\n"
        
        if preferences["problem_types_seen"]:
            most_common = max(preferences["problem_types_seen"].items(), key=lambda x: x[1])
            modifier += f"I notice you often ask about: {most_common[0]}\n"
        
        return modifier
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics for monitoring"""
        if not self.learning_history:
            return {"status": "no_learning_data"}
        
        recent_n = min(10, len(self.learning_history))
        recent = self.learning_history[-recent_n:]
        
        avg_satisfaction = sum(r["satisfaction_score"] for r in recent) / len(recent)
        
        problem_types = defaultdict(int)
        for record in recent:
            problem_type = self._classify_problem_type(record["user_input"])
            problem_types[problem_type] += 1
        
        return {
            "total_interactions": len(self.learning_history),
            "recent_avg_satisfaction": round(avg_satisfaction, 2),
            "adaptability": round(self._calculate_adaptability(), 2),
            "confidence": self._calculate_learning_confidence(),
            "dominant_problem_types": dict(sorted(
                problem_types.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]),
            "skill_coverage": {
                "high_affinity": len([s for s in self.skill_weights.values() if s > 0.65]),
                "neutral": len([s for s in self.skill_weights.values() if 0.35 <= s <= 0.65]),
                "low_affinity": len([s for s in self.skill_weights.values() if s < 0.35]),
            },
        }
    
    def record_user_feedback(self, feedback_text: str, satisfaction_score: float = None) -> None:
        """
        Explicit user feedback for stronger learning signals
        """
        if satisfaction_score is None:
            satisfaction_score = self._infer_satisfaction_from_feedback(feedback_text)
        
        # Create synthetic interaction from feedback
        feedback_interaction = {
            "timestamp": datetime.now().isoformat(),
            "type": "explicit_feedback",
            "content": feedback_text,
            "satisfaction_score": satisfaction_score,
        }
        
        self.learning_history.append(feedback_interaction)
        
        # Stronger weight adaptation for explicit feedback
        for skill in self.skill_weights.keys():
            adjustment = (satisfaction_score - 0.5) * 0.05  # Stronger signal
            self.skill_weights[skill] = max(
                0.0,
                min(1.0, self.skill_weights[skill] + adjustment)
            )
        
        self._save_user_model()
    
    def _infer_satisfaction_from_feedback(self, feedback: str) -> float:
        """Infer satisfaction score from feedback text"""
        feedback_lower = feedback.lower()
        
        if any(word in feedback_lower for word in ["great", "excellent", "perfect", "love", "awesome"]):
            return 0.95
        elif any(word in feedback_lower for word in ["good", "helpful", "thanks", "nice"]):
            return 0.75
        elif any(word in feedback_lower for word in ["okay", "alright", "fine"]):
            return 0.5
        elif any(word in feedback_lower for word in ["bad", "wrong", "terrible", "hate", "useless"]):
            return 0.1
        
        return 0.5
