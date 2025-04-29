from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.schemas.like import LikeResponse
from backend.app.services.like import LikeService

router = APIRouter()

@router.post("/{mechanism_id}", response_model=LikeResponse)
def create_like(mechanism_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    メカニズムにいいねを付けるエンドポイント
    
    注意: 現在は認証機能が未実装のため、user_idをクエリパラメータで受け取っています。
    認証機能実装後は、認証済みユーザーのIDを使用するように変更します。
    """
    # 既にいいねしているか確認
    existing_like = LikeService.get_like(db, user_id=user_id, mechanism_id=mechanism_id)
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既にいいねしています"
        )
    
    # いいねを作成
    LikeService.create_like(db, user_id=user_id, mechanism_id=mechanism_id)
    
    # いいね数を取得して返す
    likes_count = LikeService.get_mechanism_likes_count(db, mechanism_id=mechanism_id)
    return {"mechanism_id": mechanism_id, "likes_count": likes_count}

@router.delete("/{mechanism_id}", response_model=LikeResponse)
def delete_like(mechanism_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    メカニズムのいいねを取り消すエンドポイント
    
    注意: 現在は認証機能が未実装のため、user_idをクエリパラメータで受け取っています。
    認証機能実装後は、認証済みユーザーのIDを使用するように変更します。
    """
    # いいねを削除
    success = LikeService.delete_like(db, user_id=user_id, mechanism_id=mechanism_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="いいねが見つかりません"
        )
    
    # いいね数を取得して返す
    likes_count = LikeService.get_mechanism_likes_count(db, mechanism_id=mechanism_id)
    return {"mechanism_id": mechanism_id, "likes_count": likes_count}

@router.get("/mechanism/{mechanism_id}", response_model=LikeResponse)
def get_mechanism_likes(mechanism_id: int, db: Session = Depends(get_db)):
    """
    メカニズムのいいね数を取得するエンドポイント
    """
    likes_count = LikeService.get_mechanism_likes_count(db, mechanism_id=mechanism_id)
    return {"mechanism_id": mechanism_id, "likes_count": likes_count}

@router.get("/popular", response_model=List[dict])
def get_popular_mechanisms(limit: int = 10, db: Session = Depends(get_db)):
    """
    人気のメカニズム（いいね数順）を取得するエンドポイント
    """
    results = LikeService.get_popular_mechanisms(db, limit=limit)
    
    # 結果をフォーマット
    popular_mechanisms = []
    for mechanism, likes_count in results:
        popular_mechanisms.append({
            "mechanism_id": mechanism.id,
            "title": mechanism.title,
            "likes_count": likes_count
        })
    
    return popular_mechanisms

@router.get("/user/{user_id}/liked", response_model=List[dict])
def get_user_liked_mechanisms(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ユーザーがいいねしたメカニズム一覧を取得するエンドポイント
    """
    mechanisms = LikeService.get_user_liked_mechanisms(db, user_id=user_id, skip=skip, limit=limit)
    
    # 結果をフォーマット
    liked_mechanisms = []
    for mechanism in mechanisms:
        liked_mechanisms.append({
            "mechanism_id": mechanism.id,
            "title": mechanism.title
        })
    
    return liked_mechanisms
