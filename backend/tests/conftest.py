import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.app.config_test import test_settings
from backend.app.database import Base, get_db
from backend.app.database_test import TestBase
from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.models.like import Like
from backend.app.models.mechanism_view import MechanismView
from backend.app.main import app

# テスト用のインメモリSQLiteデータベースを設定
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# テスト用セッションファクトリを作成
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# テスト用のデータベース依存関係を上書き
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# アプリケーションの依存関係を上書き
app.dependency_overrides[get_db] = override_get_db

# テスト用のクライアントを作成
client = TestClient(app)

# テスト前にテーブルを作成
@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    # テスト用テーブルを作成
    # 全てのモデルをインポートして、テーブルが正しく作成されるようにする
    from backend.app.models.user import User
    from backend.app.models.mechanism import Mechanism
    from backend.app.models.category import Category
    from backend.app.models.like import Like
    from backend.app.models.mechanism_view import MechanismView
    
    # テーブルを作成
    Base.metadata.create_all(bind=test_engine)
    yield
    # テスト後にテーブルを削除
    Base.metadata.drop_all(bind=test_engine)

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

@pytest.fixture(scope="function")
def test_mechanism_view(db_session, test_user, test_mechanism):
    """
    テスト用メカニズム閲覧履歴を提供するフィクスチャ
    """
    mechanism_view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(mechanism_view)
    db_session.commit()
    db_session.refresh(mechanism_view)
    return mechanism_view
