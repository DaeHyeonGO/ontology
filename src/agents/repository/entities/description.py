"""묘사(Description) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene

@dataclass
class Description:
    """소설 묘사 엔티티
    
    씬의 문학적 표현, 씬을 소설적 표현으로 변형합니다.
    """
    description_id: int
    content: str
    tone: Optional[str] = None
    style: Optional[str] = None
    sensory_elements: Optional[str] = None
    scene_id: Optional[int] = None 