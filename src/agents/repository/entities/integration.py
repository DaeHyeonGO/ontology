"""통합(Integration) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .chapter import Chapter

@dataclass
class Integration:
    """소설 통합 엔티티
    
    모든 장을 하나의 소설로 묶는 과정, 모든 리비전을 이어 하나의 소설로 엮습니다.
    """
    integration_id: int
    title: str
    subtitle: Optional[str] = None
    overall_structure: Optional[str] = None
    connecting_elements: Optional[str] = None
    
    # 관계
    chapters: List[Chapter] = field(default_factory=list) 