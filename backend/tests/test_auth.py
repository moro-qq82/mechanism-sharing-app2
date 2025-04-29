import pytest
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.services.auth import create_user, get_user_by_email, authenticate_user
from backend.app.utils.security import get_password_hash, verify_password

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

# エンドポイントのテストは別途実装する
