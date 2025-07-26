from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ユーザー作成用スキーマ
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# ユーザー情報表示用スキーマ
class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ユーザー認証用スキーマ
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# トークン用スキーマ
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# トークンデータ用スキーマ
class TokenData(BaseModel):
    user_id: Optional[int] = None
