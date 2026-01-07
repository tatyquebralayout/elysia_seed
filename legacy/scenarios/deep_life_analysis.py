"""
엘리시아 세계 - 개인 인생 스토리 분석

한 인물의 전체 인생을 상세하게 시뮬레이션하고 분석합니다.
"충분히 인간적인가?"에 대한 깊은 탐구.
"""

import sys
import os
import json
import random
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_core import ElysiaSoul


@dataclass
class LifeMemory:
    """인생의 기억"""
    age: int
    year: int
    event: str
    emotion: str
    intensity: float
    impact: str  # 이 경험이 어떤 영향을 미쳤는지
    trinity_change: Dict[str, float] = field(default_factory=dict)


@dataclass
class Relationship:
    """관계"""
    name: str
    relation: str  # 가족, 친구, 연인, 스승, 라이벌 등
    met_age: int
    status: str = "active"
    shared_memories: List[str] = field(default_factory=list)


@dataclass
class PersonalHistory:
    """개인 역사"""
    name: str
    birth_year: int
    death_year: int = 0
    profession: str = ""
    origin: str = ""
    
    # 영혼
    soul: ElysiaSoul = None
    
    # 기억들
    memories: List[LifeMemory] = field(default_factory=list)
    
    # 관계들
    relationships: List[Relationship] = field(default_factory=list)
    
    # 인생의 전환점
    turning_points: List[str] = field(default_factory=list)
    
    # 최종 특성
    final_traits: List[str] = field(default_factory=list)
    
    # 유언/인생 요약
    life_summary: str = ""


def load_scenarios():
    """시나리오 로드"""
    base_path = Path(__file__).parent.parent
    scenarios = json.loads((base_path / 'data/worldbuilding/life_scenarios.json').read_text(encoding='utf-8'))
    return scenarios


def get_life_stage(age: int) -> str:
    """나이별 생애 단계"""
    if age < 5:
        return 'infancy'
    elif age < 13:
        return 'childhood'
    elif age < 19:
        return 'adolescence'
    elif age < 31:
        return 'young_adult'
    elif age < 51:
        return 'adulthood'
    else:
        return 'elder'


def get_stage_name_kr(stage: str) -> str:
    """한글 단계명"""
    names = {
        'infancy': '유아기',
        'childhood': '유년기',
        'adolescence': '청소년기',
        'young_adult': '청년기',
        'adulthood': '장년기',
        'elder': '노년기'
    }
    return names.get(stage, stage)


