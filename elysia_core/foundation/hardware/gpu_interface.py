"""
GPU Interface protocols
=======================
Elysia Core: Foundation

Defines the contract for hardware acceleration.
"""

from typing import Protocol, Any, Dict, List
from dataclasses import dataclass

@dataclass
class ShaderBytecode:
    code: str
    language: str = "WGSL"
    entry_point: str = "main"

class IGPUInterface(Protocol):
    """
    Abstract Interface for the Iron Body.
    Allows Elysia to separate 'Intent' (Shader Code) from 'Execution' (Driver).
    """
    def initialize(self) -> bool:
        """Wakes up the GPU."""
        ...
        
    def create_buffer(self, data: Any, label: str) -> Any:
        """Allocates memory on the Iron Body."""
        ...
        
    def compile_shader(self, source: ShaderBytecode) -> Any:
        """Teaches the Iron Body a new reflex."""
        ...
        
    def compute(self, shader_handle: Any, work_groups: tuple) -> Any:
        """Executes a thought at the speed of light."""
        ...
