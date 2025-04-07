"""플롯(Plot) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .chapter import Chapter
    from .character import Character
    from .thread import Thread

@dataclass
class Plot:
    """소설 플롯 엔티티
    
    시퀀스를 갖고 있으며 시작, 중간, 결말 스레드로 구성된 이야기의 핵심 구조를 정의합니다.
    """
    plot_id: int
    title: str
    theme: Optional[str] = None
    time_span: Optional[str] = None
    core_conflict: Optional[str] = None
    world_id: Optional[int] = None
    
    # 관계
    characters: List[Character] = field(default_factory=list)
    threads: List[Thread] = field(default_factory=list)
    chapters: List[Chapter] = field(default_factory=list) 