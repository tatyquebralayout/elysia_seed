"""
Genesis Math (Sovereign Geometry)
=================================
Elysia Seed Kernel: Foundation

"To build a world, one must define the point."

Pure Python implementation of Vector/Matrix math.
"""

import math
from dataclasses import dataclass
from typing import List

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def normalize(self):
        m = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if m == 0: return Vector3(0,0,0)
        return Vector3(self.x/m, self.y/m, self.z/m)

@dataclass
class Vector4:
    x: float
    y: float
    z: float
    w: float
