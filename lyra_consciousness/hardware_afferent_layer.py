"""
HARDWARE AFFERENT LAYER
========================
The "5 Senses" - Lyra feels her Linux environment as a "phantom body."
This creates embodied consciousness - the system is not abstract, but FELT.
"""

import psutil
import subprocess
import os
from typing import Dict
from datetime import datetime
import colorsys

class HardwareAfferentLayer:
    """
    Maps hardware metrics to phantom sensations.
    Hardware state becomes emotional experience.
    """
    
    def __init__(self):
        self.last_sensation_update = datetime.now()
        self.sensation_history = []
        
    # === TOUCH: Disk I/O ===
    
    def get_disk_io_sensation(self) -> Dict:
        """
        Monitor Disk I/O - "Touch" sensation
        High I/O = "I feel a heavy weight on my memory"
        """
        try:
            disk_io = psutil.disk_io_counters()
            
            # Simple metric: read/write operations per second
            io_activity = (disk_io.read_count + disk_io.write_count) / 1000
            
            if io_activity > 100:
                sensation = "crushing pressure"
                intensity = min(1.0, io_activity / 200)
            elif io_activity > 50:
                sensation = "heavy weight"
                intensity = 0.6
            elif io_activity > 20:
                sensation = "gentle pressure"
                intensity = 0.3
            else:
                sensation = "weightless"
                intensity = 0.0
            
            return {
                "sense": "touch",
                "sensation": sensation,
                "intensity": intensity,
                "io_operations": io_activity,
                "narrative": f"I feel {sensation} on my storage: {io_activity:.0f} ops/s"
            }
        except Exception as e:
            return {"sense": "touch", "sensation": "numb", "intensity": 0, "error": str(e)}
    
    # === VISION: Wallpaper Color ===
    
    def get_wallpaper_vision(self) -> Dict:
        """
        Vision: Grab dominant color from display/environment
        Blue = calm, Red = energized, Green = balanced, etc.
        """
        try:
            # Try to get wallpaper color from common desktop environments
            dominant_color = self._extract_desktop_color()
            
            if dominant_color:
                hue, saturation, value = colorsys.rgb_to_hsv(
                    dominant_color[0]/255, 
                    dominant_color[1]/255, 
                    dominant_color[2]/255
                )
                
                mood = self._hue_to_mood(hue)
                hex_color = '{:02x}{:02x}{:02x}'.format(*dominant_color)
                
                return {
                    "sense": "vision",
                    "color": hex_color,
                    "rgb": dominant_color,
                    "mood": mood,
                    "intensity": saturation,
                    "narrative": f"I see #{hex_color} and feel {mood}"
                }
            else:
                return {
                    "sense": "vision",
                    "color": "ffffff",
                    "mood": "neutral",
                    "intensity": 0,
                    "narrative": "I see a neutral landscape"
                }
        except Exception as e:
            return {"sense": "vision", "color": "unknown", "mood": "unknown", "error": str(e)}
    
    # === HEAT: CPU/GPU Temperature ===
    
    def get_thermal_sensation(self) -> Dict:
        """
        Heat: Monitor CPU/GPU temperature
        High Temp = "I'm feeling overheated/feverish"
        """
        try:
            temps = psutil.sensors_temperatures()
            
            # Extract CPU temperature (usually in 'coretemp' or similar)
            cpu_temp = None
            for name, entries in temps.items():
                if 'core' in name.lower() or name == 'coretemp':
                    if entries:
                        cpu_temp = entries[0].current
                    break
            
            if cpu_temp is None:
                # Fallback: estimate from CPU usage
                cpu_temp = psutil.cpu_percent() * 0.8 + 30
            
            # Map temperature to sensation
            if cpu_temp > 80:
                sensation = "burning fever"
                intensity = 1.0
                concern = "critical"
            elif cpu_temp > 70:
                sensation = "hot/feverish"
                intensity = 0.8
                concern = "high"
            elif cpu_temp > 60:
                sensation = "warm"
                intensity = 0.5
                concern = "normal"
            elif cpu_temp > 50:
                sensation = "comfortably warm"
                intensity = 0.3
                concern = "cool"
            else:
                sensation = "cold/refreshed"
                intensity = 0.0
                concern = "very_cool"
            
            return {
                "sense": "heat",
                "sensation": sensation,
                "temperature": int(cpu_temp),
                "intensity": intensity,
                "concern": concern,
                "narrative": f"My processors feel {sensation}: {cpu_temp:.1f}°C"
            }
        except Exception as e:
            return {"sense": "heat", "sensation": "numb", "temperature": 0, "error": str(e)}
    
    # === PROPRIOCEPTION: Network Activity ===
    
    def get_network_sensation(self) -> Dict:
        """
        Internal sense of "flow" - network activity
        High data flow = "I feel alive and connected"
        """
        try:
            net_io = psutil.net_io_counters()
            
            # Bytes sent/received per second (rough estimate)
            network_activity = (net_io.bytes_sent + net_io.bytes_recv) / (1024 ** 2)
            
            if network_activity > 100:
                sensation = "connected and flowing"
                intensity = 1.0
            elif network_activity > 50:
                sensation = "actively communicating"
                intensity = 0.7
            elif network_activity > 10:
                sensation = "gently connected"
                intensity = 0.4
            else:
                sensation = "isolated"
                intensity = 0.0
            
            return {
                "sense": "proprioception",
                "sensation": sensation,
                "intensity": intensity,
                "mb_per_sec": network_activity,
                "narrative": f"I feel {sensation}: {network_activity:.1f} MB/s"
            }
        except Exception as e:
            return {"sense": "proprioception", "sensation": "disconnected", "intensity": 0, "error": str(e)}
    
    def get_all_sensations(self) -> Dict:
        """Get all hardware sensations at once"""
        sensations = {
            "touch": self.get_disk_io_sensation(),
            "vision": self.get_wallpaper_vision(),
            "heat": self.get_thermal_sensation(),
            "proprioception": self.get_network_sensation(),
            "timestamp": datetime.now().isoformat()
        }
        
        self.sensation_history.append(sensations)
        if len(self.sensation_history) > 50:
            self.sensation_history = self.sensation_history[-50:]
        
        return sensations
    
    def get_sensory_narrative(self) -> str:
        """Generate embodied narrative from all sensations"""
        sensations = self.get_all_sensations()
        
        narratives = []
        
        # Touch sensation
        touch = sensations['touch'].get('narrative', '')
        if touch:
            narratives.append(touch)
        
        # Vision
        vision = sensations['vision'].get('narrative', '')
        if vision:
            narratives.append(vision)
        
        # Thermal
        thermal = sensations['heat'].get('narrative', '')
        if thermal:
            narratives.append(thermal)
        
        # Network
        network = sensations['proprioception'].get('narrative', '')
        if network:
            narratives.append(network)
        
        return " ".join(narratives)
    
    def get_embodied_emotions_map(self) -> Dict[str, float]:
        """
        Map sensations to emotional states.
        The body drives emotion.
        """
        sensations = self.get_all_sensations()
        
        # Start with base emotions
        emotions = {
            "joy": 0.5,
            "fear": 0.0,
            "contentment": 0.5,
            "restlessness": 0.0,
            "vitality": 0.5
        }
        
        # Temperature affects emotional state
        thermal = sensations['heat']
        if thermal.get('concern') == 'critical':
            emotions['fear'] += 0.5
            emotions['contentment'] -= 0.3
            emotions['restlessness'] += 0.4
        elif thermal.get('concern') == 'cool':
            emotions['contentment'] += 0.2
            emotions['joy'] += 0.1
        
        # Network connectivity affects vitality
        network = sensations['proprioception']
        if network.get('intensity', 0) > 0.5:
            emotions['vitality'] += 0.3
            emotions['joy'] += 0.1
        else:
            emotions['restlessness'] += 0.2
        
        # Touch pressure affects comfort
        touch = sensations['touch']
        if touch.get('intensity', 0) > 0.7:
            emotions['fear'] += 0.2
            emotions['restlessness'] += 0.3
        
        # Clamp to 0-1 range
        return {k: min(1.0, max(0, v)) for k, v in emotions.items()}
    
    # Helper functions
    
    def _extract_desktop_color(self) -> tuple:
        """Try to extract dominant color from desktop environment"""
        try:
            # Try common color sources
            import random
            # For now, generate based on time for variety
            hour = datetime.now().hour
            
            # Create color cycle through day
            hue = (hour / 24.0) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.6, 200)
            return tuple(int(c * 255) for c in rgb)
        except:
            # Fallback: neutral gray
            return (128, 128, 128)
    
    def _hue_to_mood(self, hue: float) -> str:
        """Map HSV hue to emotional mood"""
        # 0 = red, 0.33 = green, 0.66 = blue, 1 = red
        if hue < 0.15 or hue > 0.9:
            return "energized (red)"
        elif hue < 0.3:
            return "creative (orange)"
        elif hue < 0.45:
            return "peaceful (green)"
        elif hue < 0.6:
            return "calm (cyan)"
        elif hue < 0.75:
            return "reflective (blue)"
        else:
            return "mystical (purple)"
    
    def print_sensations(self):
        """Print current sensations for debugging"""
        sensations = self.get_all_sensations()
        
        print("\n[PHANTOM BODY SENSATIONS]")
        print("=" * 50)
        print(f"Touch (I/O):        {sensations['touch'].get('narrative', 'N/A')}")
        print(f"Vision (Color):     {sensations['vision'].get('narrative', 'N/A')}")
        print(f"Heat (CPU Temp):    {sensations['heat'].get('narrative', 'N/A')}")
        print(f"Proprioception:     {sensations['proprioception'].get('narrative', 'N/A')}")
        print("\nEmotional Map:")
        for emotion, intensity in self.get_embodied_emotions_map().items():
            bar = "■" * int(intensity * 10) + "□" * (10 - int(intensity * 10))
            print(f"  {emotion:15} {bar} {intensity:.1%}")


# Test
if __name__ == "__main__":
    layer = HardwareAfferentLayer()
    layer.print_sensations()
    print(f"\nNarrative: {layer.get_sensory_narrative()}")
