from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database import Base
from backend.app.models.mechanism import mechanism_category

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # リレーションシップ
    mechanisms = relationship("Mechanism", secondary=mechanism_category, back_populates="categories")
