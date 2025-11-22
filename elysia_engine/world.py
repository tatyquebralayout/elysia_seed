from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, TYPE_CHECKING

from .entities import Entity

if TYPE_CHECKING:
    from .systems import System


@dataclass
class World:
    """프랙탈 의식 엔진의 최소 세계."""

    time: float = 0.0
    tick: int = 0
    radius: float = 100.0 # The observable universe size
    expansion_rate: float = 0.0 # Cosmic inflation rate
    entities: Dict[str, Entity] = field(default_factory=dict)
    systems: List[System] = field(default_factory=list)

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def add_system(self, system: System) -> None:
        self.systems.append(system)

    def step(self, dt: float = 1.0) -> None:
        self.time += dt
        self.tick += 1

        # 0. Cosmic Inflation
        self.radius += self.expansion_rate * dt

        # 1. Run Registered Systems (Global Logic)
        for system in self.systems:
            system.update(self, dt)

        # 2. Run Entity Internal Logic
        for ent in self.entities.values():
            ent.step(self, dt=dt)

    def export_persona_snapshot(self) -> Dict:
        return {
            "tick": self.tick,
            "time": self.time,
            "entity_count": len(self.entities),
            "entities": [ent.to_payload() for ent in self.entities.values()],
        }