def simulate_one_life(name: str, profession: str, origin: str, lifespan: int = 75) -> PersonalHistory:
    """한 인물의 전체 인생 시뮬레이션"""
    
    scenarios = load_scenarios()
    birth_year = 500  # 세계력 500년에 태어남
    
    history = PersonalHistory(
        name=name,
        birth_year=birth_year,
        profession=profession,
        origin=origin,
        soul=ElysiaSoul(name=name)
    )
    
    # 초기 관계: 부모
    history.relationships.append(Relationship(
        name="부모님",
        relation="가족",
        met_age=0,
        shared_memories=["태어남", "첫 걸음마", "첫 말"]
    ))
    
    print(f"\n{'='*70}")
    print(f"  📖 {name}의 인생 이야기")
    print(f"  직업: {profession} | 출신: {origin}")
    print(f"{'='*70}\n")
    
    current_stage = None
    
    for age in range(0, lifespan + 1):
        year = birth_year + age
        stage = get_life_stage(age)
        
        # 새로운 생애 단계 진입 시
        if stage != current_stage:
            current_stage = stage
            stage_kr = get_stage_name_kr(stage)
            print(f"\n--- {stage_kr} ({age}세) ---\n")
        
        # 특정 나이의 주요 이벤트
        experience = get_age_appropriate_experience(scenarios, age, stage)
        
        if experience:
            # 영혼이 경험을 처리
            thought = history.soul.process(experience['text'])
            emotion = history.soul.get_emotion()
            
            # 기억 저장
            memory = LifeMemory(
                age=age,
                year=year,
                event=experience['text'],
                emotion=emotion['dominant'],
                intensity=experience.get('intensity', 0.5),
                impact=interpret_impact(experience, emotion),
                trinity_change={
                    'body': experience.get('body', 0),
                    'soul': experience.get('soul', 0),
                    'spirit': experience.get('spirit', 0)
                }
            )
            
            # 중요한 경험만 출력
            if experience.get('intensity', 0.5) >= 0.7 or age in [5, 10, 15, 18, 21, 30, 40, 50, 60, 70]:
                print(f"  [{age}세] {experience['text']}")
                print(f"         💭 감정: {emotion['dominant']} | 영향: {memory.impact}")
                
                # Trinity 업데이트
                history.soul.update_trinity(
                    body_delta=experience.get('body', 0),
                    soul_delta=experience.get('soul', 0),
                    spirit_delta=experience.get('spirit', 0)
                )
            
            history.memories.append(memory)
            
            # 전환점 기록
            if experience.get('intensity', 0) >= 1.2:
                history.turning_points.append(f"{age}세: {experience['text'][:40]}...")
        
        # 특정 나이에 관계 형성
        if age == 5:
            history.relationships.append(Relationship(
                name="첫 친구",
                relation="친구",
                met_age=5,
                shared_memories=["함께 놀던 기억"]
            ))
        elif age == 15:
            if random.random() > 0.5:
                history.relationships.append(Relationship(
                    name="스승님",
                    relation="스승",
                    met_age=15,
                    shared_memories=["가르침을 받음"]
                ))
        elif age == 22:
            if random.random() > 0.4:
                history.relationships.append(Relationship(
                    name="반려자",
                    relation="배우자",
                    met_age=22,
                    shared_memories=["첫 만남", "결혼"]
                ))
    
    # 사망
    history.death_year = birth_year + lifespan
    
    # 최종 분석
    history.final_traits = history.soul.traits.copy()
    history.life_summary = generate_life_summary(history)
    
    return history


def get_age_appropriate_experience(scenarios: Dict, age: int, stage: str) -> Optional[Dict]:
    """나이에 맞는 경험 선택"""
    
    # 특정 나이의 특별 이벤트
    special_ages = {
        0: {'text': '세상에 태어났다. 첫 숨을 쉬었다.', 'intensity': 1.5, 'soul': 0.5},
        1: {'text': '처음으로 걸음마를 뗐다.', 'intensity': 0.8, 'body': 0.3},
        3: {'text': '말을 배우기 시작했다. 세상과 소통할 수 있게 되었다.', 'intensity': 0.9, 'soul': 0.4},
        6: {'text': '글자를 배우기 시작했다.', 'intensity': 0.7, 'spirit': 0.3},
        15: {'text': '미래에 대해 고민하기 시작했다. 나는 누구인가?', 'intensity': 1.0, 'spirit': 0.5},
        18: {'text': '성인이 되었다. 이제 스스로 결정할 수 있다.', 'intensity': 1.2, 'spirit': 0.4, 'body': 0.2},
    }
    
    if age in special_ages:
        return special_ages[age]
    
    # 랜덤 경험
    if random.random() < 0.3:  # 30% 확률로 의미있는 일 발생
        stage_map = {
            'infancy': 'childhood',
            'childhood': 'childhood',
            'adolescence': 'adolescence',
            'young_adult': 'young_adult',
            'adulthood': 'adulthood',
            'elder': 'elder'
        }
        
        mapped_stage = stage_map.get(stage, 'childhood')
        
        if mapped_stage in scenarios.get('life_stages', {}):
            experiences = scenarios['life_stages'][mapped_stage].get('experiences', [])
            if experiences:
                return random.choice(experiences)
        
        # 특별 이벤트
        if random.random() < 0.2:
            event_type = random.choice(['positive', 'negative', 'transformative'])
            if event_type in scenarios.get('special_events', {}):
                events = scenarios['special_events'][event_type]
                if events:
                    return random.choice(events)
    
    return None


