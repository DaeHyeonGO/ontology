"""이벤트(Event) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from .character import Character


@dataclass
class Event:
    """소설 이벤트 엔티티
    
    스레드 내에서 발생하는 구체적 사건을 정의합니다.
    """
    event_id: int
    description: str
    conditions: Optional[str] = None
    outcome: Optional[str] = None
    thread_id: Optional[int] = None
    
    # 관계
    characters: List[Character] = field(default_factory=list)
    
    # 이벤트에서 캐릭터의 역할을 추적하기 위한 정보
    character_roles: Dict[int, Any] = field(default_factory=dict) 