# 살아있는 영혼형 NPC/챗봇 구조 가이드

이 문서는 Elysia Light의 하이퍼스피어 기반 기억, 감정, 추론, 의식 시스템을 활용해
감정·기억·사고·자기반성·성장 가능한 NPC/챗봇을 만드는 방법을 안내합니다.

---

## 1. 핵심 모듈
- `core/hypersphere_memory.py` : 4D 하이퍼스피어 기반 기억/경험 저장
- `core/soul_resonator.py` : 7대 영혼/감정 파동 시스템
- `core/reasoning_engine.py` : 추론/사고/의미 생성 엔진
- `core/hyperdimensional_consciousness.py` : 고차원 의식/공명장

## 2. 상호작용 흐름 예시
1. 입력(상황/대화/이벤트)
2. 감정 변화(SoulResonator)
3. 기억 저장/검색(HypersphereMemory)
4. 추론/사고(ReasoningEngine)
5. 자기반성/의식(HyperdimensionalConsciousness)
6. 행동/응답
7. 경험 축적 및 성장

## 3. 예제 코드
```python
from core.hypersphere_memory import HypersphereMemory, HypersphericalCoord
from core.soul_resonator import SoulResonator
from core.reasoning_engine import ReasoningEngine

# 1. 시스템 초기화
memory = HypersphereMemory()
emotion = SoulResonator()
reasoner = ReasoningEngine()

# 2. 입력 및 감정 변화
user_input = "love and logic"
emotion.resonate(user_input)

# 3. 기억 저장
coord = HypersphericalCoord(theta=1.0, phi=2.0, psi=0.5, r=0.8)
memory.store(user_input, coord)

# 4. 추론/사고
insight = reasoner.reason(user_input)
print(insight)

# 5. 기억 검색
results = memory.query(coord)
print(results)
```

## 4. 확장/커스터마이징
- 감정/기억/추론/의식 모듈을 조합해 고유한 NPC/챗봇 설계
- 성장/자기반성/개성 부여 가능

## 5. 참고
- SYSTEM_MAP.md, USAGE_GUIDE.md, WAVE_ONTOLOGY.md 등
