import pytest
from fastapi.testclient import TestClient
import time

def test_record_mechanism_view_anonymous(client, test_mechanism):
    """
    匿名ユーザーがメカニズム詳細画面を閲覧した際に閲覧履歴が記録されるかテスト
    """
    # 初期状態の閲覧回数を取得
    initial_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
    assert initial_response.status_code == 200
    initial_data = initial_response.json()
    initial_total_views = initial_data["total_views"]
    
    # 閲覧履歴を記録
    view_response = client.post(f"/api/mechanisms/{test_mechanism.id}/view")
    assert view_response.status_code == 201
    view_data = view_response.json()
    assert view_data["mechanism_id"] == test_mechanism.id
    assert view_data["user_id"] is None  # 匿名ユーザー
    
    # 閲覧回数が増加したことを確認
    updated_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views")
    assert updated_response.status_code == 200
    updated_data = updated_response.json()
    assert updated_data["total_views"] == initial_total_views + 1
    assert updated_data["user_views"] is None  # 匿名ユーザーなのでuser_viewsはNone

def test_record_mechanism_view_authenticated(client, test_mechanism, auth_headers):
    """
    認証済みユーザーがメカニズム詳細画面を閲覧した際に閲覧履歴が記録されるかテスト
    """
    # 初期状態の閲覧回数を取得
    initial_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views", headers=auth_headers)
    assert initial_response.status_code == 200
    initial_data = initial_response.json()
    initial_total_views = initial_data["total_views"]
    initial_user_views = initial_data.get("user_views", 0)
    
    # 閲覧履歴を記録
    view_response = client.post(f"/api/mechanisms/{test_mechanism.id}/view", headers=auth_headers)
    assert view_response.status_code == 201
    view_data = view_response.json()
    assert view_data["mechanism_id"] == test_mechanism.id
    assert view_data["user_id"] is not None  # 認証済みユーザー
    
    # 閲覧回数が増加したことを確認
    updated_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views", headers=auth_headers)
    assert updated_response.status_code == 200
    updated_data = updated_response.json()
    assert updated_data["total_views"] == initial_total_views + 1
    assert updated_data["user_views"] == initial_user_views + 1

def test_multiple_mechanism_views(client, test_mechanism, auth_headers):
    """
    同じメカニズムを複数回閲覧した際に閲覧回数が正しく増加するかテスト
    """
    # 初期状態の閲覧回数を取得
    initial_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views", headers=auth_headers)
    assert initial_response.status_code == 200
    initial_data = initial_response.json()
    initial_total_views = initial_data["total_views"]
    initial_user_views = initial_data.get("user_views", 0)
    
    # 3回閲覧履歴を記録
    for _ in range(3):
        view_response = client.post(f"/api/mechanisms/{test_mechanism.id}/view", headers=auth_headers)
        assert view_response.status_code == 201
        # 連続リクエストによるエラーを防ぐために少し待機
        time.sleep(0.1)
    
    # 閲覧回数が3回増加したことを確認
    updated_response = client.get(f"/api/mechanisms/{test_mechanism.id}/views", headers=auth_headers)
    assert updated_response.status_code == 200
    updated_data = updated_response.json()
    assert updated_data["total_views"] == initial_total_views + 3
    assert updated_data["user_views"] == initial_user_views + 3

def test_get_mechanism_views_batch(client, test_mechanism, auth_headers, db_session):
    """
    複数メカニズムの閲覧回数を一括取得するテスト
    """
    # 2つ目のメカニズムを作成
    from backend.app.models.mechanism import Mechanism
    from backend.app.models.mechanism_view import MechanismView
    
    # 既存の2つ目のメカニズムを検索
    second_mechanism = db_session.query(Mechanism).filter(
        Mechanism.title == "2つ目のテストメカニズム"
    ).first()
    
    # 存在しない場合は作成
    if not second_mechanism:
        second_mechanism = Mechanism(
            title="2つ目のテストメカニズム",
            description="これは2つ目のテスト用メカニズムです",
            reliability=4,
            file_path="/test/file2.pdf",
            thumbnail_path="/test/thumbnail2.jpg",
            user_id=test_mechanism.user_id
        )
        db_session.add(second_mechanism)
        db_session.commit()
        db_session.refresh(second_mechanism)
    
    # 両方のメカニズムに閲覧履歴を記録
    client.post(f"/api/mechanisms/{test_mechanism.id}/view", headers=auth_headers)
    client.post(f"/api/mechanisms/{second_mechanism.id}/view", headers=auth_headers)
    
    # 複数メカニズムの閲覧回数を一括取得
    batch_response = client.post(
        "/api/mechanisms/views/batch",
        json=[test_mechanism.id, second_mechanism.id],
        headers=auth_headers
    )
    
    assert batch_response.status_code == 200
    batch_data = batch_response.json()
    assert "items" in batch_data
    assert len(batch_data["items"]) == 2
    
    # 各メカニズムの閲覧回数が含まれていることを確認
    mechanism_ids = [item["mechanism_id"] for item in batch_data["items"]]
    assert test_mechanism.id in mechanism_ids
    assert second_mechanism.id in mechanism_ids
    
    # 各メカニズムの閲覧回数が1以上であることを確認
    for item in batch_data["items"]:
        assert item["total_views"] > 0
        assert item["user_views"] > 0

def test_mechanism_detail_includes_views_count(client, test_mechanism, auth_headers):
    """
    メカニズム詳細APIレスポンスに閲覧回数が含まれているかテスト
    """
    # 閲覧履歴を記録
    client.post(f"/api/mechanisms/{test_mechanism.id}/view", headers=auth_headers)
    
    # メカニズム詳細を取得
    detail_response = client.get(f"/api/mechanisms/{test_mechanism.id}", headers=auth_headers)
    assert detail_response.status_code == 200
    detail_data = detail_response.json()
    
    # 閲覧回数が含まれていることを確認
    assert "views_count" in detail_data
    assert detail_data["views_count"] > 0

def test_mechanism_list_includes_views_count(client, test_mechanism, auth_headers):
    """
    メカニズム一覧APIレスポンスに閲覧回数が含まれているかテスト
    """
    # 閲覧履歴を記録
    client.post(f"/api/mechanisms/{test_mechanism.id}/view", headers=auth_headers)
    
    # メカニズム一覧を取得
    list_response = client.get("/api/mechanisms", headers=auth_headers)
    assert list_response.status_code == 200
    list_data = list_response.json()
    
    # テスト用メカニズムを見つける
    test_mechanism_in_list = next(
        (item for item in list_data["items"] if item["id"] == test_mechanism.id),
        None
    )
    
    assert test_mechanism_in_list is not None
    # 閲覧回数が含まれていることを確認
    assert "views_count" in test_mechanism_in_list
    assert test_mechanism_in_list["views_count"] > 0
