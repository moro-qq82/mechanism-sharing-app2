import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.config_test import test_settings
from backend.app.database import Base
from backend.app.database_test import TestBase
from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.models.like import Like

# テスト用データベース接続URLを設定
SQLALCHEMY_DATABASE_URL = test_settings.DATABASE_URL

# テスト用エンジンを作成
test_engine = create_engine(SQLALCHEMY_DATABASE_URL)

# テスト用セッションファクトリを作成
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    """
    テスト用データベースセッションを提供するフィクスチャ
    """
    # テスト用テーブルを作成
    Base.metadata.create_all(bind=test_engine)
    
    # テスト用セッションを作成
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # テスト後にセッションをロールバックしてクリーンアップ
        session.rollback()
        session.close()
        
        # テスト用テーブルを削除
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_user(db_session):
    """
    テスト用ユーザーを提供するフィクスチャ
    """
    user = User(
        email="test@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_category(db_session):
    """
    テスト用カテゴリーを提供するフィクスチャ
    """
    category = Category(
        name="テストカテゴリー"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

@pytest.fixture(scope="function")
def test_mechanism(db_session, test_user, test_category):
    """
    テスト用メカニズムを提供するフィクスチャ
    """
    mechanism = Mechanism(
        title="テストメカニズム",
        description="これはテスト用のメカニズムです",
        reliability=3,
        file_path="/test/file.pdf",
        thumbnail_path="/test/thumbnail.jpg",
        user_id=test_user.id
    )
    mechanism.categories.append(test_category)
    db_session.add(mechanism)
    db_session.commit()
    db_session.refresh(mechanism)
    return mechanism

@pytest.fixture(scope="function")
def test_like(db_session, test_user, test_mechanism):
    """
    テスト用いいねを提供するフィクスチャ
    """
    like = Like(
        user_id=test_user.id,
        mechanism_id=test_mechanism.id
    )
    db_session.add(like)
    db_session.commit()
    db_session.refresh(like)
    return like
