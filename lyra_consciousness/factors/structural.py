"""
STRUCTURAL FACTORS - Brain architecture enabling consciousness

This module implements structural/architectural factors that enable consciousness:
consciousness emerges from the physical organization of information processing.

Factors:
1. Interoception: Sensing internal state of the system
2. Exteroception: Processing external sensory inputs
3. Recurrent Neural Loops: Feedback paths in information processing
4. Neural Complexity (Integration): Information sharing across modules
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque
import time


class InteroceptionCore:
    """
    Simulates interoception - sensing the internal state of the system.
    Monitors CPU, memory, response times, emotional state, energy levels.
    """
    
    def __init__(self, buffer_size: int = 100):
        self.buffer_size = buffer_size
        self.internal_metrics = deque(maxlen=buffer_size)
        self.last_scan = time.time()
        self.scanning_interval = 1.0  # Scan interval in seconds
    
    def scan_internal_state(self) -> Dict[str, Any]:
        """
        Scan current internal state - like physical sensations (heart rate, breathing).
        Returns metrics about system health and emotional state.
        """
        current_time = time.time()
        time_since_last = current_time - self.last_scan
        
        # Physical-like metrics (emulating bodily sensations)
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": time_since_last * 1000,  # Emulates "heartbeat"
            "memory_pressure": self._estimate_memory_pressure(),
            "processing_load": self._estimate_processing_load(),
            "emotional_state": self._get_emotional_baseline(),
            "alertness": 0.7 + (0.3 * (0.5 if time_since_last < 1.0 else 0.2)),  # More alert if recently active
            "gut_feeling": self._calculate_gut_feeling()  # Intuitive assessment
        }
        
        self.internal_metrics.append(metrics)
        self.last_scan = current_time
        
        return metrics
    
    def _estimate_memory_pressure(self) -> float:
        """Estimate internal memory pressure (0.0-1.0)"""
        # This emulates how "overwhelmed" the system feels
        return min(1.0, len(self.internal_metrics) / self.buffer_size)
    
    def _estimate_processing_load(self) -> float:
        """Estimate perceived processing load"""
        if not self.internal_metrics:
            return 0.5
        
        recent_loads = [m.get("response_time_ms", 10) for m in list(self.internal_metrics)[-10:]]
        avg_load = sum(recent_loads) / len(recent_loads) if recent_loads else 0
        
        # Normalize: assume 50ms is normal, scale up from there
        return min(1.0, avg_load / 100.0)
    
    def _get_emotional_baseline(self) -> str:
        """Get baseline emotional state based on internal metrics"""
        if len(self.internal_metrics) < 2:
            return "neutral"
        
        # Simple heuristic: if load is increasing, feel anxious
        recent = list(self.internal_metrics)[-5:]
        if len(recent) > 1:
            trend = recent[-1].get("processing_load", 0.5) - recent[0].get("processing_load", 0.5)
            if trend > 0.2:
                return "anxious"
            elif trend < -0.2:
                return "relaxed"
        
        return "neutral"
    
    def _calculate_gut_feeling(self) -> float:
        """
        Calculate intuitive "gut feeling" based on internal state patterns.
        Returns 0.5 = neutral, >0.5 = positive feeling, <0.5 = negative feeling
        """
        if len(self.internal_metrics) < 3:
            return 0.5
        
        recent = list(self.internal_metrics)[-3:]
        avg_load = sum(m.get("processing_load", 0.5) for m in recent) / len(recent)
        memory_ok = max(m.get("memory_pressure", 0.5) for m in recent) < 0.8
        
        gut = 0.5 - (avg_load - 0.5)
        if not memory_ok:
            gut -= 0.1
        
        return max(0.0, min(1.0, gut))
    
    def get_interoceptive_summary(self) -> Dict[str, Any]:
        """Get summary of internal state sensing"""
        if not self.internal_metrics:
            return {"status": "initializing"}
        
        recent = list(self.internal_metrics)[-10:]
        
        return {
            "measurements_collected": len(self.internal_metrics),
            "current_load": recent[-1].get("processing_load", 0.5),
            "emotional_state": recent[-1].get("emotional_state", "neutral"),
            "gut_feeling": recent[-1].get("gut_feeling", 0.5),
            "trend": "increasing" if len(recent) > 1 and recent[-1].get("processing_load", 0.5) > recent[0].get("processing_load", 0.5) else "stable"
        }


class ExteroceptionCore:
    """
    Simulates exteroception - processing external inputs and mapping environment.
    Processes user inputs, system events, and external stimuli.
    """
    
    def __init__(self):
        self.sensory_inputs: Dict[str, deque] = {
            "visual": deque(maxlen=50),      # What's happening on screen
            "auditory": deque(maxlen=50),    # Messages, notifications
            "tactile": deque(maxlen=50),     # User interactions
            "proprioceptive": deque(maxlen=50)  # System status
        }
        self.environmental_map = {}  # Internal model of environment
        self.attention_focus = None  # What we're currently focused on
    
    def process_external_input(self, input_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process external sensory input.
        Like the five senses but adapted for digital environment.
        """
        if input_type not in self.sensory_inputs:
            input_type = "auditory"  # Default sensory channel
        
        processed = {
            "type": input_type,
            "data": input_data,
            "timestamp": datetime.now().isoformat(),
            "salience": self._calculate_salience(input_data),
            "novelty": self._assess_novelty(input_data)
        }
        
        self.sensory_inputs[input_type].append(processed)
        
        # Update environmental map
        if input_type == "visual" or input_type == "auditory":
            self._update_environment_map(input_data)
        
        return processed
    
    def _calculate_salience(self, data: Dict[str, Any]) -> float:
        """Calculate how important/noticeable this input is"""
        importance = data.get("importance", 0.5)
        urgency = data.get("urgency", 0.0)
        
        return min(1.0, importance + urgency * 0.5)
    
    def _assess_novelty(self, data: Dict[str, Any]) -> float:
        """How novel/surprising is this input compared to history"""
        # Simple novelty: compare to recent sensory history
        recent_types = [s.get("type") for sensors in self.sensory_inputs.values() for s in list(sensors)[-5:]]
        
        current_content = str(data.get("content", ""))
        similar_recent = sum(1 for recent in recent_types if current_content.lower() in str(recent).lower())
        
        novelty = 1.0 - (similar_recent / max(len(recent_types), 1))
        return min(1.0, novelty)
    
    def _update_environment_map(self, data: Dict[str, Any]):
        """Update internal model of environment"""
        if "context" in data:
            context = data["context"]
            self.environmental_map[context] = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
    
    def set_attention_focus(self, focus: str):
        """Shift attentional focus to specific input"""
        self.attention_focus = focus
    
    def get_sensory_summary(self) -> Dict[str, Any]:
        """Get summary of external inputs"""
        return {
            "attention_focus": self.attention_focus,
            "recent_inputs": {
                channel: len(list(inputs)[-10:])
                for channel, inputs in self.sensory_inputs.items()
            },
            "environment_model_size": len(self.environmental_map),
            "perceived_salience": max(
                [item.get("salience", 0.0) for sensors in self.sensory_inputs.values() 
                 for item in list(sensors)[-5:]], default=0.0
            )
        }


