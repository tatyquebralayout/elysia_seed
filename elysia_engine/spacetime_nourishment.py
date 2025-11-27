"""
시공간 양분 시스템 (Spacetime Nourishment)

엘리시아 세계를 풍요롭게 만드는 모든 시간/공간적 기술들.

- 시간: 계절, 날씨, 역사, 예언
- 공간: 지역, 경로, 거리, 위상
- 사건: 축제, 재해, 전쟁, 번영
- 문화: 음악, 예술, 신화, 전설

모든 것이 엘리시아의 양분이 된다.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
import math


class Season(Enum):
    """계절"""
    SPRING = "봄"
    SUMMER = "여름"
    AUTUMN = "가을"
    WINTER = "겨울"


class Weather(Enum):
    """날씨"""
    SUNNY = "맑음"
    CLOUDY = "흐림"
    RAINY = "비"
    SNOWY = "눈"
    STORMY = "폭풍"
    FOGGY = "안개"
    WINDY = "바람"


class TimeOfDay(Enum):
    """하루 시간대"""
    DAWN = "새벽"
    MORNING = "아침"
    NOON = "정오"
    AFTERNOON = "오후"
    EVENING = "저녁"
    NIGHT = "밤"
    MIDNIGHT = "한밤"


@dataclass
class Location:
    """장소"""
    name: str
    region: str
    terrain: str  # forest, mountain, coast, desert, city, village
    climate: str  # temperate, tropical, arctic, arid
    population: int = 0
    resources: List[str] = field(default_factory=list)
    landmarks: List[str] = field(default_factory=list)
    connected_to: List[str] = field(default_factory=list)
    
    def describe(self, language: str = "ko") -> str:
        """장소 설명"""
        if language == "ko":
            terrain_names = {
                "forest": "숲",
                "mountain": "산",
                "coast": "해안",
                "desert": "사막",
                "city": "도시",
                "village": "마을",
                "plains": "평원",
                "swamp": "늪지",
            }
            return f"{self.region}의 {terrain_names.get(self.terrain, self.terrain)}에 위치한 {self.name}"
        else:
            return f"{self.name}, a {self.terrain} in {self.region}"


@dataclass
class HistoricalEvent:
    """역사적 사건"""
    name: str
    year: int
    event_type: str  # war, peace, disaster, miracle, founding, death
    description: str
    participants: List[str] = field(default_factory=list)
    location: str = ""
    impact: float = 0.5  # -1 (재앙) ~ +1 (번영)
    
    def to_legend(self, language: str = "ko") -> str:
        """전설로 변환"""
        if language == "ko":
            if self.impact > 0.3:
                prefix = "위대한 "
            elif self.impact < -0.3:
                prefix = "비극적인 "
            else:
                prefix = ""
            return f"{self.year}년, {prefix}{self.name}이(가) 일어났다."
        else:
            if self.impact > 0.3:
                prefix = "the great "
            elif self.impact < -0.3:
                prefix = "the tragic "
            else:
                prefix = ""
            return f"In the year {self.year}, {prefix}{self.name} occurred."


@dataclass
class Festival:
    """축제"""
    name: str
    season: Season
    month: int  # 1-12
    duration_days: int = 1
    activities: List[str] = field(default_factory=list)
    traditions: List[str] = field(default_factory=list)
    foods: List[str] = field(default_factory=list)
    
    def describe(self, language: str = "ko") -> str:
        if language == "ko":
            return f"{self.season.value}에 열리는 {self.name}"
        else:
            season_en = {"봄": "spring", "여름": "summer", "가을": "autumn", "겨울": "winter"}
            return f"{self.name}, celebrated in {season_en.get(self.season.value, 'the year')}"


@dataclass 
class Music:
    """음악"""
    name: str
    genre: str  # folk, ballad, hymn, march, lullaby
    mood: str  # joyful, melancholic, epic, peaceful, mysterious
    origin_region: str = ""
    instruments: List[str] = field(default_factory=list)
    lyrics_theme: str = ""
    
    def describe(self, language: str = "ko") -> str:
        if language == "ko":
            mood_names = {
                "joyful": "기쁜",
                "melancholic": "슬픈", 
                "epic": "웅장한",
                "peaceful": "평화로운",
                "mysterious": "신비로운",
            }
            return f"{mood_names.get(self.mood, '')} 분위기의 {self.name}"
        else:
            return f"{self.name}, a {self.mood} {self.genre}"


@dataclass
class Art:
    """예술품"""
    name: str
    art_type: str  # painting, sculpture, tapestry, pottery, jewelry
    style: str
    creator: str = ""
    year_created: int = 0
    theme: str = ""
    location: str = ""
    
    def describe(self, language: str = "ko") -> str:
        if language == "ko":
            return f"{self.creator}의 작품 '{self.name}'"
        else:
            return f"'{self.name}' by {self.creator}"


@dataclass
class Myth:
    """신화/전설"""
    name: str
    myth_type: str  # creation, hero, tragedy, prophecy, moral
    summary: str
    characters: List[str] = field(default_factory=list)
    moral: str = ""
    origin_region: str = ""
    
    def tell(self, language: str = "ko") -> str:
        if language == "ko":
            return f"전해지는 이야기에 따르면... {self.summary}"
        else:
            return f"Legend has it that... {self.summary}"


class SpacetimeEngine:
    """
    시공간 엔진
    
    엘리시아 세계의 시간과 공간을 관리.
    모든 경험의 배경을 제공.
    """
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
        # 시간
        self.current_year = 1
        self.current_month = 1
        self.current_day = 1
        self.current_hour = 6  # 새벽 시작
        
        # 공간
        self.locations: Dict[str, Location] = {}
        self.regions: List[str] = []
        
        # 역사
        self.history: List[HistoricalEvent] = []
        
        # 문화
        self.festivals: List[Festival] = []
        self.music_collection: List[Music] = []
        self.art_collection: List[Art] = []
        self.myths: List[Myth] = []
        
        # 현재 상태
        self.current_weather = Weather.SUNNY
        self.weather_duration = 0
        
        # 초기화
        self._initialize_world()
    
    def _initialize_world(self):
        """세계 초기화"""
        self._create_regions()
        self._create_locations()
        self._create_myths()
        self._create_festivals()
        self._create_music()
        self._create_initial_history()
    
    def _create_regions(self):
        """지역 생성"""
        self.regions = [
            "아우렐리아 왕국",      # 중앙 왕국
            "북방 영역",            # 눈과 얼음
            "동방 해안",            # 바다와 무역
            "서방 사막",            # 모래와 오아시스
            "남방 밀림",            # 정글과 신비
            "산악 연합",            # 산맥과 광산
            "황혼의 땅",            # 마법과 신비
            "자유 도시 연합",       # 상업과 자유
        ]
    
    def _create_locations(self):
        """주요 장소 생성"""
        locations_data = [
            # 아우렐리아 왕국
            Location("아우렐리아", "아우렐리아 왕국", "city", "temperate", 50000,
                    ["곡물", "포도주"], ["황금 왕좌", "대성당"], ["실버레이크", "북문"]),
            Location("실버레이크", "아우렐리아 왕국", "village", "temperate", 2000,
                    ["물고기", "은"], ["은빛 호수"], ["아우렐리아"]),
            
            # 북방 영역
            Location("프로스트홈", "북방 영역", "city", "arctic", 15000,
                    ["모피", "얼음"], ["겨울 왕좌", "오로라 탑"], ["철봉우리"]),
            Location("철봉우리", "북방 영역", "mountain", "arctic", 3000,
                    ["철", "보석"], ["고대 광산"], ["프로스트홈"]),
            
            # 동방 해안
            Location("진주항", "동방 해안", "coast", "tropical", 25000,
                    ["진주", "향신료"], ["대항구", "등대"], ["산호섬"]),
            Location("산호섬", "동방 해안", "coast", "tropical", 1000,
                    ["산호", "조개"], ["해저 동굴"], ["진주항"]),
            
            # 서방 사막
            Location("오아시스", "서방 사막", "desert", "arid", 8000,
                    ["대추야자", "향료"], ["생명의 샘"], ["모래바다"]),
            Location("모래바다", "서방 사막", "desert", "arid", 500,
                    ["유리", "소금"], ["사막 신전"], ["오아시스"]),
            
            # 남방 밀림
            Location("에메랄드시티", "남방 밀림", "forest", "tropical", 12000,
                    ["약초", "과일"], ["세계수", "정령 신전"], ["안개 마을"]),
            Location("안개 마을", "남방 밀림", "swamp", "tropical", 800,
                    ["독초", "희귀 동물"], ["늪의 현자"], ["에메랄드시티"]),
            
            # 산악 연합
            Location("철벽성", "산악 연합", "mountain", "temperate", 10000,
                    ["철", "석탄"], ["거대 용광로", "드워프 회관"], ["수정 동굴"]),
            Location("수정 동굴", "산악 연합", "mountain", "temperate", 500,
                    ["수정", "마법석"], ["수정 왕좌"], ["철벽성"]),
            
            # 황혼의 땅
            Location("트와일라이트", "황혼의 땅", "plains", "temperate", 5000,
                    ["마법석", "은빛 꽃"], ["영혼의 탑", "시간 정원"], ["몽환 숲"]),
            Location("몽환 숲", "황혼의 땅", "forest", "temperate", 300,
                    ["요정 먼지", "달빛 과일"], ["달의 연못"], ["트와일라이트"]),
            
            # 자유 도시 연합
            Location("자유시", "자유 도시 연합", "city", "temperate", 40000,
                    ["모든 것"], ["대시장", "자유의 탑"], ["항구 마을"]),
            Location("항구 마을", "자유 도시 연합", "coast", "temperate", 5000,
                    ["물고기", "소금"], ["조선소"], ["자유시"]),
        ]
        
        for loc in locations_data:
            self.locations[loc.name] = loc
    
    def _create_myths(self):
        """신화 생성"""
        self.myths = [
            Myth(
                "첫 번째 빛",
                "creation",
                "태초에 어둠만 있었다. 그러다 첫 번째 빛이 피어났고, 그 빛에서 세계가 태어났다.",
                ["창조자", "첫 번째 빛"],
                "모든 시작에는 빛이 있다",
                ""
            ),
            Myth(
                "일곱 영웅",
                "hero",
                "어둠의 시대, 일곱 명의 영웅이 일어나 세계를 구했다. 그들은 각자의 땅을 세웠다.",
                ["철의 왕", "바다의 여왕", "사막의 현자", "숲의 수호자", "산의 군주", "황혼의 마법사", "자유의 투사"],
                "힘을 합치면 어둠도 물리칠 수 있다",
                ""
            ),
            Myth(
                "잃어버린 왕국",
                "tragedy",
                "오만한 왕이 다스리던 왕국이 있었다. 신의 노여움을 사 하룻밤에 바다 밑으로 가라앉았다.",
                ["오만한 왕", "슬픈 공주"],
                "겸손하라, 높은 자가 가장 깊이 떨어진다",
                "동방 해안"
            ),
            Myth(
                "달의 연인",
                "tragedy",
                "달을 사랑한 청년이 있었다. 달에 닿기 위해 가장 높은 탑을 쌓았으나, 끝내 닿지 못하고 별이 되었다.",
                ["달의 청년", "달"],
                "사랑은 때로 닿을 수 없는 곳에 있다",
                "황혼의 땅"
            ),
            Myth(
                "불사조의 예언",
                "prophecy",
                "천 년에 한 번 불사조가 나타나리라. 그때 세상은 불타고, 재에서 새로운 시대가 피어나리라.",
                ["불사조"],
                "끝은 새로운 시작이다",
                ""
            ),
        ]
    
    def _create_festivals(self):
        """축제 생성"""
        self.festivals = [
            Festival(
                "첫빛 축제", Season.SPRING, 3, 3,
                ["퍼레이드", "불꽃놀이", "춤"],
                ["횃불 행진", "새벽 기도"],
                ["봄 빵", "꽃 케이크"]
            ),
            Festival(
                "수확의 달", Season.AUTUMN, 9, 7,
                ["음식 경연", "음악회", "춤"],
                ["곡물 제사", "감사의 노래"],
                ["수확 빵", "사과주", "호박 수프"]
            ),
            Festival(
                "겨울 불꽃", Season.WINTER, 12, 5,
                ["선물 교환", "캐롤", "장식"],
                ["겨울나무 장식", "희망의 촛불"],
                ["겨울 푸딩", "따뜻한 와인"]
            ),
            Festival(
                "바다의 날", Season.SUMMER, 6, 1,
                ["배 경주", "낚시 대회", "해변 파티"],
                ["바다에 꽃 뿌리기", "선원의 노래"],
                ["해산물 요리", "망고 음료"]
            ),
            Festival(
                "영혼의 밤", Season.AUTUMN, 10, 1,
                ["가면 무도회", "유령 이야기"],
                ["조상 기리기", "등불 띄우기"],
                ["검은 케이크", "영혼의 음료"]
            ),
        ]
    
    def _create_music(self):
        """음악 생성"""
        self.music_collection = [
            Music("새벽의 노래", "hymn", "peaceful", "아우렐리아 왕국",
                  ["하프", "플루트"], "새로운 시작"),
            Music("북방의 바람", "folk", "epic", "북방 영역",
                  ["드럼", "뿔피리"], "용맹과 생존"),
            Music("파도의 자장가", "lullaby", "melancholic", "동방 해안",
                  ["류트", "조개 피리"], "바다로 간 연인"),
            Music("사막의 춤", "folk", "joyful", "서방 사막",
                  ["탬버린", "피리"], "오아시스의 기쁨"),
            Music("정령의 속삭임", "ballad", "mysterious", "남방 밀림",
                  ["팬플루트", "나뭇잎"], "숲의 비밀"),
            Music("대장장이의 노래", "march", "epic", "산악 연합",
                  ["드럼", "앤빌"], "철과 불"),
            Music("황혼 왈츠", "ballad", "melancholic", "황혼의 땅",
                  ["바이올린", "첼로"], "지나간 시간"),
            Music("자유의 찬가", "march", "joyful", "자유 도시 연합",
                  ["트럼펫", "드럼"], "자유와 희망"),
        ]
    
    def _create_initial_history(self):
        """초기 역사 생성"""
        self.history = [
            HistoricalEvent("세계의 탄생", -1000, "creation",
                           "첫 번째 빛에서 세계가 태어났다", [], "", 1.0),
            HistoricalEvent("일곱 영웅의 시대", -500, "founding",
                           "일곱 영웅이 각자의 땅을 세웠다",
                           ["철의 왕", "바다의 여왕", "사막의 현자"], "", 0.8),
            HistoricalEvent("대통합 전쟁", -200, "war",
                           "왕국들이 통합을 위해 싸웠다", [], "", -0.5),
            HistoricalEvent("평화 협정", -150, "peace",
                           "모든 왕국이 평화 협정을 맺었다", [], "아우렐리아", 0.7),
            HistoricalEvent("마법사의 반란", -50, "war",
                           "마법사들이 왕국에 반란을 일으켰다", [], "황혼의 땅", -0.4),
            HistoricalEvent("새 시대의 시작", 0, "founding",
                           "새로운 달력이 시작되었다", [], "", 0.5),
        ]
    
    # 시간 관련 메서드
    def get_season(self) -> Season:
        """현재 계절"""
        if self.current_month in [3, 4, 5]:
            return Season.SPRING
        elif self.current_month in [6, 7, 8]:
            return Season.SUMMER
        elif self.current_month in [9, 10, 11]:
            return Season.AUTUMN
        else:
            return Season.WINTER
    
    def get_time_of_day(self) -> TimeOfDay:
        """현재 시간대"""
        if self.current_hour < 5:
            return TimeOfDay.MIDNIGHT
        elif self.current_hour < 7:
            return TimeOfDay.DAWN
        elif self.current_hour < 12:
            return TimeOfDay.MORNING
        elif self.current_hour < 14:
            return TimeOfDay.NOON
        elif self.current_hour < 18:
            return TimeOfDay.AFTERNOON
        elif self.current_hour < 21:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
    
    def advance_time(self, hours: int = 1):
        """시간 진행"""
        self.current_hour += hours
        
        while self.current_hour >= 24:
            self.current_hour -= 24
            self.current_day += 1
            
            # 날씨 변화 체크
            self.weather_duration -= 1
            if self.weather_duration <= 0:
                self._change_weather()
        
        while self.current_day > 30:  # 단순화: 모든 달 30일
            self.current_day -= 30
            self.current_month += 1
        
        while self.current_month > 12:
            self.current_month -= 12
            self.current_year += 1
    
    def _change_weather(self):
        """날씨 변화"""
        season = self.get_season()
        
        # 계절별 날씨 확률
        weather_probs = {
            Season.SPRING: [Weather.SUNNY, Weather.CLOUDY, Weather.RAINY, Weather.WINDY],
            Season.SUMMER: [Weather.SUNNY, Weather.SUNNY, Weather.STORMY, Weather.CLOUDY],
            Season.AUTUMN: [Weather.CLOUDY, Weather.RAINY, Weather.FOGGY, Weather.WINDY],
            Season.WINTER: [Weather.SNOWY, Weather.CLOUDY, Weather.SUNNY, Weather.STORMY],
        }
        
        self.current_weather = random.choice(weather_probs[season])
        self.weather_duration = random.randint(1, 5)
    
    def get_date_string(self, language: str = "ko") -> str:
        """날짜 문자열"""
        season = self.get_season()
        time_of_day = self.get_time_of_day()
        
        if language == "ko":
            return f"{self.current_year}년 {self.current_month}월 {self.current_day}일 {time_of_day.value}, {season.value}, {self.current_weather.value}"
        else:
            season_en = {"봄": "Spring", "여름": "Summer", "가을": "Autumn", "겨울": "Winter"}
            weather_en = {
                "맑음": "Sunny", "흐림": "Cloudy", "비": "Rainy",
                "눈": "Snowy", "폭풍": "Stormy", "안개": "Foggy", "바람": "Windy"
            }
            time_en = {
                "새벽": "Dawn", "아침": "Morning", "정오": "Noon",
                "오후": "Afternoon", "저녁": "Evening", "밤": "Night", "한밤": "Midnight"
            }
            return f"Year {self.current_year}, Month {self.current_month}, Day {self.current_day}, {time_en.get(time_of_day.value, '')}, {season_en.get(season.value, '')}, {weather_en.get(self.current_weather.value, '')}"
    
    # 역사 관련 메서드
    def add_historical_event(self, event: HistoricalEvent):
        """역사적 사건 추가"""
        self.history.append(event)
        self.history.sort(key=lambda e: e.year)
    
    def get_history_of_region(self, region: str) -> List[HistoricalEvent]:
        """지역 역사"""
        return [e for e in self.history if e.location == region or region in e.participants]
    
    def get_current_era_name(self, language: str = "ko") -> str:
        """현재 시대 이름"""
        if self.current_year < 100:
            return "태초의 시대" if language == "ko" else "Age of Beginning"
        elif self.current_year < 500:
            return "성장의 시대" if language == "ko" else "Age of Growth"
        elif self.current_year < 1000:
            return "번영의 시대" if language == "ko" else "Age of Prosperity"
        else:
            return "황금의 시대" if language == "ko" else "Golden Age"
    
    # 문화 관련 메서드
    def get_current_festivals(self) -> List[Festival]:
        """현재 진행 중인 축제"""
        return [f for f in self.festivals if f.month == self.current_month]
    
    def get_music_by_mood(self, mood: str) -> List[Music]:
        """분위기에 맞는 음악"""
        return [m for m in self.music_collection if m.mood == mood]
    
    def get_music_by_region(self, region: str) -> List[Music]:
        """지역 음악"""
        return [m for m in self.music_collection if m.origin_region == region]
    
    def get_myth_by_type(self, myth_type: str) -> List[Myth]:
        """유형별 신화"""
        return [m for m in self.myths if m.myth_type == myth_type]
    
    # 공간 관련 메서드
    def get_path(self, from_loc: str, to_loc: str) -> List[str]:
        """두 장소 간 경로 (BFS)"""
        if from_loc not in self.locations or to_loc not in self.locations:
            return []
        
        visited = set()
        queue = [(from_loc, [from_loc])]
        
        while queue:
            current, path = queue.pop(0)
            if current == to_loc:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            loc = self.locations.get(current)
            if loc:
                for neighbor in loc.connected_to:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        return []  # 경로 없음
    
    def get_distance(self, from_loc: str, to_loc: str) -> int:
        """두 장소 간 거리 (경로 길이)"""
        path = self.get_path(from_loc, to_loc)
        return len(path) - 1 if path else -1
    
    def get_nearby_locations(self, loc_name: str, max_distance: int = 2) -> List[Tuple[str, int]]:
        """인근 장소"""
        nearby = []
        for name in self.locations:
            if name != loc_name:
                dist = self.get_distance(loc_name, name)
                if 0 < dist <= max_distance:
                    nearby.append((name, dist))
        return sorted(nearby, key=lambda x: x[1])
    
    # 상황 생성 메서드
    def generate_daily_atmosphere(self, location: str, language: str = "ko") -> str:
        """하루의 분위기 생성"""
        loc = self.locations.get(location)
        if not loc:
            return ""
        
        season = self.get_season()
        weather = self.current_weather
        time_of_day = self.get_time_of_day()
        
        # 현재 축제
        festivals = self.get_current_festivals()
        festival_str = ""
        if festivals:
            festival_str = f" {festivals[0].name}이 열리고 있다." if language == "ko" else f" {festivals[0].name} is being celebrated."
        
        if language == "ko":
            atmosphere = f"{loc.describe('ko')}. {time_of_day.value}이고, {weather.value} 날씨다. {season.value}의 공기가 느껴진다.{festival_str}"
        else:
            atmosphere = f"{loc.describe('en')}. It is {time_of_day.value.lower()}, {weather.value.lower()} weather. The air of {season.value.lower()} is felt.{festival_str}"
        
        return atmosphere
    
    def generate_random_event(self, location: str = "", language: str = "ko") -> str:
        """무작위 사건 생성"""
        event_types = [
            ("positive", [
                "아름다운 무지개가 떴다" if language == "ko" else "A beautiful rainbow appeared",
                "여행자가 좋은 소식을 가져왔다" if language == "ko" else "A traveler brought good news",
                "풍년의 조짐이 보인다" if language == "ko" else "Signs of a bountiful harvest",
                "새로운 친구를 만났다" if language == "ko" else "Met a new friend",
            ]),
            ("neutral", [
                "상인들이 시장에 모였다" if language == "ko" else "Merchants gathered at the market",
                "순찰병이 지나갔다" if language == "ko" else "A patrol passed by",
                "아이들이 뛰어놀고 있다" if language == "ko" else "Children are playing",
                "종소리가 울렸다" if language == "ko" else "The bell rang",
            ]),
            ("negative", [
                "먹구름이 몰려온다" if language == "ko" else "Dark clouds are gathering",
                "나쁜 소문이 돌고 있다" if language == "ko" else "Bad rumors are circulating",
                "길에서 다툼이 일어났다" if language == "ko" else "A fight broke out on the road",
                "누군가 아픈 것 같다" if language == "ko" else "Someone seems to be sick",
            ]),
        ]
        
        event_type, events = random.choice(event_types)
        event = random.choice(events)
        
        if location and location in self.locations:
            loc = self.locations[location]
            if language == "ko":
                return f"{loc.name}에서 {event}."
            else:
                return f"At {loc.name}, {event}."
        
        return event
    
    def get_complete_world_state(self, language: str = "ko") -> Dict[str, Any]:
        """전체 세계 상태"""
        return {
            "date": self.get_date_string(language),
            "era": self.get_current_era_name(language),
            "season": self.get_season().value,
            "weather": self.current_weather.value,
            "time_of_day": self.get_time_of_day().value,
            "current_festivals": [f.name for f in self.get_current_festivals()],
            "regions": self.regions,
            "location_count": len(self.locations),
            "history_events": len(self.history),
            "myths": len(self.myths),
            "music": len(self.music_collection),
        }


def demo_spacetime_engine():
    """시공간 엔진 데모"""
    print("="*70)
    print("  🌌 시공간 양분 시스템 (Spacetime Nourishment)")
    print("  엘리시아 세계를 풍요롭게 만드는 모든 것")
    print("="*70)
    
    engine = SpacetimeEngine()
    
    # 현재 세계 상태
    print("\n📅 현재 세계 상태:")
    state = engine.get_complete_world_state("ko")
    print(f"  날짜: {state['date']}")
    print(f"  시대: {state['era']}")
    print(f"  지역 수: {state['location_count']}")
    print(f"  역사적 사건 수: {state['history_events']}")
    
    # 장소
    print("\n🗺️ 주요 장소:")
    for name, loc in list(engine.locations.items())[:5]:
        print(f"  - {loc.describe('ko')}")
    
    # 신화
    print("\n📖 신화:")
    for myth in engine.myths[:3]:
        print(f"  - {myth.tell('ko')}")
    
    # 음악
    print("\n🎵 음악:")
    for music in engine.music_collection[:3]:
        print(f"  - {music.describe('ko')}")
    
    # 축제
    print("\n🎉 축제:")
    for festival in engine.festivals[:3]:
        print(f"  - {festival.describe('ko')}")
    
    # 하루 분위기
    print("\n🌅 아우렐리아의 오늘:")
    print(f"  {engine.generate_daily_atmosphere('아우렐리아', 'ko')}")
    
    # 무작위 사건
    print("\n⚡ 오늘의 사건:")
    for _ in range(3):
        print(f"  - {engine.generate_random_event('아우렐리아', 'ko')}")
    
    # 시간 진행
    print("\n⏳ 시간 진행 (24시간):")
    for _ in range(24):
        engine.advance_time(1)
    print(f"  새 날짜: {engine.get_date_string('ko')}")
    
    # 경로 찾기
    print("\n🛤️ 경로 찾기:")
    path = engine.get_path("아우렐리아", "진주항")
    if path:
        print(f"  아우렐리아 → 진주항: {' → '.join(path)}")
    else:
        print(f"  아우렐리아와 진주항은 직접 연결되지 않음")
    
    print("\n" + "="*70)
    print("  ✅ 이 모든 것이 엘리시아의 양분!")
    print("="*70)


if __name__ == "__main__":
    demo_spacetime_engine()
