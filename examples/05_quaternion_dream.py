import sys
import math
import random
import time
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from elysia_engine import Entity, World
from elysia_engine.physics import PhysicsWorld
from elysia_engine.tensor import SoulTensor
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.dream import DreamSystem
from elysia_engine.oracle import Oracle
from elysia_engine.math_utils import Vector3

def run_simulation():
    print("--- INITIALIZING QUANTUM DREAM SIMULATION ---")

    # 1. Setup Universe
    physics = PhysicsWorld()
    physics.gravity_constant = 2.0

    world = World(physics=physics)
    global_mind = GlobalConsciousness(physics=physics)
    dream_sys = DreamSystem()

    world.add_system(global_mind)
    world.add_system(dream_sys)

    print("[System] Global Consciousness & Dream System Online.")

    # 2. Create a Crisis (High Entropy)
    # A chaotic swarm of entities with random phases
    print("[Setup] Creating Chaotic Swarm (Entropy Injection)...")
    for i in range(10):
        soul = SoulTensor(
            amplitude=10.0,
            frequency=random.uniform(10, 100),
            phase=random.uniform(0, 6.28),
            spin=random.choice([1.0, -1.0])
        )
        ent = Entity(id=f"chaos_{i}", soul=soul)
        # Scattered positions
        ent.physics.position = Vector3(
            random.uniform(-20, 20),
            random.uniform(-20, 20),
            random.uniform(-5, 5)
        )
        world.add_entity(ent)
        physics.register_entity(ent)

    # 3. Run Simulation
    print("\n--- STARTING TIME FLOW ---")
    for i in range(1, 50):
        world.step(dt=1.0)

        # Check if Dream happened (by checking Torsion)
        if i % 5 == 0:
            msg = Oracle.consult_akashic(global_mind)
            torsion = physics.spacetime_torsion
            is_twisted = abs(torsion.w - 1.0) > 0.01

            status = "STANDARD"
            if is_twisted:
                status = "ROTATED (Dream Logic Applied)"

            print(f"[Tick {i:02d}] Global: {msg}")
            print(f"          Spacetime Metric: {status}")
            if is_twisted:
                print(f"          Torsion: {torsion}")

        time.sleep(0.01)

if __name__ == "__main__":
    run_simulation()