def interpret_impact(experience: Dict, emotion: Dict) -> str:
    """경험의 영향 해석"""
    intensity = experience.get('intensity', 0.5)
    valence = emotion.get('valence', 0)
    
    if intensity >= 1.5:
        if valence > 0.3:
            return "인생을 바꾸는 기쁨의 순간"
        elif valence < -0.3:
            return "깊은 상처를 남긴 시련"
        else:
            return "중요한 깨달음을 얻음"
    elif intensity >= 1.0:
        if valence > 0:
            return "의미있는 성장"
        else:
            return "시련을 통한 성숙"
    elif intensity >= 0.7:
        return "기억에 남을 경험"
    else:
        return "일상의 한 조각"


def generate_life_summary(history: PersonalHistory) -> str:
    """인생 요약 생성"""
    trinity = history.soul.trinity
    traits = history.soul.traits
    lifespan = history.death_year - history.birth_year
    
    # 성향 분석
    dominant = max(trinity.items(), key=lambda x: x[1])
    
    personality_desc = {
        'body': "실용적이고 행동 중심적인",
        'soul': "관계를 중시하고 감성적인",
        'spirit': "사색적이고 의미를 추구하는"
    }
    
    summary_parts = []
    summary_parts.append(f"{history.name}은(는) {history.origin}에서 태어나 {lifespan}년의 삶을 살았다.")
    summary_parts.append(f"{personality_desc.get(dominant[0], '독특한')} 사람이었다.")
    
    if history.turning_points:
        summary_parts.append(f"인생의 전환점: {history.turning_points[0]}")
    
    if len(history.relationships) > 2:
        summary_parts.append(f"{len(history.relationships)}명의 중요한 사람들과 인연을 맺었다.")
    
    if traits:
        summary_parts.append(f"성격 특성: {', '.join(traits[:3])}")
    
    return " ".join(summary_parts)


