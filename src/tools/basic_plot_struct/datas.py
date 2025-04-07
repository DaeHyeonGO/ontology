from typing import List, Optional
from pydantic import BaseModel

class Character(BaseModel):
    name: str
    role: str  # 주인공, 조연, 적대자 등
    description: Optional[str] = None
    motivation: Optional[str] = None

class Event(BaseModel):
    title: str
    description: str
    characters_involved: List[str]  # Character names
    importance: int = 1  # 1-5 scale
    
class PlotPoint(BaseModel):
    event: Event
    timing: str  # "발단", "전개", "위기", "절정", "결말" 중 하나
    consequences: List[str]
    emotional_impact: Optional[str] = None

class BasicPlot(BaseModel):
    sequence: int
    title: str
    genre: List[str]  # "로맨스", "판타지", "미스터리" 등
    theme: str
    characters: List[Character]
    plot_points: List[PlotPoint]
    setting: str
    time_period: Optional[str] = None
    main_conflict: str
    resolution: Optional[str] = None
    subplot_threads: List[str] = []

