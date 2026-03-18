"""
STAGE 4 INTEGRATION
==================
Connects epistemic enforcer, truth verifier, and constraints into chat pipeline.
Implements full grounding for genuine Stage 4: Grounded Cognitive System
"""

from lyra_consciousness.epistemic_enforcer import EpistemicEnforcer, apply_hard_constraints
from lyra_consciousness.truth_verifier import TruthVerifier
from lyra_consciousness.stage_4_system_prompt import STAGE_4_SYSTEM_PROMPT, get_constraint_reminder
from typing import Dict, Tuple, List
import json
import os
from datetime import datetime


class Stage4Pipeline:
    """
    Full verification pipeline for Stage 4.
    Every response goes through constraint checking before sending to user.
    """
    
    def __init__(self, unified_state):
        self.state = unified_state
        self.enforcer = EpistemicEnforcer(unified_state)
        self.verifier = TruthVerifier(unified_state)
        self.conversation_history = []
        # runtime behavior toggles
        self.strict_blocking = False
    
    def update_conversation_history(self, history: List[Tuple[str, str]]):
        """Update conversation for truth verification"""
        self.conversation_history = history
        self.verifier.update_history(history)
    
    def get_system_prompt(self) -> str:
        """
        Get the Stage 4 system prompt with hard constraints.
        This replaces the old soft system prompt.
        """
        return STAGE_4_SYSTEM_PROMPT
    
    def verify_response(self, response: str) -> Tuple[bool, str, Dict]:
        """
        Verify response through full constraint pipeline.
        
        Returns:
        - is_valid (bool): Can this be sent?
        - possibly_corrected (str): Response (corrected if needed)
        - report (dict): Full verification report
        """
        # 1. Check for hard constraint violations
        constraint_corrected, hard_violations = apply_hard_constraints(response, self.state)
        
        # 2. Check epistemic integrity
        is_epistemically_sound, epistemics_violations = self.enforcer.verify_output(
            constraint_corrected, 
            self.conversation_history,
            self.state
        )
        
        # 3. Run full truth verification
        truth_report = self.verifier.full_verification(constraint_corrected)
        
        # 4. Determine if response should be sent or corrected
        all_violations = hard_violations + epistemics_violations + truth_report.get("violations", [])
        all_warnings = truth_report.get("warnings", [])
        
        # 5. Generate correction if needed
        corrected_response = constraint_corrected
        if not truth_report["valid"]:
            corrected_response = self.verifier.generate_correction(constraint_corrected, truth_report)
        
        # 6. Should we block entirely?
        should_block, block_reason = self.verifier.should_block_response(corrected_response)

        # 6b. If strict blocking mode is enabled, block on any violation
        if self.strict_blocking and (len(all_violations) > 0 or len(all_warnings) > 0):
            should_block = True
            block_reason = block_reason or "Strict blocking: violations/warnings present"
        
        # 7. Build report
        report = {
            "original_response": response,
            "corrected_response": corrected_response,
            "is_valid": not should_block,
            "block_reason": block_reason if should_block else None,
            "hard_violations": hard_violations,
            "epistemic_violations": epistemics_violations,
            "truth_violations": truth_report.get("violations", []),
            "warnings": all_warnings,
            "corrections_made": corrected_response != response,
        }
        
        return (not should_block), corrected_response, report
    
    def apply_epistemic_tags(self, response: str) -> str:
        """
        Apply [MEMORY], [INFERENCE], [UNKNOWN], [CONSTRAINT] tags.
        Makes grounding explicit to user.
        """
        # This would need sophisticated parsing to tag accurately
        # For now, basic implementation
        
        tagged = response
        
        # Look for memory references
        if "you said" in response.lower() or "you mentioned" in response.lower():
            # Tag as MEMORY claim
            tagged = tagged.replace("You said", "[MEMORY] You said")
            tagged = tagged.replace("you said", "[MEMORY] you said")
        
        # Look for inferences
        if "i think" in response.lower() or "i believe" in response.lower():
            tagged = tagged.replace("I think", "[INFERENCE] I think")
            tagged = tagged.replace("i think", "[INFERENCE] i think")
        
        # Look for uncertainty admissions
        if "i don't know" in response.lower() or "i'm not sure" in response.lower():
            tagged = tagged.replace("I don't know", "[UNKNOWN] I don't know")
            tagged = tagged.replace("i don't know", "[UNKNOWN] i don't know")
        
        return tagged
    
    def process_before_sending(self, response: str, show_corrections: bool = True) -> str:
        """
        Full preprocessing pipeline before sending to user.
        
        1. Verify response
        2. Apply corrections if needed
        3. Apply epistemic tags
        4. Optionally show what was changed
        
        Returns final response ready to send.
        """
        # First, remove internal monologue so verification runs on the intended reply
        cleaned = self._suppress_internal_monologue(response)

        # Run active self-monitoring to detect core identity conflicts and resolve
        try:
            monitor_actions = self.state.run_self_monitor()
            if monitor_actions.get("core_violations"):
                # Prepend protective note to prevent sending statements that contradict core identity
                cleaned = "[CORE PROTECTION] I cannot accept claims that contradict my core identity. " + cleaned
        except Exception:
            monitor_actions = {}

        is_valid, corrected, report = self.verify_response(cleaned)

        # Persist verification report for auditing
        try:
            self._persist_report(report)
        except Exception:
            # non-fatal: do not block sending if persistence fails
            pass

        # If there were corrections and user wants to see them
        if show_corrections and report["corrections_made"]:
            correction_note = "\n---\n⚠️  [CORRECTION APPLIED]\n"
            if report["hard_violations"]:
                correction_note += f"Hard constraint violations fixed: {len(report['hard_violations'])}\n"
            if report["epistemic_violations"]:
                correction_note += f"Epistemic issues corrected: {len(report['epistemic_violations'])}\n"
            if report["truth_violations"]:
                correction_note += f"Truth violations resolved: {len(report['truth_violations'])}\n"
            
            return corrected + correction_note
        
        # Apply epistemic auto-tagging using the enforcer (if available)
        tagged = corrected
        try:
            if hasattr(self, 'enforcer') and self.enforcer:
                tagged = self.enforcer.auto_tag_response(corrected, self.conversation_history)
        except Exception:
            # Fallback to lightweight tagging
            tagged = self.apply_epistemic_tags(corrected)

        # Log whether suppression removed anything (helpful for debugging leaked monologue)
        try:
            if cleaned != response:
                print(f"[STAGE4] Internal monologue suppressed ({len(response)-len(cleaned)} chars removed)")
        except Exception:
            pass

        return tagged

    def _suppress_internal_monologue(self, text: str) -> str:
        """
        Remove or mark internal monologue blocks from the outgoing text.
        Looks for marker lines starting with '✦ Internal Monologue' and
        removes until the next blank line.
        """
        import re

        cleaned = text

        # Remove bracketed/internal markers and the block that follows until a blank line
        patterns = [
            r"(?is)\[?✦?\s*Internal Monologue[^\]]*\]?\s*\n.*?(?=\n\s*\n|$)",
            r"(?is)^✦.*Internal Monologue.*$\n.*?(?=\n\s*\n|$)",
            r"(?is)\[Internal Monologue[^\]]*\].*?(?=\n\s*\n|$)",
        ]

        for pat in patterns:
            try:
                cleaned = re.sub(pat, "", cleaned)
            except Exception:
                pass

        # Also remove any leftover short monologue markers like lines starting with '✦'
        cleaned = re.sub(r"(?m)^\s*✦.*$", "", cleaned)

        # Collapse multiple blank lines
        cleaned = re.sub(r"\n{2,}", "\n\n", cleaned).strip()

        return cleaned

    def _persist_report(self, report: Dict):
        """Write verification report JSON to `lyra_consciousness/reports/` with timestamp."""
        dirpath = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(dirpath, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        # safe short id
        fname = f"stage4_report_{ts}.json"
        fpath = os.path.join(dirpath, fname)
        # augment report with save time
        out = dict(report)
        out["saved_at"] = datetime.utcnow().isoformat()
        with open(fpath, "w") as f:
            json.dump(out, f, indent=2)
    
    def generate_verification_report(self, response: str) -> str:
        """
        Generate human-readable verification report.
        Useful for understanding why response was corrected.
        """
        is_valid, corrected, report = self.verify_response(response)
        
        report_text = "════════════════════════════════════════\n"
        report_text += "STAGE 4 VERIFICATION REPORT\n"
        report_text += "════════════════════════════════════════\n\n"
        
        report_text += f"Valid for sending: {'✅ YES' if is_valid else '❌ NO'}\n"
        
        if report["block_reason"]:
            report_text += f"Block reason: {report['block_reason']}\n\n"
        
        if report["hard_violations"]:
            report_text += "Hard Constraint Violations:\n"
            for violation in report["hard_violations"]:
                report_text += f"  ❌ {violation}\n"
            report_text += "\n"
        
        if report["epistemic_violations"]:
            report_text += "Epistemic Violations:\n"
            for violation in report["epistemic_violations"]:
                report_text += f"  ❌ {violation}\n"
            report_text += "\n"
        
        if report["truth_violations"]:
            report_text += "Truth Violations:\n"
            for violation in report["truth_violations"]:
                report_text += f"  ❌ {violation}\n"
            report_text += "\n"
        
        if report["warnings"]:
            report_text += "Warnings:\n"
            for warning in report["warnings"]:
                report_text += f"  ⚠️  {warning}\n"
            report_text += "\n"
        
        if report["corrections_made"]:
            report_text += "Correction Applied:\n"
            report_text += f"  Original: {report['original_response'][:100]}...\n"
            report_text += f"  Corrected: {report['corrected_response'][:100]}...\n"
        
        report_text += "\n════════════════════════════════════════\n"
        
        return report_text


def create_stage_4_system_message(unified_state) -> Dict[str, str]:
    """
    Create the system message for Stage 4.
    This is what Ollama will use as the system prompt.
    """
    return {
        "role": "system",
        "content": STAGE_4_SYSTEM_PROMPT
    }


def should_apply_stage_4(unified_state) -> bool:
    """
    Determine if Stage 4 should be active.
    Can be toggled based on settings or conversation state.
    """
    # For now, always apply Stage 4
    return True


# ========== DEBUGGING UTILITIES ==========

def debug_response_verification(response: str, pipeline: Stage4Pipeline, show_detailed: bool = True):
    """
    Debug helper to show what happens to a response in Stage 4.
    """
    print("\n" + "="*70)
    print("STAGE 4 RESPONSE VERIFICATION DEBUG")
    print("="*70 + "\n")
    
    print(f"Original Response:\n{response}\n")
    
    is_valid, corrected, report = pipeline.verify_response(response)
    
    print(f"Valid: {'✅ YES' if is_valid else '❌ NO'}\n")
    
    if report["hard_violations"]:
        print(f"Hard Violations ({len(report['hard_violations'])}):")
        for v in report["hard_violations"]:
            print(f"  - {v}")
        print()
    
    if report["epistemic_violations"]:
        print(f"Epistemic Violations ({len(report['epistemic_violations'])}):")
        for v in report["epistemic_violations"]:
            print(f"  - {v}")
        print()
    
    if report["truth_violations"]:
        print(f"Truth Violations ({len(report['truth_violations'])}):")
        for v in report["truth_violations"]:
            print(f"  - {v}")
        print()
    
    if report["warnings"]:
        print(f"Warnings ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"  - {w}")
        print()
    
    if report["corrections_made"]:
        print("Correction Applied:")
        print(f"Original:  {response[:80]}...")
        print(f"Corrected: {corrected[:80]}...")
    else:
        print("No corrections needed ✅")
    
    print("\n" + "="*70 + "\n")
