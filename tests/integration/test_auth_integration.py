import pytest
import json
from fastapi.testclient import TestClient

def test_register_and_login_flow(client):
    """
    ユーザー登録からログインまでの一連のフローをテストする
    """
    # 1. 新規ユーザー登録
    register_data = {
        "email": "newuser@example.com",
        "password": "securepassword123"
    }
    
    response = client.post("/register", json=register_data)
    assert response.status_code == 201, f"登録に失敗しました: {response.text}"
    
    register_response = response.json()
    assert "access_token" in register_response
    assert "user" in register_response
    assert register_response["user"]["email"] == register_data["email"]
    
    # 2. ログアウト（トークンを破棄）
    token = register_response["access_token"]
    
    # 3. 登録したユーザーでログイン
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    
    response = client.post("/login", json=login_data)
    assert response.status_code == 200, f"ログインに失敗しました: {response.text}"
    
    login_response = response.json()
    assert "access_token" in login_response
    assert "user" in login_response
    assert login_response["user"]["email"] == login_data["email"]
    
    # 4. 取得したトークンで認証が必要なエンドポイントにアクセス
    token = login_response["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200, f"認証に失敗しました: {response.text}"
    
    user_data = response.json()
    assert user_data["email"] == login_data["email"]

def test_login_with_invalid_credentials(client, test_user):
    """
    無効な認証情報でのログイン失敗をテストする
    """
    # 無効なパスワードでログイン
    login_data = {
        "email": test_user.email,
        "password": "wrongpassword"
    }
    
    response = client.post("/login", json=login_data)
    assert response.status_code == 401, f"無効なパスワードでログインできてしまいました: {response.text}"
    
    # 存在しないユーザーでログイン
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    
    response = client.post("/login", json=login_data)
    assert response.status_code == 401, f"存在しないユーザーでログインできてしまいました: {response.text}"

def test_access_protected_route_without_token(client):
    """
    トークンなしで認証が必要なエンドポイントにアクセスできないことをテストする
    """
    response = client.get("/users/me")
    assert response.status_code == 401, f"認証なしでアクセスできてしまいました: {response.text}"

def test_access_protected_route_with_invalid_token(client):
    """
    無効なトークンで認証が必要なエンドポイントにアクセスできないことをテストする
    """
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401, f"無効なトークンでアクセスできてしまいました: {response.text}"

def test_register_with_existing_email(client, test_user):
    """
    既存のメールアドレスで登録できないことをテストする
    """
    register_data = {
        "email": test_user.email,
        "password": "newpassword123"
    }
    
    response = client.post("/register", json=register_data)
    assert response.status_code == 400, f"既存のメールアドレスで登録できてしまいました: {response.text}"
