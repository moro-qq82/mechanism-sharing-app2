from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from backend.app.models.like import Like
from backend.app.models.mechanism import Mechanism


class LikeService:
    """
    いいね関連のビジネスロジックを提供するサービスクラス
    """

    @staticmethod
    def get_likes_by_mechanism_id(db: Session, mechanism_id: int) -> int:
        """
        メカニズムに対するいいね数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            いいね数
        """
        return db.query(Like).filter(Like.mechanism_id == mechanism_id).count()

    @staticmethod
    def get_like(db: Session, user_id: int, mechanism_id: int) -> Optional[Like]:
        """
        特定のユーザーによる特定のメカニズムへのいいねを取得する

        Args:
            db: データベースセッション
            user_id: ユーザーID
            mechanism_id: メカニズムID

        Returns:
            いいねオブジェクト、存在しない場合はNone
        """
        return db.query(Like).filter(
            Like.user_id == user_id,
            Like.mechanism_id == mechanism_id
        ).first()

    @staticmethod
    def create_like(db: Session, user_id: int, mechanism_id: int) -> Like:
        """
        新しいいいねを作成する

        Args:
            db: データベースセッション
            user_id: ユーザーID
            mechanism_id: メカニズムID

        Returns:
            作成されたいいねオブジェクト
        """
        db_like = Like(user_id=user_id, mechanism_id=mechanism_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like

    @staticmethod
    def delete_like(db: Session, user_id: int, mechanism_id: int) -> bool:
        """
        いいねを削除する

        Args:
            db: データベースセッション
            user_id: ユーザーID
            mechanism_id: メカニズムID

        Returns:
            削除が成功したかどうか
        """
        db_like = LikeService.get_like(db, user_id, mechanism_id)
        if db_like:
            db.delete(db_like)
            db.commit()
            return True
        return False

    @staticmethod
    def get_mechanism_likes_count(db: Session, mechanism_id: int) -> int:
        """
        メカニズムのいいね数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            いいね数
        """
        return db.query(Like).filter(Like.mechanism_id == mechanism_id).count()

    @staticmethod
    def get_user_liked_mechanisms(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Mechanism]:
        """
        ユーザーがいいねしたメカニズム一覧を取得する

        Args:
            db: データベースセッション
            user_id: ユーザーID
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            メカニズムのリスト
        """
        return db.query(Mechanism).join(Like).filter(
            Like.user_id == user_id
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_popular_mechanisms(db: Session, limit: int = 10) -> List[Mechanism]:
        """
        いいね数の多い人気のメカニズム一覧を取得する

        Args:
            db: データベースセッション
            limit: 取得する最大件数

        Returns:
            メカニズムのリスト
        """
        # いいね数でグループ化して降順ソート
        return db.query(Mechanism, func.count(Like.id).label('likes_count'))\
            .join(Like)\
            .group_by(Mechanism.id)\
            .order_by(func.count(Like.id).desc())\
            .limit(limit)\
            .all()
