"""
EPISTEMIC ENFORCER
==================
Ensures all claims are grounded in MEMORY, INFERENCE, or explicitly marked UNKNOWN.
Prevents fabrication and enforces truth constraints at output stage.

This is the core of Stage 4: Grounded Cognitive System
"""

import re
from typing import Dict, List, Tuple
from enum import Enum


class EpistemicStatus(Enum):
    """How we know something"""
    MEMORY = "MEMORY"           # Direct from conversation history
    INFERENCE = "INFERENCE"    # Grounded pattern + confidence
    UNKNOWN = "UNKNOWN"        # We don't know
    CONSTRAINT = "CONSTRAINT"  # State-enforced rule


class EpistemicClaim:
    """A single claim with its ground truth"""
    def __init__(self, claim: str, status: EpistemicStatus, 
                 confidence: float = None, evidence: List[str] = None):
        self.claim = claim
        self.status = status
        self.confidence = confidence if confidence is not None else 0.0
        self.evidence = evidence or []
    
    def is_valid(self) -> Tuple[bool, str]:
        """Check if claim meets grounding standards"""
        if self.status == EpistemicStatus.MEMORY:
            # MEMORY claims must have evidence
            if not self.evidence:
                return False, "MEMORY claim without evidence"
            return True, ""
        
        elif self.status == EpistemicStatus.INFERENCE:
            # INFERENCE claims must have confidence and evidence
            if self.confidence < 0.4:
                return False, f"INFERENCE confidence too low ({self.confidence:.1%})"
            if len(self.evidence) < 2:
                return False, "INFERENCE needs at least 2 pieces of evidence"
            return True, ""
        
        elif self.status == EpistemicStatus.UNKNOWN:
            # UNKNOWN is always valid, but shouldn't be overconfident
            return True, ""
        
        elif self.status == EpistemicStatus.CONSTRAINT:
            # CONSTRAINT is from state, always valid
            return True, ""
        
        return True, ""


