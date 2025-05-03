import pytest
from fastapi.testclient import TestClient

def test_get_categories(client, test_category):
    """
    カテゴリー一覧取得のテスト
    """
    response = client.get("/api/categories")
    assert response.status_code == 200, f"カテゴリー一覧の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # テスト用カテゴリーが含まれていることを確認
    assert any(category["id"] == test_category.id for category in data)
    assert any(category["name"] == test_category.name for category in data)

def test_get_category_by_id(client, test_category):
    """
    カテゴリー詳細取得のテスト
    """
    response = client.get(f"/api/categories/{test_category.id}")
    assert response.status_code == 200, f"カテゴリー詳細の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == test_category.name

def test_get_nonexistent_category(client):
    """
    存在しないカテゴリーの取得テスト
    """
    response = client.get("/api/categories/999")
    assert response.status_code == 404, f"存在しないカテゴリーが取得できてしまいました: {response.text}"

def test_create_category(client, auth_headers):
    """
    カテゴリー作成のテスト
    """
    category_data = {
        "name": "新しいカテゴリー"
    }
    
    response = client.post(
        "/api/categories",
        json=category_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201, f"カテゴリーの作成に失敗しました: {response.text}"
    
    data = response.json()
    assert data["name"] == category_data["name"]
    assert "id" in data
    
    # 作成したカテゴリーが取得できることを確認
    category_id = data["id"]
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200

def test_create_category_without_auth(client):
    """
    認証なしでカテゴリー作成ができないことをテスト
    """
    category_data = {
        "name": "認証なしカテゴリー"
    }
    
    response = client.post(
        "/api/categories",
        json=category_data
    )
    
    assert response.status_code == 401, f"認証なしでカテゴリーが作成できてしまいました: {response.text}"

def test_create_duplicate_category(client, test_category, auth_headers):
    """
    重複するカテゴリー名で作成できないことをテスト
    """
    category_data = {
        "name": test_category.name
    }
    
    response = client.post(
        "/api/categories",
        json=category_data,
        headers=auth_headers
    )
    
    assert response.status_code == 400, f"重複するカテゴリーが作成できてしまいました: {response.text}"

def test_update_category(client, test_category, auth_headers):
    """
    カテゴリー更新のテスト
    """
    update_data = {
        "name": "更新されたカテゴリー名"
    }
    
    response = client.put(
        f"/api/categories/{test_category.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200, f"カテゴリーの更新に失敗しました: {response.text}"
    
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == update_data["name"]
    
    # 更新されたカテゴリーが取得できることを確認
    response = client.get(f"/api/categories/{test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]

def test_update_category_without_auth(client, test_category):
    """
    認証なしでカテゴリー更新ができないことをテスト
    """
    update_data = {
        "name": "認証なし更新カテゴリー"
    }
    
    response = client.put(
        f"/api/categories/{test_category.id}",
        json=update_data
    )
    
    assert response.status_code == 401, f"認証なしでカテゴリーが更新できてしまいました: {response.text}"

def test_update_nonexistent_category(client, auth_headers):
    """
    存在しないカテゴリーの更新テスト
    """
    update_data = {
        "name": "存在しないカテゴリー"
    }
    
    response = client.put(
        "/api/categories/999",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 404, f"存在しないカテゴリーが更新できてしまいました: {response.text}"

def test_delete_category(client, auth_headers):
    """
    カテゴリー削除のテスト
    """
    # 削除用のカテゴリーを作成
    category_data = {
        "name": "削除用カテゴリー"
    }
    
    response = client.post(
        "/api/categories",
        json=category_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    category_id = response.json()["id"]
    
    # カテゴリーを削除
    response = client.delete(
        f"/api/categories/{category_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200, f"カテゴリーの削除に失敗しました: {response.text}"
    
    # 削除されたカテゴリーが取得できないことを確認
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 404

def test_delete_category_without_auth(client, test_category):
    """
    認証なしでカテゴリー削除ができないことをテスト
    """
    response = client.delete(f"/api/categories/{test_category.id}")
    assert response.status_code == 401, f"認証なしでカテゴリーが削除できてしまいました: {response.text}"

def test_delete_nonexistent_category(client, auth_headers):
    """
    存在しないカテゴリーの削除テスト
    """
    response = client.delete(
        "/api/categories/999",
        headers=auth_headers
    )
    
    assert response.status_code == 404, f"存在しないカテゴリーが削除できてしまいました: {response.text}"
