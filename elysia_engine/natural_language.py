"""
자연 언어 창발 시스템 (Natural Language Emergence)

내적 상태(숫자) → 자연어(한글/영어) 변환

LLM 없이 규칙 기반으로 감정, 생각, 대화를 자연스러운 언어로 표현.
프랙탈 원리: 작은 감정 벡터가 문장으로, 문장이 대화로, 대화가 이야기로.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable
import random
import math


@dataclass
class LanguageState:
    """언어 생성을 위한 내적 상태"""
    emotion_valence: float = 0.0      # -1 (부정) ~ +1 (긍정)
    emotion_arousal: float = 0.5      # 0 (차분) ~ 1 (격앙)
    certainty: float = 0.5            # 0 (불확실) ~ 1 (확신)
    formality: float = 0.5            # 0 (캐주얼) ~ 1 (격식)
    social_distance: float = 0.5      # 0 (친밀) ~ 1 (거리감)
    focus: str = "self"               # self, other, world, abstract
    tense: str = "present"            # past, present, future
    
    
class KoreanPatterns:
    """한글 문장 패턴"""
    
    # 존재 진술
    EXISTENCE = [
        "나는 {name}이야.",
        "나는 {name}라고 해.",
        "{name}, 그게 나야.",
        "내 이름은 {name}이야.",
    ]
    
    EXISTENCE_FORMAL = [
        "저는 {name}입니다.",
        "제 이름은 {name}입니다.",
        "{name}이라고 합니다.",
    ]
    
    # 감정 표현 (valence x arousal 조합)
    EMOTIONS = {
        # (valence >= 0.3, arousal >= 0.5) = 기쁨/흥분
        ("positive", "high"): [
            "정말 기뻐!",
            "너무 좋아!",
            "신난다!",
            "행복해!",
            "완전 설레!",
        ],
        # (valence >= 0.3, arousal < 0.5) = 평온/만족
        ("positive", "low"): [
            "기분이 좋아.",
            "마음이 편해.",
            "만족스러워.",
            "평화로워.",
            "감사해.",
        ],
        # (valence <= -0.3, arousal >= 0.5) = 분노/불안
        ("negative", "high"): [
            "화가 나!",
            "짜증나!",
            "불안해...",
            "무서워...",
            "견딜 수가 없어!",
        ],
        # (valence <= -0.3, arousal < 0.5) = 슬픔/우울
        ("negative", "low"): [
            "슬퍼...",
            "우울해...",
            "외로워...",
            "힘들어...",
            "지쳤어...",
        ],
        # (|valence| < 0.3) = 중립
        ("neutral", "high"): [
            "뭔가 이상해.",
            "좀 신경이 쓰여.",
            "복잡한 기분이야.",
            "정신없어.",
        ],
        ("neutral", "low"): [
            "그냥 그래.",
            "평범해.",
            "특별할 것 없어.",
            "담담해.",
        ],
    }
    
    # 의지 표현
    DESIRES = [
        "{goal}을/를 하고 싶어.",
        "{goal}이/가 되고 싶어.",
        "언젠가 {goal}을/를 할 거야.",
        "{goal}, 그게 내 꿈이야.",
    ]
    
    DESIRES_FORMAL = [
        "{goal}을/를 하고 싶습니다.",
        "{goal}이/가 되고자 합니다.",
        "{goal}을/를 목표로 하고 있습니다.",
    ]
    
    # 생각 표현
    THOUGHTS = {
        "self": [
            "나는 어떤 사람일까...",
            "내가 뭘 원하는 걸까?",
            "나는 왜 이러는 걸까.",
            "스스로가 궁금해.",
        ],
        "other": [
            "{other}는 어떤 사람일까?",
            "{other}의 마음이 궁금해.",
            "{other}를 더 알고 싶어.",
            "{other}와 함께하고 싶어.",
        ],
        "world": [
            "세상은 참 넓어.",
            "이 세계에는 뭐가 있을까?",
            "밖으로 나가고 싶어.",
            "새로운 곳을 보고 싶어.",
        ],
        "abstract": [
            "삶이란 뭘까...",
            "의미가 뭘까?",
            "왜 존재하는 걸까...",
            "진실은 뭘까?",
        ],
    }
    
    # 일상 활동
    ACTIVITIES = {
        "eating": [
            "{food}을/를 먹었어. {taste}.",
            "{food} 맛있다!",
            "배고파서 {food}을/를 먹었어.",
        ],
        "working": [
            "오늘도 {work}을/를 했어.",
            "{work} 일이 끝났어.",
            "열심히 {work}을/를 하는 중이야.",
        ],
        "resting": [
            "좀 쉬어야겠어.",
            "피곤해서 누웠어.",
            "오늘은 푹 쉴 거야.",
        ],
        "socializing": [
            "{other}랑 이야기했어.",
            "{other}를 만났어.",
            "{other}와 좋은 시간을 보냈어.",
        ],
        "creating": [
            "{creation}을/를 만들었어!",
            "새로운 {creation}이 완성됐어.",
            "{creation} 작업 중이야.",
        ],
        "learning": [
            "{subject}을/를 배웠어.",
            "새로운 것을 알게 됐어.",
            "{subject}가 흥미로워.",
        ],
    }
    
    # 일기 형식
    DIARY_INTRO = [
        "오늘은...",
        "오늘 하루는",
        "일기. ",
        "{date}. ",
    ]
    
    DIARY_CONCLUSION = [
        "그런 하루였어.",
        "내일은 어떨까?",
        "오늘도 수고했어, 나.",
        "잘 자, 나.",
    ]
    
    # 대화 - 인사
    GREETINGS = {
        "morning": ["좋은 아침!", "안녕, 잘 잤어?", "일어났어?"],
        "day": ["안녕!", "뭐해?", "오늘 어때?"],
        "evening": ["좋은 저녁!", "저녁 먹었어?", "오늘 하루 어땠어?"],
        "night": ["잘 자.", "좋은 꿈 꿔.", "내일 봐."],
    }
    
    # 대화 - 반응
    RESPONSES = {
        "agreement": ["응, 맞아.", "그렇지.", "나도 그렇게 생각해.", "동감이야."],
        "disagreement": ["음, 글쎄...", "그건 좀 다른 것 같아.", "나는 다르게 생각해."],
        "curiosity": ["정말?", "그래?", "어떻게?", "왜?"],
        "empathy": ["그랬구나...", "힘들었겠다.", "이해해.", "괜찮아."],
        "surprise": ["와!", "대박!", "진짜?!", "놀랍다!"],
    }


class EnglishPatterns:
    """영어 문장 패턴"""
    
    EXISTENCE = [
        "I'm {name}.",
        "My name is {name}.",
        "Call me {name}.",
        "{name}, that's me.",
    ]
    
    EMOTIONS = {
        ("positive", "high"): [
            "I'm so happy!",
            "This is amazing!",
            "I feel great!",
            "I'm thrilled!",
            "This is wonderful!",
        ],
        ("positive", "low"): [
            "I feel good.",
            "I'm content.",
            "I'm at peace.",
            "Life is good.",
            "I'm grateful.",
        ],
        ("negative", "high"): [
            "I'm angry!",
            "This is frustrating!",
            "I'm anxious...",
            "I'm scared...",
            "I can't take this!",
        ],
        ("negative", "low"): [
            "I'm sad...",
            "I feel down...",
            "I'm lonely...",
            "I'm tired...",
            "I'm exhausted...",
        ],
        ("neutral", "high"): [
            "Something feels off.",
            "I'm a bit restless.",
            "It's complicated.",
            "I'm busy.",
        ],
        ("neutral", "low"): [
            "I'm okay.",
            "Nothing special.",
            "Just another day.",
            "I'm calm.",
        ],
    }
    
    DESIRES = [
        "I want to {goal}.",
        "I wish I could {goal}.",
        "My dream is to {goal}.",
        "Someday, I'll {goal}.",
    ]
    
    THOUGHTS = {
        "self": [
            "Who am I, really?",
            "What do I want?",
            "Why am I like this?",
            "I wonder about myself.",
        ],
        "other": [
            "What is {other} like?",
            "I'm curious about {other}.",
            "I want to know {other} better.",
            "I'd like to be with {other}.",
        ],
        "world": [
            "The world is so vast.",
            "What's out there?",
            "I want to explore.",
            "I want to see new places.",
        ],
        "abstract": [
            "What is life...?",
            "What does it all mean?",
            "Why do we exist?",
            "What is truth?",
        ],
    }
    
    ACTIVITIES = {
        "eating": [
            "I had {food}. {taste}.",
            "{food} is delicious!",
            "I was hungry, so I ate {food}.",
        ],
        "working": [
            "I worked on {work} today.",
            "Finished my {work}.",
            "Working on {work} right now.",
        ],
        "resting": [
            "I need some rest.",
            "Taking a break.",
            "Going to rest today.",
        ],
        "socializing": [
            "Talked with {other}.",
            "Met {other} today.",
            "Had a good time with {other}.",
        ],
        "creating": [
            "Created a {creation}!",
            "Finished making {creation}.",
            "Working on {creation}.",
        ],
        "learning": [
            "Learned about {subject}.",
            "Discovered something new.",
            "{subject} is interesting.",
        ],
    }
    
    DIARY_INTRO = [
        "Today...",
        "Today was",
        "Diary entry. ",
        "{date}. ",
    ]
    
    DIARY_CONCLUSION = [
        "That was my day.",
        "Wonder what tomorrow brings?",
        "Good job today, me.",
        "Good night, self.",
    ]
    
    GREETINGS = {
        "morning": ["Good morning!", "Hey, sleep well?", "You're up!"],
        "day": ["Hey!", "What's up?", "How's your day?"],
        "evening": ["Good evening!", "Had dinner?", "How was today?"],
        "night": ["Good night.", "Sweet dreams.", "See you tomorrow."],
    }
    
    RESPONSES = {
        "agreement": ["Yeah, right.", "Exactly.", "I think so too.", "I agree."],
        "disagreement": ["Hmm, I'm not sure...", "I see it differently.", "I disagree."],
        "curiosity": ["Really?", "Yeah?", "How?", "Why?"],
        "empathy": ["I see...", "That must be hard.", "I understand.", "It's okay."],
        "surprise": ["Wow!", "Amazing!", "Really?!", "Incredible!"],
    }


class NaturalLanguageGenerator:
    """
    자연어 생성기
    
    내적 상태를 받아 자연스러운 한글/영어 문장으로 변환.
    LLM 없이 규칙 기반 + 확률적 선택으로 다양성 확보.
    """
    
    def __init__(self, language: str = "ko"):
        """
        language: "ko" (한글) 또는 "en" (영어)
        """
        self.language = language
        self.patterns = KoreanPatterns if language == "ko" else EnglishPatterns
        
        # 최근 생성된 문장들 (반복 방지)
        self.recent_outputs: List[str] = []
        self.max_history = 20
        
    def set_language(self, language: str):
        """언어 변경"""
        self.language = language
        self.patterns = KoreanPatterns if language == "ko" else EnglishPatterns
        
    def _avoid_repetition(self, candidates: List[str]) -> str:
        """최근 사용된 문장 피하기"""
        available = [c for c in candidates if c not in self.recent_outputs]
        if not available:
            available = candidates
        
        choice = random.choice(available)
        self.recent_outputs.append(choice)
        if len(self.recent_outputs) > self.max_history:
            self.recent_outputs.pop(0)
        
        return choice
    
    def _get_emotion_key(self, state: LanguageState) -> Tuple[str, str]:
        """감정 상태를 키로 변환"""
        if state.emotion_valence >= 0.3:
            valence = "positive"
        elif state.emotion_valence <= -0.3:
            valence = "negative"
        else:
            valence = "neutral"
            
        arousal = "high" if state.emotion_arousal >= 0.5 else "low"
        
        return (valence, arousal)
    
    def generate_existence(self, name: str, state: LanguageState) -> str:
        """존재 진술 생성"""
        if state.formality > 0.6 and self.language == "ko":
            patterns = self.patterns.EXISTENCE_FORMAL
        else:
            patterns = self.patterns.EXISTENCE
            
        template = self._avoid_repetition(patterns)
        return template.format(name=name)
    
    def generate_emotion(self, state: LanguageState) -> str:
        """감정 표현 생성"""
        key = self._get_emotion_key(state)
        patterns = self.patterns.EMOTIONS.get(key, self.patterns.EMOTIONS[("neutral", "low")])
        return self._avoid_repetition(patterns)
    
    def generate_desire(self, goal: str, state: LanguageState) -> str:
        """의지/욕구 표현 생성"""
        if state.formality > 0.6 and self.language == "ko":
            patterns = self.patterns.DESIRES_FORMAL
        else:
            patterns = self.patterns.DESIRES
            
        template = self._avoid_repetition(patterns)
        return template.format(goal=goal)
    
    def generate_thought(self, state: LanguageState, other: str = "") -> str:
        """생각 표현 생성"""
        patterns = self.patterns.THOUGHTS.get(state.focus, self.patterns.THOUGHTS["self"])
        template = self._avoid_repetition(patterns)
        return template.format(other=other) if other else template
    
    def generate_activity(self, activity_type: str, **kwargs) -> str:
        """활동 표현 생성"""
        patterns = self.patterns.ACTIVITIES.get(
            activity_type, 
            self.patterns.ACTIVITIES.get("resting", ["..."])
        )
        template = self._avoid_repetition(patterns)
        
        # 기본값 설정
        defaults = {
            "food": "음식" if self.language == "ko" else "food",
            "taste": "맛있었어" if self.language == "ko" else "It was good",
            "work": "일" if self.language == "ko" else "work",
            "other": "누군가" if self.language == "ko" else "someone",
            "creation": "작품" if self.language == "ko" else "something",
            "subject": "그것" if self.language == "ko" else "it",
        }
        
        for key, default in defaults.items():
            if key not in kwargs:
                kwargs[key] = default
                
        return template.format(**kwargs)
    
    def generate_greeting(self, time_of_day: str = "day") -> str:
        """인사 생성"""
        patterns = self.patterns.GREETINGS.get(time_of_day, self.patterns.GREETINGS["day"])
        return self._avoid_repetition(patterns)
    
    def generate_response(self, response_type: str) -> str:
        """반응 생성"""
        patterns = self.patterns.RESPONSES.get(response_type, self.patterns.RESPONSES["agreement"])
        return self._avoid_repetition(patterns)
    
    def generate_diary_entry(
        self, 
        name: str,
        date: str,
        activities: List[Dict],
        state: LanguageState
    ) -> str:
        """일기 항목 생성"""
        parts = []
        
        # 인트로
        intro = self._avoid_repetition(self.patterns.DIARY_INTRO)
        parts.append(intro.format(date=date))
        
        # 감정 상태
        parts.append(self.generate_emotion(state))
        
        # 활동들
        for activity in activities[:3]:  # 최대 3개
            activity_str = self.generate_activity(
                activity.get("type", "resting"),
                **activity
            )
            parts.append(activity_str)
        
        # 마무리
        parts.append(self._avoid_repetition(self.patterns.DIARY_CONCLUSION))
        
        return " ".join(parts)
    
    def generate_conversation_turn(
        self,
        speaker_name: str,
        speaker_state: LanguageState,
        context: str = "",
        is_greeting: bool = False,
        is_response: bool = False,
        response_to_emotion: Optional[Tuple[str, str]] = None
    ) -> str:
        """대화 턴 생성"""
        
        if is_greeting:
            return self.generate_greeting()
        
        if is_response and response_to_emotion:
            valence, _ = response_to_emotion
            if valence == "negative":
                return self.generate_response("empathy")
            elif valence == "positive":
                return self.generate_response("agreement")
            else:
                return self.generate_response("curiosity")
        
        # 일반 대화: 감정 + 생각
        parts = []
        
        # 감정 표현 (확률적)
        if random.random() < 0.6:
            parts.append(self.generate_emotion(speaker_state))
        
        # 생각 표현
        parts.append(self.generate_thought(speaker_state))
        
        return " ".join(parts)
    
    def generate_inner_monologue(
        self,
        name: str,
        state: LanguageState,
        memories: List[str] = None,
        relationships: Dict[str, float] = None
    ) -> str:
        """내면의 독백 생성"""
        parts = []
        
        # 자기 존재 인식
        if random.random() < 0.3:
            parts.append(self.generate_existence(name, state))
        
        # 감정 상태
        parts.append(self.generate_emotion(state))
        
        # 생각
        if state.focus == "other" and relationships:
            # 관계 중 하나를 선택
            other = random.choice(list(relationships.keys())) if relationships else ""
            parts.append(self.generate_thought(state, other=other))
        else:
            parts.append(self.generate_thought(state))
        
        # 기억 회상 (확률적)
        if memories and random.random() < 0.3:
            memory = random.choice(memories[-5:])  # 최근 5개 중
            if self.language == "ko":
                parts.append(f"그때 {memory}...")
            else:
                parts.append(f"I remember {memory}...")
        
        return " ".join(parts)


class BilingualGenerator(NaturalLanguageGenerator):
    """
    이중 언어 생성기
    
    한글과 영어를 동시에 생성하거나, 상황에 따라 전환.
    """
    
    def __init__(self, primary_language: str = "ko"):
        super().__init__(primary_language)
        self.ko_generator = NaturalLanguageGenerator("ko")
        self.en_generator = NaturalLanguageGenerator("en")
        
    def generate_both(self, method_name: str, *args, **kwargs) -> Dict[str, str]:
        """한글과 영어 모두 생성"""
        ko_method = getattr(self.ko_generator, method_name)
        en_method = getattr(self.en_generator, method_name)
        
        return {
            "ko": ko_method(*args, **kwargs),
            "en": en_method(*args, **kwargs),
        }
    
    def generate_mixed(self, method_name: str, *args, **kwargs) -> str:
        """주 언어로 생성, 부 언어 괄호 표기"""
        primary = getattr(self, f"{self.language}_generator")
        secondary_lang = "en" if self.language == "ko" else "ko"
        secondary = getattr(self, f"{secondary_lang}_generator")
        
        primary_method = getattr(primary, method_name)
        secondary_method = getattr(secondary, method_name)
        
        primary_text = primary_method(*args, **kwargs)
        secondary_text = secondary_method(*args, **kwargs)
        
        return f"{primary_text} ({secondary_text})"