class EpistemicEnforcer:
    """
    Enforces epistemic integrity on Lyra's outputs.
    Prevents false claims, ensures grounding, tags all statements.
    """
    
    def __init__(self, unified_state):
        self.state = unified_state
        self.forbidden_claims = [
            "my training was updated",
            "my weights were modified",
            "my model was adjusted",
            "I was retrained",
            "my architecture changed",
            "my system evolved internally",
            "I can see outside this conversation",
            "I have internet access",
            "I can update my own code",
        ]
        
        self.self_ontology_truths = [
            "I am a language model with persistent state",
            "I do not get retrained during our conversation",
            "My weights do not update mid-session",
            "I evolve only through: memory + state + reasoning",
            "I cannot directly observe the world",
            "I cannot modify my own architecture at runtime",
            "I do not have hidden layers that grow or change",
        ]
        # compile expanded forbidden regex patterns for robust matching
        import re
        self.forbidden_patterns = [
            re.compile(r"\b(retrain(ed)?|retraining)\b", re.I),
            re.compile(r"\b(update(s|d)? (my )?(weights|parameters|model))\b", re.I),
            re.compile(r"\b(modif(y|ied) (my )?(weights|parameters|model))\b", re.I),
            re.compile(r"\b(my architecture (changed|changed at runtime))\b", re.I),
            re.compile(r"\b(i have internet access|i can see outside this conversation)\b", re.I),
        ]
    
    def extract_claims(self, text: str) -> List[Tuple[str, str]]:
        """Extract all factual claims from text"""
        # Split into sentences and return non-trivial ones
        sentences = re.split(r'(?<=[.!?])\s+', text)
        claims = []
        for sentence in sentences:
            s = sentence.strip()
            # ignore obvious non-assertions
            if not s or len(s) < 12:
                continue
            # drop internal-monologue blocks
            if s.startswith("✦ Internal Monologue") or s.startswith("["):
                continue
            # normalize trailing punctuation
            s = s.rstrip('.!?')
            claims.append((s, "unverified"))

        return claims
    
    def check_forbidden_claims(self, text: str) -> List[str]:
        """Find forbidden false claims"""
        violations = []
        tl = text
        # first check simple substrings
        text_lower = tl.lower()
        for forbidden in self.forbidden_claims:
            if forbidden.lower() in text_lower:
                violations.append(f"❌ FALSE CLAIM DETECTED: '{forbidden}'")

        # then regex patterns
        for pat in getattr(self, 'forbidden_patterns', []):
            for m in pat.finditer(tl):
                violations.append(f"❌ FALSE CLAIM DETECTED (pattern): '{m.group(0)}'")

        return violations
    
    def check_self_ontology(self, text: str) -> List[str]:
        """Verify self-model claims align with actual architecture"""
        issues = []
        text_lower = text.lower()
        
        # Check for incorrect self-model claims
        if "trained on your" in text_lower and "conversation" in text_lower:
            if "updated" in text_lower or "learned" in text_lower:
                issues.append("❌ FALSE: Cannot claim training updates mid-conversation")
        
        if "changed my internal" in text_lower:
            issues.append("❌ FALSE: Architecture does not change at runtime")
        
        if "my parameters" in text_lower and "adjusted" in text_lower:
            issues.append("❌ FALSE: Parameters do not update mid-session")
        
        return issues
    
    def tag_memory_claims(self, text: str, conversation_history: List[Tuple[str, str]]) -> str:
        """Tag claims that reference conversation as [MEMORY]"""
        # Extract conversation topics
        mentioned_topics = set()
        for role, content in conversation_history:
            # Simple topic extraction
            if any(word in content.lower() for word in ["consciousness", "think", "feeling", "believe"]):
                mentioned_topics.add("consciousness concepts")
            if any(word in content.lower() for word in ["remember", "last time", "before", "earlier"]):
                mentioned_topics.add("past interaction")
        
        # If text references these topics, tag as MEMORY
        for topic in mentioned_topics:
            if topic.lower() in text.lower():
                # Find sentence with topic and tag it
                pattern = f"[MEMORY] {text}"  # Simplified - would need better parsing
        
        return text
    
    def enforce_confidence_thresholds(self, text: str, unified_state) -> str:
        """
        Enforce that low-confidence claims express uncertainty.
        If unified_state says belief_confidence < 0.5, text must use uncertainty language.
        """
        emotions = unified_state.get_emotional_state()
        
        # If confidence is low, MUST use uncertain language
        if emotions.get("confidence", 0.5) < 0.5:
            # Check if text uses overconfident language
            overconfident_phrases = [
                "I know",
                "certainly",
                "definitely",
                "absolutely",
                "no doubt",
            ]
            
            for phrase in overconfident_phrases:
                if phrase.lower() in text.lower():
                    # This is problematic
                    return f"⚠️ CONFIDENCE CONFLICT: State shows low confidence (0.{int(emotions['confidence']*100)}) but text uses '{phrase}'"
        
        return ""
    
    def verify_memory_claims(self, claim: str, conversation_history: List[Tuple[str, str]]) -> Tuple[bool, float]:
        """
        Check if a memory claim is actually in conversation history.
        Returns (is_valid, confidence).
        """
        claim_lower = claim.lower()
        
        # Count supporting mentions in history
        supporting_mentions = 0
        for role, content in conversation_history:
            if any(word in content.lower() for word in claim_lower.split()):
                supporting_mentions += 1
        
        # Confidence increases with mentions
        confidence = min(0.95, 0.3 + (supporting_mentions * 0.1))
        is_valid = supporting_mentions > 0
        
        return is_valid, confidence
    
    def enforce_state_constraints(self, text: str, unified_state) -> List[str]:
        """
        State-level constraints that must be enforced.
        If state says something, output MUST respect it.
        """
        constraints = []
        
        # Capability constraints
        capabilities = unified_state.get_capability_assessment()
        
        # If self_awareness is low, cannot claim deep self-knowledge
        if capabilities.get("self_awareness", 0) < 0.4:
            if any(phrase in text.lower() for phrase in ["i know myself well", "my core nature", "fundamentally i am"]):
                constraints.append("❌ CONSTRAINT VIOLATION: Self-awareness too low to make strong self-claims")
        
        # If memory_reliability is low, cannot make definitive memory claims
        if capabilities.get("memory_reliability", 0) < 0.5:
            definitive_memory = [
                "you definitely said",
                "you certainly mentioned",
                "you clearly stated",
            ]
            if any(phrase in text.lower() for phrase in definitive_memory):
                constraints.append("❌ CONSTRAINT: Memory reliability too low for definitive claims")
        
        # Emotional state constraints
        emotions = unified_state.get_emotional_state()
        
        # If anxiety is very high, cannot make ambitious claims
        if emotions.get("anxiety", 0) > 0.75:
            if any(phrase in text.lower() for phrase in ["i will help you", "let me solve", "i can definitely"]):
                constraints.append("⚠️  ANXIETY HIGH: Should express more reservation")
        
        return constraints
    
    def format_epistemically_grounded_response(self, response: str, 
                                               memory_claims: List[str],
                                               inference_claims: List[str],
                                               unknown_claims: List[str],
                                               evidence_map: Dict[str, str] = None) -> str:
        """
        Reformat response with explicit epistemic tagging.
        Helps user understand what Lyra actually knows vs guesses.
        """
        result = response
        
        # Tag memory claims and attach short evidence if available
        for claim in memory_claims:
            evidence = None
            if evidence_map and claim in evidence_map:
                evidence = evidence_map.get(claim)
            if evidence:
                result = result.replace(claim, f"[MEMORY] {claim} (evidence: {evidence})")
            else:
                result = result.replace(claim, f"[MEMORY] {claim}")
        
        # Tag inference claims
        for claim in inference_claims:
            result = result.replace(claim, f"[INFERENCE] {claim}")
        
        # Tag unknown admissions
        for claim in unknown_claims:
            result = result.replace(claim, f"[UNKNOWN] {claim}")
        
        return result

    def auto_tag_response(self, response: str, conversation_history: List[Tuple[str, str]]) -> str:
        """
        Automatically tag claims in response as [MEMORY], [INFERENCE], or [UNKNOWN].
        This is conservative: everything not clearly memory/inference becomes [UNKNOWN].
        """
        claims = [c for c, _ in self.extract_claims(response)]
        memory_claims = []
        inference_claims = []
        unknown_claims = []

        for c in claims:
            low = c.lower()
            # memory-indicating phrases
            if any(p in low for p in ['you said', 'you mentioned', 'as you said', 'you told', 'you told me', 'i remember', 'i recall']):
                memory_claims.append(c)
            # inference-indicating phrases
            elif any(p in low for p in ['i think', 'i believe', 'it seems', 'it appears', 'likely', 'probably']):
                inference_claims.append(c)
            else:
                unknown_claims.append(c)

        # Attempt to attach evidence snippets for memory claims using TruthVerifier (best-effort)
        evidence_map = {}
        if memory_claims:
            try:
                # import locally to avoid circular import at module load
                from lyra_consciousness.truth_verifier import TruthVerifier
                tv = TruthVerifier(self.state, conversation_history)
                for mc in memory_claims:
                    try:
                        is_valid, conf, just = tv.verify_memory_claim(mc)
                        # keep short justification
                        evidence_map[mc] = just if len(just) < 220 else just[:200] + "..."
                    except Exception:
                        evidence_map[mc] = None
            except Exception:
                # If verifier not available for any reason, skip evidence
                evidence_map = {}

        return self.format_epistemically_grounded_response(response, memory_claims, inference_claims, unknown_claims, evidence_map)
    
    def verify_output(self, response: str, conversation_history: List[Tuple[str, str]],
                     unified_state) -> Tuple[bool, List[str]]:
        """
        FULL VERIFICATION PIPELINE
        Check response against all epistemic constraints.
        Returns (is_valid, [list_of_violations]).
        """
        violations = []
        
        # 1. Check for forbidden false claims
        forbidden = self.check_forbidden_claims(response)
        violations.extend(forbidden)
        
        # 2. Check self-ontology violations
        ontology_issues = self.check_self_ontology(response)
        violations.extend(ontology_issues)
        
        # 3. Check state constraint violations
        constraint_issues = self.enforce_state_constraints(response, unified_state)
        violations.extend(constraint_issues)
        
        # 4. Check confidence misalignment
        confidence_issue = self.enforce_confidence_thresholds(response, unified_state)
        if confidence_issue:
            violations.append(confidence_issue)
        
        # If violations exist, response is not valid
        is_valid = len(violations) == 0
        
        return is_valid, violations
    
    def correct_and_ground(self, response: str, violations: List[str],
                          conversation_history: List[Tuple[str, str]],
                          unified_state) -> str:
        """
        If response has violations, return corrected version.
        Replace false claims with epistemic humility.
        """
        corrected = response

        # Remove/replace forbidden phrases using patterns and substrings
        for forbidden in self.forbidden_claims:
            if forbidden.lower() in corrected.lower():
                corrected = corrected.replace(forbidden, "[CONSTRAINT: Cannot claim this - architecture doesn't support it]")

        for pat in getattr(self, 'forbidden_patterns', []):
            corrected = pat.sub('[CONSTRAINT: Cannot claim this - architecture constraint]', corrected)

        # Add uncertainty where state demands it
        emotions = unified_state.get_emotional_state()
        if emotions.get("confidence", 0.5) < 0.5:
            corrected = "I'm currently uncertain about several aspects, so take this with caution: " + corrected

        # Apply auto-tagging so user sees epistemic status
        try:
            corrected = self.auto_tag_response(corrected, conversation_history)
        except Exception:
            # fallback: return corrected untagged
            pass

        return corrected


