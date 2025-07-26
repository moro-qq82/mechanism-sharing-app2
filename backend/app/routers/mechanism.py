from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from pathlib import Path

from backend.app.database import get_db
from backend.app.middlewares.auth import get_current_user, get_current_user_optional
from backend.app.models.user import User
from backend.app.schemas.mechanism import MechanismCreate, MechanismUpdate, MechanismListResponse, MechanismDetailResponse, PaginatedMechanismResponse
from backend.app.services.mechanism import MechanismService
from backend.app.services.mechanism_view import MechanismViewService
from backend.app.services.mechanism_download import MechanismDownloadService

router = APIRouter()

# ファイル保存先ディレクトリ
UPLOAD_DIR = Path("uploads")
FILE_DIR = UPLOAD_DIR / "files"
THUMBNAIL_DIR = UPLOAD_DIR / "thumbnails"

@router.get("/", response_model=PaginatedMechanismResponse)
def get_mechanisms(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """
    メカニズム一覧を取得するエンドポイント
    
    Args:
        page: ページ番号（デフォルト: 1）
        limit: 1ページあたりの件数（デフォルト: 10）
        db: データベースセッション
        
    Returns:
        メカニズム一覧とページネーション情報
    """
    # ページネーションのためのスキップ数を計算
    skip = (page - 1) * limit
    
    # メカニズム一覧を取得
    result = MechanismService.get_mechanisms(db, skip=skip, limit=limit)
    
    # レスポンス用にデータを整形
    items = []
    for mechanism in result["items"]:
        # カテゴリー名のリストを取得
        categories = [category.name for category in mechanism.categories]
        
        # いいね数を取得
        likes_count = MechanismService.get_likes_count(db, mechanism.id)
        
        # 閲覧回数を取得
        views_count = MechanismViewService.get_mechanism_views_count(db, mechanism.id)
        
        # メカニズム情報を追加
        items.append({
            "id": mechanism.id,
            "title": mechanism.title,
            "description": mechanism.description,
            "reliability": mechanism.reliability,
            "thumbnail_path": mechanism.thumbnail_path,
            "user": mechanism.user,
            "categories": categories,
            "likes_count": likes_count,
            "views_count": views_count,
            "created_at": mechanism.created_at
        })
    
    # ページネーション情報を含めたレスポンスを返す
    return {
        "items": items,
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "pages": result["pages"]
    }

@router.get("/{mechanism_id}", response_model=MechanismDetailResponse)
def get_mechanism(mechanism_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDのメカニズム詳細を取得するエンドポイント
    
    Args:
        mechanism_id: メカニズムID
        db: データベースセッション
        
    Returns:
        メカニズム詳細情報
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムを取得
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id=mechanism_id)
    if mechanism is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="メカニズムが見つかりません")
    
    # カテゴリー名のリストを取得
    categories = [category.name for category in mechanism.categories]
    
    # いいね数を取得
    likes_count = MechanismService.get_likes_count(db, mechanism.id)
    
    # 閲覧回数を取得
    views_count = MechanismViewService.get_mechanism_views_count(db, mechanism.id)
    
    # メカニズム詳細情報を返す
    return {
        "id": mechanism.id,
        "title": mechanism.title,
        "description": mechanism.description,
        "reliability": mechanism.reliability,
        "file_path": mechanism.file_path,
        "thumbnail_path": mechanism.thumbnail_path,
        "user": mechanism.user,
        "categories": categories,
        "likes_count": likes_count,
        "views_count": views_count,
        "created_at": mechanism.created_at,
        "updated_at": mechanism.updated_at
    }

