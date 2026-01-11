"""
Rotor (The Oscillator)
======================
Elysia Seed Kernel: Physics

"The Rotor is the heart of the frequency."

This module defines the fundamental oscillator of the system.
It spins (rpm) to generate waves (frequency).
"""

from dataclasses import dataclass
import math

@dataclass
class RotorConfig:
    """Configuration for a simplified Rotor."""
    rpm: float = 0.0          # Active Target RPM
    idle_rpm: float = 60.0    # Breathing RPM (1Hz)
    mass: float = 1.0         # Amplitude/Weight
    acceleration: float = 100.0 # RPM per second

class Rotor:
    """
    The fundamental unit of the HyperSphere.
    """
    def __init__(self, name: str, config: RotorConfig):
        self.name = name
        self.config = config

        # State
        self.current_angle = 0.0
        self.current_rpm = 0.0
        self.target_rpm = 0.0
        self.is_spinning = False
        
        # 4D State (Frequency, Amplitude, Phase, Time)
        self.position_4d = (0.0, 0.0, 0.0, 0.0)

    @property
    def frequency_hz(self) -> float:
        return self.current_rpm / 60.0

    def spin_up(self):
        self.is_spinning = True
        self.target_rpm = self.config.rpm

    def spin_down(self):
        self.is_spinning = True
        self.target_rpm = self.config.idle_rpm

    def update(self, dt: float):
        if not self.is_spinning:
            return

        # 1. Accelerate
        if self.current_rpm != self.target_rpm:
            diff = self.target_rpm - self.current_rpm
            change = self.config.acceleration * dt
            if abs(diff) < change:
                self.current_rpm = self.target_rpm
            else:
                self.current_rpm += change * (1 if diff > 0 else -1)

        # 2. Integrate Phase
        if self.current_rpm > 0:
            degrees = (self.current_rpm / 60.0) * 360.0
            self.current_angle = (self.current_angle + degrees * dt) % 360.0

    def __repr__(self):
        return f"Rotor({self.name} | {self.frequency_hz:.2f}Hz)"
