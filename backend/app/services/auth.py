from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, Token
from backend.app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    メールアドレスでユーザーを検索する
    
    Args:
        db: データベースセッション
        email: 検索するメールアドレス
        
    Returns:
        Optional[User]: 見つかったユーザー、見つからない場合はNone
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    新しいユーザーを作成する
    
    Args:
        db: データベースセッション
        user: 作成するユーザー情報
        
    Returns:
        User: 作成されたユーザー
        
    Raises:
        HTTPException: メールアドレスが既に使用されている場合
    """
    # メールアドレスが既に使用されているか確認
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に使用されています"
        )
    
    # パスワードをハッシュ化
    hashed_password = get_password_hash(user.password)
    
    # ユーザーを作成
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )
    
    # データベースに保存
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    ユーザーを認証する
    
    Args:
        db: データベースセッション
        email: メールアドレス
        password: パスワード
        
    Returns:
        Optional[User]: 認証されたユーザー、認証に失敗した場合はNone
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def login_user(db: Session, email: str, password: str) -> Token:
    """
    ユーザーをログインさせる
    
    Args:
        db: データベースセッション
        email: メールアドレス
        password: パスワード
        
    Returns:
        Token: アクセストークンとユーザー情報
        
    Raises:
        HTTPException: 認証に失敗した場合
    """
    # ユーザーを認証
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # アクセストークンを作成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    # ユーザー情報をレスポンス用に変換
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        is_admin=user.is_admin,
        created_at=user.created_at
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )
