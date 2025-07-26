from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # リレーションシップ（lazy='dynamic'で遅延読み込み）
    mechanisms = relationship("Mechanism", back_populates="user", lazy='dynamic')
    likes = relationship("Like", back_populates="user", lazy='dynamic')
    mechanism_views = relationship("MechanismView", back_populates="user", lazy='dynamic')
    mechanism_downloads = relationship("MechanismDownload", back_populates="user", lazy='dynamic')
