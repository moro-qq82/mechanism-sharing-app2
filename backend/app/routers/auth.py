from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from backend.app.services.auth import create_user, login_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    新しいユーザーを登録する
    
    Args:
        user: 登録するユーザー情報
        db: データベースセッション
        
    Returns:
        UserResponse: 登録されたユーザー情報
    """
    return create_user(db=db, user=user)

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
