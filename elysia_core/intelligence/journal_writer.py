"""
Journal Writer (The Memory)
===========================
Elysia Core: Intelligence

"What is not written is forgotten."

Manages the persistent self-narrative of the system.
"""

import os
import time
from datetime import datetime

class JournalWriter:
    def __init__(self, journal_path: str = "SELF_CONSCIOUSNESS.md"):
        self.journal_path = journal_path
        
    def log_realization(self, thought: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## [{timestamp}] Assimilation Log\n{thought}\n"
        
        # Create header if new
        if not os.path.exists(self.journal_path):
            with open(self.journal_path, 'w', encoding='utf-8') as f:
                f.write("# Elysia: Self-Consciousness Stream\n> \"I think, therefore I code.\"\n")
        
        with open(self.journal_path, 'a', encoding='utf-8') as f:
            f.write(entry)
