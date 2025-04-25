from pydantic import BaseModel
from typing import List

# カテゴリー作成用スキーマ
class CategoryCreate(BaseModel):
    name: str

# カテゴリー情報表示用スキーマ
class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# カテゴリー一覧表示用スキーマ
class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
