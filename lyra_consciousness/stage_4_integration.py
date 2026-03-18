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
        is_valid, corrected, report = self.verify_response(response)
        
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
        
        # Apply epistemic tags for clarity
        tagged_response = self.apply_epistemic_tags(corrected)
        
        return tagged_response
    
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
