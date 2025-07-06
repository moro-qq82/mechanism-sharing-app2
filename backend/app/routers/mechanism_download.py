from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.database import get_db
from backend.app.middlewares.auth import get_current_user_optional
from backend.app.models.user import User
from backend.app.schemas.mechanism_download import MechanismDownloadResponse, MechanismDownloadCount, MechanismDownloadsResponse
from backend.app.services.mechanism_download import MechanismDownloadService
from backend.app.services.mechanism import MechanismService

router = APIRouter()

@router.post("/{mechanism_id}/download", response_model=MechanismDownloadResponse)
def record_mechanism_download(
    mechanism_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    メカニズムダウンロード履歴を記録するエンドポイント（5分間重複防止機能付き）
    
    Args:
        mechanism_id: メカニズムID
        response: レスポンスオブジェクト（ステータスコード設定用）
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        メカニズムダウンロード履歴（新規作成または既存のレコード）
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムの存在確認
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id=mechanism_id)
    if mechanism is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="メカニズムが見つかりません")
    
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # ダウンロード履歴を記録（5分間重複防止機能付き）
    mechanism_download, is_new = MechanismDownloadService.create_mechanism_download(db, mechanism_id, user_id)
    
    # ステータスコードを設定
    if is_new:
        response.status_code = status.HTTP_201_CREATED  # 新規作成
    else:
        response.status_code = status.HTTP_200_OK  # 既存レコード
    
    return mechanism_download

@router.get("/{mechanism_id}/downloads", response_model=MechanismDownloadCount)
def get_mechanism_downloads(
    mechanism_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    メカニズムのダウンロード回数を取得するエンドポイント
    
    Args:
        mechanism_id: メカニズムID
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        メカニズムのダウンロード回数
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムの存在確認
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id=mechanism_id)
    if mechanism is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="メカニズムが見つかりません")
    
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # ダウンロード統計情報を取得
    stats = MechanismDownloadService.get_mechanism_downloads_stats(db, mechanism_id, user_id)
    
    return stats

@router.post("/downloads/batch", response_model=MechanismDownloadsResponse)
def get_mechanisms_downloads(
    mechanism_ids: List[int],
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    複数メカニズムのダウンロード回数を一括取得するエンドポイント
    
    Args:
        mechanism_ids: メカニズムIDのリスト
        db: データベースセッション
        current_user: 現在のユーザー（ログインしていない場合はNone）
        
    Returns:
        複数メカニズムのダウンロード回数
    """
    # ユーザーIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user else None
    
    # ダウンロード統計情報を取得
    stats = MechanismDownloadService.get_mechanisms_downloads_stats(db, mechanism_ids, user_id)
    
    return {"items": stats}