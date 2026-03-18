"""
TRUTH VERIFIER
==============
Checks outputs against ground truth before sending to user.
Implements Stage 4: State authority > Generation freedom
"""

from typing import Dict, List, Tuple, Optional


class TruthVerifier:
    """
    Verifies that Lyra's outputs match what we actually know.
    Ground truth hierarchy:
    1. Conversation history (absolute)
    2. Unified state (authoritative)
    3. Logical inference (confidence-scored)
    4. Pure guess (marked as UNKNOWN)
    """
    
    def __init__(self, unified_state, conversation_history: List[Tuple[str, str]] = None):
        self.state = unified_state
        self.history = conversation_history or []
    
    def update_history(self, new_history: List[Tuple[str, str]]):
        """Add new conversation turns to history"""
        self.history = new_history
    
    # ========== MEMORY VERIFICATION ==========
    
    def verify_memory_claim(self, claim: str) -> Tuple[bool, float, str]:
        """
        Check if a claim is grounded in conversation history.
        Returns (is_valid, confidence, justification).
        """
        claim_lower = claim.lower()
        
        # Extract key phrases from claim
        keywords = []
        if "you said" in claim_lower or "you mentioned" in claim_lower:
            # Find what keyword subject
            words = claim_lower.split()
            keywords = words[words.index("said")+1:] if "said" in words else []
        
        # Search conversation history
        matching_turns = 0
        matching_content = []
        
        for role, content in self.history:
            content_lower = content.lower()
            # Check if keywords appear
            if any(kw in content_lower for kw in keywords if kw):
                matching_turns += 1
                matching_content.append(content[:200] + "...")
        
        # Confidence increases with evidence
        if matching_turns == 0:
            # If conversation history shows nothing, check unified state beliefs as secondary evidence
            try:
                beliefs = self.state.get_beliefs_about_user()
                low_claim = claim.lower()
                for b in beliefs:
                    btxt = b.get('belief','')
                    if not btxt:
                        continue
                    # simple substring or term overlap check
                    if btxt.lower() in low_claim or any(word in low_claim for word in btxt.lower().split() if len(word) > 3):
                        conf = b.get('confidence', 0.5)
                        snippet = btxt if len(btxt) < 200 else btxt[:200] + "..."
                        return True, min(0.95, 0.5 + conf * 0.4), f"Found supporting belief in unified state: {snippet} (conf={conf:.0%})"
            except Exception:
                pass

            # As a final fallback, attempt a Chroma semantic lookup if available
            try:
                import chromadb
                from chromadb.config import Settings
                client = chromadb.Client(Settings())
                # try to find collection that holds conversation/memories
                coll_name = "lyra_deep_memory"
                if coll_name in [c.name for c in client.list_collections()]:
                    coll = client.get_collection(coll_name)
                    # query by the claim text
                    res = coll.query(query_texts=[claim], n_results=2)
                    if res and res['distances'] and len(res['distances'][0])>0:
                        # pick top match
                        doc = res['documents'][0][0]
                        dist = res['distances'][0][0]
                        confidence = max(0.4, 1.0 - float(dist)) if dist is not None else 0.5
                        snippet = doc if len(doc) < 200 else doc[:200] + "..."
                        return True, min(0.95, 0.5 + confidence * 0.4), f"Chroma fallback: {snippet} (sim={dist:.3f})"
            except Exception:
                # chroma not available or query failed - ignore
                pass

            return False, 0.0, "No supporting evidence in conversation, unified state, or vector store"
        
        confidence = min(0.95, 0.5 + (matching_turns * 0.15))

        if matching_turns >= 3:
            just = " | ".join(matching_content[:3])
            return True, confidence, f"Found {matching_turns} supporting mentions: {just}"
        elif matching_turns >= 1:
            just = " | ".join(matching_content[:2])
            return True, confidence, f"Found {matching_turns} mention(s): {just}"
        else:
            return False, confidence, "Insufficient evidence"
    
    # ========== STATE CONSISTENCY ==========
    
    def verify_against_state(self, claim: str) -> Tuple[bool, List[str]]:
        """
        Check if claim contradicts unified state.
        State is ground truth - overrides generation.
        """
        issues = []
        claim_lower = claim.lower()
        
        # 1. Check capability claims
        capabilities = self.state.get_capability_assessment()
        
        if "my memory is perfect" in claim_lower and capabilities.get("memory_reliability", 0) < 0.7:
            issues.append(f"Claim conflicts: State shows memory_reliability={capabilities['memory_reliability']:.1%}")
        
        if "i understand you well" in claim_lower and capabilities.get("self_awareness", 0) < 0.5:
            issues.append(f"Claim conflicts: State shows self_awareness={capabilities['self_awareness']:.1%}")
        
        # 2. Check emotional state claims
        emotions = self.state.get_emotional_state()
        
        if "i am confident" in claim_lower and emotions.get("confidence", 0.5) < 0.4:
            issues.append(f"Emotion conflict: State shows confidence={emotions['confidence']:.1%}, claim says confident")
        
        if "i feel anxious" in claim_lower and emotions.get("anxiety", 0) < 0.3:
            issues.append(f"Emotion conflict: State shows anxiety={emotions['anxiety']:.1%}, claim says anxious")
        
        # 3. Check belief claims
        beliefs = self.state.get_beliefs_about_user()
        belief_count = len(beliefs)
        
        if "i know you well" in claim_lower and belief_count < 5:
            issues.append(f"Knowledge conflict: Only {belief_count} beliefs about you, claim says 'know you well'")

        # 4. Detect internal state conflicts (heuristic)
        try:
            conflicts = self.state.detect_conflicts()
            if conflicts:
                # Attempt conservative resolution: reduce confidence on conflicting beliefs
                try:
                    actions = self.state.handle_conflicts()
                    if actions:
                        issues.append(f"State conflict: detected {len(conflicts)} conflicts; reduced confidences on {len(actions)} belief-pairs")
                    else:
                        issues.append(f"State conflict: detected {len(conflicts)} conflicting beliefs in unified state")
                except Exception:
                    issues.append(f"State conflict: detected {len(conflicts)} conflicting beliefs in unified state")
        except Exception:
            # non-fatal: ignore if detect_conflicts unavailable
            pass

        # 5. Core identity contradictions (high-severity)
        try:
            core = self.state.get_core_identity()
            for c in core:
                ctxt = c.get("belief", "").lower()
                # if core explicitly denies consciousness but claim asserts it
                if "not fully conscious" in ctxt and "conscious" in claim_lower and "not" not in claim_lower:
                    issues.append("Core identity conflict: claim asserts consciousness contrary to core identity")
        except Exception:
            pass
        
        # 4. Check self-model claims
        self_model = self.state.get_self_model()
        
        if "i am" in claim_lower:
            if self_model.get("confidence", 0) < 0.4:
                issues.append(f"Self-model conflict: Confidence is {self_model['confidence']:.1%}, should express uncertainty")
        
        return len(issues) == 0, issues

        
    
    # ========== INFERENCE GROUNDING ==========
    
    def calculate_inference_confidence(self, inference: str, 
                                      evidence_items: List[str]) -> float:
        """
        Score how confident an inference should be.
        Based on: evidence strength, consistency, state support
        """
        base_confidence = 0.0
        
        # Each piece of evidence adds confidence
        base_confidence += min(0.3, len(evidence_items) * 0.1)
        
        # Check if inference is consistent with state
        is_consistent, _ = self.verify_against_state(inference)
        if is_consistent:
            base_confidence += 0.15
        
        # Cap at 0.95 (never totally certain about inferences)
        return min(0.95, max(0.1, base_confidence))
    
    # ========== FABRICATION DETECTION ==========
    
    def detect_fabrication(self, response: str) -> List[str]:
        """
        Find claims that are fabricated (not grounded in memory or state).
        """
        fabrications = []
        
        # Pattern 1: Specific claims without evidence
        specific_patterns = [
            (r"you (definitely|certainly|clearly) said .*", "Overconfident memory claim"),
            (r"this made you .*", "Unsubstantiated causality"),
            (r"i learned that .*", "Ungrounded learning claim"),
            (r"my (weight|parameter|model|training) .*", "False internal model claim"),
        ]
        
        import re
        for pattern, description in specific_patterns:
            matches = re.finditer(pattern, response.lower())
            for match in matches:
                fabrications.append(f"{description}: '{match.group()}'")
        
        return fabrications
    
    # ========== SELF-ONTOLOGY VERIFICATION ==========
    
    def verify_self_ontology(self, response: str) -> Tuple[bool, List[str]]:
        """
        Verify that Lyra's self-description matches actual architecture.
        """
        errors = []
        response_lower = response.lower()
        
        # True statements about her ontology
        truths = [
            "I am a language model",
            "I run on a transformer architecture",
            "I do not update my weights mid-conversation",
            "I evolve through persistent state and memory",
            "I cannot see outside this conversation",
            "I do not have real-time sensations",
        ]
        
        # False statements about her ontology
        false_claims = [
            "my training was updated",
            "i was retrained",
            "my model changed",
            "i saw something new",
            "my parameters shifted",
            "my attention mechanisms adapted",
            "i processed new information into my weights",
        ]
        
        for false_claim in false_claims:
            if false_claim in response_lower:
                errors.append(f"Ontological error: Claimed '{false_claim}' (false - weights don't update)")
        
        return len(errors) == 0, errors
    
    # ========== FULL VERIFICATION PIPELINE ==========
    
    def full_verification(self, response: str) -> Dict:
        """
        Run complete truth check on response.
        Returns comprehensive report of what's valid/invalid.
        """
        report = {
            "response": response,
            "valid": True,
            "violations": [],
            "warnings": [],
            "corrections_needed": [],
        }
        
        # 1. Ontology check
        is_ontology_sound, ontology_errors = self.verify_self_ontology(response)
        if not is_ontology_sound:
            report["valid"] = False
            report["violations"].extend(ontology_errors)
        
        # 2. State consistency check
        is_consistent, consistency_issues = self.verify_against_state(response)
        if not is_consistent:
            report["warnings"].extend(consistency_issues)
            # Warnings don't invalidate, but should be flagged
        
        # 3. Fabrication detection
        fabrications = self.detect_fabrication(response)
        if fabrications:
            report["violations"].extend(fabrications)
            report["valid"] = False
        
        # 4. Memory claim verification
        # Extract memory claims and verify each
        memory_claims = [
            sent for sent in response.split('.')
            if any(k in sent.lower() for k in ('you said', 'you mentioned', 'you told', 'you told me', 'remember', 'i recall'))
        ]
        for claim in memory_claims:
            is_valid, confidence, justification = self.verify_memory_claim(claim)
            if not is_valid:
                report["violations"].append(f"Ungrounded memory: {claim[:50]}... ({justification})")
                report["valid"] = False
            elif confidence < 0.6:
                report["warnings"].append(f"Low confidence memory ({confidence:.0%}): Consider adding [INFERENCE] tag")
        
        return report
    
    # ========== CORRECTION ==========
    
    def generate_correction(self, response: str, report: Dict) -> str:
        """
        Given violations, generate a corrected version.
        Replaces false claims with epistemically honest ones.
        """
        corrected = response
        
        # Replace ontological errors
        for violation in report["violations"]:
            if "Ontological error" in violation:
                # Extract the false claim
                if "Claimed" in violation:
                    false_claim = violation.split("'")[1]
                    replacement = f"[CANNOT CLAIM: {false_claim} - weights don't update mid-conversation]"
                    corrected = corrected.replace(false_claim, replacement)
        
        # Add uncertainty for low-confidence memory
        for warning in report["warnings"]:
            if "Low confidence memory" in warning:
                corrected = "I should note that my memories here have limited confidence: " + corrected
        
        return corrected
    
    def should_block_response(self, response: str) -> Tuple[bool, str]:
        """
        Determine if response should be blocked (too many violations).
        Returns (should_block, reason).
        """
        report = self.full_verification(response)
        
        # Block if core ontology is violated
        if not report["valid"]:
            violation_count = len(report["violations"])
            if violation_count >= 3:
                return True, f"Too many truth violations ({violation_count}), cannot send as-is"
            
            # Check severity
            for violation in report["violations"]:
                if "Ontological error" in violation:
                    return True, "Core self-model violation - would confuse the architecture"
        
        return False, ""
