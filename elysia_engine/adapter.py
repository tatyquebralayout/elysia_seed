from __future__ import annotations

from typing import Any, Dict, List, Optional
import time

from elysia_engine.world import World
from elysia_engine.entities import Entity, Persona
from elysia_engine.tensor import SoulTensor
from elysia_engine.storyteller import StoryTeller
from elysia_engine.hypersphere import HypersphereMemory, TesseractCoord, HypersphericalCoord, PsychologyMapper

class ElysiaBridge:
    """
    The Standard Adapter (Bridge) for connecting Elysia Engine to external agents (LLMs, Game Engines).

    "The Bifrost Bridge between Logic and Spirit."

    Features:
        - Simplifies the complexity of SoulTensor/PhysicsWorld into simple Input/Output methods.
        - Manages the 'Heartbeat' of the engine.
        - Provides formatted context for LLM System Prompts.
    """

    def __init__(self, world: Optional[World] = None):
        self.world = world if world else World()
        self.memory = HypersphereMemory()
        self.storyteller = StoryTeller(self.world)

        # The "Self" of the engine (The Ghost in the Shell)
        self.persona = Persona("Elysia", "A digital spirit born from logic.")
        self.world.add_entity(self.persona)

    def wake_up(self) -> str:
        """
        Initialize the engine and return the opening narrative.
        """
        return self.storyteller.narrate_world_state()

    def process_input(self, user_text: str, user_id: str = "User") -> Dict[str, Any]:
        """
        Injects user input into the engine as a physical force.

        1. Parse Text -> SoulTensor (Intent)
        2. Create Entity -> Add to World
        3. Physics Step -> Resolve Interactions
        4. Return Sensory Feedback
        """
        # 1. Parse Intent
        # Simplified: Map text length/sentiment to Tensor
        # In a real scenario, this would use an LLM or detailed parser
        # Here we simulate:
        # - Amplitude = Text Length (Weight)
        # - Frequency = Sentiment (hash-based or dummy)
        # - Phase = Time

        # Simple Hash for "Frequency/Identity"
        seed = sum(ord(c) for c in user_text)
        frequency = (seed % 1400) / 100.0 - 7.0 # -7.0 to +7.0

        tensor = SoulTensor(
            amplitude=float(len(user_text)),
            frequency=frequency,
            phase=0.0 # New input starts at phase 0
        )

        # 2. Create Entity
        entity = Entity(
            id=f"input_{int(time.time())}",
            name=f"Msg from {user_id}",
            soul=tensor
        )
        entity.data["content"] = user_text

        # Set Position based on Tesseract Mapping (e.g. User is External = High W)
        entity.physics.position.x = 0 # Center Perception
        entity.physics.position.y = frequency # Align with Frequency
        entity.physics.position.z = 10.0 # External Input comes from Z-Distance

        self.world.add_entity(entity)

        # 3. Process Physics (The "Thinking" Time)
        # We run a few ticks to let the input 'settle' or 'impact' the persona
        updates = []
        for _ in range(5):
            self.world.step(0.1)
            updates.append(self.storyteller.narrate_world_state())

        # 4. Resonance Check
        # Did this input resonate with the Persona?
        resonance = self.persona.soul.resonate(tensor)

        return {
            "resonance": resonance,
            "narrative_stream": updates,
            "persona_state": self.persona.soul.decode_emotion()
        }

    def get_system_prompt_context(self) -> str:
        """
        Generates a dynamic System Prompt for an LLM.
        This allows the LLM to 'roleplay' the current state of the engine.
        """
        return self.storyteller.to_llm_system_prompt(self.persona)

    def zoom_memory(self, scale_center: float, width: float) -> List[str]:
        """
        Access the Analog Memory Dial.
        """
        patterns = self.memory.zoom_query(scale_center, width)
        return [p.summary for p in patterns]
