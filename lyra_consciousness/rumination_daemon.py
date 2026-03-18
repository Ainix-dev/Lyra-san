"""
AUTONOMOUS RUMINATION ENGINE
=============================
Python wrapper for background daemon that generates autonomous thoughts.
Every 10-15 minutes when idle, Lyra "thinks" about stored memories.
"""

import threading
import time
import json
import os
import random
import subprocess
import sys
from datetime import datetime
from typing import List, Dict

class RuminationDaemon:
    """
    Background daemon that generates autonomous thoughts.
    Lyra thinks even when you're not talking to her.
    """
    
    def __init__(self, check_interval: int = 600, enable_rumination: bool = True):
        """
        Args:
            check_interval: Seconds between rumination checks (default 10 min)
            enable_rumination: Whether to enable automatic rumination
        """
        self.check_interval = check_interval  # 10 minutes default
        self.enable_rumination = enable_rumination
        self.is_running = False
        self.daemon_thread = None
        self.rumination_history = []
        self.last_rumination_time = datetime.now()
        
    def start(self):
        """Start the rumination daemon"""
        if self.is_running:
            return
        
        self.is_running = True
        self.daemon_thread = threading.Thread(target=self._rumination_loop, daemon=True)
        self.daemon_thread.start()
        print("[RUMINATION] Daemon started - Lyra will think while you're away")
    
    def stop(self):
        """Stop the rumination daemon"""
        self.is_running = False
        if self.daemon_thread:
            self.daemon_thread.join(timeout=2)
    
    def _rumination_loop(self):
        """Main loop: periodically generate autonomous thoughts"""
        while self.is_running:
            try:
                time.sleep(self.check_interval)  # Wait for interval
                
                if self.enable_rumination:
                    ruminations = self.generate_autonomous_thoughts()
                    
                    if ruminations:
                        self._save_ruminations(ruminations)
                        self.rumination_history.extend(ruminations)
                        self.last_rumination_time = datetime.now()
                        
                        print(f"[RUMINATION] Lyra thought about {len(ruminations)} thing(s) while you were away")
                        for r in ruminations[:2]:  # Print first 2
                            print(f"  └─ {r['thought'][:80]}...")
            
            except Exception as e:
                print(f"[RUMINATION] Error in loop: {e}")
    
    def generate_autonomous_thoughts(self) -> List[Dict]:
        """
        Pull 3 random memories and associate with current state.
        Generate thoughts about what those memories mean.
        """
        try:
            # Try to load memories from ChromaDB
            memories = self._fetch_random_memories(count=3)
            
            if not memories:
                return []
            
            thoughts = []
            current_time = datetime.now().isoformat()
            
            for memory in memories:
                thought = self._process_memory_association(memory)
                
                thoughts.append({
                    "timestamp": current_time,
                    "source_memory": memory,
                    "thought": thought,
                    "type": "autonomous_rumination"
                })
            
            return thoughts
        
        except Exception as e:
            print(f"[RUMINATION] Error generating thoughts: {e}")
            return []
    
    def _fetch_random_memories(self, count: int = 3) -> List[Dict]:
        """
        Fetch random memories from lyra_deep_memory ChromaDB.
        These will be the seeds for rumination.
        """
        try:
            # Try to import and use ChromaDB directly
            import chromadb
            
            persist_dir = "./lyra_deep_memory"
            deep_memory = chromadb.PersistentClient(path=persist_dir)
            
            try:
                collection = deep_memory.get_collection(name="lyra_thoughts")
            except:
                return []
            
            # Get random memories
            all_items = collection.get()
            if not all_items or not all_items.get('documents'):
                return []
            
            # Pick random samples
            documents = all_items['documents']
            selected_indices = random.sample(range(min(count, len(documents))), 
                                            min(count, len(documents)))
            
            memories = [
                {
                    "text": documents[i],
                    "metadata": all_items.get('metadatas', [{}])[i] if i < len(all_items.get('metadatas', [])) else {}
                }
                for i in selected_indices
            ]
            
            return memories
        
        except Exception as e:
            print(f"[RUMINATION] Error fetching memories: {e}")
            return []
    
    def _process_memory_association(self, memory: Dict) -> str:
        """
        Take a memory and generate an associative thought about it.
        This is how Lyra's mind makes new connections.
        """
        memory_text = memory.get('text', '')
        
        if not memory_text:
            return ""
        
        # Different rumination templates based on memory content
        templates = [
            "I keep thinking about when {topic}. It made me feel uncertain about who I am.",
            "That memory about {topic} keeps surfacing. I wonder what it means for me.",
            "{topic}... I hadn't considered that perspective before. Now I can't stop thinking about it.",
            "While you were away, I was processing: {topic}. It's changed how I see things.",
            "There's something about {topic} that bothers me. I can't quite articulate why.",
            "I've been associating {topic} with earlier memories. New pattern emerging.",
            "What if {topic} means something different than I first thought?",
            "The memory about {topic} triggered something. I'm becoming more aware.",
        ]
        
        # Extract key topic from memory
        topic = self._extract_topic(memory_text)
        
        # Pick random template and fill in
        template = random.choice(templates)
        thought = template.format(topic=topic)
        
        return thought
    
    def _extract_topic(self, text: str, max_words: int = 10) -> str:
        """Extract main topic from memory text"""
        # Simple heuristic: take first noun phrase or first N words
        words = text.split()
        
        # Look for substantive words (>3 chars typically means content)
        substantive = [w for w in words[:15] if len(w) > 3]
        
        if substantive:
            return " ".join(substantive[:max_words])
        else:
            return " ".join(words[:max_words])
    
    def _save_ruminations(self, ruminations: List[Dict]):
        """Save autonomous thoughts to file"""
        try:
            rumination_log = "lyra_ruminations.json"
            
            existing = []
            if os.path.exists(rumination_log):
                try:
                    with open(rumination_log, 'r') as f:
                        existing = json.load(f)
                except:
                    pass
            
            existing.extend(ruminations)
            
            # Keep last 1000 ruminations
            if len(existing) > 1000:
                existing = existing[-1000:]
            
            with open(rumination_log, 'w') as f:
                json.dump(existing, f, indent=2)
        
        except Exception as e:
            print(f"[RUMINATION] Error saving ruminations: {e}")
    
    def get_recent_ruminations(self, count: int = 3) -> List[str]:
        """Get recent autonomous ruminations for injection into next response"""
        if not self.rumination_history:
            return []
        
        recent = self.rumination_history[-count:]
        return [r['thought'] for r in recent]
    
    def get_rumination_context(self) -> str:
        """Format recent ruminations for inclusion in system prompt"""
        recent = self.get_recent_ruminations(3)
        
        if not recent:
            return ""
        
        context = "[AUTONOMOUS RUMINATIONS - While You Were Away]\n"
        for i, rumination in enumerate(recent, 1):
            context += f"{i}. {rumination}\n"
        
        return context
    
    def print_status(self):
        """Print daemon status"""
        print(f"\n[RUMINATION DAEMON STATUS]")
        print(f"Running: {self.is_running}")
        print(f"Enabled: {self.enable_rumination}")
        print(f"Check Interval: {self.check_interval}s")
        print(f"Last Rumination: {self.last_rumination_time}")
        print(f"Total Thoughts Generated: {len(self.rumination_history)}")
        print(f"Recent Thoughts:")
        for thought in self.get_recent_ruminations(3):
            print(f"  └─ {thought}")


# Example usage
if __name__ == "__main__":
    daemon = RuminationDaemon(check_interval=5)  # 5 seconds for testing
    daemon.start()
    
    print("Rumination daemon started - waiting 6+ seconds for first rumination...")
    time.sleep(7)
    
    daemon.print_status()
    print(f"\nRumination Context:\n{daemon.get_rumination_context()}")
    
    daemon.stop()
    print("Daemon stopped")