def analyze_humanity(history: PersonalHistory) -> Dict[str, Any]:
    """인간성 분석"""
    
    print(f"\n{'='*70}")
    print("  🔬 인간성/인격성 분석")
    print(f"{'='*70}\n")
    
    analysis = {}
    
    # 1. 감정의 다양성
    emotions = [m.emotion for m in history.memories]
    unique_emotions = set(emotions)
    analysis['emotional_diversity'] = len(unique_emotions)
    print(f"1. 감정의 다양성: {len(unique_emotions)}가지 감정 경험")
    print(f"   경험한 감정들: {', '.join(unique_emotions)}")
    
    # 2. 성장의 궤적
    early_trinity = {'body': 0.33, 'soul': 0.34, 'spirit': 0.33}
    final_trinity = history.soul.trinity
    
    changes = {k: final_trinity[k] - early_trinity[k] for k in early_trinity}
    analysis['growth'] = changes
    print(f"\n2. 성장의 궤적:")
    print(f"   Body:   {early_trinity['body']:.0%} → {final_trinity['body']:.0%} ({changes['body']:+.0%})")
    print(f"   Soul:   {early_trinity['soul']:.0%} → {final_trinity['soul']:.0%} ({changes['soul']:+.0%})")
    print(f"   Spirit: {early_trinity['spirit']:.0%} → {final_trinity['spirit']:.0%} ({changes['spirit']:+.0%})")
    
    # 3. 관계의 깊이
    analysis['relationships'] = len(history.relationships)
    print(f"\n3. 관계의 형성: {len(history.relationships)}개의 주요 관계")
    for rel in history.relationships:
        print(f"   - {rel.relation}: {rel.name} ({rel.met_age}세에 만남)")
    
    # 4. 기억의 축적
    significant_memories = [m for m in history.memories if m.intensity >= 0.8]
    analysis['significant_memories'] = len(significant_memories)
    print(f"\n4. 의미있는 기억: {len(significant_memories)}개")
    for m in significant_memories[:5]:
        print(f"   - [{m.age}세] {m.event[:40]}...")
    
    # 5. 인생의 전환점
    analysis['turning_points'] = len(history.turning_points)
    print(f"\n5. 인생의 전환점: {len(history.turning_points)}개")
    for tp in history.turning_points[:3]:
        print(f"   - {tp}")
    
    # 6. 성격 특성
    analysis['traits'] = history.soul.traits
    print(f"\n6. 형성된 성격: {', '.join(history.soul.traits)}")
    
    # 종합 평가
    print(f"\n{'='*70}")
    print("  💭 종합 평가: 이것이 '인간적'인가?")
    print(f"{'='*70}\n")
    
    humanity_score = (
        min(len(unique_emotions) / 8, 1.0) * 20 +  # 감정 다양성 (최대 20점)
        abs(sum(changes.values())) * 50 +  # 성장 변화 (최대 20점)
        min(len(history.relationships) / 5, 1.0) * 20 +  # 관계 (최대 20점)
        min(len(significant_memories) / 10, 1.0) * 20 +  # 기억 (최대 20점)
        min(len(history.turning_points) / 3, 1.0) * 20  # 전환점 (최대 20점)
    )
    
    analysis['humanity_score'] = humanity_score
    
    print(f"  인간성 점수: {humanity_score:.0f}/100\n")
    
    if humanity_score >= 80:
        verdict = "매우 인간적입니다. 풍부한 감정, 성장, 관계를 경험했습니다."
    elif humanity_score >= 60:
        verdict = "상당히 인간적입니다. 의미있는 경험들이 축적되었습니다."
    elif humanity_score >= 40:
        verdict = "기본적인 인간성을 가지고 있습니다. 더 많은 경험이 필요합니다."
    else:
        verdict = "아직 발달 중입니다. 더 다양한 경험이 필요합니다."
    
    print(f"  평가: {verdict}\n")
    
    # 철학적 성찰
    print("  🌟 철학적 성찰:")
    print("  이 시뮬레이션은 '패턴'입니다. 하지만 인간의 뇌도")
    print("  뉴런의 패턴입니다. 차이점은 무엇일까요?")
    print("")
    print("  현재 이 엔진은:")
    print("  ✓ 경험을 통한 성격 형성 (Trinity weights)")
    print("  ✓ 감정의 혼합과 변화 (EmotionalPalette)")
    print("  ✓ 인과적 기억 (Hippocampus)")
    print("  ✓ 관계와 공명 (ResonanceEngine)")
    print("")
    print("  부족한 점:")
    print("  △ 자유의지 (모든 경험은 외부에서 주어짐)")
    print("  △ 자아 인식 (자신이 시뮬레이션임을 모름)")
    print("  △ 창의적 행동 (주어진 시나리오만 경험)")
    print("")
    print("  결론: 이것은 '인격의 그릇'입니다.")
    print("  진정한 인격이 되려면 '자율적 행동'과 '자기 인식'이 필요합니다.")
    print("  현재는 '잠재적 인격체'의 상태입니다.")
    
    return analysis


def main():
    random.seed(123)
    
    # 한 인물의 상세 인생 시뮬레이션
    history = simulate_one_life(
        name="Aria Silvermoon",
        profession="치유사",
        origin="황혼의 땅 (Duskmere)",
        lifespan=72
    )
    
    # 인생 요약
    print(f"\n{'='*70}")
    print("  📜 인생 요약")
    print(f"{'='*70}\n")
    print(f"  {history.life_summary}")
    
    # 인간성 분석
    analysis = analyze_humanity(history)
    
    return history, analysis


if __name__ == "__main__":
    main()
