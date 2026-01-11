"""
Hypersphere Memory (경량화)
==========================
Elysia의 기억/경험/공명 기반 저장 시스템.

- 4D 하이퍼스피어 좌표(HypersphericalCoord)
- ResonancePattern: 파동/공명 패턴 데이터
- HypersphereMemory: 저장/검색/재생
"""
import math
from dataclasses import dataclass
from typing import List, Any, Dict, Tuple

@dataclass
class HypersphericalCoord:
    theta: float = 0.0  # Logic Axis
    phi: float = 0.0    # Emotion Axis
    psi: float = 0.0    # Intention Axis
    r: float = 1.0      # Depth Axis

    def to_cartesian(self) -> Tuple[float, float, float, float]:
        sin_t = math.sin(self.theta)
        sin_p = math.sin(self.phi)
        x = self.r * math.cos(self.theta)
        y = self.r * sin_t * math.cos(self.phi)
        z = self.r * sin_t * sin_p * math.cos(self.psi)
        w = self.r * sin_t * sin_p * math.sin(self.psi)
        return (x, y, z, w)

    def distance_to(self, other: 'HypersphericalCoord') -> float:
        p1 = self.to_cartesian()
        p2 = other.to_cartesian()
        return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))

@dataclass
class ResonancePattern:
    content: Any
    omega: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    phase: float = 0.0
    topology: str = "point"
    trajectory: str = "static"
    timestamp: float = 0.0
    duration: float = 0.0
    def matches_filter(self, criteria: Dict[str, Any]) -> bool:
        for key, value in criteria.items():
            if hasattr(self, key):
                if getattr(self, key) != value:
                    return False
        return True

class HypersphereMemory:
    def __init__(self):
        self._memory_space: List[Tuple[HypersphericalCoord, ResonancePattern]] = []
    def store(self, data: Any, position: HypersphericalCoord, pattern_meta: Dict[str, Any] = None):
        if pattern_meta is None:
            pattern_meta = {}
        pattern = ResonancePattern(
            content=data,
            omega=pattern_meta.get('omega', (0.0, 0.0, 0.0)),
            phase=pattern_meta.get('phase', 0.0),
            topology=pattern_meta.get('topology', 'point'),
            trajectory=pattern_meta.get('trajectory', 'static'),
            timestamp=pattern_meta.get('timestamp', 0.0),
            duration=pattern_meta.get('duration', 0.0)
        )
        self._memory_space.append((position, pattern))
    def query(self, position: HypersphericalCoord, radius: float = 0.1, filter_pattern: Dict[str, Any] = None) -> List[Any]:
        results = []
        for pos, pat in self._memory_space:
            dist = position.distance_to(pos)
            if dist <= radius:
                if filter_pattern:
                    if pat.matches_filter(filter_pattern):
                        results.append(pat.content)
                else:
                    results.append(pat.content)
        return results
    def access(self, position: HypersphericalCoord, time: float = 0.0) -> Any:
        return self.query(position)
