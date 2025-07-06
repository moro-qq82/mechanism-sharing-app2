import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.main import app
from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.services.auth import create_user
from backend.app.schemas.user import UserCreate


@pytest.fixture
def db_session(TestingSessionLocal):
    """テスト用データベースセッション"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: Session):
    """テスト用ユーザーを作成"""
    user_data = UserCreate(
        email="download_test@example.com",
        password="testpassword123"
    )
    user = create_user(db_session, user_data)
    return user


@pytest.fixture
def test_mechanism(db_session: Session, test_user: User):
    """テスト用メカニズムを作成"""
    # テスト用カテゴリを作成
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    # テスト用メカニズムを作成
    mechanism = Mechanism(
        title="Test Mechanism",
        description="Test Description",
        reliability=3,
        file_path="test/path/file.jpg",
        thumbnail_path="test/path/thumbnail.jpg",
        user_id=test_user.id
    )
    mechanism.categories = [category]
    db_session.add(mechanism)
    db_session.commit()
    db_session.refresh(mechanism)
    
    return mechanism


@pytest.fixture
def auth_headers(test_user: User):
    """認証ヘッダーを生成"""
    from backend.app.utils.security import create_access_token
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}


class TestMechanismDownloadAPI:
    """メカニズムダウンロードAPIのテストクラス"""

    def test_record_mechanism_download_success(self, client, test_mechanism: Mechanism, auth_headers: dict):
        """ダウンロード履歴記録APIが正常に動作することをテスト"""
        response = client.post(
            f"/api/mechanisms/{test_mechanism.id}/download",
            headers=auth_headers
        )
        
        # レスポンスを検証
        assert response.status_code == 201  # 新規作成
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["user_id"] is not None
        assert "downloaded_at" in data

    def test_record_mechanism_download_without_auth(self, client, test_mechanism: Mechanism):
        """未認証でもダウンロード履歴を記録できることをテスト"""
        response = client.post(f"/api/mechanisms/{test_mechanism.id}/download")
        
        # レスポンスを検証
        assert response.status_code == 201  # 新規作成
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["user_id"] is None
        assert "downloaded_at" in data

    def test_record_mechanism_download_duplicate_prevention(self, client, test_mechanism: Mechanism, auth_headers: dict):
        """5分以内の重複ダウンロードが防止されることをテスト"""
        # 最初のダウンロード履歴を記録
        response1 = client.post(
            f"/api/mechanisms/{test_mechanism.id}/download",
            headers=auth_headers
        )
        assert response1.status_code == 201  # 新規作成
        
        # 同じユーザーが再度ダウンロード（5分以内）
        response2 = client.post(
            f"/api/mechanisms/{test_mechanism.id}/download",
            headers=auth_headers
        )
        assert response2.status_code == 200  # 既存レコード
        
        # 同じレコードが返されることを確認
        data1 = response1.json()
        data2 = response2.json()
        assert data1["id"] == data2["id"]

    def test_record_mechanism_download_not_found(self, client, auth_headers: dict):
        """存在しないメカニズムのダウンロード履歴記録でエラーになることをテスト"""
        response = client.post("/api/mechanisms/99999/download", headers=auth_headers)
        
        # レスポンスを検証
        assert response.status_code == 404
        data = response.json()
        assert "メカニズムが見つかりません" in data["detail"]

    def test_get_mechanism_downloads_success(self, client, test_mechanism: Mechanism, auth_headers: dict):
        """ダウンロード回数取得APIが正常に動作することをテスト"""
        # ダウンロード履歴を記録
        client.post(f"/api/mechanisms/{test_mechanism.id}/download", headers=auth_headers)
        
        # ダウンロード回数を取得
        response = client.get(
            f"/api/mechanisms/{test_mechanism.id}/downloads",
            headers=auth_headers
        )
        
        # レスポンスを検証
        assert response.status_code == 200
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["total_downloads"] == 1
        assert data["user_downloads"] == 1

    def test_get_mechanism_downloads_without_auth(self, client, test_mechanism: Mechanism):
        """未認証でダウンロード回数を取得できることをテスト"""
        response = client.get(f"/api/mechanisms/{test_mechanism.id}/downloads")
        
        # レスポンスを検証
        assert response.status_code == 200
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["total_downloads"] == 0
        assert "user_downloads" not in data

    def test_get_mechanism_downloads_not_found(self, client, auth_headers: dict):
        """存在しないメカニズムのダウンロード回数取得でエラーになることをテスト"""
        response = client.get("/api/mechanisms/99999/downloads", headers=auth_headers)
        
        # レスポンスを検証
        assert response.status_code == 404
        data = response.json()
        assert "メカニズムが見つかりません" in data["detail"]

    def test_get_mechanisms_downloads_batch(self, client, test_mechanism: Mechanism, auth_headers: dict):
        """複数メカニズムのダウンロード回数一括取得APIが正常に動作することをテスト"""
        # ダウンロード履歴を記録
        client.post(f"/api/mechanisms/{test_mechanism.id}/download", headers=auth_headers)
        
        # 複数メカニズムのダウンロード回数を取得
        response = client.post(
            "/api/mechanisms/downloads/batch",
            json=[test_mechanism.id],
            headers=auth_headers
        )
        
        # レスポンスを検証
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        
        item = data["items"][0]
        assert item["mechanism_id"] == test_mechanism.id
        assert item["total_downloads"] == 1
        assert item["user_downloads"] == 1

    def test_get_mechanisms_downloads_batch_without_auth(self, client, test_mechanism: Mechanism):
        """未認証で複数メカニズムのダウンロード回数を取得できることをテスト"""
        response = client.post(
            "/api/mechanisms/downloads/batch",
            json=[test_mechanism.id]
        )
        
        # レスポンスを検証
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        
        item = data["items"][0]
        assert item["mechanism_id"] == test_mechanism.id
        assert item["total_downloads"] == 0
        assert "user_downloads" not in item