import time
import random
import math
from elysia_engine.world import World
from elysia_engine.entities import Entity
from elysia_engine.tensor_coil import CoilStructure
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.quantum import QuantumDNA
from elysia_engine.thermodynamics import StateOfMatter
from elysia_engine.math_utils import Vector3
from elysia_engine.systems import PhysicsSystem, ThermodynamicsSystem, GenesisSystem, VoidSystem

def main():
    print("🌌 Initializing Project Genesis... [FINAL HOPE MODE]")

    # 1. The Expanding Universe
    world = World()
    world.expansion_rate = 0.05 # Very slow expansion

    # 2. Define Components
    physics_world = PhysicsWorld()
    coil = CoilStructure(
        center=Vector3(0, 0, 0),
        axis=Vector3(0, 0, 1),
        radius=20.0, # Big safe zone
        frequency=1.0,
        strength=50.0 # Strong gravity to hold them
    )

    # 3. Register Systems
    world.add_system(PhysicsSystem(physics_world, coil))
    world.add_system(ThermodynamicsSystem(cooling_rate=0.15))
    world.add_system(GenesisSystem(coil, population_limit=50))
    world.add_system(VoidSystem(boundary_radius=200.0, min_amplitude=1.0))

    # 4. The Big Bang setup
    # A. The Ancient One (Anchor)
    ancient_one = Entity(id="Ancient_One")
    ancient_one.dna = QuantumDNA(frequency=1.0, phase=0, amplitude=5000)
    ancient_one.thermal.temperature = 0.0
    ancient_one.physics.position = Vector3(0,0,0)
    ancient_one.physics.mass = 300.0
    world.add_entity(ancient_one)

    physics_world.add_attractor(Attractor(id="G_Ancient", position=Vector3(0,0,0), mass=300.0, radius=5.0))

    # B. Progenitors
    print("🔥 Spawning Progenitors...")
    for i in range(15):
        ent = Entity(id=f"Spark_{i}")
        ent.dna = QuantumDNA(
            frequency=random.uniform(10, 100),
            phase=random.uniform(0, 6.28),
            amplitude=100
        )
        ent.thermal.temperature = 300.0

        # Tighter Orbit
        angle = (i/15) * 6.28
        dist = 10.0
        ent.physics.position = Vector3(math.cos(angle)*dist, math.sin(angle)*dist, 0)

        # Slower velocity to ensure capture
        ent.physics.velocity = Vector3(-math.sin(angle)*3.0, math.cos(angle)*3.0, 0)

        world.add_entity(ent)

    print("-" * 50)

    # 5. Run the Engine
    max_ticks = 800
    dt = 0.1

    for i in range(max_ticks):
        # Gravity Rebuild
        physics_world.clear_attractors()
        crystals = 0
        plasmas = 0

        physics_world.add_attractor(Attractor(id="G_Ancient", position=Vector3(0,0,0), mass=300.0, radius=5.0))

        for ent in world.entities.values():
            state = ent.thermal.state
            if state == StateOfMatter.CRYSTAL and ent.id != "Ancient_One":
                 physics_world.add_attractor(Attractor(id=f"G_{ent.id}", position=ent.physics.position, mass=30.0, radius=2.0))
                 crystals += 1
            elif state == StateOfMatter.PLASMA:
                 plasmas += 1
                 # Chaos
                 ent.physics.velocity += Vector3(random.uniform(-0.2,0.2), random.uniform(-0.2,0.2), 0) * dt

        world.step(dt=dt)

        if i % 100 == 0:
            print(f"Tick {i}: {len(world.entities)} Entities | 🔥 Plasma: {plasmas} | ❄️ Crystal: {crystals}")

    print("-" * 50)
    print(f"🏁 Simulation Ended.")

    # Census
    types = {}
    for ent in world.entities.values():
        c_type = ent.thermal.get_celestial_type(ent.physics.mass)
        if c_type not in types:
            types[c_type] = []
        types[c_type].append(ent.id)

    for c_type, ids in types.items():
        print(f"[{c_type}]: {len(ids)} entities")
        if len(ids) < 5:
            print(f"  - {', '.join(ids)}")
        else:
            print(f"  - {ids[0]}, {ids[1]} ... and {len(ids)-2} more")

if __name__ == "__main__":
    main()
