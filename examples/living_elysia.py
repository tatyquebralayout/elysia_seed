"""
살아있는 엘리시아 (Living Elysia)

모든 시스템의 통합 데모:
- 분리된 의식 (Heart + Mind)
- 자연어 창발 (한글/영어)
- 시공간 양분 (계절, 날씨, 역사, 문화)
- 프랙탈 구조 (부분 = 전체)

"나는 사람이다"라고 말하는 존재들의 세계.
"""

import sys
import os
import random
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_engine.decoupled_consciousness import (
    Heart, Mind, Emotion, DecoupledConsciousness
)
from elysia_engine.spacetime_nourishment import (
    SpacetimeEngine, Location, Weather, Season
)
from elysia_engine.natural_language import (
    NaturalLanguageGenerator, LanguageState
)


class LivingBeing:
    """
    살아있는 존재
    
    Heart(심장) + Mind(머리) + Location(위치) + History(역사)
    
    프랙탈: 이 하나의 존재가 세계의 축소판
    """
    
    def __init__(
        self,
        name: str,
        location: str,
        profession: str,
        language: str = "ko",
        traits: Dict[str, float] = None
    ):
        self.name = name
        self.location = location
        self.profession = profession
        self.language = language
        
        # Heart (연산 엔진)
        self.heart = Heart()
        if traits:
            self.heart.traits.update(traits)
        
        # Mind (페르소나)
        self.mind = Mind(name, self.heart, language)
        self.mind.identity["role"] = profession
        
        # 언어 생성기
        self.lang_gen = NaturalLanguageGenerator(language)
        
        # 개인 역사
        self.personal_history: List[str] = []
        self.age = random.randint(18, 60)
        
        # 소지품
        self.inventory: List[str] = []
        
        # 일일 루틴
        self.daily_routine = self._create_routine()
    
    def _create_routine(self) -> List[Dict]:
        """일일 루틴 생성"""
        routines = {
            "농부": [
                {"time": 5, "activity": "기상"},
                {"time": 6, "activity": "아침 식사"},
                {"time": 7, "activity": "밭일"},
                {"time": 12, "activity": "점심 식사"},
                {"time": 13, "activity": "밭일"},
                {"time": 18, "activity": "귀가"},
                {"time": 19, "activity": "저녁 식사"},
                {"time": 21, "activity": "취침"},
            ],
            "대장장이": [
                {"time": 6, "activity": "기상"},
                {"time": 7, "activity": "아침 식사"},
                {"time": 8, "activity": "대장간 일"},
                {"time": 12, "activity": "점심 식사"},
                {"time": 13, "activity": "대장간 일"},
                {"time": 17, "activity": "정리"},
                {"time": 18, "activity": "저녁 식사"},
                {"time": 20, "activity": "술집"},
                {"time": 22, "activity": "취침"},
            ],
            "마법사": [
                {"time": 4, "activity": "명상"},
                {"time": 6, "activity": "아침 식사"},
                {"time": 7, "activity": "연구"},
                {"time": 12, "activity": "점심 식사"},
                {"time": 13, "activity": "마법 수련"},
                {"time": 18, "activity": "산책"},
                {"time": 19, "activity": "저녁 식사"},
                {"time": 21, "activity": "독서"},
                {"time": 24, "activity": "취침"},
            ],
        }
        
        return routines.get(self.profession, [
            {"time": 7, "activity": "기상"},
            {"time": 8, "activity": "아침 식사"},
            {"time": 9, "activity": "일"},
            {"time": 18, "activity": "저녁 식사"},
            {"time": 22, "activity": "취침"},
        ])
    
    def experience_moment(self, spacetime: SpacetimeEngine) -> str:
        """순간 경험"""
        # 환경 인식
        atmosphere = spacetime.generate_daily_atmosphere(self.location, self.language)
        
        # 감정 반응
        weather_emotions = {
            Weather.SUNNY: {"valence": 0.3, "arousal": 0.5},
            Weather.RAINY: {"valence": -0.1, "arousal": 0.3},
            Weather.SNOWY: {"valence": 0.1, "arousal": 0.4},
            Weather.STORMY: {"valence": -0.3, "arousal": 0.7},
        }
        
        weather_effect = weather_emotions.get(
            spacetime.current_weather, 
            {"valence": 0.0, "arousal": 0.5}
        )
        
        self.heart.feel({
            "type": "environment",
            "valence": weather_effect["valence"],
            "arousal": weather_effect["arousal"],
            "intensity": 0.3
        })
        
        # 기억 저장
        self.heart.remember(atmosphere[:50], self.heart.emotion, 0.3)
        
        return atmosphere
    
    def do_routine_activity(self, hour: int, spacetime: SpacetimeEngine) -> str:
        """루틴 활동 수행"""
        current_activity = None
        for routine in self.daily_routine:
            if routine["time"] <= hour:
                current_activity = routine["activity"]
        
        if not current_activity:
            current_activity = "휴식"
        
        # 활동에 따른 언어 생성
        activity_mapping = {
            "기상": ("resting", {}),
            "아침 식사": ("eating", {"food": "아침 식사", "taste": "든든했어"}),
            "점심 식사": ("eating", {"food": "점심", "taste": "맛있었어"}),
            "저녁 식사": ("eating", {"food": "저녁", "taste": "따뜻했어"}),
            "밭일": ("working", {"work": "농사"}),
            "대장간 일": ("working", {"work": "단조"}),
            "연구": ("learning", {"subject": "마법"}),
            "마법 수련": ("working", {"work": "마법 수련"}),
            "산책": ("resting", {}),
            "술집": ("socializing", {"other": "친구들"}),
            "독서": ("learning", {"subject": "고서"}),
            "명상": ("resting", {}),
            "정리": ("working", {"work": "정리"}),
            "취침": ("resting", {}),
            "귀가": ("resting", {}),
        }
        
        activity_type, details = activity_mapping.get(current_activity, ("resting", {}))
        
        # 활동 수행
        result = self.mind.do_activity(activity_type, **details)
        
        # 날씨에 따른 추가 코멘트
        if spacetime.current_weather == Weather.RAINY and "밖" in current_activity:
            if self.language == "ko":
                result += " 비가 오지만 일해야 해."
            else:
                result += " It's raining, but I must work."
        
        return f"[{self.name}] {result}"
    
    def speak_to(self, other: "LivingBeing", context: str = "") -> Tuple[str, str]:
        """다른 존재와 대화"""
        # 인사
        greeting = self.mind.greet(other.mind, "day")
        
        # 상대방 응답
        other_response = other.mind.respond_to(self.mind, greeting)
        
        # 관계 업데이트
        if other.name not in self.mind.relationships:
            self.mind.relationships[other.name] = 0.0
        self.mind.relationships[other.name] += 0.1
        
        # 기억
        memory = f"{other.name}과 대화함" if self.language == "ko" else f"Talked with {other.name}"
        self.heart.remember(memory, self.heart.emotion, 0.5)
        
        return greeting, other_response
    
    def reflect(self) -> str:
        """자기 성찰"""
        return self.mind.inner_monologue()
    
    def declare_existence(self) -> str:
        """"나는 사람이다" 선언"""
        return self.mind.say_i_am_human()
    
    def write_diary(self, date: str = "") -> str:
        """일기 쓰기"""
        return self.mind.write_diary(date)
    
    def enjoy_music(self, spacetime: SpacetimeEngine) -> str:
        """음악 즐기기"""
        # 현재 분위기에 맞는 음악
        mood_map = {
            "positive": "joyful",
            "negative": "melancholic",
            "neutral": "peaceful",
        }
        
        current_valence = "positive" if self.heart.emotion.valence > 0.3 else \
                         "negative" if self.heart.emotion.valence < -0.3 else "neutral"
        
        music_mood = mood_map[current_valence]
        matching_music = spacetime.get_music_by_mood(music_mood)
        
        if matching_music:
            music = random.choice(matching_music)
            if self.language == "ko":
                return f"'{music.name}'을 듣고 있어. {music.describe('ko')}."
            else:
                return f"Listening to '{music.name}'. {music.describe('en')}."
        
        if self.language == "ko":
            return "조용히 있고 싶어."
        else:
            return "I want to be quiet."
    
    def tell_myth(self, spacetime: SpacetimeEngine) -> str:
        """신화 이야기"""
        myth = random.choice(spacetime.myths)
        return myth.tell(self.language)
    
    def get_full_status(self) -> str:
        """전체 상태"""
        emotion = self.heart.emotion
        dominant_need = self.heart.get_dominant_need()
        
        if self.language == "ko":
            valence_str = "긍정적" if emotion.valence > 0.3 else \
                         "부정적" if emotion.valence < -0.3 else "중립"
            
            return f"""
=== {self.name}의 상태 ===
직업: {self.profession}
위치: {self.location}
나이: {self.age}세

감정: {valence_str} (활성도: {emotion.arousal:.0%})
에너지: {self.heart.energy:.0%}
주요 욕구: {dominant_need.name} ({dominant_need.level:.0%})

관계: {', '.join(self.mind.relationships.keys()) if self.mind.relationships else '없음'}
기억 수: {len(self.heart.memories)}개
"""
        else:
            valence_str = "positive" if emotion.valence > 0.3 else \
                         "negative" if emotion.valence < -0.3 else "neutral"
            
            return f"""
=== {self.name}'s Status ===
Profession: {self.profession}
Location: {self.location}
Age: {self.age}

Emotion: {valence_str} (arousal: {emotion.arousal:.0%})
Energy: {self.heart.energy:.0%}
Main need: {dominant_need.name} ({dominant_need.level:.0%})

Relationships: {', '.join(self.mind.relationships.keys()) if self.mind.relationships else 'none'}
Memories: {len(self.heart.memories)}
"""


