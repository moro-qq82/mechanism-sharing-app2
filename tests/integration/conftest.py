import pytest
import os
import sys
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# バックエンドのパスを追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.models.like import Like
from backend.app.utils.security import get_password_hash, create_access_token

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

# テスト用のデータベースエンジンを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# テスト用のセッションを作成
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """テスト用のデータベースセッションを提供するフィクスチャ"""
    # テーブルを作成
    Base.metadata.create_all(bind=engine)
    
    # セッションを作成
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # テーブルを削除
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """テスト用のFastAPIクライアントを提供するフィクスチャ"""
    # テスト用のデータベースセッションを使用するように依存関係をオーバーライド
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # テストクライアントを作成
    with TestClient(app=app) as client:
        yield client
    
    # 依存関係のオーバーライドをクリア
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session):
    """テスト用のユーザーを作成するフィクスチャ"""
    # ユーザーを作成
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user

@pytest.fixture(scope="function")
def test_token(test_user):
    """テスト用のJWTトークンを作成するフィクスチャ"""
    # トークンを作成
    access_token = create_access_token(data={"sub": str(test_user.id)})
    return access_token

@pytest.fixture(scope="function")
def test_category(db_session):
    """テスト用のカテゴリーを作成するフィクスチャ"""
    # カテゴリーを作成
    category = Category(name="テストカテゴリー")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    return category

@pytest.fixture(scope="function")
def test_mechanism(db_session, test_user, test_category):
    """テスト用のメカニズムを作成するフィクスチャ"""
    # メカニズムを作成
    mechanism = Mechanism(
        title="テストメカニズム",
        description="これはテスト用のメカニズムです。",
        reliability=3,
        file_path="/test/file.pdf",
        thumbnail_path="/test/thumbnail.jpg",
        user_id=test_user.id
    )
    mechanism.categories = [test_category]
    
    db_session.add(mechanism)
    db_session.commit()
    db_session.refresh(mechanism)
    
    return mechanism

@pytest.fixture(scope="function")
def test_like(db_session, test_user, test_mechanism):
    """テスト用のいいねを作成するフィクスチャ"""
    # いいねを作成
    like = Like(
        user_id=test_user.id,
        mechanism_id=test_mechanism.id
    )
    db_session.add(like)
    db_session.commit()
    db_session.refresh(like)
    
    return like

@pytest.fixture(scope="function")
def auth_headers(test_token):
    """認証ヘッダーを提供するフィクスチャ"""
    return {"Authorization": f"Bearer {test_token}"}
