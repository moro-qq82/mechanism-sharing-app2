from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.schemas.category import CategoryCreate, CategoryResponse
from backend.app.services.category import CategoryService
from backend.app.middlewares.auth import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    カテゴリー一覧を取得するエンドポイント
    """
    categories = CategoryService.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDのカテゴリーを取得するエンドポイント
    """
    db_category = CategoryService.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリーが見つかりません")
    return db_category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    新しいカテゴリーを作成するエンドポイント
    """
    db_category = CategoryService.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="同じ名前のカテゴリーが既に存在します"
        )
    return CategoryService.create_category(db=db, category=category)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定されたIDのカテゴリーを更新するエンドポイント
    """
    # 同名のカテゴリーが存在するか確認
    existing_category = CategoryService.get_category_by_name(db, name=category.name)
    if existing_category and existing_category.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="同じ名前のカテゴリーが既に存在します"
        )
    
    db_category = CategoryService.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリーが見つかりません")
    return db_category

@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定されたIDのカテゴリーを削除するエンドポイント
    """
    success = CategoryService.delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリーが見つかりません")
    return {"message": "カテゴリーが正常に削除されました"}