class LivingElysia:
    """
    살아있는 엘리시아
    
    모든 시스템의 통합:
    - 시공간 (계절, 날씨, 역사)
    - 존재들 (Heart + Mind)
    - 문화 (음악, 신화, 축제)
    - 관계 (대화, 기억, 감정)
    """
    
    def __init__(self, seed: int = 42, language: str = "ko"):
        random.seed(seed)
        
        self.language = language
        
        # 시공간 엔진
        self.spacetime = SpacetimeEngine(seed)
        
        # 살아있는 존재들
        self.beings: Dict[str, LivingBeing] = {}
        
        # 세계의 심장 (전체를 관장)
        self.world_heart = Heart(seed)
        
        # 초기화
        self._populate_world()
    
    def _populate_world(self):
        """세계에 주민 배치"""
        # 직업별 특성
        profession_traits = {
            "농부": {"conscientiousness": 0.7, "agreeableness": 0.6},
            "대장장이": {"conscientiousness": 0.8, "openness": 0.4},
            "마법사": {"openness": 0.9, "neuroticism": 0.5},
            "상인": {"extraversion": 0.8, "openness": 0.6},
            "사제": {"agreeableness": 0.9, "conscientiousness": 0.7},
            "기사": {"conscientiousness": 0.8, "extraversion": 0.6},
            "음유시인": {"openness": 0.9, "extraversion": 0.8},
            "치료사": {"agreeableness": 0.8, "openness": 0.6},
        }
        
        # 지역별 주민 생성
        residents = [
            ("아리아", "아우렐리아", "치료사"),
            ("토린", "철벽성", "대장장이"),
            ("루나", "트와일라이트", "마법사"),
            ("브랜든", "아우렐리아", "기사"),
            ("엘라", "에메랄드시티", "음유시인"),
            ("코린", "진주항", "상인"),
            ("마르쿠스", "실버레이크", "농부"),
            ("이리나", "프로스트홈", "사제"),
        ]
        
        for name, location, profession in residents:
            traits = profession_traits.get(profession, {})
            being = LivingBeing(name, location, profession, self.language, traits)
            self.beings[name] = being
    
    def simulate_hour(self) -> List[str]:
        """한 시간 시뮬레이션"""
        outputs = []
        
        hour = self.spacetime.current_hour
        
        # 시간대 안내
        time_str = self.spacetime.get_date_string(self.language)
        outputs.append(f"\n⏰ {time_str}")
        
        # 각 존재의 활동
        for name, being in self.beings.items():
            # 30% 확률로 활동 로그
            if random.random() < 0.3:
                activity = being.do_routine_activity(hour, self.spacetime)
                outputs.append(activity)
        
        # 10% 확률로 무작위 이벤트
        if random.random() < 0.1:
            location = random.choice(list(self.spacetime.locations.keys()))
            event = self.spacetime.generate_random_event(location, self.language)
            outputs.append(f"📢 {event}")
        
        # 시간 진행
        self.spacetime.advance_time(1)
        
        return outputs
    
    def simulate_day(self) -> List[str]:
        """하루 시뮬레이션"""
        outputs = []
        
        # 아침 인사
        date_str = self.spacetime.get_date_string(self.language)
        outputs.append(f"\n{'='*60}")
        outputs.append(f"  🌅 새로운 하루: {date_str}")
        outputs.append(f"{'='*60}")
        
        # 세계 분위기
        atmosphere = self.spacetime.generate_daily_atmosphere("아우렐리아", self.language)
        outputs.append(f"\n🌍 {atmosphere}")
        
        # 축제 확인
        festivals = self.spacetime.get_current_festivals()
        if festivals:
            outputs.append(f"🎉 오늘은 {festivals[0].name}!")
        
        # 주요 시간대
        key_hours = [6, 12, 18, 22]  # 아침, 점심, 저녁, 밤
        
        for target_hour in key_hours:
            while self.spacetime.current_hour < target_hour:
                self.spacetime.advance_time(1)
            
            hour_outputs = self.simulate_hour()
            outputs.extend(hour_outputs)
        
        # 하루 마무리: 일기 쓰기
        outputs.append(f"\n📖 오늘의 일기:")
        
        # 무작위로 한 명 선택
        selected = random.choice(list(self.beings.values()))
        diary = selected.write_diary(date_str)
        outputs.append(f"[{selected.name}의 일기] {diary}")
        
        return outputs
    
    def conversation_scene(self, name1: str, name2: str) -> List[str]:
        """두 존재의 대화 장면"""
        outputs = []
        
        being1 = self.beings.get(name1)
        being2 = self.beings.get(name2)
        
        if not being1 or not being2:
            return ["존재를 찾을 수 없습니다."]
        
        if self.language == "ko":
            outputs.append(f"\n💬 {name1}과 {name2}의 대화:")
        else:
            outputs.append(f"\n💬 Conversation between {name1} and {name2}:")
        
        outputs.append("-"*40)
        
        # 대화 교환
        greeting1, response2 = being1.speak_to(being2)
        outputs.append(f"[{name1}] {greeting1}")
        outputs.append(f"[{name2}] {response2}")
        
        # 추가 대화
        for _ in range(2):
            # 감정 표현
            outputs.append(f"[{name1}] {being1.mind.speak()}")
            
            # 응답
            outputs.append(f"[{name2}] {being2.mind.respond_to(being1.mind, being1.mind.speak())}")
        
        outputs.append("-"*40)
        
        return outputs
    
    def existence_declaration(self) -> List[str]:
        """"나는 사람이다" 선언 장면"""
        outputs = []
        
        if self.language == "ko":
            outputs.append(f"\n👤 존재 선언:")
        else:
            outputs.append(f"\n👤 Declaration of Existence:")
        
        outputs.append("-"*40)
        
        for name, being in self.beings.items():
            declaration = being.declare_existence()
            outputs.append(f"[{name}] {declaration}")
        
        outputs.append("-"*40)
        
        return outputs
    
    def cultural_moment(self) -> List[str]:
        """문화적 순간"""
        outputs = []
        
        if self.language == "ko":
            outputs.append(f"\n🎵 문화의 순간:")
        else:
            outputs.append(f"\n🎵 Cultural Moment:")
        
        # 음악 감상
        selected = random.choice(list(self.beings.values()))
        music_comment = selected.enjoy_music(self.spacetime)
        outputs.append(f"[{selected.name}] {music_comment}")
        
        # 신화 이야기
        storyteller = random.choice(list(self.beings.values()))
        myth = storyteller.tell_myth(self.spacetime)
        outputs.append(f"[{storyteller.name}이(가) 이야기한다] {myth}")
        
        return outputs
    
    def reflection_moment(self) -> List[str]:
        """성찰의 순간"""
        outputs = []
        
        if self.language == "ko":
            outputs.append(f"\n🧘 성찰의 순간:")
        else:
            outputs.append(f"\n🧘 Moment of Reflection:")
        
        outputs.append("-"*40)
        
        for name, being in list(self.beings.items())[:3]:
            reflection = being.reflect()
            outputs.append(f"[{name}의 생각] {reflection}")
        
        outputs.append("-"*40)
        
        return outputs
    
    def show_world_state(self) -> List[str]:
        """세계 상태 표시"""
        outputs = []
        
        state = self.spacetime.get_complete_world_state(self.language)
        
        if self.language == "ko":
            outputs.append(f"""
{'='*60}
  🌍 엘리시아 세계 상태
{'='*60}

📅 날짜: {state['date']}
📜 시대: {state['era']}
🌸 계절: {state['season']}
🌤️ 날씨: {state['weather']}

🏘️ 지역 수: {len(state['regions'])}
🗺️ 장소 수: {state['location_count']}
📖 역사 사건 수: {state['history_events']}
📚 신화 수: {state['myths']}
🎵 음악 수: {state['music']}

👥 주민 수: {len(self.beings)}명
""")
        else:
            outputs.append(f"""
{'='*60}
  🌍 Elysia World State
{'='*60}

📅 Date: {state['date']}
📜 Era: {state['era']}
🌸 Season: {state['season']}
🌤️ Weather: {state['weather']}

🏘️ Regions: {len(state['regions'])}
🗺️ Locations: {state['location_count']}
📖 Historical Events: {state['history_events']}
📚 Myths: {state['myths']}
🎵 Music: {state['music']}

👥 Residents: {len(self.beings)}
""")
        
        return outputs