@router.post("/", response_model=MechanismDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_mechanism(
    title: str = Form(...),
    description: str = Form(...),
    reliability: int = Form(...),
    categories: str = Form(...),
    file: UploadFile = File(...),
    thumbnail: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    新しいメカニズムを投稿するエンドポイント
    
    Args:
        title: タイトル
        description: 説明文
        reliability: 信頼性レベル（1-5）
        categories: カテゴリー（カンマ区切り）
        file: アップロードファイル
        thumbnail: サムネイル画像（オプション）
        db: データベースセッション
        current_user: 現在のユーザー
        
    Returns:
        作成されたメカニズム情報
        
    Raises:
        HTTPException: 入力値が不正な場合
    """
    # 信頼性レベルのバリデーション
    if reliability < 1 or reliability > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="信頼性レベルは1から5の間で指定してください"
        )
    
    # カテゴリーをリストに変換
    category_list = [cat.strip() for cat in categories.split(",") if cat.strip()]
    
    # メカニズム作成用データを作成
    mechanism_data = MechanismCreate(
        title=title,
        description=description,
        reliability=reliability,
        categories=category_list
    )
    
    # ファイルを保存
    file_path = MechanismService.save_upload_file(file, str(FILE_DIR))
    
    # サムネイルがある場合は保存
    thumbnail_path = None
    if thumbnail:
        thumbnail_path = MechanismService.save_upload_file(thumbnail, str(THUMBNAIL_DIR))
    
    # メカニズムを作成
    mechanism = MechanismService.create_mechanism(
        db=db,
        mechanism=mechanism_data,
        user_id=current_user.id,
        file_path=file_path,
        thumbnail_path=thumbnail_path
    )
    
    # カテゴリー名のリストを取得
    categories = [category.name for category in mechanism.categories]
    
    # いいね数を取得（新規作成なので0）
    likes_count = 0
    
    # 閲覧回数（新規作成なので0）
    views_count = 0
    
    # 作成されたメカニズム情報を返す
    return {
        "id": mechanism.id,
        "title": mechanism.title,
        "description": mechanism.description,
        "reliability": mechanism.reliability,
        "file_path": mechanism.file_path,
        "thumbnail_path": mechanism.thumbnail_path,
        "user": current_user,
        "categories": categories,
        "likes_count": likes_count,
        "views_count": views_count,
        "created_at": mechanism.created_at,
        "updated_at": mechanism.updated_at
    }

@router.get("/{mechanism_id}/download")
async def download_mechanism_file(
    mechanism_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    メカニズムファイルをダウンロードするエンドポイント
    
    Args:
        mechanism_id: メカニズムID
        db: データベースセッション
        current_user: 現在のユーザー（オプショナル）
        
    Returns:
        ファイルレスポンス
        
    Raises:
        HTTPException: メカニズムが見つからない場合
    """
    # メカニズムを取得
    mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id)
    if not mechanism:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="メカニズムが見つかりません"
        )
    
    # ダウンロード履歴を記録
    try:
        user_id = current_user.id if current_user else None
        MechanismDownloadService.create_mechanism_download(db, mechanism_id, user_id)
    except Exception as e:
        # ダウンロード履歴の記録に失敗してもファイルダウンロードは継続
        print(f"ダウンロード履歴記録エラー: {e}")
    
    # ファイルパスを構築
    file_path = Path(mechanism.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません"
        )
    
    # ファイル名を取得
    filename = file_path.name
    
    # Content-Dispositionヘッダーを設定してファイルダウンロードを強制
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )

@router.put("/{mechanism_id}", response_model=MechanismDetailResponse)
def update_mechanism(
    mechanism_id: int,
    mechanism_update: MechanismUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    メカニズムを編集するエンドポイント
    
    Args:
        mechanism_id: 編集するメカニズムのID
        mechanism_update: 更新データ
        db: データベースセッション
        current_user: 現在のユーザー
        
    Returns:
        更新されたメカニズム情報
        
    Raises:
        HTTPException: メカニズムが見つからない場合、または編集権限がない場合
    """
    # 信頼性レベルのバリデーション（指定されている場合のみ）
    if mechanism_update.reliability is not None:
        if mechanism_update.reliability < 1 or mechanism_update.reliability > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="信頼性レベルは1から5の間で指定してください"
            )
    
    # メカニズムを更新
    updated_mechanism = MechanismService.update_mechanism(
        db=db,
        mechanism_id=mechanism_id,
        mechanism_update=mechanism_update,
        current_user_id=current_user.id
    )
    
    if not updated_mechanism:
        # メカニズムが存在しないか、編集権限がない場合
        mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id)
        if not mechanism:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="メカニズムが見つかりません"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このメカニズムを編集する権限がありません"
            )
    
    # カテゴリー名のリストを取得
    categories = [category.name for category in updated_mechanism.categories]
    
    # いいね数を取得
    likes_count = MechanismService.get_likes_count(db, updated_mechanism.id)
    
    # 閲覧回数を取得
    views_count = MechanismViewService.get_mechanism_views_count(db, updated_mechanism.id)
    
    # 更新されたメカニズム情報を返す
    return {
        "id": updated_mechanism.id,
        "title": updated_mechanism.title,
        "description": updated_mechanism.description,
        "reliability": updated_mechanism.reliability,
        "file_path": updated_mechanism.file_path,
        "thumbnail_path": updated_mechanism.thumbnail_path,
        "user": updated_mechanism.user,
        "categories": categories,
        "likes_count": likes_count,
        "views_count": views_count,
        "created_at": updated_mechanism.created_at,
        "updated_at": updated_mechanism.updated_at
    }

@router.delete("/{mechanism_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mechanism(
    mechanism_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    メカニズムを削除するエンドポイント
    
    Args:
        mechanism_id: 削除するメカニズムのID
        db: データベースセッション
        current_user: 現在のユーザー
        
    Returns:
        削除成功の場合は204 No Content
        
    Raises:
        HTTPException: メカニズムが見つからない場合、または削除権限がない場合
    """
    # メカニズムを削除
    success = MechanismService.delete_mechanism(
        db=db,
        mechanism_id=mechanism_id,
        current_user_id=current_user.id
    )
    
    if not success:
        # メカニズムが存在しないか、削除権限がない場合
        mechanism = MechanismService.get_mechanism_by_id(db, mechanism_id)
        if not mechanism:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="メカニズムが見つかりません"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このメカニズムを削除する権限がありません"
            )
    
    # 削除成功の場合は204 No Contentを返す
    return
