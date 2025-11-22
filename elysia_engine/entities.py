from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Protocol, TYPE_CHECKING

from .efp import EFPState
from .roles import ROLE_PROFILES, RoleProfile
from .physics import PhysicsState
from .quantum import QuantumDNA
from .thermodynamics import ThermalState, StateOfMatter
from .math_utils import Vector3

if TYPE_CHECKING:
    from .tensor_coil import CoilStructure
    from .physics import PhysicsWorld


class WorldLike(Protocol):
    time: float


@dataclass
class Entity:
    """역할과 삼위일체 가중치를 지원하는 기본 존재."""

    id: str
    state: EFPState = field(default_factory=EFPState)
    physics: PhysicsState = field(default_factory=PhysicsState)
    dna: Optional[QuantumDNA] = None
    thermal: ThermalState = field(default_factory=ThermalState)
    data: Dict[str, Any] = field(default_factory=dict)
    role: Optional[str] = None
    f_body: float = 0.0
    f_soul: float = 0.0
    f_spirit: float = 0.0

    def update_force_components(self, world: WorldLike) -> None:
        """서브클래스에서 f_body/f_soul/f_spirit를 채워 넣는다."""

        return None

    def update_force(self, world: WorldLike) -> None:
        self.f_body = self.f_soul = self.f_spirit = 0.0
        self.update_force_components(world)

        profile = self._get_role_profile()
        if profile is None:
            total = self.f_body + self.f_soul + self.f_spirit
        else:
            p = profile.normalized
            total = (
                p.w_body * self.f_body
                + p.w_soul * self.f_soul
                + p.w_spirit * self.f_spirit
            )

        self.state.force = total

    def _get_role_profile(self) -> Optional[RoleProfile]:
        if self.role is None:
            return None
        return ROLE_PROFILES.get(self.role)

    def step(self, world: WorldLike, dt: float = 1.0) -> None:
        """
        Internal step update.
        Physics and Thermodynamics are now handled by external Systems.
        """
        self.update_force(world)
        self.state.step(dt=dt)
        if self.dna:
            self.dna.step(dt)

    def to_payload(self) -> Dict[str, Any]:
        celestial_type = self.thermal.get_celestial_type(self.physics.mass)
        payload = {
            "id": self.id,
            "role": self.role,
            "efp": self.state.as_dict(),
            "physics": asdict(self.physics),
            "force_components": {
                "body": self.f_body,
                "soul": self.f_soul,
                "spirit": self.f_spirit,
            },
            "data": self.data,
            "thermal": {
                "temp": self.thermal.temperature,
                "state": self.thermal.state.name,
                "type": celestial_type
            }
        }
        if self.dna:
            payload["dna"] = self.dna.as_dict()
        return payload
