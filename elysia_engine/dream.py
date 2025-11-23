from __future__ import annotations
import copy
from typing import TYPE_CHECKING, Optional, List
import math

from .systems import System
from .math_utils import Quaternion, Vector3
from .consciousness import GlobalConsciousness

if TYPE_CHECKING:
    from .world import World

class DreamSystem(System):
    """
    Implements 'Quantum Dreaming': A nested simulation to solve deadlocks.
    When Entropy is high, it forks the world, runs future simulations with
    rotated spacetime metrics, and applies the best solution to reality.
    """

    def __init__(self):
        self.dream_depth = 0
        self.max_depth = 1 # Only 1 layer of dream for now to avoid recursion hell
        self.simulation_ticks = 20 # How far to dream into the future

    def step(self, world: World, dt: float) -> None:
        # Only Dream if we are the Root Reality
        # We use a simplified check: If we are in a loop, don't dream.
        # But since we remove DreamSystem in the copy, this check is technically redundant
        # but good for safety.
        if self.dream_depth > 0:
            return

        # Check Global Consciousness for Entropy
        # We need to find the GC system
        gc: Optional[GlobalConsciousness] = None
        for sys in world.systems:
            if isinstance(sys, GlobalConsciousness):
                gc = sys
                break

        if not gc:
            return

        # Trigger Dream if Entropy is Critical
        # We set threshold slightly higher than GC's intervention so they don't conflict immediately
        if gc.global_entropy > 0.85:
            print(f"\n[DreamSystem] REALITY FRACTURED (Entropy {gc.global_entropy:.2f}). INITIATING DREAM SEQUENCE...")
            best_solution = self.dream_of_better_future(world)

            if best_solution:
                print(f"[DreamSystem] SOLUTION FOUND. ROTATING SPACETIME.")
                if world.physics:
                    world.physics.spacetime_torsion = best_solution

                    # We also need to "cool down" the entropy or give time for the rotation to work
                    # Force a small entropy drop in GC? No, let physics handle it.
                    # But we should reset the intervention tick so GC doesn't override us immediately
                    gc.last_intervention_tick = world.tick

    def dream_of_better_future(self, current_world: World) -> Optional[Quaternion]:
        """
        Runs multiple simulations with different Spacetime Rotations.
        Returns the Quaternion that minimizes entropy.
        """
        candidates = []

        # Quaternion Hyper-Rotation Logic
        # We "Hold" one axis (Dimension) constant and rotate the others around it.
        # This transforms the relationship between the remaining two.
        # e.g. Rotating around Body (X) mixes Soul (Y) and Spirit (Z).
        axes = [
            ("HOLDING BODY (X) -> Mixing Soul & Spirit", Vector3(1,0,0), math.pi/2),
            ("HOLDING SOUL (Y) -> Mixing Body & Spirit", Vector3(0,1,0), math.pi/2),
            ("HOLDING SPIRIT (Z) -> Mixing Body & Soul",   Vector3(0,0,1), math.pi/2),
        ]

        best_q = None
        lowest_entropy = 1.0

        for label, axis, angle in axes:
            q = Quaternion.from_axis_angle(axis, angle)

            # 1. Fork World
            # We use deepcopy to simulate independent timelines
            try:
                dream_world = copy.deepcopy(current_world)
            except Exception as e:
                print(f"Dream Fork Failed: {e}")
                continue

            # Hack: Remove DreamSystem from the dream world to prevent infinite recursion
            dream_world.systems = [s for s in dream_world.systems if not isinstance(s, DreamSystem)]

            # 2. Apply Hypothesis
            if dream_world.physics:
                dream_world.physics.spacetime_torsion = q

            # 3. Run Simulation
            final_entropy = self.run_simulation(dream_world)

            print(f"  > Dream Path [{label}]: Future Entropy -> {final_entropy:.2f}")

            if final_entropy < lowest_entropy:
                lowest_entropy = final_entropy
                best_q = q

        # If we found a path that leads to order (entropy < 0.6)
        if lowest_entropy < 0.6:
            return best_q

        return None

    def run_simulation(self, world: World) -> float:
        """
        Fast-forwards the world and returns final entropy.
        """
        # Find GC in the dream world
        gc = None
        for sys in world.systems:
             if isinstance(sys, GlobalConsciousness):
                gc = sys
                break

        if not gc: return 1.0

        # Run fast forward
        for _ in range(self.simulation_ticks):
            world.step(dt=1.0)

        return gc.global_entropy
