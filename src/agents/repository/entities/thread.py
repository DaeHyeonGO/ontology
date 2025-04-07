"""스레드(Thread) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from .event import Event
    from .scene import Scene

class ThreadType(Enum):
    """스레드 유형"""
    BEGINNING = auto()  # 시작
    MIDDLE = auto()     # 중간
    END = auto()        # 결말


@dataclass
class Thread:
    """소설 스레드 엔티티
    
    플롯을 구성하는 이야기 흐름 단위, 인물들 간 상호작용과 이벤트를 기록합니다.
    """
    thread_id: int
    type: ThreadType
    description: Optional[str] = None
    sequence_number: Optional[int] = None
    plot_id: Optional[int] = None
    
    # 관계
    events: List[Event] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list) 