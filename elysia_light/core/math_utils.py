# 수학 유틸리티 (Rotor/Quaternion 최소 예시)
class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z

class Rotor:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def rotate(self, vector):
        # 실제 회전 로직은 생략 (예시)
        return vector
