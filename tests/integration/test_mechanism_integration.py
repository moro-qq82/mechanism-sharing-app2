import pytest
import io
import os
from fastapi.testclient import TestClient

def test_get_mechanisms_list(client, test_mechanism):
    """
    メカニズム一覧取得のテスト
    """
    response = client.get("/api/mechanisms")
    assert response.status_code == 200, f"メカニズム一覧の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "pages" in data
    
    # テスト用メカニズムが含まれていることを確認
    assert any(mechanism["id"] == test_mechanism.id for mechanism in data["items"])
    
    # ページネーションのテスト
    response = client.get("/api/mechanisms?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 5

def test_get_mechanism_detail(client, test_mechanism):
    """
    メカニズム詳細取得のテスト
    """
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200, f"メカニズム詳細の取得に失敗しました: {response.text}"
    
    data = response.json()
    assert data["id"] == test_mechanism.id
    assert data["title"] == test_mechanism.title
    assert data["description"] == test_mechanism.description
    assert data["reliability"] == test_mechanism.reliability
    assert data["file_path"] == test_mechanism.file_path
    assert data["thumbnail_path"] == test_mechanism.thumbnail_path
    assert data["user"]["id"] == test_mechanism.user_id
    assert "categories" in data
    assert "likes_count" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_nonexistent_mechanism(client):
    """
    存在しないメカニズムの取得テスト
    """
    response = client.get("/api/mechanisms/999")
    assert response.status_code == 404, f"存在しないメカニズムが取得できてしまいました: {response.text}"

def test_create_mechanism(client, auth_headers, test_category):
    """
    メカニズム作成のテスト
    """
    # テスト用のファイルを作成
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    thumbnail_content = b"test thumbnail content"
    thumbnail = io.BytesIO(thumbnail_content)
    
    # マルチパートフォームデータを作成
    form_data = {
        "title": "新しいメカニズム",
        "description": "これは統合テスト用の新しいメカニズムです。",
        "reliability": "4",
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
    
    assert response.status_code == 201, f"メカニズムの作成に失敗しました: {response.text}"
    
    data = response.json()
    assert data["title"] == form_data["title"]
    assert data["description"] == form_data["description"]
    assert data["reliability"] == int(form_data["reliability"])
    assert test_category.name in data["categories"]
    assert data["file_path"] is not None
    assert data["thumbnail_path"] is not None
    assert "user" in data
    assert "likes_count" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # 作成したメカニズムが取得できることを確認
    mechanism_id = data["id"]
    response = client.get(f"/api/mechanisms/{mechanism_id}")
    assert response.status_code == 200

def test_create_mechanism_without_auth(client, test_category):
    """
    認証なしでメカニズム作成ができないことをテスト
    """
    # テスト用のファイルを作成
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    # マルチパートフォームデータを作成
    form_data = {
        "title": "認証なしメカニズム",
        "description": "これは認証なしで作成しようとするメカニズムです。",
        "reliability": "3",
        "categories": test_category.name
    }
    
    files = {
        "file": ("test_file.pdf", file, "application/pdf")
    }
    
    response = client.post(
        "/api/mechanisms",
        data=form_data,
        files=files
    )
    
    assert response.status_code == 401, f"認証なしでメカニズムが作成できてしまいました: {response.text}"

def test_create_mechanism_with_invalid_data(client, auth_headers):
    """
    無効なデータでメカニズム作成ができないことをテスト
    """
    # テスト用のファイルを作成
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    # タイトルなしのフォームデータ
    form_data = {
        "description": "これはタイトルのないメカニズムです。",
        "reliability": "3",
        "categories": "テスト"
    }
    
    files = {
        "file": ("test_file.pdf", file, "application/pdf")
    }
    
    response = client.post(
        "/api/mechanisms",
        data=form_data,
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 422, f"無効なデータでメカニズムが作成できてしまいました: {response.text}"
    
    # 信頼性レベルが範囲外のフォームデータ
    form_data = {
        "title": "無効な信頼性レベル",
        "description": "これは信頼性レベルが範囲外のメカニズムです。",
        "reliability": "10",  # 1-5の範囲外
        "categories": "テスト"
    }
    
    response = client.post(
        "/api/mechanisms",
        data=form_data,
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 400, f"無効な信頼性レベルでメカニズムが作成できてしまいました: {response.text}"

def test_like_mechanism_flow(client, test_mechanism, auth_headers):
    """
    メカニズムへのいいね追加と取り消しのフローをテスト
    """
    # 1. いいねを追加
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id},
        headers=auth_headers
    )
    
    assert response.status_code == 201, f"いいねの追加に失敗しました: {response.text}"
    
    # 2. メカニズム詳細を取得していいね数を確認
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["likes_count"] >= 1  # テスト用のいいねが既に存在する可能性があるため
    
    # 3. いいねを取り消し
    response = client.delete(
        f"/api/likes/{test_mechanism.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200, f"いいねの取り消しに失敗しました: {response.text}"
    
    # 4. メカニズム詳細を再取得していいね数を確認
    response = client.get(f"/api/mechanisms/{test_mechanism.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["likes_count"] == 0  # いいねが取り消されたことを確認

def test_like_mechanism_without_auth(client, test_mechanism):
    """
    認証なしでいいねができないことをテスト
    """
    response = client.post(
        "/api/likes",
        json={"mechanism_id": test_mechanism.id}
    )
    
    assert response.status_code == 401, f"認証なしでいいねができてしまいました: {response.text}"

def test_like_nonexistent_mechanism(client, auth_headers):
    """
    存在しないメカニズムへのいいねができないことをテスト
    """
    response = client.post(
        "/api/likes",
        json={"mechanism_id": 999},
        headers=auth_headers
    )
    
    assert response.status_code == 404, f"存在しないメカニズムにいいねができてしまいました: {response.text}"
