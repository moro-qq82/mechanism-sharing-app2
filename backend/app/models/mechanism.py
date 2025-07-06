from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base

# メカニズムとカテゴリーの中間テーブル
mechanism_category = Table(
    "mechanism_categories",
    Base.metadata,
    Column("mechanism_id", Integer, ForeignKey("mechanisms.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)

class Mechanism(Base):
    __tablename__ = "mechanisms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    reliability = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    thumbnail_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # リレーションシップ
    user = relationship("User", back_populates="mechanisms")
    categories = relationship("Category", secondary=mechanism_category, back_populates="mechanisms")
    likes = relationship("Like", back_populates="mechanism")
    views = relationship("MechanismView", back_populates="mechanism")
    downloads = relationship("MechanismDownload", back_populates="mechanism")
