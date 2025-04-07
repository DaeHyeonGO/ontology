"""리비전(Revision) 엔티티 클래스"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .chapter import Chapter

@dataclass
class Revision:
    """소설 리비전 엔티티
    
    장의 편집/수정 버전, 각 장을 단편의 소설 형식으로 재구성합니다.
    """
    revision_id: int
    version: str
    changes: Optional[str] = None
    reason: Optional[str] = None
    date_created: Optional[date] = None
    chapter_id: Optional[int] = None 