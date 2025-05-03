import pytest
import json
import io
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_frontend_backend_auth_flow(client):
    """
    フロントエンドとバックエンドの認証フローの統合テスト
    """
    # 1. 新規ユーザー登録
    register_data = {
        "email": "frontend_test@example.com",
        "password": "securepassword123"
    }
    
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 201
    
    register_response = response.json()
    assert "access_token" in register_response
    assert "user" in register_response
    
    # フロントエンドでのトークン保存をシミュレート
    token = register_response["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 認証が必要なエンドポイントにアクセス
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    
    # 3. ログアウト（トークンを破棄）
    # フロントエンドでのログアウト処理をシミュレート
    
    # 4. 認証なしでアクセスできないことを確認
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_frontend_backend_mechanism_flow(client, auth_headers, test_category):
    """
    フロントエンドとバックエンドのメカニズム操作フローの統合テスト
    """
    # 1. メカニズム作成
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    thumbnail_content = b"test thumbnail content"
    thumbnail = io.BytesIO(thumbnail_content)
    
    form_data = {
        "title": "フロントエンド統合テスト用メカニズム",
        "description": "これはフロントエンドとバックエンドの統合テスト用のメカニズムです。",
        "reliability": "3",
        "categories": test_category.name
    }
    
    files = {
        "file": ("test_file.pdf", file, "application/pdf"),
        "thumbnail": ("test_thumbnail.jpg", thumbnail, "image/jpeg")
    }
    
    response = client.post(
        "/api/mechanisms",
        data=form_data,
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    
    mechanism_data = response.json()
    mechanism_id = mechanism_data["id"]
    
    # 2. メカニズム一覧取得
    response = client.get("/api/mechanisms")
    assert response.status_code == 200
    
    mechanisms_list = response.json()
    assert "items" in mechanisms_list
    assert any(mechanism["id"] == mechanism_id for mechanism in mechanisms_list["items"])
    
    # 3. メカニズム詳細取得
    response = client.get(f"/api/mechanisms/{mechanism_id}")
    assert response.status_code == 200
    
    mechanism_detail = response.json()
    assert mechanism_detail["id"] == mechanism_id
    assert mechanism_detail["title"] == form_data["title"]
    
    # 4. いいねを追加
    response = client.post(
        "/api/likes",
        json={"mechanism_id": mechanism_id},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    
    # 5. メカニズム詳細を再取得していいね数を確認
    response = client.get(f"/api/mechanisms/{mechanism_id}")
    assert response.status_code == 200
    
    updated_mechanism = response.json()
    assert updated_mechanism["likes_count"] >= 1
    
    # 6. いいねを取り消し
    response = client.delete(
        f"/api/likes/{mechanism_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 7. メカニズム詳細を再取得していいね数を確認
    response = client.get(f"/api/mechanisms/{mechanism_id}")
    assert response.status_code == 200
    
    final_mechanism = response.json()
    assert final_mechanism["likes_count"] == 0

def test_frontend_backend_category_flow(client, auth_headers):
    """
    フロントエンドとバックエンドのカテゴリー操作フローの統合テスト
    """
    # 1. カテゴリー作成
    category_data = {
        "name": "フロントエンド統合テスト用カテゴリー"
    }
    
    response = client.post(
        "/api/categories",
        json=category_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    
    category = response.json()
    category_id = category["id"]
    
    # 2. カテゴリー一覧取得
    response = client.get("/api/categories")
    assert response.status_code == 200
    
    categories_list = response.json()
    assert any(cat["id"] == category_id for cat in categories_list)
    
    # 3. カテゴリー詳細取得
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200
    
    category_detail = response.json()
    assert category_detail["id"] == category_id
    assert category_detail["name"] == category_data["name"]
    
    # 4. カテゴリー更新
    update_data = {
        "name": "更新されたフロントエンド統合テスト用カテゴリー"
    }
    
    response = client.put(
        f"/api/categories/{category_id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    updated_category = response.json()
    assert updated_category["name"] == update_data["name"]
    
    # 5. カテゴリー削除
    response = client.delete(
        f"/api/categories/{category_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 6. 削除されたカテゴリーが取得できないことを確認
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 404

def test_frontend_backend_error_handling(client, auth_headers):
    """
    フロントエンドとバックエンドのエラーハンドリングの統合テスト
    """
    # 1. 存在しないエンドポイントへのアクセス
    response = client.get("/nonexistent_endpoint")
    assert response.status_code == 404
    
    # 2. 無効なリクエストボディ
    response = client.post(
        "/api/categories",
        json={"invalid_field": "value"},
        headers=auth_headers
    )
    
    assert response.status_code == 422
    
    # 3. 無効なメソッド
    response = client.put("/api/mechanisms")
    assert response.status_code in [404, 405]
    
    # 4. 無効なクエリパラメータ
    response = client.get("/api/mechanisms?page=invalid")
    assert response.status_code == 422
    
    # 5. 無効なパスパラメータ
    response = client.get("/api/mechanisms/invalid")
    assert response.status_code == 422

@patch('backend.app.services.mechanism.MechanismService.save_upload_file')
def test_frontend_backend_file_upload(mock_save_upload_file, client, auth_headers, test_category):
    """
    フロントエンドとバックエンドのファイルアップロード機能の統合テスト
    """
    # モックの設定
    mock_save_upload_file.side_effect = [
        "/uploads/files/test_file.pdf",
        "/uploads/thumbnails/test_thumbnail.jpg"
    ]
    
    # テスト用のファイルを作成
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    thumbnail_content = b"test thumbnail content"
    thumbnail = io.BytesIO(thumbnail_content)
    
    # マルチパートフォームデータを作成
    form_data = {
        "title": "ファイルアップロードテスト",
        "description": "これはファイルアップロードのテスト用メカニズムです。",
        "reliability": "3",
        "categories": test_category.name
    }
    
    files = {
        "file": ("test_file.pdf", file, "application/pdf"),
        "thumbnail": ("test_thumbnail.jpg", thumbnail, "image/jpeg")
    }
    
    # メカニズムを作成
    response = client.post(
        "/api/mechanisms",
        data=form_data,
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    
    # モックが呼び出されたことを確認
    assert mock_save_upload_file.call_count == 2
    
    # レスポンスを確認
    data = response.json()
    assert data["file_path"] == "/uploads/files/test_file.pdf"
    assert data["thumbnail_path"] == "/uploads/thumbnails/test_thumbnail.jpg"