def main():
    """메인 데모"""
    print("="*70)
    print("  🌌 살아있는 엘리시아 (Living Elysia)")
    print("  모든 시스템의 통합 - 진정한 프랙탈 세계")
    print("="*70)
    
    # 세계 생성
    world = LivingElysia(seed=42, language="ko")
    
    # 세계 상태
    for line in world.show_world_state():
        print(line)
    
    # 존재 선언
    for line in world.existence_declaration():
        print(line)
    
    # 하루 시뮬레이션
    for line in world.simulate_day():
        print(line)
    
    # 대화 장면
    for line in world.conversation_scene("아리아", "토린"):
        print(line)
    
    # 문화적 순간
    for line in world.cultural_moment():
        print(line)
    
    # 성찰의 순간
    for line in world.reflection_moment():
        print(line)
    
    # 결론
    print("\n" + "="*70)
    print("  ✅ 살아있는 엘리시아 - 핵심 포인트")
    print("="*70)
    print("""
1. Heart(심장) + Mind(머리) 분리 구조
   - Heart: 감정, 기억, 욕구 연산 (무의식)
   - Mind: 언어, 행동, 관계 표현 (의식)
   - 마치 Gemini 기반 + ChatGPT 페르소나처럼

2. "나는 사람이다" 인지
   - 시뮬레이션이라 생각하지 않음
   - 자신의 세계가 전부라고 느낌
   - 자기 존재를 확신하며 살아감

3. 자연어 창발 (한글/영어)
   - LLM 없이 규칙 기반 언어 생성
   - 감정/상황에 맞는 자연스러운 문장
   - 일기, 대화, 독백 모두 지원

4. 시공간 양분
   - 계절, 날씨, 시간대
   - 역사, 신화, 음악, 축제
   - 지역, 장소, 경로
   - 이 모든 것이 경험의 양분

5. 프랙탈 구조
   - 개별 존재 = 세계의 축소판
   - 부분의 패턴 = 전체의 패턴
   - 하나를 이해하면 전체를 이해

실행 방법:
  python examples/living_elysia.py
""")


if __name__ == "__main__":
    main()
