from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.user import UserResponse

# カテゴリー情報表示用スキーマ
class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# メカニズム作成用スキーマ
class MechanismCreate(BaseModel):
    title: str
    description: str
    reliability: int
    categories: List[str]

# メカニズム情報表示用スキーマ（一覧用）
class MechanismListResponse(BaseModel):
    id: int
    title: str
    description: str
    reliability: int
    thumbnail_path: Optional[str] = None
    user: UserResponse
    categories: List[str]
    likes_count: int
    created_at: datetime

    class Config:
        from_attributes = True

# メカニズム情報表示用スキーマ（詳細用）
class MechanismDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    reliability: int
    file_path: str
    thumbnail_path: Optional[str] = None
    user: UserResponse
    categories: List[str]
    likes_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ページネーション用スキーマ
class PaginatedMechanismResponse(BaseModel):
    items: List[MechanismListResponse]
    total: int
    page: int
    limit: int
    pages: int
