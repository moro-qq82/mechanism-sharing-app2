from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import TokenData
from backend.app.utils.security import SECRET_KEY, ALGORITHM, oauth2_scheme

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    JWTトークンからユーザーを取得する
    
    Args:
        token: JWTトークン
        db: データベースセッション
        
    Returns:
        User: 現在のユーザー
        
    Raises:
        HTTPException: トークンが無効な場合
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # トークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        try:
            user_id = int(user_id_str)
            token_data = TokenData(user_id=user_id)
        except ValueError:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # ユーザーをデータベースから取得
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    現在のアクティブなユーザーを取得する
    
    Args:
        current_user: 現在のユーザー
        
    Returns:
        User: 現在のアクティブなユーザー
        
    Raises:
        HTTPException: ユーザーが非アクティブな場合
    """
    # 将来的にユーザーの状態（アクティブ/非アクティブ）を管理する場合に使用
    return current_user

async def get_current_user_optional(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    JWTトークンからユーザーを取得する（オプショナル）
    トークンが無効または存在しない場合はNoneを返す
    
    Args:
        authorization: Authorization ヘッダー
        db: データベースセッション
        
    Returns:
        Optional[User]: 現在のユーザー、または None
    """
    if not authorization:
        return None
    
    try:
        # Bearer トークンから実際のトークン部分を取得
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        # トークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None
        
        try:
            user_id = int(user_id_str)
        except ValueError:
            return None
        
        # ユーザーをデータベースから取得
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except (JWTError, ValueError):
        return None
