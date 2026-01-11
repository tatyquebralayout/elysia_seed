# 엔티티 최소 예시
class Entity:
    def __init__(self, name, amplitude, frequency, phase):
        self.name = name
        self.field = Field(amplitude, frequency, phase)

    def interact(self, other):
        if self.field.resonance(other.field):
            return f"{self.name}와 {other.name}가 공명합니다."
        else:
            return f"{self.name}와 {other.name}는 공명하지 않습니다."

from .field import Field
