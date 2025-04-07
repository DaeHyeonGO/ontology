"""장(Chapter) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .plot import Plot
    from .scene import Scene
    from .revision import Revision


@dataclass
class Chapter:
    """소설 장 엔티티
    
    소설의 구조적 단위를 정의합니다.
    """
    chapter_id: int
    title: str
    sequence_number: Optional[int] = None
    main_theme: Optional[str] = None
    integration_id: Optional[int] = None
    
    # 관계
    plots: List[Plot] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    revisions: List[Revision] = field(default_factory=list) 