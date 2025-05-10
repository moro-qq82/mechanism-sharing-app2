from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.database import get_db
from backend.app.middlewares.auth import get_current_user_optional
from backend.app.models.user import User
from backend.app.schemas.mechanism_view import MechanismViewResponse, MechanismViewCount, MechanismViewsResponse
from backend.app.services.mechanism_view import MechanismViewService
from backend.app.services.mechanism import MechanismService

router = APIRouter()

@router.post("/{mechanism_id}/view", response_model=MechanismViewResponse, status_code=status.HTTP_201_CREATED)
def record_mechanism_view(
    mechanism_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    メカニズム閲覧履歴を記録するエンドポイント
    
    Args:
        mechanism_id: メカニズムID
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        作成されたメカニズム閲覧履歴
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムの存在確認
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id=mechanism_id)
    if mechanism is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="メカニズムが見つかりません")
    
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # 閲覧履歴を記録
    mechanism_view = MechanismViewService.create_mechanism_view(db, mechanism_id, user_id)
    
    return mechanism_view

@router.get("/{mechanism_id}/views", response_model=MechanismViewCount)
def get_mechanism_views(
    mechanism_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    メカニズムの閲覧回数を取得するエンドポイント
    
    Args:
        mechanism_id: メカニズムID
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        メカニズムの閲覧回数
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムの存在確認
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id=mechanism_id)
    if mechanism is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="メカニズムが見つかりません")
    
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # 閲覧統計情報を取得
    stats = MechanismViewService.get_mechanism_views_stats(db, mechanism_id, user_id)
    
    return stats

@router.post("/views/batch", response_model=MechanismViewsResponse)
def get_mechanisms_views(
    mechanism_ids: List[int],
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    複数メカニズムの閲覧回数を一括取得するエンドポイント
    
    Args:
        mechanism_ids: メカニズムIDのリスト
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        複数メカニズムの閲覧回数
    """
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # 閲覧統計情報を取得
    stats = MechanismViewService.get_mechanisms_views_stats(db, mechanism_ids, user_id)
    
    return {"items": stats}
