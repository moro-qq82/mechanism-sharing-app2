import pytest
from sqlalchemy.orm import Session
import uuid

from backend.app.schemas.user import UserCreate
from backend.app.services.auth import create_user, get_user_by_email, authenticate_user
from backend.app.utils.security import get_password_hash, verify_password
from backend.app.database import Base

def test_password_hash():
    """パスワードのハッシュ化と検証をテストする"""
    password = "testpassword"
    hashed = get_password_hash(password)
    
    # ハッシュ化されたパスワードは元のパスワードと異なるはず
    assert hashed != password
    
    # 正しいパスワードで検証できるはず
    assert verify_password(password, hashed) is True
    
    # 間違ったパスワードでは検証できないはず
    assert verify_password("wrongpassword", hashed) is False

def test_create_user(db_session: Session):
    """ユーザー作成をテストする"""
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword"
    )
    
    # ユーザーを作成
    user = create_user(db_session, user_data)
    
    # 作成されたユーザーを検証
    assert user.email == user_data.email
    assert user.password_hash != user_data.password  # パスワードはハッシュ化されているはず
    assert verify_password(user_data.password, user.password_hash) is True

def test_get_user_by_email(db_session: Session):
    """メールアドレスでのユーザー検索をテストする"""
    # テスト用ユーザーを作成
    email = "test_get@example.com"
    user_data = UserCreate(
        email=email,
        password="testpassword"
    )
    create_user(db_session, user_data)
    
    # ユーザーを検索
    user = get_user_by_email(db_session, email)
    
    # 検索結果を検証
    assert user is not None
    assert user.email == email
    
    # 存在しないメールアドレスでは見つからないはず
    non_existent_user = get_user_by_email(db_session, "nonexistent@example.com")
    assert non_existent_user is None

def test_authenticate_user(db_session: Session):
    """ユーザー認証をテストする"""
    # テスト用ユーザーを作成
    email = "test_auth@example.com"
    password = "testpassword"
    user_data = UserCreate(
        email=email,
        password=password
    )
    create_user(db_session, user_data)
    
    # 正しい認証情報でユーザーを認証
    authenticated_user = authenticate_user(db_session, email, password)
    assert authenticated_user is not None
    assert authenticated_user.email == email
    
    # 間違ったパスワードでは認証できないはず
    wrong_password_user = authenticate_user(db_session, email, "wrongpassword")
    assert wrong_password_user is None
    
    # 存在しないメールアドレスでは認証できないはず
    non_existent_user = authenticate_user(db_session, "nonexistent@example.com", password)
    assert non_existent_user is None

# エンドポイントのテスト

def test_register_endpoint(client):
    """ユーザー登録エンドポイントのテスト"""
    # テスト用のユーザーデータ（一意のメールアドレスを使用）
    unique_email = f"test_register_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    
    # POSTリクエストを送信
    response = client.post("/api/auth/register", json=user_data)
    
    # レスポンスを検証
    print(f"Response: {response.json()}")
    assert response.status_code == 201
    data = response.json()
    # 現在のレスポンス形式はTokenオブジェクト（access_token, token_type, user）
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]
    assert "id" in data["user"]
    assert "created_at" in data["user"]
    # パスワードはレスポンスに含まれないはず
    assert "password" not in data["user"]

def test_register_endpoint_duplicate_email(client):
    """既存のメールアドレスでユーザー登録を試みるテスト"""
    # テスト用のユーザーデータ（一意のメールアドレスを使用）
    import uuid
    unique_email = f"test_duplicate_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    
    # 最初のリクエスト（成功するはず）
    response = client.post("/api/auth/register", json=user_data)
    print(f"Response for duplicate test (first request): {response.json()}")
    assert response.status_code == 201
    
    # 同じメールアドレスで2回目のリクエスト（失敗するはず）
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data  # エラーメッセージが含まれているはず

def test_login_endpoint(client):
    """ログインエンドポイントのテスト"""
    # テスト用のユーザーを登録（一意のメールアドレスを使用）
    import uuid
    unique_email = f"test_login_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    client.post("/api/auth/register", json=user_data)
    
    # ログインリクエストを送信
    response = client.post("/api/auth/login", json=user_data)
    
    # レスポンスを検証
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]

def test_login_endpoint_invalid_credentials(client):
    """無効な認証情報でログインを試みるテスト"""
    # テスト用のユーザーを登録（一意のメールアドレスを使用）
    import uuid
    unique_email = f"test_invalid_login_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword"
    }
    client.post("/api/auth/register", json=user_data)
    
    # 間違ったパスワードでログインリクエストを送信
    invalid_data = {
        "email": user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=invalid_data)
    
    # レスポンスを検証
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data  # エラーメッセージが含まれているはず

def test_login_endpoint_nonexistent_user(client):
    """存在しないユーザーでログインを試みるテスト"""
    # 存在しないユーザーでログインリクエストを送信
    invalid_data = {
        "email": "nonexistent@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=invalid_data)
    
    # レスポンスを検証
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data  # エラーメッセージが含まれているはず
