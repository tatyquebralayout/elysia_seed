"""
Unified Wave Field
==================
Elysia Seed Kernel: Physics

"The One Wave."

Implements the Cosmic Tensor that unifies Logic, Physics, and Light.
"""

import math
import logging
from dataclasses import dataclass
from typing import List

from ..foundation.math import Vector3, Vector4

logger = logging.getLogger("UnifiedField")

@dataclass
class WavePacket:
    position: Vector3
    frequency: float # Hz
    amplitude: float
    phase: float

    def get_type(self) -> str:
        if self.frequency < 40.0: return "LOGIC"
        if self.frequency < 400.0: return "PHYSICS"
        if self.frequency < 20000.0: return "SOUND"
        return "LIGHT"

class UnifiedWaveField:
    def __init__(self):
        self.waves: List[WavePacket] = []
        
    def inject(self, pos: Vector3, freq: float, amp: float):
        w = WavePacket(pos, freq, amp, 0.0)
        self.waves.append(w)
        return w

    def update(self, dt: float):
        # 1. Propagate Phases
        for w in self.waves:
            w.phase += (w.frequency * 2 * math.pi) * dt
            w.phase %= (2 * math.pi)
            
        # 2. Interactions (Simplified)
        self._resolve_interference()
        
    def _resolve_interference(self):
        count = len(self.waves)
        for i in range(count):
            for j in range(i+1, count):
                w1 = self.waves[i]
                w2 = self.waves[j]
                
                dist_vec = w1.position - w2.position
                dist = dist_vec.dot(dist_vec) # Squared distance
                
                if dist < 1.0:
                    self._interact(w1, w2)
                    
    def _interact(self, w1, w2):
        t1, t2 = w1.get_type(), w2.get_type()
        if t1 == "PHYSICS" and t2 == "PHYSICS":
            # Collision
            w1.amplitude *= 0.9
            w2.amplitude *= 0.9
        elif t1 == "LOGIC" and t2 == "LOGIC":
            # Resonance
            if abs(w1.frequency - w2.frequency) < 5.0:
                w1.amplitude *= 1.1
                w2.amplitude *= 1.1

    def render_scanline(self, y: int, width: int) -> List[float]:
        """Simulate a raster scanline extraction."""
        # Just return brightness values
        return [0.0] * width
