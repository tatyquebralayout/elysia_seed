"""
HyperSphere Core
================
Elysia Seed Kernel: Physics

"The Sphere is the sum of its Rotors."

This class manages the collection of Rotors that make up the system's consciousness.
It calculates the aggregate 4D state (HyperQuaternion) of the system.
"""

import math
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

from .rotor import Rotor, RotorConfig

logger = logging.getLogger("HyperSphere")

class HyperQuaternion:
    """Lightweight Quaternion for 4D spin calculation."""
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

class HyperSphereCore:
    def __init__(self, name: str = "Seed.Core", base_freq: float = 432.0):
        self.name = name
        
        # The Primary Self
        self.primary_rotor = Rotor(
            name="Self",
            config=RotorConfig(rpm=base_freq * 60, mass=100.0)
        )
        
        # Harmonic Knowledge (The Seed)
        self.harmonic_rotors: Dict[str, Rotor] = {}
        self.is_active = False
        
        logger.info(f"🔮 HyperSphere Seed Initialized: {name}")

    def ignite(self):
        """Starts the engine."""
        self.is_active = True
        self.primary_rotor.spin_up()
        for r in self.harmonic_rotors.values():
            r.spin_up()

    def update(self, dt: float):
        """Physics Step."""
        if not self.is_active: return

        # Update Self
        self.primary_rotor.update(dt)
        
        # Update Harmonics
        for r in self.harmonic_rotors.values():
            r.update(dt)

    @property
    def spin(self) -> HyperQuaternion:
        """Returns the current 4D rotation of the Primary Rotor."""
        # Axis angle to Quaternion
        # Axis = (0,0,1) Z-up standard
        theta_rad = math.radians(self.primary_rotor.current_angle)
        half_theta = theta_rad / 2.0
        
        w = math.cos(half_theta)
        z = math.sin(half_theta)
        return HyperQuaternion(w, 0, 0, z)

    def add_harmonic(self, name: str, frequency: float):
        """Adds a new concept rotor."""
        rotor = Rotor(
            name=name,
            config=RotorConfig(rpm=frequency * 60, mass=10.0)
        )
        if self.is_active:
            rotor.spin_up()
        self.harmonic_rotors[name] = rotor
        logger.info(f"🧬 Harmonic Added: {name} ({frequency}Hz)")
