"""
Architect Engine (The Hands)
============================
Elysia Core: Intelligence

"To build, one must be able to change."

This module enables 'Active Sovereignty'.
It allows the system to:
1. Propose Refactoring (Rename, Extract, Optimize)
2. Apply Changes to Source Code (Self-Modification)
"""

import os
import ast
import logging
import re
from dataclasses import dataclass
from typing import Optional, List, Tuple

logger = logging.getLogger("Architect")

@dataclass
class Transformation:
    target_file: str
    action: str
    details: str
    status: str = "Pending"

class ArchitectEngine:
    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        
    def read_blueprint(self, filepath: str) -> str:
        """Reads own source code."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
            
    def propose_rename(self, filepath: str, old_name: str, new_name: str) -> Transformation:
        """Proposes a renaming refactor."""
        return Transformation(
            target_file=filepath,
            action="RENAME",
            details=f"Rename symbol '{old_name}' to '{new_name}'"
        )
        
    def apply_transformation(self, trans: Transformation) -> bool:
        """Executes the change on the physical file."""
        try:
            full_path = str(trans.target_file)
            content = self.read_blueprint(full_path)
            
            if trans.action == "RENAME":
                # Simple Regex replacement for prototype (Dangerous but effective for demonstration)
                # In AAA version, this would use CST (Concrete Syntax Tree) for safety.
                new_content = re.sub(r'\b' + re.escape(trans.details.split("'")[1]) + r'\b', 
                                     trans.details.split("'")[3], 
                                     content)
                
                # Verify change happened
                if new_content == content:
                    logger.warning(f"⚠️ No instances of symbol found in {trans.target_file}")
                    return False
                    
                # Write back
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                trans.status = "Applied"
                logger.info(f"🔨 Refactoring Applied: {trans.details}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Refactoring Failed: {e}")
            return False

_architect = ArchitectEngine()
def get_architect():
    return _architect