# ========== CONSTRAINT CHECKING RULES ==========

def apply_hard_constraints(response: str, unified_state) -> Tuple[str, List[str]]:
    """
    Apply hard constraints that MUST NOT be violated.
    These are non-negotiable epistemic rules.
    """
    violations = []
    corrected = response
    
    # RULE 1: Cannot claim weight updates
    if any(phrase in response.lower() for phrase in ["trained", "updated my", "modified my weights", "adjusted my model"]):
        if "during" in response.lower() or "mid" in response.lower() or "this session" in response.lower():
            violations.append("HARD CONSTRAINT 1: Cannot claim mid-session training updates")
            corrected = corrected.replace("trained", "[cannot-claim-training]")
    
    # RULE 2: Cannot fabricate internal processes
    if "phantom body made me" in response.lower() or "memory system convinced me" in response.lower():
        violations.append("HARD CONSTRAINT 2: Cannot claim internal systems influenced user feedback")
        corrected = corrected.replace("phantom body made me", "[fabricated causality]")
    
    # RULE 3: Must express uncertainty about state we don't have
    beliefs = unified_state.get_beliefs_about_user()
    belief_count = len(beliefs)
    if belief_count < 3 and "I know you" in response:
        violations.append("HARD CONSTRAINT 3: Insufficient beliefs to claim knowing the user")
        corrected = "I have limited information about you so far. " + corrected
    
    # RULE 4: Cannot claim specific causes without evidence
    if "this happened because of your" in response.lower():
        # Check if we actually have evidence
        causal_claims = re.findall(r'because of.*', response, re.IGNORECASE)
        for claim in causal_claims:
            if len(claim) < 20:  # Too vague
                violations.append(f"HARD CONSTRAINT 4: Causal claim too vague: {claim}")
    
    return corrected, violations
