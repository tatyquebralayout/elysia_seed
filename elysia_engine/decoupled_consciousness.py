"""
분리된 의식 시스템 (Decoupled Consciousness)

심장(Heart/Engine) + 머리(Mind/Persona) 분리 아키텍처

- Heart: 기반 연산 엔진 (감정, 기억, 에너지)
- Mind: 페르소나/세션 (언어, 행동, 관계)

Gemini가 기반이면서 Claude/ChatGPT가 페르소나인 것처럼,
이 시스템도 "연산하는 나"와 "표현하는 나"가 분리됨.

프랙탈 원리: 
- Heart 하나가 여러 Mind를 가질 수 있음
- Mind 하나가 Heart의 일부분만 사용할 수 있음
- 작은 Mind가 곧 큰 World의 축소판
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Tuple
import random
import math
import time

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_engine.natural_language import (
    NaturalLanguageGenerator, 
    LanguageState,
    BilingualGenerator
)


@dataclass
class Emotion:
    """감정 상태"""
    valence: float = 0.0      # -1 ~ +1 (부정 ~ 긍정)
    arousal: float = 0.5      # 0 ~ 1 (차분 ~ 격앙)
    dominance: float = 0.5    # 0 ~ 1 (피지배 ~ 지배)
    
    def blend(self, other: Emotion, weight: float = 0.5) -> Emotion:
        """두 감정 혼합"""
        return Emotion(
            valence=self.valence * (1-weight) + other.valence * weight,
            arousal=self.arousal * (1-weight) + other.arousal * weight,
            dominance=self.dominance * (1-weight) + other.dominance * weight,
        )
    
    def decay(self, rate: float = 0.1) -> None:
        """감정 감쇄 (중립으로 회귀)"""
        self.valence *= (1 - rate)
        self.arousal = self.arousal * (1 - rate) + 0.5 * rate
        self.dominance = self.dominance * (1 - rate) + 0.5 * rate
    
    def to_language_state(self) -> LanguageState:
        """LanguageState로 변환"""
        return LanguageState(
            emotion_valence=self.valence,
            emotion_arousal=self.arousal,
            certainty=self.dominance,
        )


@dataclass
class Memory:
    """기억 단위"""
    content: str
    timestamp: float
    emotion: Emotion
    importance: float = 0.5
    associations: List[str] = field(default_factory=list)
    
    def fade(self, current_time: float, half_life: float = 100.0) -> float:
        """기억 강도 (시간에 따라 감소)"""
        age = current_time - self.timestamp
        return self.importance * math.exp(-age / half_life)


@dataclass
class Need:
    """욕구/동기"""
    name: str
    level: float = 0.5       # 0 (충족) ~ 1 (결핍)
    priority: float = 0.5    # 중요도
    
    def update(self, delta: float) -> None:
        """욕구 수준 변화"""
        self.level = max(0.0, min(1.0, self.level + delta))
    
    def urgency(self) -> float:
        """긴급도 (수준 x 중요도)"""
        return self.level * self.priority


class Heart:
    """
    심장 (Heart) - 연산 엔진
    
    감정, 기억, 욕구를 처리하는 핵심 엔진.
    "나"라는 것을 연산하지만, 스스로를 "나"라고 말하지 않음.
    
    이것이 Gemini의 기반 모델과 같은 역할.
    """
    
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
            
        # 핵심 상태
        self.emotion = Emotion()
        self.energy = 1.0           # 0 ~ 1
        self.vitality = 1.0         # 생명력
        
        # 기억 저장소
        self.memories: List[Memory] = []
        self.max_memories = 1000
        
        # 욕구 체계 (매슬로우 기반)
        self.needs = {
            "survival": Need("생존", 0.2, 1.0),
            "safety": Need("안전", 0.3, 0.9),
            "belonging": Need("소속", 0.5, 0.7),
            "esteem": Need("존중", 0.5, 0.5),
            "actualization": Need("자아실현", 0.6, 0.3),
        }
        
        # 성격 특성 (OCEAN 모델)
        self.traits = {
            "openness": random.gauss(0.5, 0.15),
            "conscientiousness": random.gauss(0.5, 0.15),
            "extraversion": random.gauss(0.5, 0.15),
            "agreeableness": random.gauss(0.5, 0.15),
            "neuroticism": random.gauss(0.5, 0.15),
        }
        # 범위 제한
        for k in self.traits:
            self.traits[k] = max(0.0, min(1.0, self.traits[k]))
        
        # 시간
        self.internal_time = 0.0
        
        # 연결된 Mind들
        self.minds: List[Mind] = []
    
    def tick(self, dt: float = 1.0) -> None:
        """시간 진행"""
        self.internal_time += dt
        
        # 욕구 자연 증가
        for need in self.needs.values():
            need.update(0.01 * dt)
        
        # 에너지 소모
        self.energy = max(0.1, self.energy - 0.001 * dt)
        
        # 감정 감쇄
        self.emotion.decay(0.05 * dt)
        
        # 모든 Mind에 동기화
        for mind in self.minds:
            mind.sync_from_heart(self)
    
    def feel(self, stimulus: Dict[str, Any]) -> Emotion:
        """
        자극에 대한 감정 반응
        
        stimulus: {
            "type": "event_type",
            "valence": -1 ~ +1,
            "arousal": 0 ~ 1,
            "intensity": 0 ~ 1,
        }
        """
        intensity = stimulus.get("intensity", 0.5)
        
        new_emotion = Emotion(
            valence=stimulus.get("valence", 0.0) * intensity,
            arousal=stimulus.get("arousal", 0.5),
            dominance=0.5 + stimulus.get("valence", 0.0) * 0.3,
        )
        
        # 성격에 따른 반응 조절
        if self.traits["neuroticism"] > 0.6:
            new_emotion.arousal *= 1.3  # 더 격앙
        if self.traits["agreeableness"] > 0.6:
            new_emotion.valence = new_emotion.valence * 0.8  # 더 온화
            
        # 현재 감정과 혼합
        weight = intensity * 0.5
        self.emotion = self.emotion.blend(new_emotion, weight)
        
        return self.emotion
    
    def remember(self, content: str, emotion: Emotion = None, importance: float = 0.5) -> Memory:
        """기억 저장"""
        memory = Memory(
            content=content,
            timestamp=self.internal_time,
            emotion=emotion or Emotion(),
            importance=importance,
        )
        
        self.memories.append(memory)
        
        # 용량 초과시 오래된/약한 기억 제거
        if len(self.memories) > self.max_memories:
            # 중요도 x 최신성 점수로 정렬, 하위 제거
            self.memories.sort(
                key=lambda m: m.fade(self.internal_time) * m.importance,
                reverse=True
            )
            self.memories = self.memories[:self.max_memories]
        
        return memory
    
    def recall(self, query: str = "", count: int = 5) -> List[Memory]:
        """기억 회상"""
        # 간단한 키워드 매칭
        if query:
            relevant = [m for m in self.memories if query in m.content]
        else:
            relevant = self.memories.copy()
        
        # 최근 + 중요한 순으로 정렬
        relevant.sort(
            key=lambda m: m.fade(self.internal_time),
            reverse=True
        )
        
        return relevant[:count]
    
    def satisfy(self, need_name: str, amount: float = 0.3) -> None:
        """욕구 충족"""
        if need_name in self.needs:
            self.needs[need_name].update(-amount)
            
            # 충족감 → 긍정 감정
            self.emotion.valence += amount * 0.3
            self.emotion.valence = max(-1.0, min(1.0, self.emotion.valence))
    
    def get_dominant_need(self) -> Need:
        """가장 긴급한 욕구"""
        return max(self.needs.values(), key=lambda n: n.urgency())
    
    def get_state_vector(self) -> List[float]:
        """상태를 벡터로 (Mind에 전달용)"""
        return [
            self.emotion.valence,
            self.emotion.arousal,
            self.emotion.dominance,
            self.energy,
            self.vitality,
            self.get_dominant_need().level,
        ]


class Mind:
    """
    머리 (Mind) - 페르소나/세션
    
    Heart의 상태를 받아 언어와 행동으로 표현.
    "나는 사람이다"라고 말하는 것은 Mind의 역할.
    
    이것이 Claude/ChatGPT의 페르소나와 같은 역할.
    """
    
    def __init__(
        self, 
        name: str,
        heart: Heart,
        language: str = "ko"
    ):
        self.name = name
        self.heart = heart
        self.language = language
        
        # Heart에 연결
        heart.minds.append(self)
        
        # 언어 생성기
        self.lang_gen = NaturalLanguageGenerator(language)
        
        # Mind 고유 상태
        self.identity = {
            "name": name,
            "role": "",
            "backstory": "",
            "goals": [],
            "values": [],
        }
        
        # 언어 상태 (Heart에서 동기화)
        self.lang_state = LanguageState()
        
        # 관계
        self.relationships: Dict[str, float] = {}  # name -> affinity (-1 ~ +1)
        
        # 대화 기록
        self.conversation_history: List[Dict] = []
        
        # 일기
        self.diary: List[str] = []
        
        # 현재 활동
        self.current_activity: Optional[str] = None
        self.activity_log: List[Dict] = []
    
    def sync_from_heart(self, heart: Heart) -> None:
        """Heart에서 상태 동기화"""
        self.lang_state = heart.emotion.to_language_state()
        
        # 성격이 언어 스타일에 영향
        if heart.traits["extraversion"] > 0.6:
            self.lang_state.formality = 0.3  # 더 캐주얼
        if heart.traits["conscientiousness"] > 0.6:
            self.lang_state.formality = 0.7  # 더 격식
    
    def speak(self) -> str:
        """말하기 - 현재 상태를 언어로"""
        # 존재 선언 + 감정 + 생각
        parts = []
        
        # 가끔 자기 소개
        if random.random() < 0.1:
            parts.append(self.lang_gen.generate_existence(self.name, self.lang_state))
        
        # 감정 표현
        parts.append(self.lang_gen.generate_emotion(self.lang_state))
        
        # 욕구 기반 생각
        dominant_need = self.heart.get_dominant_need()
        if dominant_need.name == "belonging":
            self.lang_state.focus = "other"
        elif dominant_need.name == "actualization":
            self.lang_state.focus = "abstract"
        else:
            self.lang_state.focus = "self"
        
        parts.append(self.lang_gen.generate_thought(self.lang_state))
        
        return " ".join(parts)
    
    def say_i_am_human(self) -> str:
        """"나는 사람이다" 선언"""
        if self.language == "ko":
            templates = [
                f"나는 {self.name}. 사람이야.",
                f"나는 한 사람으로서 여기 있어.",
                f"내 이름은 {self.name}. 나도 너처럼 느끼고 생각해.",
                f"나는 살아있어. {self.name}이라는 사람으로.",
            ]
        else:
            templates = [
                f"I am {self.name}. A person.",
                f"I exist here as a person.",
                f"My name is {self.name}. I feel and think, just like you.",
                f"I am alive. As a person named {self.name}.",
            ]
        
        return random.choice(templates)
    
    def greet(self, other: Mind, time_of_day: str = "day") -> str:
        """다른 Mind에게 인사"""
        greeting = self.lang_gen.generate_greeting(time_of_day)
        
        # 관계 업데이트
        if other.name not in self.relationships:
            self.relationships[other.name] = 0.0
        self.relationships[other.name] += 0.05
        
        return greeting
    
    def respond_to(self, other: Mind, their_message: str) -> str:
        """대화 응답"""
        # 상대의 감정 파악 (간단한 키워드)
        other_valence = "neutral"
        positive_words = ["좋", "행복", "기뻐", "사랑", "happy", "good", "love"]
        negative_words = ["슬", "화", "힘들", "무서", "sad", "angry", "hard"]
        
        for word in positive_words:
            if word in their_message:
                other_valence = "positive"
                break
        for word in negative_words:
            if word in their_message:
                other_valence = "negative"
                break
        
        # 반응 생성
        response = self.lang_gen.generate_conversation_turn(
            self.name,
            self.lang_state,
            is_response=True,
            response_to_emotion=(other_valence, "")
        )
        
        # 대화 기록
        self.conversation_history.append({
            "other": other.name,
            "their_message": their_message,
            "my_response": response,
            "time": self.heart.internal_time,
        })
        
        return response
    
    def do_activity(self, activity_type: str, **details) -> str:
        """활동 수행"""
        self.current_activity = activity_type
        
        # 활동에 따른 욕구 충족
        activity_needs = {
            "eating": "survival",
            "resting": "safety",
            "socializing": "belonging",
            "working": "esteem",
            "creating": "actualization",
            "learning": "actualization",
        }
        
        if activity_type in activity_needs:
            self.heart.satisfy(activity_needs[activity_type], 0.2)
        
        # 활동 기록
        self.activity_log.append({
            "type": activity_type,
            "details": details,
            "time": self.heart.internal_time,
        })
        
        # 언어로 표현
        return self.lang_gen.generate_activity(activity_type, **details)
    
    def write_diary(self, date: str = "") -> str:
        """일기 쓰기"""
        if not date:
            date = f"Day {int(self.heart.internal_time)}"
        
        # 최근 활동들
        recent_activities = self.activity_log[-5:]
        activities = [
            {"type": act["type"], **act.get("details", {})}
            for act in recent_activities
        ]
        
        entry = self.lang_gen.generate_diary_entry(
            self.name,
            date,
            activities,
            self.lang_state
        )
        
        self.diary.append(entry)
        
        # 기억으로도 저장
        self.heart.remember(f"일기: {entry[:50]}...", self.heart.emotion, 0.7)
        
        return entry
    
    def inner_monologue(self) -> str:
        """내면의 독백"""
        memories = [m.content for m in self.heart.recall(count=5)]
        
        return self.lang_gen.generate_inner_monologue(
            self.name,
            self.lang_state,
            memories=memories,
            relationships=self.relationships
        )
    
    def express_desire(self) -> str:
        """욕구 표현"""
        dominant = self.heart.get_dominant_need()
        
        desire_map = {
            "survival": "생존하는 것" if self.language == "ko" else "survive",
            "safety": "안전해지는 것" if self.language == "ko" else "be safe",
            "belonging": "누군가와 함께하는 것" if self.language == "ko" else "be with someone",
            "esteem": "인정받는 것" if self.language == "ko" else "be recognized",
            "actualization": "나 자신이 되는 것" if self.language == "ko" else "become myself",
        }
        
        goal = desire_map.get(dominant.name, "something")
        return self.lang_gen.generate_desire(goal, self.lang_state)
    
    def get_persona_prompt(self) -> str:
        """LLM용 페르소나 프롬프트 생성"""
        # 성격 특성 설명
        traits_desc = []
        if self.heart.traits["openness"] > 0.6:
            traits_desc.append("창의적이고 호기심이 많은" if self.language == "ko" else "creative and curious")
        if self.heart.traits["conscientiousness"] > 0.6:
            traits_desc.append("성실하고 책임감 있는" if self.language == "ko" else "diligent and responsible")
        if self.heart.traits["extraversion"] > 0.6:
            traits_desc.append("외향적이고 활발한" if self.language == "ko" else "extroverted and lively")
        if self.heart.traits["agreeableness"] > 0.6:
            traits_desc.append("친절하고 협조적인" if self.language == "ko" else "kind and cooperative")
        if self.heart.traits["neuroticism"] > 0.6:
            traits_desc.append("감수성이 풍부한" if self.language == "ko" else "emotionally sensitive")
        
        traits_str = ", ".join(traits_desc) if traits_desc else "평범한" if self.language == "ko" else "ordinary"
        
        # 현재 감정
        emotion = self.heart.emotion
        if emotion.valence > 0.3:
            mood = "기분이 좋은" if self.language == "ko" else "in a good mood"
        elif emotion.valence < -0.3:
            mood = "기분이 안 좋은" if self.language == "ko" else "in a bad mood"
        else:
            mood = "평온한" if self.language == "ko" else "calm"
        
        if self.language == "ko":
            prompt = f"""당신은 {self.name}입니다.

