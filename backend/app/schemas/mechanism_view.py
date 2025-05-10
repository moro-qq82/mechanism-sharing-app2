from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MechanismViewBase(BaseModel):
    """
    メカニズム閲覧履歴の基本スキーマ
    """
    mechanism_id: int
    user_id: Optional[int] = None

class MechanismViewCreate(MechanismViewBase):
    """
    メカニズム閲覧履歴作成用スキーマ
    """
    pass

class MechanismViewResponse(MechanismViewBase):
    """
    メカニズム閲覧履歴レスポンス用スキーマ
    """
    id: int
    viewed_at: datetime

    class Config:
        orm_mode = True

class MechanismViewCount(BaseModel):
    """
    メカニズム閲覧回数レスポンス用スキーマ
    """
    mechanism_id: int
    total_views: int
    user_views: Optional[int] = None

class MechanismViewsResponse(BaseModel):
    """
    メカニズム閲覧回数レスポンス用スキーマ（複数）
    """
    items: List[MechanismViewCount]
