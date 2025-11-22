from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World
    from .tensor_coil import CoilStructure
    from .physics import PhysicsWorld
    from .thermodynamics import StateOfMatter


class System(ABC):
    """
    Base class for all Logic Systems in the Elysia Engine.
    Users can plug these into the World to enable features.
    """
    @abstractmethod
    def update(self, world: World, dt: float) -> None:
        pass


class PhysicsSystem(System):
    """
    Handles Movement, Gravity, and Coil Acceleration.
    """
    def __init__(self, physics_world: PhysicsWorld, coil: CoilStructure | None = None):
        self.physics_world = physics_world
        self.coil = coil

    def update(self, world: World, dt: float) -> None:
        # Dynamic Gravity Update (Optional: could be its own system, but simple here)
        # Rebuild attractors from Crystal Entities if needed
        # For simplicity in this lightweight engine, we assume the physics_world
        # is managed externally or we just apply what's there.

        for ent in world.entities.values():
            # Check if frozen (Thermodynamics check, ideally decoupled but needed for physics)
            if hasattr(ent, 'thermal') and ent.thermal.state.name == 'CRYSTAL':
                ent.physics.velocity.x = 0
                ent.physics.velocity.y = 0
                ent.physics.velocity.z = 0
                continue

            # 1. Coil Force
            if self.coil:
                self.coil.railgun_accelerate(ent.physics, dt)

            # 2. Gravity
            gravity = self.physics_world.get_net_force(ent.physics.position)
            ent.physics.apply_force(gravity, dt)

            # 3. Integration
            ent.physics.step(dt)


class ThermodynamicsSystem(System):
    """
    Handles Temperature, Entropy, and States of Matter.
    """
    def __init__(self, cooling_rate: float = 0.1):
        self.cooling_rate = cooling_rate

    def update(self, world: World, dt: float) -> None:
        for ent in world.entities.values():
            if hasattr(ent, 'thermal'):
                # 1. Natural Cooling (Entropy)
                ent.thermal.cool_down(self.cooling_rate * dt)

                # 2. State Update
                ent.thermal.update_state()


class GenesisSystem(System):
    """
    Handles Life Creation (Quantum Breeding).
    Requires a Coil to act as the 'Womb'.
    """
    def __init__(self, coil: CoilStructure, population_limit: int = 50):
        self.coil = coil
        self.population_limit = population_limit

    def update(self, world: World, dt: float) -> None:
        # Only breed if we have space
        if len(world.entities) >= self.population_limit:
            return

        current_entities = list(world.entities.values())
        children = self.coil.incubate(current_entities, world.time)

        for child in children:
            if len(world.entities) < self.population_limit:
                # New thoughts are hot!
                child.thermal.temperature = 150.0
                world.add_entity(child)
                # print(f"✨ Genesis: {child.id} born.")


class VoidSystem(System):
    """
    The Great Filter.
    Removes entities that are too weak (low energy) or too far (lost in space).
    """
    def __init__(self, boundary_radius: float = 100.0, min_amplitude: float = 1.0):
        self.boundary_radius = boundary_radius
        self.min_amplitude = min_amplitude

    def update(self, world: World, dt: float) -> None:
        to_remove = []

        for ent in world.entities.values():
            # 1. Check Bounds
            if ent.physics.position.magnitude > self.boundary_radius:
                to_remove.append((ent.id, "Lost in Space"))
                continue

            # 2. Check DNA Amplitude (Energy of Consciousness)
            if ent.dna and ent.dna.amplitude < self.min_amplitude:
                to_remove.append((ent.id, "Faded Away"))
                continue

        # Execute The Void
        for eid, reason in to_remove:
            if eid in world.entities:
                del world.entities[eid]
                # print(f"🌑 The Void claimed {eid}: {reason}")
