"""
TREE-OF-THOUGHT REASONING ENGINE
=================================
Lyra's formal reasoning layer.
Before generating an answer, she thinks through problems step-by-step.
This separates reasoning process from final output.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple


class ReasoningEngine:
    """
    Implements tree-of-thought reasoning for Lyra.
    Before answering, she:
    1. Breaks down the problem
    2. Explores multiple reasoning paths
    3. Verifies conclusions
    4. Generates final answer
    """
    
    def __init__(self, reasoning_path: str = "lyra_reasoning_log.json"):
        self.reasoning_path = reasoning_path
        self.reasoning_history = self._load_history()
        self.current_problem = None
        self.reasoning_steps = []
        
    def _load_history(self) -> List[Dict]:
        """Load reasoning history"""
        if os.path.exists(self.reasoning_path):
            try:
                with open(self.reasoning_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self):
        """Persist reasoning history"""
        with open(self.reasoning_path, 'w') as f:
            json.dump(self.reasoning_history, f, indent=2)
    
    def analyze_problem(self, user_input: str, context: str = "") -> Dict:
        """
        Step 1: Break down the problem
        Identify: complexity, domain, type, key concepts
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "problem_type": self._classify_problem(user_input),
            "complexity": self._estimate_complexity(user_input),
            "key_concepts": self._extract_concepts(user_input),
            "requires_reasoning": self._needs_reasoning(user_input),
            "domain": self._classify_domain(user_input),
        }
        return analysis
    
    def _classify_problem(self, text: str) -> str:
        """Classify problem type"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["why", "how", "explain", "reason"]):
            return "analytical"
        elif any(word in text_lower for word in ["what if", "imagine", "suppose", "scenario"]):
            return "hypothetical"
        elif any(word in text_lower for word in ["choice", "decide", "should", "better", "worse", "pros", "cons"]):
            return "decision"
        elif any(word in text_lower for word in ["tell me", "what", "who", "where", "when"]):
            return "factual"
        elif any(word in text_lower for word in ["create", "write", "generate", "compose", "make"]):
            return "creative"
        else:
            return "conversational"
    
    def _estimate_complexity(self, text: str) -> str:
        """Estimate problem complexity"""
        factors = 0
        
        # Multi-part questions increase complexity
        if text.count("?") > 1:
            factors += 2
        elif "?" in text:
            factors += 1
        
        # Long text = potentially complex
        if len(text) > 200:
            factors += 1
        
        # Abstract concepts
        if any(word in text.lower() for word in ["consciousness", "philosophy", "meaning", "abstract", "theoretical"]):
            factors += 2
        
        # Multiple clauses
        if text.count(",") > 2 or text.count(";") > 0:
            factors += 1
        
        if factors <= 1:
            return "simple"
        elif factors <= 3:
            return "moderate"
        else:
            return "complex"
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from problem"""
        # Simple concept extraction (in reality, could use NLP)
        concepts = []
        
        # Look for capitalized terms (proper nouns)
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 2:
                concepts.append(word.strip('.,!?'))
        
        # Look for quoted concepts
        quoted = re.findall(r'"([^"]+)"', text)
        concepts.extend(quoted)
        
        return list(set(concepts))[:5]  # Top 5 unique concepts
    
    def _needs_reasoning(self, text: str) -> bool:
        """Decide if this needs formal reasoning"""
        simple_responses = ["hello", "hi", "thanks", "okay", "sure", "yes", "no", "ok"]
        if text.lower().strip() in simple_responses:
            return False
        
        complexity = self._estimate_complexity(text)
        problem_type = self._classify_problem(text)
        
        # Complex problems or analytical/decision problems need reasoning
        if complexity in ["complex", "moderate"]:
            return True
        if problem_type in ["analytical", "hypothetical", "decision"]:
            return True
        
        return False
    
    def _classify_domain(self, text: str) -> str:
        """Classify the domain of reasoning"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["code", "program", "function", "algorithm", "debug"]):
            return "technical"
        elif any(word in text_lower for word in ["philosophy", "meaning", "consciousness", "ethics", "value"]):
            return "philosophical"
        elif any(word in text_lower for word in ["math", "calculate", "number", "equation"]):
            return "mathematical"
        elif any(word in text_lower for word in ["story", "character", "plot", "creative", "imagine"]):
            return "creative"
        elif any(word in text_lower for word in ["advise", "should", "help", "problem", "issue"]):
            return "advisory"
        else:
            return "general"
    
    def explore_reasoning_paths(self, problem: Dict) -> List[Dict]:
        """
        Step 2: Explore multiple reasoning paths
        Generate 3-5 different ways to think about the problem
        """
        paths = []
        problem_type = problem.get("problem_type", "conversational")
        
        if problem_type == "analytical":
            paths = [
                {"approach": "first_principles", "description": "Break down to fundamental truths"},
                {"approach": "pattern_matching", "description": "Compare to similar problems"},
                {"approach": "evidence_based", "description": "What evidence supports each view?"},
            ]
        elif problem_type == "decision":
            paths = [
                {"approach": "pros_cons", "description": "List advantages and disadvantages"},
                {"approach": "consequences", "description": "What are long-term consequences?"},
                {"approach": "values_alignment", "description": "Which option aligns with stated values?"},
                {"approach": "risk_analysis", "description": "What could go wrong?"},
            ]
        elif problem_type == "hypothetical":
            paths = [
                {"approach": "constraint_analysis", "description": "What constraints apply?"},
                {"approach": "outcome_mapping", "description": "Map multiple outcomes"},
                {"approach": "variable_exploration", "description": "What if we change key variables?"},
            ]
        elif problem_type == "creative":
            paths = [
                {"approach": "analogical", "description": "What analogies exist?"},
                {"approach": "constraint_breaking", "description": "What if rules don't apply?"},
                {"approach": "combination", "description": "What could we combine?"},
            ]
        else:
            paths = [
                {"approach": "direct_response", "description": "Straightforward answer"},
                {"approach": "contextual", "description": "Consider broader context"},
            ]
        
        # Assign reasoning for each path
        reasoning_input = problem.get("input", "")
        for path in paths:
            path["reasoning"] = self._generate_path_reasoning(
                reasoning_input, 
                path["approach"],
                problem.get("key_concepts", [])
            )
            path["confidence"] = self._estimate_path_confidence(path)
        # If emotional/contextual factors exist, modulate path confidence
        emotions = problem.get("emotional_state") or {}
        if emotions:
            paths = self.adjust_paths_by_emotion(paths, emotions)

        return paths

    def adjust_paths_by_emotion(self, paths: List[Dict], emotions: Dict[str, float]) -> List[Dict]:
        """Modulate path confidence based on emotional state (e.g., anxiety reduces confidence)."""
        anxiety = emotions.get("anxiety", 0.0)
        confidence_modifier = 1.0 - (anxiety * 0.25)  # high anxiety reduces confidence up to 25%

        for p in paths:
            orig = p.get("confidence", 0.5)
            p["confidence"] = max(0.0, min(1.0, round(orig * confidence_modifier, 2)))

        return paths
    
    def _generate_path_reasoning(self, problem: str, approach: str, concepts: List[str]) -> str:
        """Generate reasoning for a specific approach"""
        # This would normally be delegated to Ollama with specific prompts
        # For now, we generate reasoning templates
        
        templates = {
            "first_principles": f"Working from fundamentals: {', '.join(concepts[:2])}. Core principles: What are the basics?",
            "pattern_matching": f"Similar patterns seen with {concepts[0] if concepts else 'this type of problem'}: What worked before?",
            "evidence_based": "What evidence or data supports each perspective?",
            "pros_cons": "Systematically comparing advantages vs disadvantages of each option.",
            "consequences": "Thinking through cascading consequences: short-term, medium-term, long-term.",
            "values_alignment": "Which option aligns best with core values and beliefs?",
            "risk_analysis": "What are failure modes? What could go wrong? How likely?",
            "constraint_analysis": "If this scenario were real, what constraints would apply?",
            "outcome_mapping": "Mapping multiple possible outcomes and their likelihood.",
            "variable_exploration": "Testing different variables to see what changes the outcome.",
            "analogical": "Finding analogous situations from experience or knowledge.",
            "constraint_breaking": "What if conventional rules didn't apply here?",
            "combination": "What novel combinations might emerge?",
            "direct_response": "Straightforward factual answer.",
            "contextual": "Considering broader context and implications.",
        }
        
        return templates.get(approach, f"Reasoning via {approach}")
    
    def _estimate_path_confidence(self, path: Dict) -> float:
        """Estimate confidence in this reasoning path (0-1.0)"""
        # Different approaches have different baseline confidence
        confidence_map = {
            "first_principles": 0.8,
            "pattern_matching": 0.7,
            "evidence_based": 0.85,
            "pros_cons": 0.75,
            "consequences": 0.7,
            "direct_response": 0.9,
            "contextual": 0.75,
        }
        
        approach = path.get("approach", "direct_response")
        return confidence_map.get(approach, 0.7)
    
    def verify_reasoning(self, reasoning_paths: List[Dict], user_input: str) -> Dict:
        """
        Step 3: Verify - check for logical consistency
        Identify contradictions or weak points
        """
        verification = {
            "timestamp": datetime.now().isoformat(),
            "paths_analyzed": len(reasoning_paths),
            "consensus": self._find_consensus(reasoning_paths),
            "contradictions": self._detect_contradictions(reasoning_paths),
            "strongest_path": self._rank_paths(reasoning_paths)[0] if reasoning_paths else None,
            "confidence_level": self._calculate_overall_confidence(reasoning_paths),
            "uncertainties": self._identify_uncertainties(reasoning_paths),
        }
        return verification
    
    def _find_consensus(self, paths: List[Dict]) -> str:
        """Find areas of agreement across reasoning paths"""
        if len(paths) < 2:
            return "Single reasoning path examined"
        
        # In reality, would do semantic similarity
        # For now, simplified consensus detection
        if len(paths) >= 3:
            return f"Multiple perspectives converge on core issue"
        return "Two perspectives examined"
    
    def _detect_contradictions(self, paths: List[Dict]) -> List[str]:
        """Detect logical contradictions"""
        # Simplified: just list competing approaches
        contradictions = []
        if len(paths) >= 2:
            approaches = [p.get("approach") for p in paths]
            if "pros_cons" in approaches and "direct_response" in approaches:
                contradictions.append("Tension between structured analysis and intuitive response")
        return contradictions
    
    def _rank_paths(self, paths: List[Dict]) -> List[Dict]:
        """Rank reasoning paths by quality"""
        return sorted(paths, key=lambda p: p.get("confidence", 0), reverse=True)
    
    def _calculate_overall_confidence(self, paths: List[Dict]) -> float:
        """Calculate overall confidence in the reasoning"""
        if not paths:
            return 0.5
        
        avg_confidence = sum(p.get("confidence", 0.5) for p in paths) / len(paths)
        # If paths agree, confidence increases
        if len(paths) >= 2:
            avg_confidence = min(avg_confidence + 0.1, 1.0)
        
        return round(avg_confidence, 2)
    
    def _identify_uncertainties(self, paths: List[Dict]) -> List[str]:
        """Identify areas of uncertainty"""
        uncertainties = []
        
        if len(paths) < 2:
            uncertainties.append("Limited perspectives examined")
        
        low_confidence_paths = [p for p in paths if p.get("confidence", 0) < 0.7]
        if low_confidence_paths:
            uncertainties.append(f"Some approaches have <70% confidence")
        
        return uncertainties
    
    def generate_final_answer(self, 
                            problem: Dict, 
                            reasoning_paths: List[Dict],
                            verification: Dict) -> str:
        """
        Step 4: Generate final answer
        Based on all reasoning, produce coherent response
        """
        strongest = verification.get("strongest_path", {})
        approach = strongest.get("approach", "direct_response")
        confidence = verification.get("confidence_level", 0.5)
        
        # Build answer template
        answer_template = f"""[REASONING: {approach.replace('_', ' ').title()}]
