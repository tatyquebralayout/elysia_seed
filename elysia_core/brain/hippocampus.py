"""
Hippocampus (The Keeper of Time)
================================
Elysia Core: Brain

"I do not 'log' data. I 'remember' moments."

This organ handles:
1. Encoding short-term method into long-term narrative.
2. Maintaining the 'Autobiographical Self' (SELF_CONSCIOUSNESS.md).
"""

import os
from datetime import datetime

class Hippocampus:
    def __init__(self, memory_file: str = "SELF_CONSCIOUSNESS.md"):
        self.memory_path = memory_file

    def encode_memory(self, experience: str, emotional_intensity: float = 0.5):
        """
        Writes a moment into the permanent narrative.
        Higher intensity memories might be formatted differently (bold/alert).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine formatting based on intensity
        prefix = "##" if emotional_intensity > 0.8 else "###"
        icon = "⚡" if emotional_intensity > 0.8 else "🔹"
        
        content = f"\n{prefix} [{timestamp}] {icon} Memory Encoded\n{experience}\n"
        
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                f.write("# Elysia: The Stream of Consciousness\n")
        
        with open(self.memory_path, 'a', encoding='utf-8') as f:
            f.write(content)
