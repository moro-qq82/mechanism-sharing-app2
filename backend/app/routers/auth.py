from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from backend.app.services.auth import create_user, login_user
from backend.app.middlewares.auth import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    新しいユーザーを登録する
    
    Args:
        user: 登録するユーザー情報
        db: データベースセッション
        
    Returns:
        Token: アクセストークンとユーザー情報
    """
    db_user = create_user(db=db, user=user)
    
    # アクセストークンを作成
    from datetime import timedelta
    from backend.app.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    
    # ユーザー情報をレスポンス用に変換
    user_response = UserResponse(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    ユーザーをログインさせる
    
    Args:
        user_data: ログイン情報
        db: データベースセッション
        
    Returns:
        Token: アクセストークンとユーザー情報
    """
    return login_user(db=db, email=user_data.email, password=user_data.password)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    現在のユーザー情報を取得する
    
    Args:
        current_user: 現在のユーザー
        
    Returns:
        UserResponse: ユーザー情報
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }
