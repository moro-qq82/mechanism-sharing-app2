from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.app.config import settings

# データベース接続URLを設定
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# エンジンを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# セッションファクトリを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラスを作成
Base = declarative_base()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
