import pytest
import os
import tempfile
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
from backend.app.models.mechanism_download import MechanismDownload
from backend.app.main import app



# # テスト用のクライアントを作成
# client = TestClient(app)


@pytest.fixture(scope="module")
def test_engine():
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    # エンジンを閉じてからファイルを削除
    engine.dispose()
    # Windows環境ではファイルの削除に失敗することがあるため、try-exceptで囲む
    try:
        os.remove(db_path)
    except PermissionError:
        # ファイルが使用中の場合は警告を出すだけにする
        import warnings
        warnings.warn(f"Could not delete temporary database file: {db_path}")


@pytest.fixture(scope="module")
def TestingSessionLocal(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# TestSessionLocalエイリアスを追加（既存テストとの互換性のため）
TestSessionLocal = None


@pytest.fixture(scope="module", autouse=True)
def setup_session_local(TestingSessionLocal):
    global TestSessionLocal
    TestSessionLocal = TestingSessionLocal


# テスト前にテーブルを作成
@pytest.fixture(scope="module", autouse=True)
def setup_test_db(test_engine):
    # テスト用テーブルを作成
    # 全てのモデルをインポートして、テーブルが正しく作成されるようにする
    from backend.app.models.user import User
    from backend.app.models.mechanism import Mechanism
    from backend.app.models.category import Category
    from backend.app.models.like import Like
    from backend.app.models.mechanism_view import MechanismView
    from backend.app.models.mechanism_download import MechanismDownload
    
    # テーブルを作成
    Base.metadata.create_all(bind=test_engine)
    yield
    # テスト後にテーブルを削除
    Base.metadata.drop_all(bind=test_engine)



# テスト用のデータベース依存関係を上書きする関数
def override_get_db():
    global TestSessionLocal
    if TestSessionLocal is None:
        raise RuntimeError("TestSessionLocal is not initialized")
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(setup_test_db, TestingSessionLocal):
    from backend.app.main import app
    from fastapi.testclient import TestClient

    # アプリケーションの依存関係を上書き
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
def db_session(TestingSessionLocal):
    """
    テスト用データベースセッションを提供するフィクスチャ
    """
    # テスト用セッションを作成
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # テスト後にセッションをロールバックしてクリーンアップ
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def test_user(db_session):
    """
    テスト用ユーザーを提供するフィクスチャ
    常に新しいユニークなユーザーを生成します。
    """
    import time
    unique_email = f"test_user_{time.time()}@example.com"
    user = User(
        email=unique_email,
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
    常に新しいユニークなカテゴリーを生成します。
    """
    import time
    unique_name = f"テストカテゴリー_{time.time()}"
    category = Category(
        name=unique_name
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

@pytest.fixture(scope="function")
def test_mechanism(db_session, test_user, test_category):
    """
    テスト用メカニズムを提供するフィクスチャ
    常に新しいユニークなメカニズムを生成します。
    """
    import time
    unique_title = f"テストメカニズム_{time.time()}"
    mechanism = Mechanism(
        title=unique_title,
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
    常に新しいいいねを生成します。
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
    常に新しいメカニズム閲覧履歴を生成します。
    """
    mechanism_view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(mechanism_view)
    db_session.commit()
    db_session.refresh(mechanism_view)
    return mechanism_view