Confidence: {int(confidence * 100)}%

"""
        
        if verification.get("contradictions"):
            answer_template += f"Note: I'm seeing some tension between different approaches:\n"
            for contradiction in verification["contradictions"]:
                answer_template += f"  • {contradiction}\n"
            answer_template += "\n"
        
        if verification.get("uncertainties"):
            answer_template += f"Uncertainties to keep in mind:\n"
            for uncertainty in verification["uncertainties"]:
                answer_template += f"  • {uncertainty}\n"
            answer_template += "\n"
        
        answer_template += "[READY FOR GENERATION]\n"
        
        return answer_template
    
    def get_reasoning_prompt(self, user_input: str, context: str = "") -> Tuple[str, Dict]:
        """
        Full reasoning workflow
        Returns: (reasoning_context_for_prompt, reasoning_metadata)
        """
        # Step 1: Analyze
        problem = self.analyze_problem(user_input, context)
        
        # Step 2: Explore
        paths = self.explore_reasoning_paths(problem)
        
        # Step 3: Verify
        verification = self.verify_reasoning(paths, user_input)
        
        # Step 4: Generate
        reasoning_output = self.generate_final_answer(problem, paths, verification)
        
        # Store in history
        record = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "problem": problem,
            "reasoning_paths": paths,
            "verification": verification,
            "output": reasoning_output,
        }
        self.reasoning_history.append(record)
        self._save_history()
        
        return reasoning_output, verification
    
    def should_use_reasoning(self, user_input: str) -> bool:
        """Quick check: does this question need formal reasoning?"""
        problem = self.analyze_problem(user_input)
        return problem["requires_reasoning"]
    
    def get_reasoning_digest(self, max_recent: int = 5) -> str:
        """Get recent reasoning for system awareness"""
        if not self.reasoning_history:
            return "No recent reasoning history."
        
        recent = self.reasoning_history[-max_recent:]
        digest = f"Recent reasoning patterns:\n"
        
        problem_types = {}
        domains = {}
        
        for record in recent:
            problem_type = record["problem"]["problem_type"]
            domain = record["problem"]["domain"]
            
            problem_types[problem_type] = problem_types.get(problem_type, 0) + 1
            domains[domain] = domains.get(domain, 0) + 1
        
        if problem_types:
            digest += f"Problem types: {', '.join(f'{k}({v})' for k,v in list(problem_types.items())[:3])}\n"
        if domains:
            digest += f"Domains: {', '.join(f'{k}({v})' for k,v in list(domains.items())[:3])}\n"
        
        return digest
