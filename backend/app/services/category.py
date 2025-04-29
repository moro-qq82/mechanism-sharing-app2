from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.category import Category
from backend.app.schemas.category import CategoryCreate


class CategoryService:
    """
    カテゴリー関連のビジネスロジックを提供するサービスクラス
    """

    @staticmethod
    def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        """
        カテゴリー一覧を取得する

        Args:
            db: データベースセッション
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            カテゴリーのリスト
        """
        return db.query(Category).offset(skip).limit(limit).all()

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
        """
        IDによりカテゴリーを取得する

        Args:
            db: データベースセッション
            category_id: カテゴリーID

        Returns:
            カテゴリーオブジェクト、存在しない場合はNone
        """
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_category_by_name(db: Session, name: str) -> Optional[Category]:
        """
        名前によりカテゴリーを取得する

        Args:
            db: データベースセッション
            name: カテゴリー名

        Returns:
            カテゴリーオブジェクト、存在しない場合はNone
        """
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def create_category(db: Session, category: CategoryCreate) -> Category:
        """
        新しいカテゴリーを作成する

        Args:
            db: データベースセッション
            category: 作成するカテゴリーのデータ

        Returns:
            作成されたカテゴリーオブジェクト
        """
        db_category = Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryCreate) -> Optional[Category]:
        """
        既存のカテゴリーを更新する

        Args:
            db: データベースセッション
            category_id: 更新するカテゴリーのID
            category: 更新データ

        Returns:
            更新されたカテゴリーオブジェクト、存在しない場合はNone
        """
        db_category = CategoryService.get_category_by_id(db, category_id)
        if db_category:
            db_category.name = category.name
            db.commit()
            db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        """
        カテゴリーを削除する

        Args:
            db: データベースセッション
            category_id: 削除するカテゴリーのID

        Returns:
            削除が成功したかどうか
        """
        db_category = CategoryService.get_category_by_id(db, category_id)
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False
