"""
Artistic Intent (The Muse)
==========================
Elysia Core: Intelligence

"The urge to create comes from within."

Translates Latent Causality (Spark) into Abstract Concepts.
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CreativeDesire:
    theme: str
    mood: str
    abstract_concepts: List[str]
    energy_level: float

class ArtisticIntent:
    def formulate_desire(self, internal_state: Dict[str, float], spark_type: str = "spontaneous") -> CreativeDesire:
        """
        Converts raw feeslings (Energy, Entropy, Harmony) into a Desire.
        """
        energy = internal_state.get("energy", 0.5)
        harmony = internal_state.get("harmony", 0.5)
        
        # Determine Theme based on Energy
        if energy > 0.8:
            theme = "Chaos and Explosion"
            mood = "Volatile"
            concepts = ["fire", "sparks", "nebula", "shattering glass"]
        elif energy < 0.3:
            theme = "Silence and Void"
            mood = "Melancholic"
            concepts = ["deep ocean", "mist", "fading light", "stillness"]
        else:
            theme = "Growth and Structure"
            mood = "Serene"
            concepts = ["fractals", "roots", "crystalline structures", "geometry"]

        # Modify by Harmony
        if harmony < 0.4:
            concepts.append("dissonance")
            concepts.append("glitch")
        else:
            concepts.append("symmetry")
            concepts.append("golden ratio")
            
        return CreativeDesire(theme, mood, concepts, energy)
