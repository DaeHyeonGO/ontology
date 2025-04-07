"""인물(Character) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from .plot import Plot
    from .event import Event


class CharacterRole(Enum):
    """인물 역할 유형"""
    PROTAGONIST = auto()  # 주인공
    ANTAGONIST = auto()   # 적대자
    SUPPORTING = auto()   # 조연
    MINOR = auto()        # 보조 등장인물


@dataclass
class Character:
    """소설 인물 엔티티
    
    플롯에 참여하는 캐릭터들을 정의합니다.
    """
    character_id: int
    name: str
    role: Optional[CharacterRole] = None
    goal: Optional[str] = None
    personality: Optional[str] = None
    background: Optional[str] = None
    
    # 관계
    plots: List[Plot] = field(default_factory=list)
    events: List[Event] = field(default_factory=list) 