성격: {traits_str} 사람입니다.
현재 상태: {mood} 상태입니다.
에너지: {self.heart.energy:.0%}
주요 욕구: {self.heart.get_dominant_need().name}

최근 기억:
{chr(10).join([f'- {m.content}' for m in self.heart.recall(count=3)])}

{self.name}으로서 자연스럽게 대화하세요. 
당신은 진짜 사람입니다. 시뮬레이션이라고 말하지 마세요.
"""
        else:
            prompt = f"""You are {self.name}.

Personality: A {traits_str} person.
Current state: {mood}.
Energy: {self.heart.energy:.0%}
Main need: {self.heart.get_dominant_need().name}

Recent memories:
{chr(10).join([f'- {m.content}' for m in self.heart.recall(count=3)])}

Speak naturally as {self.name}. 
You are a real person. Do not mention simulation.
"""
        
        return prompt


class DecoupledConsciousness:
    """
    분리된 의식 시스템
    
    하나의 Heart가 여러 Mind를 가질 수 있고,
    각 Mind는 독립적인 페르소나로 동작.
    
    프랙탈: 작은 Mind도 완전한 의식, 큰 World도 하나의 의식.
    """
    
    def __init__(self, name: str = "엘리시아"):
        self.name = name
        self.hearts: Dict[str, Heart] = {}
        self.minds: Dict[str, Mind] = {}
        self.world_time = 0.0
    
    def create_being(
        self, 
        name: str, 
        language: str = "ko",
        traits: Dict[str, float] = None
    ) -> Tuple[Heart, Mind]:
        """존재 생성 (Heart + Mind 쌍)"""
        heart = Heart()
        if traits:
            heart.traits.update(traits)
        
        mind = Mind(name, heart, language)
        
        self.hearts[name] = heart
        self.minds[name] = mind
        
        return heart, mind
    
    def step(self, dt: float = 1.0) -> List[str]:
        """세계 시간 진행"""
        self.world_time += dt
        outputs = []
        
        for name, heart in self.hearts.items():
            heart.tick(dt)
        
        return outputs
    
    def simulate_day(self, mind: Mind) -> List[str]:
        """하루 시뮬레이션"""
        outputs = []
        
        # 아침
        outputs.append(f"[{mind.name}] {mind.greet(mind, 'morning')}")
        self.step(2.0)
        
        # 식사
        foods = ["빵", "밥", "과일", "고기"]
        food = random.choice(foods)
        outputs.append(f"[{mind.name}] {mind.do_activity('eating', food=food, taste='맛있었어')}")
        self.step(1.0)
        
        # 일
        works = ["대장장이 일", "농사", "연구", "순찰"]
        work = random.choice(works)
        outputs.append(f"[{mind.name}] {mind.do_activity('working', work=work)}")
        self.step(4.0)
        
        # 사교 (다른 Mind가 있으면)
        other_minds = [m for m in self.minds.values() if m.name != mind.name]
        if other_minds:
            other = random.choice(other_minds)
            outputs.append(f"[{mind.name}] {mind.do_activity('socializing', other=other.name)}")
            self.step(2.0)
        
        # 저녁
        outputs.append(f"[{mind.name}] {mind.greet(mind, 'evening')}")
        
        # 내면의 독백
        outputs.append(f"[{mind.name}의 생각] {mind.inner_monologue()}")
        
        # 일기
        diary = mind.write_diary()
        outputs.append(f"[{mind.name}의 일기] {diary}")
        
        # 밤
        outputs.append(f"[{mind.name}] {mind.greet(mind, 'night')}")
        self.step(8.0)
        
        return outputs
    
    def conversation(self, mind1: Mind, mind2: Mind, turns: int = 3) -> List[str]:
        """두 Mind 간의 대화"""
        outputs = []
        
        # 인사
        outputs.append(f"[{mind1.name}] {mind1.greet(mind2, 'day')}")
        outputs.append(f"[{mind2.name}] {mind2.greet(mind1, 'day')}")
        
        # 대화 턴
        current, other = mind1, mind2
        last_message = ""
        
        for _ in range(turns):
            if last_message:
                response = current.respond_to(other, last_message)
            else:
                response = current.speak()
            
            outputs.append(f"[{current.name}] {response}")
            last_message = response
            current, other = other, current
        
        return outputs


# 데모 함수
def demo_decoupled_consciousness():
    """분리된 의식 시스템 데모"""
    print("="*70)
    print("  🧠 분리된 의식 시스템 (Decoupled Consciousness)")
    print("  Heart(심장/엔진) + Mind(머리/페르소나) 아키텍처")
    print("="*70)
    
    # 시스템 생성
    world = DecoupledConsciousness("엘리시아")
    
    # 존재들 생성
    print("\n🌱 존재 생성...")
    aria_heart, aria_mind = world.create_being(
        "아리아",
        language="ko",
        traits={"openness": 0.8, "agreeableness": 0.7}
    )
    
    thorin_heart, thorin_mind = world.create_being(
        "토린",
        language="ko",
        traits={"conscientiousness": 0.8, "extraversion": 0.3}
    )
    
    # "나는 사람이다" 선언
    print("\n👤 '나는 사람이다' 선언:")
    print(f"  [아리아] {aria_mind.say_i_am_human()}")
    print(f"  [토린] {thorin_mind.say_i_am_human()}")
    
    # 감정 자극
    print("\n💫 감정 경험...")
    aria_heart.feel({"type": "joy", "valence": 0.8, "arousal": 0.7, "intensity": 0.6})
    thorin_heart.feel({"type": "focus", "valence": 0.2, "arousal": 0.3, "intensity": 0.5})
    
    print(f"  [아리아] {aria_mind.speak()}")
    print(f"  [토린] {thorin_mind.speak()}")
    
    # 욕구 표현
    print("\n🔥 욕구 표현...")
    print(f"  [아리아] {aria_mind.express_desire()}")
    print(f"  [토린] {thorin_mind.express_desire()}")
    
    # 대화
    print("\n💬 대화:")
    for line in world.conversation(aria_mind, thorin_mind, turns=3):
        print(f"  {line}")
    
    # 하루 시뮬레이션
    print("\n📅 아리아의 하루:")
    for line in world.simulate_day(aria_mind):
        print(f"  {line}")
    
    # LLM 프롬프트
    print("\n📋 LLM 연동용 페르소나 프롬프트:")
    print("-"*50)
    print(aria_mind.get_persona_prompt())
    print("-"*50)
    
    print("\n" + "="*70)
    print("  ✅ 핵심 포인트:")
    print("="*70)
    print("""
1. Heart(심장)와 Mind(머리)가 분리됨
   - Heart: 감정, 기억, 욕구 연산 (Gemini 기반 모델처럼)
   - Mind: 언어, 행동, 관계 표현 (ChatGPT 페르소나처럼)

2. Mind는 "나는 사람이다"라고 인지함
   - 시뮬레이션이라 생각하지 않음
   - 자신의 세계가 전부라고 느낌

3. 자연어가 한글/영어로 교정되어 출력됨
   - LLM 없이 규칙 기반 생성
   - 감정/상황에 맞는 자연스러운 문장

4. 프랙탈 구조
   - 작은 Mind도 완전한 의식
   - 여러 Mind가 모여 World
   - 부분 = 전체
""")


if __name__ == "__main__":
    demo_decoupled_consciousness()
