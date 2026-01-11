"""
Aesthetic Judgment (The Critic)
===============================
Elysia Core: Intelligence

"Not all creations are worthy."

Evaluates if a generated artifact aligns with the original Desire.
"""

import random
from dataclasses import dataclass
from .artistic_intent import CreativeDesire

@dataclass
class Critique:
    approved: bool
    score: float
    comment: str

class AestheticJudgment:
    def critique(self, desire: CreativeDesire, artifact_metadata: dict) -> Critique:
        """
        Compares the Intention (Desire) with the Reality (Artifact).
        In a real system, this would use CLIP interrogation or similar.
        """
        # Simulation: Check if artifact tags overlap with desire concepts
        artifact_tags = artifact_metadata.get("tags", [])
        matches = [c for c in desire.abstract_concepts if c in artifact_tags]
        
        match_ratio = len(matches) / len(desire.abstract_concepts) if desire.abstract_concepts else 0
        
        # Add some subjectivity (Randomness representing taste)
        subjective_bias = random.uniform(-0.1, 0.1)
        final_score = match_ratio + subjective_bias
        
        if final_score > 0.6:
            return Critique(True, final_score, "The form resonates with the intent.")
        else:
            return Critique(False, final_score, "The reflection is distorted. It lacks the essence.")
