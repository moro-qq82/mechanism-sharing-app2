from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base

class MechanismView(Base):
    """
    メカニズム閲覧履歴モデル
    メカニズム詳細画面の閲覧履歴を記録する
    """
    __tablename__ = "mechanism_views"

    id = Column(Integer, primary_key=True, index=True)
    mechanism_id = Column(Integer, ForeignKey("mechanisms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # ログインしていない場合はNULL
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # リレーションシップ
    mechanism = relationship("Mechanism", back_populates="views")
    user = relationship("User", back_populates="mechanism_views")
