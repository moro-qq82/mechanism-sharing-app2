from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mechanism_id = Column(Integer, ForeignKey("mechanisms.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ユニーク制約（一人一回のいいね制約）
    __table_args__ = (
        UniqueConstraint('user_id', 'mechanism_id', name='unique_user_mechanism_like'),
    )

    # リレーションシップ
    user = relationship("User", back_populates="likes")
    mechanism = relationship("Mechanism", back_populates="likes")
