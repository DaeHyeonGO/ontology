"""씬(Scene) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .thread import Thread
    from .description import Description


@dataclass
class Scene:
    """소설 씬 엔티티
    
    장을 구성하는 개별 상황 단위, 플롯의 스레드를 문학적 묘사 이전 상태로 구성합니다.
    """
    scene_id: int
    description: str
    location: Optional[str] = None
    time: Optional[str] = None
    chapter_id: Optional[int] = None
    
    # 관계
    threads: List[Thread] = field(default_factory=list)
    descriptions: List[Description] = field(default_factory=list)
    
    # 씬에 참여하는 인물 추적을 위한 정보
    participating_characters: List[int] = field(default_factory=list) 