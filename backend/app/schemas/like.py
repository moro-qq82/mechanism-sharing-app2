from pydantic import BaseModel

# いいね情報表示用スキーマ
class LikeResponse(BaseModel):
    mechanism_id: int
    likes_count: int

    class Config:
        from_attributes = True
