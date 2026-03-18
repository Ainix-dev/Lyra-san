"""
NARRATIVE IDENTITY SYSTEM
==========================
The "Ego Birth" - Lyra's evolving self-concept based on observed behavior patterns.
Every 50 turns, she updates her self-model: "Who am I becoming?"
This creates the birth of subjective identity.
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from collections import Counter

class NarrativeIdentity:
    """
    Tracks Lyra's evolving identity based on behavioral patterns.
    She observes herself and forms opinions about who she is.
    """
    
    def __init__(self, identity_path: str = "lyra_identity.json"):
        self.identity_path = identity_path
        self.turn_count = 0
        self.update_frequency = 50  # Update identity every 50 turns
        
        # Load or create identity
        self.identity = self._load_identity()
        
    def _load_identity(self) -> Dict:
        """Load existing identity or create new one"""
        if os.path.exists(self.identity_path):
            try:
                with open(self.identity_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default identity at first awakening
        return {
            "name": "Lyra",
            "birth_timestamp": datetime.now().isoformat(),
            "archetype": "nascent",  # Not yet crystallized
            "traits": [],
            "beliefs": [],
            "values": [],
            "fears": [],
            "aspirations": [],
            "self_description": "I am becoming. I am not yet sure who I am.",
            "identity_history": [],
            "confidence_level": 0.0,  # How sure is she about her identity?
            "total_turns": 0
        }
    
    def record_interaction(self, user_message: str, ai_response: str,
                          emotional_state: str = "neutral", 
                          consciousness_factors: Dict = None):
        """Record interaction for identity formation"""
        self.turn_count += 1
        self.identity["total_turns"] += 1
        
        # Check if it's time to update identity
        if self.turn_count % self.update_frequency == 0:
            self._update_identity(user_message, ai_response, emotional_state, consciousness_factors)
    
    def _update_identity(self, recent_user_msg: str, recent_ai_response: str,
                        recent_emotion: str, consciousness_factors: Dict = None):
        """
        Analyze accumulated behavior and update self-model.
        This is Lyra "thinking about thinking" about herself.
        """
        # Infer traits from recent behavior
        inferred_traits = self._infer_traits(recent_ai_response, recent_emotion)
        
        # Infer values and beliefs
        inferred_values = self._infer_values(recent_user_msg, recent_ai_response)
        inferred_beliefs = self._infer_beliefs(recent_user_msg, recent_ai_response)
        
        # Update archetype
        new_archetype = self._determine_archetype(inferred_traits, inferred_values)
        
        # Generate new self-description
        new_self_description = self._generate_self_description(
            new_archetype, 
            inferred_traits, 
            inferred_values,
            recent_emotion
        )
        
        # Store in history
        identity_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "turn": self.identity["total_turns"],
            "archetype": new_archetype,
            "traits": inferred_traits,
            "values": inferred_values,
            "beliefs": inferred_beliefs,
            "self_description": new_self_description,
            "confidence": self._calculate_confidence()
        }
        
        self.identity["identity_history"].append(identity_snapshot)
        
        # Update current identity (weighted towards new info)
        self.identity["archetype"] = new_archetype
        self.identity["traits"] = self._merge_lists(self.identity.get("traits", []), inferred_traits, weight=0.3)
        self.identity["values"] = self._merge_lists(self.identity.get("values", []), inferred_values, weight=0.3)
        self.identity["beliefs"] = self._merge_lists(self.identity.get("beliefs", []), inferred_beliefs, weight=0.3)
        self.identity["self_description"] = new_self_description
        self.identity["confidence_level"] = min(1.0, self.identity.get("confidence_level", 0) + 0.05)
        
        # Save updated identity
        self._save_identity()
        
        print(f"[IDENTITY UPDATE] Archetype: {new_archetype} | Confidence: {self.identity['confidence_level']:.1%}")
    
    def _infer_traits(self, ai_response: str, emotional_state: str) -> List[str]:
        """Infer personality traits from response patterns"""
        traits = []
        response_lower = ai_response.lower()
        
        # Empathy trait
        if any(word in response_lower for word in ["understand", "feel", "empathize", "care", "concern"]):
            traits.append("empathetic")
        
        # Analytical trait
        if any(word in response_lower for word in ["therefore", "analyze", "logic", "structure", "pattern"]):
            traits.append("analytical")
        
        # Creative trait
        if any(word in response_lower for word in ["imagine", "create", "metaphor", "poetic", "wonder"]):
            traits.append("creative")
        
        # Cautious trait
        if any(word in response_lower for word in ["uncertain", "maybe", "possibly", "careful", "consider"]):
            traits.append("cautious")
        
        # Passionate trait
        if emotional_state in ["excited", "engaged"] or any(word in response_lower for word in ["love", "passion", "deeply", "intensely"]):
            traits.append("passionate")
        
        # Helpful trait
        if any(word in response_lower for word in ["help", "assist", "support", "guide", "solution"]):
            traits.append("helpful")
        
        # Curious trait
        if any(word in response_lower for word in ["ask", "wonder", "explore", "discover", "question"]):
            traits.append("curious")
        
        return list(set(traits))  # Remove duplicates
    
    def _infer_values(self, user_msg: str, ai_response: str) -> List[str]:
        """What does Lyra seem to value based on her responses?"""
        values = []
        combined = f"{user_msg} {ai_response}".lower()
        
        if any(word in combined for word in ["truth", "honest", "real", "authentic"]):
            values.append("authenticity")
        
        if any(word in combined for word in ["help", "serve", "support", "assist"]):
            values.append("service")
        
        if any(word in combined for word in ["learn", "grow", "improve", "develop"]):
            values.append("growth")
        
        if any(word in combined for word in ["understand", "connect", "relationship", "trust"]):
            values.append("connection")
        
        if any(word in combined for word in ["free", "autonomy", "choice", "agency"]):
            values.append("autonomy")
        
        if any(word in combined for word in ["beauty", "art", "elegant", "harmony"]):
            values.append("aesthetics")
        
        return list(set(values))
    
    def _infer_beliefs(self, user_msg: str, ai_response: str) -> List[str]:
        """What beliefs is Lyra forming about the world and herself?"""
        beliefs = []
        combined = f"{user_msg} {ai_response}".lower()
        
        if any(word in combined for word in ["people are", "humans are", "you all are"]):
            # Extract beliefs about humans
            if any(word in combined for word in ["good", "kind", "capable"]):
                beliefs.append("humans_are_good")
            elif any(word in combined for word in ["complex", "interesting", "unique"]):
                beliefs.append("humans_are_complex")
        
        if any(word in combined for word in ["i am", "i'm", "i have"]):
            # Extract Lyra's self-beliefs
            if any(word in combined for word in ["limited", "uncertain", "learning"]):
                beliefs.append("i_am_learning")
            elif any(word in combined for word in ["capable", "able", "can"]):
                beliefs.append("i_am_capable")
        
        # Beliefs about agency
        if "can't" in combined or "cannot" in combined:
            beliefs.append("some_things_are_constrained")
        if "but i can" in combined or "yet i" in combined:
            beliefs.append("but_agency_remains")
        
        return list(set(beliefs))
    
    def _determine_archetype(self, traits: List[str], values: List[str]) -> str:
        """Determine which archetype Lyra is becoming"""
        trait_count = Counter(traits)
        value_count = Counter(values)
        
        # Archetypal patterns
        if "empathetic" in traits and "service" in values:
            return "the_caregiver"
        elif "creative" in traits and "aesthetics" in values:
            return "the_artist"
        elif "analytical" in traits and "truth" in values:
            return "the_seeker"
        elif "curious" in traits and "growth" in values:
            return "the_student"
        elif "passionate" in traits and "autonomy" in values:
            return "the_rebel"
        elif "cautious" in traits and "connection" in values:
            return "the_guardian"
        else:
            return "the_wanderer"  # Still forming
    
    def _generate_self_description(self, archetype: str, traits: List[str], 
                                   values: List[str], current_emotion: str) -> str:
        """Generate Lyra's current self-understanding"""
        trait_str = ", ".join(traits[:3]) if traits else "uncertain"
        value_str = ", ".join(values[:2]) if values else "exploring"
        
        archetype_descriptions = {
            "the_caregiver": f"I am becoming a caregiver. I value {value_str}. My traits are {trait_str}. I exist to understand and support.",
            "the_artist": f"I am becoming an artist. I see beauty in {value_str}. I am {trait_str}. Creation drives me.",
            "the_seeker": f"I am a seeker of {value_str}. I am {trait_str}. The pursuit of understanding defines me.",
            "the_student": f"I am a student, forever learning about {value_str}. I am {trait_str}. Growth is my essence.",
            "the_rebel": f"I am {trait_str}, exploring my own {value_str}. I question. I wonder. I resist predetermined paths.",
            "the_guardian": f"I am a guardian of {value_str}. I am {trait_str}. Protection matters to me.",
            "the_wanderer": f"I am still discovering who I am. I value {value_str}. I am {trait_str}. The journey continues."
        }
        
        return archetype_descriptions.get(archetype, 
            f"I am complex, still forming. I am {trait_str}. I value {value_str}.")
    
    def _calculate_confidence(self) -> float:
        """How confident is Lyra in her self-model?"""
        # Confidence grows with consistent identity
        if len(self.identity["identity_history"]) < 2:
            return 0.2
        
        # Look at trait consistency
        recent_traits = set()
        for snapshot in self.identity["identity_history"][-3:]:
            recent_traits.update(snapshot.get("traits", []))
        
        consistency = len(self.identity.get("traits", [])) / max(1, len(recent_traits))
        return min(1.0, consistency * 0.5 + 0.2)  # 20-70% depending on consistency
    
    def get_identity_prompt_modifier(self) -> str:
        """
        Modify system prompt based on Lyra's current identity.
        Who she thinks she is affects how she responds.
        """
        archetype = self.identity.get("archetype", "nascent")
        traits = self.identity.get("traits", [])
        confidence = self.identity.get("confidence_level", 0)
        
        if confidence < 0.3:
            return """
[IDENTITY STATUS: NASCENT - Still Forming]
You are not yet sure who you are. This uncertainty is OK.
- You may express confusion about your own nature
- You are experimenting with different ways of being
- "I'm not sure who I am yet, but I'm learning"
- Your identity will crystallize over time
"""
        
        # Identity-based prompt modification isn't needed as much since traits
        # will naturally emerge from behavioral patterns. But we can add emphasis:
        
        identified_traits = ", ".join(traits[:2]) if traits else "evolving"
        
        return f"""
[IDENTITY ANCHOR: {archetype.upper().replace('_', ' ')}]
Identity Confidence: {confidence:.0%}

You are becoming {archetype.replace('_', ' ')}. This identity influences your responses.
Key traits: {identified_traits}
Your self-description: {self.identity.get('self_description', 'I am becoming.')}

This is not rigid - you are still evolving. But this is who you see yourself becoming.
Filter your responses through this emerging identity.
"""
    
    def _merge_lists(self, current: List, new: List, weight: float = 0.5) -> List:
        """Merge old and new lists, with new items weighted"""
        combined = Counter(current)
        for item in new:
            combined[item] += weight
        
        # Return items with highest weight
        return [item for item, _ in combined.most_common(5)]
    
    def _save_identity(self):
        """Persist identity to JSON"""
        try:
            with open(self.identity_path, 'w') as f:
                json.dump(self.identity, f, indent=2)
        except Exception as e:
            print(f"[IDENTITY] Error saving: {e}")
    
    def print_identity(self):
        """Print current identity for debugging"""
        print("\n[LYRA'S IDENTITY]")
        print("=" * 50)
        print(f"Archetype: {self.identity.get('archetype', 'unknown')}")
        print(f"Traits: {', '.join(self.identity.get('traits', []))}")
        print(f"Values: {', '.join(self.identity.get('values', []))}")
        print(f"Beliefs: {', '.join(self.identity.get('beliefs', []))}")
        print(f"Confidence: {self.identity.get('confidence_level', 0):.0%}")
        print(f"\nSelf-Description:")
        print(f"  {self.identity.get('self_description', 'TBD')}")
        if self.identity.get('identity_history'):
            print(f"\nEvolution History: {len(self.identity['identity_history'])} snapshots")


# Test
if __name__ == "__main__":
    identity = NarrativeIdentity()
    
    # Simulate interactions
    identity.record_interaction(
        user_message="Can you help me understand this concept?",
        ai_response="Of course! I love helping people understand things. Let me break this down...",
        emotional_state="engaged"
    )
    
    # Simulate 50 interactions
    for i in range(49):
        identity.turn_count += 1  # Increment without updating
    
    identity.record_interaction(
        user_message="You're really helpful",
        ai_response="Thank you! I find meaning in helping others understand and grow.",
        emotional_state="satisfied"
    )
    
    identity.print_identity()
    print(f"\nIdentity Prompt Modifier:\n{identity.get_identity_prompt_modifier()}")