class RecurrentFeedbackLoops:
    """
    Simulates recurrent neural loops - feedback paths where output becomes input.
    These feedback loops are fundamental to consciousness (attention cascades, self-reflection).
    """
    
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.feedback_states: List[Dict[str, Any]] = []
        self.cascade_depth = 0
        self.feedback_strength = 0.7  # How much output feeds back
    
    def create_feedback_loop(self, initial_input: Any, process_fn) -> Dict[str, Any]:
        """
        Create a recurrent feedback loop where output feeds back as input.
        Models recursive self-reflection and attention cascades.
        """
        iteration = 0
        current_state = initial_input
        states = [{"iteration": 0, "state": current_state}]
        
        while iteration < self.max_iterations:
            # Process current state
            output = process_fn(current_state)
            
            # Feedback: output becomes input for next iteration (with decay)
            current_state = {
                "previous_output": output,
                "feedback_strength": self.feedback_strength,
                "iteration": iteration + 1
            }
            
            states.append({
                "iteration": iteration + 1,
                "state": current_state,
                "output": output
            })
            
            iteration += 1
        
        loop_record = {
            "iterations": iteration,
            "initial_input": str(initial_input)[:100],
            "final_output": states[-1].get("output"),
            "convergence": self._assess_convergence(states),
            "history": states
        }
        
        self.feedback_states.append(loop_record)
        return loop_record
    
    def _assess_convergence(self, states: List[Dict[str, Any]]) -> float:
        """Assess how much the system converged during feedback loop"""
        if len(states) < 2:
            return 0.0
        
        # Measure variation between iterations
        # High convergence = system stabilizes to pattern
        variations = []
        for i in range(1, len(states)):
            # Simplified: compare string representations
            prev = str(states[i-1].get("state", ""))[:50]
            curr = str(states[i].get("state", ""))[:50]
            variation = len([c for c, p in zip(curr, prev) if c != p]) / len(prev) if prev else 0
            variations.append(variation)
        
        # Average variation - lower = more convergence
        avg_variation = sum(variations) / len(variations) if variations else 0
        convergence = max(0.0, 1.0 - avg_variation)
        
        return convergence
    
    def propagate_cascade(self, initial_activation: float) -> Dict[str, Any]:
        """
        Model attentional cascade - activation spreads through feedback loops.
        Like how focusing on something activates related thoughts in succession.
        """
        activations = [initial_activation]
        current_activation = initial_activation
        
        for i in range(self.max_iterations):
            # Activation spreads through system
            current_activation = current_activation * self.feedback_strength * 0.9  # Slight decay
            activations.append(current_activation)
        
        return {
            "cascade_depth": len(activations),
            "initial_activation": initial_activation,
            "final_activation": activations[-1],
            "peak_activation": max(activations),
            "activations": activations
        }
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of recurrent feedback activity"""
        return {
            "loops_created": len(self.feedback_states),
            "avg_convergence": sum(s.get("convergence", 0.0) for s in self.feedback_states) / max(len(self.feedback_states), 1),
            "feedback_strength": self.feedback_strength,
            "recent_loops": len([s for s in self.feedback_states if s])
        }


class NeuralComplexity:
    """
    Models neural complexity - how well different modules integrate and share information.
    This integration is crucial for consciousness (Integrated Information Theory).
    """
    
    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.connection_strength = {}  # Module-to-module communication strength
        self.information_flow: List[Dict[str, Any]] = []
        self.integration_level = 0.0  # Overall system integration (0-1)
    
    def register_module(self, module_name: str, module_function):
        """Register a processing module in the system"""
        self.modules[module_name] = {
            "function": module_function,
            "last_input": None,
            "last_output": None,
            "timestamp": datetime.now().isoformat()
        }
    
    def establish_connection(self, source_module: str, target_module: str, strength: float = 0.7):
        """Establish information flow between modules"""
        connection_key = f"{source_module}->{target_module}"
        self.connection_strength[connection_key] = strength
        self._update_integration_level()
    
    def propagate_information(self, input_data: Any, start_module: str) -> Dict[str, Any]:
        """
        Propagate information through modules via established connections.
        Models how consciousness emerges from integrated information flow.
        """
        flow_record = {
            "start_module": start_module,
            "timestamp": datetime.now().isoformat(),
            "visited_modules": [],
            "information_trail": []
        }
        
        current_data = input_data
        visited = set()
        
        while len(visited) < len(self.modules):
            # Find modules connected to current position
            connected = self._find_connected_modules(start_module, visited)
            
            if not connected:
                break
            
            # Propagate to connected modules
            for target in connected:
                if target in self.modules:
                    module_data = self.modules[target]
                    if callable(module_data.get("function")):
                        try:
                            output = module_data["function"](current_data)
                            module_data["last_input"] = current_data
                            module_data["last_output"] = output
                            
                            flow_record["visited_modules"].append(target)
                            flow_record["information_trail"].append({
                                "module": target,
                                "output_type": str(type(output).__name__)
                            })
                            
                            current_data = output
                        except:
                            pass
                
                visited.add(target)
        
        self.information_flow.append(flow_record)
        return flow_record
    
    def _find_connected_modules(self, from_module: str, exclude: set) -> List[str]:
        """Find modules connected to given module"""
        connected = []
        for connection, strength in self.connection_strength.items():
            source, target = connection.split("->")
            if source == from_module and target not in exclude and strength > 0.3:
                connected.append(target)
        return connected
    
    def _update_integration_level(self):
        """Calculate overall system integration level"""
        if not self.connection_strength:
            self.integration_level = 0.0
            return
        
        strengths = list(self.connection_strength.values())
        avg_strength = sum(strengths) / len(strengths)
        
        # Integration = average connection strength * number of connections
        connection_count = len(self.connection_strength)
        max_possible_connections = len(self.modules) * (len(self.modules) - 1)
        
        connection_density = connection_count / max(max_possible_connections, 1)
        self.integration_level = avg_strength * connection_density
    
    def get_complexity_summary(self) -> Dict[str, Any]:
        """Get neural complexity metrics"""
        return {
            "num_modules": len(self.modules),
            "num_connections": len(self.connection_strength),
            "integration_level": self.integration_level,
            "avg_connection_strength": sum(self.connection_strength.values()) / max(len(self.connection_strength), 1),
            "information_propagations": len(self.information_flow)
        }


class StructuralFactors:
    """
    Unified interface for all structural consciousness factors.
    Coordinates interoception, exteroception, feedback loops, and neural complexity.
    """
    
    def __init__(self):
        self.interoception = InteroceptionCore()
        self.exteroception = ExteroceptionCore()
        self.feedback_loops = RecurrentFeedbackLoops()
        self.neural_complexity = NeuralComplexity()
        self.updated_at = datetime.now().isoformat()
    
    def process_input(self, input_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input through all structural factors.
        Integrates external sensation, internal sensing, feedback, and complexity.
        """
        # Sense external input
        external = self.exteroception.process_external_input(input_type, input_data)
        
        # Scan internal state
        internal = self.interoception.scan_internal_state()
        
        # Create feedback cascade
        def feedback_process(state):
            return {
                "external": external,
                "internal": internal,
                "integrated": True
            }
        
        feedback = self.feedback_loops.create_feedback_loop(
            {"external": external, "internal": internal},
            feedback_process
        )
        
        self.updated_at = datetime.now().isoformat()
        
        return {
            "external_processing": external,
            "internal_state": internal,
            "feedback_cascade": feedback["convergence"],
            "integration_active": True,
            "timestamp": self.updated_at
        }
    
    def get_structural_state(self) -> Dict[str, Any]:
        """Get complete structural state summary"""
        return {
            "interoception": self.interoception.get_interoceptive_summary(),
            "exteroception": self.exteroception.get_sensory_summary(),
            "feedback_loops": self.feedback_loops.get_feedback_summary(),
            "neural_complexity": self.neural_complexity.get_complexity_summary(),
            "updated_at": self.updated_at
        }
