"""세계관(World) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .plot import Plot

@dataclass
class World:
    """소설 세계관 엔티티
    
    모든 플롯의 기반이 되는 배경 설정을 정의합니다.
    """
    world_id: int
    name: str
    time_period: Optional[str] = None
    geography: Optional[str] = None
    social_structure: Optional[str] = None
    laws_of_nature: Optional[str] = None
    plots: List[Plot] = field(default_factory=list) 