from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict

@dataclass
class CharacterEntity:
    id: Optional[int] = None
    name: str = ""
    role: str = ""
    description: Optional[str] = None
    motivation: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterEntity':
        return cls(
            id=data.get('id'),
            name=data.get('name', ""),
            role=data.get('role', ""),
            description=data.get('description'),
            motivation=data.get('motivation')
        )

@dataclass
class EventEntity:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    importance: int = 1
    characters: List[CharacterEntity] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventEntity':
        return cls(
            id=data.get('id'),
            title=data.get('title', ""),
            description=data.get('description', ""),
            importance=data.get('importance', 1)
        )

@dataclass
class PlotPointEntity:
    id: Optional[int] = None
    event_id: Optional[int] = None
    timing: str = ""
    emotional_impact: Optional[str] = None
    consequences: List[str] = field(default_factory=list)
    event: Optional[EventEntity] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlotPointEntity':
        return cls(
            id=data.get('id'),
            event_id=data.get('event_id'),
            timing=data.get('timing', ""),
            emotional_impact=data.get('emotional_impact')
        )

@dataclass
class BasicPlotEntity:
    id: Optional[int] = None
    sequence: int = 0
    title: str = ""
    theme: str = ""
    setting: str = ""
    time_period: Optional[str] = None
    main_conflict: str = ""
    resolution: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    characters: List[CharacterEntity] = field(default_factory=list)
    plot_points: List[PlotPointEntity] = field(default_factory=list)
    subplot_threads: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BasicPlotEntity':
        return cls(
            id=data.get('id'),
            title=data.get('title', ""),
            theme=data.get('theme', ""),
            setting=data.get('setting', ""),
            time_period=data.get('time_period'),
            main_conflict=data.get('main_conflict', ""),
            resolution=data.get('resolution')
        )
