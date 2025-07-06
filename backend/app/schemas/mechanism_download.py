from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MechanismDownloadBase(BaseModel):
    """
    メカニズムダウンロード履歴の基本スキーマ
    """
    mechanism_id: int
    user_id: Optional[int] = None

class MechanismDownloadCreate(MechanismDownloadBase):
    """
    メカニズムダウンロード履歴作成用スキーマ
    """
    pass

class MechanismDownloadResponse(MechanismDownloadBase):
    """
    メカニズムダウンロード履歴レスポンス用スキーマ
    """
    id: int
    downloaded_at: datetime

    class Config:
        orm_mode = True

class MechanismDownloadCount(BaseModel):
    """
    メカニズムダウンロード回数レスポンス用スキーマ
    """
    mechanism_id: int
    total_downloads: int
    user_downloads: Optional[int] = None

class MechanismDownloadsResponse(BaseModel):
    """
    メカニズムダウンロード回数レスポンス用スキーマ（複数）
    """
    items: List[MechanismDownloadCount]