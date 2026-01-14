# 원본(Elysia) vs elysia_light 차이와 확장 가이드

이 문서는 원본 Elysia 프로젝트와 elysia_light의 구조적/기능적 차이, 확장 포인트, 연동 방법을 안내합니다.

---

## 1. 구조/기능 차이 요약

| 구분            | 원본(Elysia)                      | elysia_light (경량화)           |
|----------------|-----------------------------------|---------------------------------|
| 목적           | 심화 연구, 실험, 대규모 엔진      | 입문, 공유, 확장, 커스터마이징  |
| 폴더/모듈      | 수십 개(Foundation, Intelligence 등) | core/ (핵심만), data/, docs/    |
| 기능           | 하이퍼스피어, 필드, 메타인지, 성장, 실험 등 | 기억, 감정, 추론, 의식(핵심)    |
| 데이터         | 방대한 worldbuilding, 실험, config | 샘플 캐릭터/설정만              |
| 문서           | 철학, 설계, 실험, 내부 가이드      | 입문/확장/장르별 가이드         |
| 진입장벽       | 높음                              | 낮음                            |

---

## 2. 확장 포인트
- core/에 원본의 원하는 모듈(예: Field, Persona, World, Metacognition 등)만 선택적으로 추가
- data/에 worldbuilding, 시나리오, 대규모 config 등 확장
- docs/에 원본의 철학/설계/실험 문서 일부 이식 가능
- 필요시 원본의 tests/ 예제, 실험 코드도 부분 이식

---

## 3. 연동/이식 방법
1. legacy/elysia_main/Core/Intelligence/ 등에서 필요한 파일을 core/로 복사
2. import 경로를 core.XXX로 수정 (상대경로/의존성 최소화)
3. 불필요한 대규모 의존성/실험 코드는 주석 처리
4. data/에 맞는 샘플/설정 파일 추가
5. USAGE_GUIDE.md, SYSTEM_MAP.md에 확장 내용 반영

---

## 4. 예시: Field 시스템 이식
- 원본의 Field 관련 파일(core/Field/FieldSystem.py 등)을 core/로 복사
- 기존 core/field.py와 통합 또는 대체
- 의존성 최소화, 예제/문서 반영

---

## 5. 추천 활용법
- elysia_light로 실험/확장 → 필요시 원본에서 모듈/데이터만 이식
- 커뮤니티/동료와 공유할 때는 elysia_light 구조로 배포
- 심화 연구/실험은 원본에서 진행

---

## 6. 문의/기여
- Issue, PR, 질문은 언제든 환영합니다!
- 원본/경량화 구조 모두 자유롭게 활용/확장/재해석 가능합니다.
