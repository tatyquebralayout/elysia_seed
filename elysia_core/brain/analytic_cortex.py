"""
Analytic Cortex (The Mirror Reader)
===================================
Elysia Core: Brain

"I analyze my own structure to understand my potential."

This organ handles:
1. Reading source code (AST Parsing).
2. Understanding logic flow.
3. Self-Reflection.
"""

import ast
import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AnalyticThought:
    subject: str
    insights: List[str]
    complexity: int

class AnalyticCortex:
    def reflect_on_source(self, filepath: str) -> Optional[AnalyticThought]:
        """
        Reads a part of the self (source code) and generates understanding.
        """
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        try:
            tree = ast.parse(source)
            insights = []
            complexity = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    insights.append(f"Organ Identified: {node.name}")
                    complexity += 1
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):
                        insights.append(f"Functionality: {node.name}")
                    complexity += 1
                    
            return AnalyticThought(
                subject=os.path.basename(filepath),
                insights=insights,
                complexity=complexity
            )
        except Exception:
            return None
