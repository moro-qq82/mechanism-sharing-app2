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
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # APIリクエスト
    response = client.post(f"/api/mechanisms/{test_mechanism.id}/view")
    
    # レスポンスの検証
    assert response.status_code == 201
    data = response.json()
    assert data["mechanism_id"] == test_mechanism.id
    assert data["user_id"] is None  # 匿名ユーザー

def test_record_mechanism_view_logged_in(client, test_mechanism, test_user, db_session):
    """ログインユーザーによるメカニズム閲覧履歴記録のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).delete()
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # APIリクエスト
    response = client.post(f"/api/mechanisms/{test_mechanism.id}/view")
    
    # レスポンスの検証
    assert response.status_code == 201
    data = response.json()
    assert data["mechanism_id"] == test_mechanism.id
    assert data["user_id"] == test_user.id

def test_record_mechanism_view_not_found(client):
    """存在しないメカニズムの閲覧履歴記録のテスト"""
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # 存在しないメカニズムID
    non_existent_id = 9999
    
    # APIリクエスト
    response = client.post(f"/api/mechanisms/{non_existent_id}/view")
    
    # レスポンスの検証
    assert response.status_code == 404
    assert "メカニズムが見つかりません" in response.json()["detail"]

def test_get_mechanism_views_anonymous(client, test_mechanism, db_session):
    """匿名ユーザーによるメカニズム閲覧回数取得のテスト"""
    # テスト前にデータベースをクリーンアップし、1件だけ閲覧履歴を作成
    db_session.query(MechanismView).filter(MechanismView.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    # 閲覧履歴を1件作成
    view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=None  # 匿名ユーザー
    )
    db_session.add(view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # APIリクエスト
    response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
    
    # レスポンスの検証
    assert response.status_code == 200
    data = response.json()
    assert data["mechanism_id"] == test_mechanism.id
    assert data["total_views"] == 1  # test_mechanism_viewの1件
    assert data["user_views"] is None  # 匿名ユーザーなのでuser_viewsはNone

def test_get_mechanism_views_logged_in(client, test_mechanism, test_user, db_session):
    """ログインユーザーによるメカニズム閲覧回数取得のテスト"""
    # テスト前にデータベースをクリーンアップし、1件だけ閲覧履歴を作成
    db_session.query(MechanismView).filter(MechanismView.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    # 閲覧履歴を1件作成
    view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # APIリクエスト
    response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
    
    # レスポンスの検証
    assert response.status_code == 200
    data = response.json()
    assert data["mechanism_id"] == test_mechanism.id
    assert data["total_views"] == 1  # test_mechanism_viewの1件
    assert data["user_views"] == 1  # テストユーザーの閲覧は1件

def test_get_mechanism_views_not_found(client):
    """存在しないメカニズムの閲覧回数取得のテスト"""
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return None
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # 存在しないメカニズムID
    non_existent_id = 9999
    
    # APIリクエスト
    response = client.get(f"/api/mechanisms/{non_existent_id}/views")
    
    # レスポンスの検証
    assert response.status_code == 404
    assert "メカニズムが見つかりません" in response.json()["detail"]

def test_get_mechanisms_views_batch(client, test_mechanism, test_user, db_session):
    """複数メカニズムの閲覧回数一括取得のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).delete()
    db_session.commit()
    
    # 1つ目のメカニズムの閲覧履歴を作成
    first_view = MechanismView(
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    db_session.add(first_view)
    db_session.commit()
    
    # 認証ミドルウェアをモックに置き換え
    def mock_get_current_user_optional_sync():
        return test_user
    
    # 依存関係を上書き
    app.dependency_overrides[get_current_user_optional] = mock_get_current_user_optional_sync
    
    # 2つ目のメカニズムを検索または作成
    second_mechanism = db_session.query(Mechanism).filter(
        Mechanism.title == "2つ目のテストメカニズム",
        Mechanism.user_id == test_user.id
    ).first()
    
    if not second_mechanism:
        second_mechanism = Mechanism(
            title="2つ目のテストメカニズム",
            description="これは2つ目のテスト用メカニズムです",
            reliability=4,
            file_path="/test/file2.pdf",
            thumbnail_path="/test/thumbnail2.jpg",
            user_id=test_user.id
        )
        db_session.add(second_mechanism)
        db_session.commit()
        db_session.refresh(second_mechanism)
    
    # 2つ目のメカニズムの閲覧履歴を検索または追加
    second_view = db_session.query(MechanismView).filter(
        MechanismView.mechanism_id == second_mechanism.id,
        MechanismView.user_id == test_user.id
    ).first()
    
    if not second_view:
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
    for item in data["items"]:
        assert "mechanism_id" in item
        assert "total_views" in item
        assert "user_views" in item
        assert item["total_views"] == 1
        assert item["user_views"] == 1
