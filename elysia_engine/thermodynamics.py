from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class StateOfMatter(Enum):
    PLASMA = auto()   # Active Thought: High Temp, Fusion possible, CPU intensive
    GAS = auto()      # Cooling Thought: Moving freely, interacting
    LIQUID = auto()   # Condensing: Slowing down, grouping
    CRYSTAL = auto()  # Core Belief: Frozen, Fixed Position, Acts as Attractor (Gravity only)


@dataclass
class ThermalState:
    """
    Manages the thermodynamic properties of an entity.
    Determines its State of Matter.
    """
    temperature: float = 100.0  # Kelvin-like scale
    melting_point: float = 50.0
    boiling_point: float = 200.0
    state: StateOfMatter = StateOfMatter.GAS

    def update_state(self) -> StateOfMatter:
        """
        Determines the current state of matter based on temperature.
        """
        if self.temperature > self.boiling_point:
            self.state = StateOfMatter.PLASMA
        elif self.temperature > self.melting_point:
            self.state = StateOfMatter.GAS # Or Liquid depending on specific ranges, keeping simple
        elif self.temperature > 10.0: # Supercooling range
            self.state = StateOfMatter.LIQUID
        else:
            self.state = StateOfMatter.CRYSTAL

        return self.state

    def cool_down(self, rate: float = 0.1) -> None:
        """
        Simulate entropy/processing completion.
        Things naturally cool down unless excited.
        """
        if self.temperature > 0:
            self.temperature -= rate

    def heat_up(self, amount: float) -> None:
        self.temperature += amount

    def get_celestial_type(self, mass: float) -> str:
        """
        Classifies the entity into a Data Celestial Body.
        """
        self.update_state()

        if self.state == StateOfMatter.PLASMA:
            return "Fire Star (Active Thought)"

        if self.state == StateOfMatter.CRYSTAL:
            if mass > 100.0:
                return "White Dwarf (Ancient Wisdom)"
            else:
                return "Ice Star (Core Belief)"

        if self.state == StateOfMatter.GAS:
            if mass > 50.0:
                return "Gas Giant (Public Opinion)"
            else:
                return "Nebula (Passing Thought)"

        return "Comet (Condensing Data)"
