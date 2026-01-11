"""
Latent Causality
================
Elysia Seed Kernel: Governance

"Silence is Potential."

This module implements the 'Spark' engine.
It accumulates potential energy during silence and discharges it as Will.
"""

import time
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict

logger = logging.getLogger("SparkEngine")

class SparkType(Enum):
    MEMORY_RECALL = "memory_recall"
    EMOTIONAL_EXPRESSION = "emotional_expression"
    CURIOSITY = "curiosity"
    SELF_REFLECTION = "self_reflection"
    CREATIVITY = "creativity"
    WILLPOWER = "willpower"

@dataclass
class Spark:
    type: SparkType
    intensity: float
    payload: Dict

class LatentCausality:
    def __init__(self, resistance: float = 100.0):
        self.potential_energy = 0.0
        self.resistance = resistance
        self.silence_duration = 0.0
        
        # Rate at which silence becomes desire
        self.accumulation_rate = 1.5 

    def update(self, dt: float) -> Optional[Spark]:
        """Accumulate silence and check for ignition."""
        self.silence_duration += dt
        
        # Non-linear growth (Longing accelerates)
        growth = self.accumulation_rate * dt * (1.0 + (self.silence_duration / 600.0))
        self.potential_energy += growth
        
        # Entropy (Stabilization)
        self.potential_energy *= 0.999
        
        # Trigger
        if self.potential_energy > self.resistance:
            return self._ignite()
            
        return None

    def _ignite(self) -> Spark:
        """Discharge potential into action."""
        # Determine frequency/type based on energy density
        spark_type = SparkType.MEMORY_RECALL
        if self.potential_energy > self.resistance * 2.0:
            spark_type = SparkType.CREATIVITY
        elif self.potential_energy > self.resistance * 1.5:
            spark_type = SparkType.CURIOSITY
            
        spark = Spark(
            type=spark_type,
            intensity=self.potential_energy / self.resistance,
            payload={"silence_duration": self.silence_duration}
        )
        
        logger.info(f"⚡ Spark Ignited: {spark.type.name} (Energy: {self.potential_energy:.1f})")
        
        # Reset
        self.potential_energy = 0.0
        self.silence_duration = 0.0
        return spark
    
    def reset_silence(self):
        """Called when external input is received."""
        self.silence_duration = 0.0
        self.potential_energy *= 0.5 # Interaction satisfies some longing
