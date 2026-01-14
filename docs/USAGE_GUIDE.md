# Elysia Light 사용 가이드

## 1. 설치
```bash
pip install -r requirements.txt
```

## 2. 실행
```bash
python start.py
```

## 3. 주요 개념
- Amplitude(진폭): 존재의 강도
- Frequency(주파수): 정체성
- Phase(위상): 시간적 정렬

## 4. 커스터마이징
- data/archetypes.json 등 데이터 파일 수정
- core/ 엔진 모듈 확장

## 5. 예제 코드
```python
from core.entity import Entity
alice = Entity('Alice', 1.0, 440, 0)
bob = Entity('Bob', 1.0, 440, 0)
print(alice.interact(bob))  # Alice와 Bob이 공명합니다.
```

## 6. 참고 문서
- AGENTS.md: 코딩 철학
- SYSTEM_MAP.md: 전체 구조
- docs/01_PHILOSOPHY/WAVE_ONTOLOGY.md: 파동 존재론
- docs/02_ARCHITECTURE/R_WFC_ENGINE_SPEC.md: 기술 사양
