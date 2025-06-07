import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.middlewares.auth import get_current_user_optional
from backend.app.models.mechanism_view import MechanismView
from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category

# テスト用のモックユーザー認証関数
async def mock_get_current_user_optional():
    return None  # 匿名ユーザー

# テスト用のモックログインユーザー認証関数
async def mock_get_current_user_logged_in(test_user):
    return test_user  # ログインユーザー

# テスト用のモックログインユーザー認証関数（固定ユーザー）
async def mock_current_user_fixed(test_user):
    return test_user

def test_record_mechanism_view_anonymous(client, test_mechanism):
    """匿名ユーザーによるメカニズム閲覧履歴記録のテスト"""
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # APIリクエスト
        response = client.post(f"/api/mechanisms/{test_mechanism.id}/view")
        
        # レスポンスの検証
        assert response.status_code == 201
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["user_id"] is None  # 匿名ユーザー
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_record_mechanism_view_logged_in(client, test_mechanism, test_user, db_session):
    """ログインユーザーによるメカニズム閲覧履歴記録のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # APIリクエスト
        response = client.post(f"/api/mechanisms/{test_mechanism.id}/view")
        
        # レスポンスの検証
        assert response.status_code == 201
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["user_id"] == test_user.id

        # DBで確認
        view_in_db = db_session.query(MechanismView).filter_by(mechanism_id=test_mechanism.id, user_id=test_user.id).first()
        assert view_in_db is not None
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_record_mechanism_view_not_found(client):
    """存在しないメカニズムの閲覧履歴記録のテスト"""
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # 存在しないメカニズムID
        non_existent_id = 9999
    
        # APIリクエスト
        response = client.post(f"/api/mechanisms/{non_existent_id}/view")
        
        # レスポンスの検証
        assert response.status_code == 404
        assert "メカニズムが見つかりません" in response.json()["detail"]
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_get_mechanism_views_anonymous(client, test_mechanism, db_session):
    """匿名ユーザーによるメカニズム閲覧回数取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    
    # 閲覧履歴を1件作成 (匿名ユーザー)
    view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=None
    )
    db_session.add(view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # APIリクエスト
        response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["total_views"] == 1
        assert data["user_views"] is None
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_get_mechanism_views_logged_in(client, test_mechanism, test_user, db_session):
    """ログインユーザーによるメカニズム閲覧回数取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    
    # 閲覧履歴を1件作成 (ログインユーザー)
    view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # APIリクエスト
        response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert data["mechanism_id"] == test_mechanism.id
        assert data["total_views"] == 1
        assert data["user_views"] == 1
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_get_mechanism_views_not_found(client):
    """存在しないメカニズムの閲覧回数取得のテスト"""
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    try:
        # 存在しないメカニズムID
        non_existent_id = 9999
    
        # APIリクエスト
        response = client.get(f"/api/mechanisms/{non_existent_id}/views")
        
        # レスポンスの検証
        assert response.status_code == 404
        assert "メカニズムが見つかりません" in response.json()["detail"]
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)


def test_get_mechanisms_views_batch(client, test_mechanism, test_user, db_session):
    """複数メカニズムの閲覧回数一括取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    import time

    # 1つ目のメカニズム(test_mechanism)の閲覧履歴を作成
    first_view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(first_view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    original_override = app.dependency_overrides.get(get_current_user_optional)
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    try:
        # 2つ目のメカニズムを作成
        second_mechanism = Mechanism(
            title=f"2つ目のテストメカニズム_{time.time()}", # Ensure unique title
            description="これは2つ目のテスト用メカニズムです",
            reliability=4,
            file_path="/test/file2.pdf",
            thumbnail_path="/test/thumbnail2.jpg",
            user_id=test_user.id
        )
        db_session.add(second_mechanism)
        db_session.commit()
        db_session.refresh(second_mechanism)
        
        # 2つ目のメカニズムの閲覧履歴を追加
        second_view = MechanismView(
            mechanism_id=second_mechanism.id,
            user_id=test_user.id
        )
        db_session.add(second_view)
        db_session.commit()
        
        # APIリクエスト
        response = client.post(
            "/api/mechanisms/views/batch",
            json=[test_mechanism.id, second_mechanism.id]
        )
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 2
        
        # 各メカニズムの閲覧統計情報を確認
        stats_map = {item["mechanism_id"]: item for item in data["items"]}

        assert test_mechanism.id in stats_map
        assert stats_map[test_mechanism.id]["total_views"] == 1
        assert stats_map[test_mechanism.id]["user_views"] == 1
        
        assert second_mechanism.id in stats_map
        assert stats_map[second_mechanism.id]["total_views"] == 1
        assert stats_map[second_mechanism.id]["user_views"] == 1
    finally:
        if original_override:
            app.dependency_overrides[get_current_user_optional] = original_override
        else:
            app.dependency_overrides.pop(get_current_user_optional, None)
