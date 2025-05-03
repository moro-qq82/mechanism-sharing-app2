from pydantic import BaseModel
from typing import Optional

# いいね情報表示用スキーマ
class LikeResponse(BaseModel):
    mechanism_id: int
    likes_count: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
