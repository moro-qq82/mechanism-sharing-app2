from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base

class MechanismDownload(Base):
    """
    メカニズムダウンロード履歴モデル
    メカニズムファイルのダウンロード履歴を記録する
    """
    __tablename__ = "mechanism_downloads"

    id = Column(Integer, primary_key=True, index=True)
    mechanism_id = Column(Integer, ForeignKey("mechanisms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # ログインしていない場合はNULL
    downloaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # リレーションシップ
    mechanism = relationship("Mechanism", back_populates="downloads")
    user = relationship("User", back_populates="mechanism_downloads")