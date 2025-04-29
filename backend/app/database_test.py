from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.app.config_test import test_settings

# テスト用データベース接続URLを設定
SQLALCHEMY_DATABASE_URL = test_settings.DATABASE_URL

# エンジンを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# セッションファクトリを作成
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラスを作成
TestBase = declarative_base()

# テスト用データベースセッションの依存関係
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
