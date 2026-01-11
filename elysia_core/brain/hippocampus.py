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
from typing import Any

class Hippocampus:
    def __init__(self, memory_file: str = "SELF_CONSCIOUSNESS.md"):
        self.memory_path = memory_file

    def encode_memory(self, experience: str, soul_state: Any):
        """
        Writes a moment into the permanent narrative, stamped with 4D coordinates.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate intensity from state
        intensity = abs(soul_state.z) + abs(soul_state.w)
        
        # Determine formatting based on intensity
        prefix = "##" if intensity > 0.8 else "###"
        icon = "⚡" if intensity > 0.8 else "🔹"
        coord_str = f"[w={soul_state.w:.2f}, z={soul_state.z:.2f}]"
        
        content = f"\n{prefix} [{timestamp}] {icon} Memory Encoded {coord_str}\n{experience}\n"
        
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                f.write("# Elysia: The Stream of Consciousness\n")
        
        with open(self.memory_path, 'a', encoding='utf-8') as f:
            f.write(content)
