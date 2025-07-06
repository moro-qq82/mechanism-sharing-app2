from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta

from backend.app.models.mechanism_view import MechanismView
from backend.app.schemas.mechanism_view import MechanismViewCreate

class MechanismViewService:
    """
    メカニズム閲覧履歴関連のビジネスロジックを提供するサービスクラス
    """

    @staticmethod
    def create_mechanism_view(db: Session, mechanism_id: int, user_id: Optional[int] = None) -> Tuple[MechanismView, bool]:
        """
        メカニズム閲覧履歴を作成する（5分間の重複防止機能付き）

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID（ログインしていない場合はNone）

        Returns:
            (MechanismView, is_new): 閲覧履歴オブジェクトと新規作成されたかのフラグ
        """
        # 5分前の時刻を計算
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        
        # 5分以内の同じユーザー・メカニズムの閲覧履歴をチェック
        recent_view = db.query(MechanismView).filter(
            MechanismView.mechanism_id == mechanism_id,
            MechanismView.user_id == user_id,
            MechanismView.viewed_at >= five_minutes_ago
        ).order_by(desc(MechanismView.viewed_at)).first()
        
        # 5分以内に閲覧履歴がある場合は既存のレコードを返す
        if recent_view:
            return recent_view, False
        
        # 5分以内に閲覧履歴がない場合は新規作成
        db_mechanism_view = MechanismView(
            mechanism_id=mechanism_id,
            user_id=user_id
        )
        
        # データベースに保存
        db.add(db_mechanism_view)
        db.commit()
        db.refresh(db_mechanism_view)
        
        return db_mechanism_view, True

    @staticmethod
    def get_mechanism_views_count(db: Session, mechanism_id: int) -> int:
        """
        メカニズムの総閲覧回数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            閲覧回数
        """
        return db.query(func.count(MechanismView.id)).filter(MechanismView.mechanism_id == mechanism_id).scalar()

    @staticmethod
    def get_user_mechanism_views_count(db: Session, mechanism_id: int, user_id: int) -> int:
        """
        特定ユーザーのメカニズム閲覧回数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID

        Returns:
            閲覧回数
        """
        return db.query(func.count(MechanismView.id)).filter(
            MechanismView.mechanism_id == mechanism_id,
            MechanismView.user_id == user_id
        ).scalar()

    @staticmethod
    def get_mechanism_views_stats(db: Session, mechanism_id: int, user_id: Optional[int] = None) -> Dict[str, int]:
        """
        メカニズムの閲覧統計情報を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID（指定された場合はユーザーごとの閲覧回数も取得）

        Returns:
            閲覧統計情報（総閲覧回数とユーザーごとの閲覧回数）
        """
        # 総閲覧回数を取得
        total_views = MechanismViewService.get_mechanism_views_count(db, mechanism_id)
        
        # レスポンス用の辞書を作成
        result = {
            "mechanism_id": mechanism_id,
            "total_views": total_views
        }
        
        # ユーザーIDが指定されている場合はユーザーごとの閲覧回数も取得
        if user_id:
            user_views = MechanismViewService.get_user_mechanism_views_count(db, mechanism_id, user_id)
            result["user_views"] = user_views
        
        return result

    @staticmethod
    def get_mechanisms_views_stats(db: Session, mechanism_ids: List[int], user_id: Optional[int] = None) -> List[Dict[str, int]]:
        """
        複数メカニズムの閲覧統計情報を取得する

        Args:
            db: データベースセッション
            mechanism_ids: メカニズムIDのリスト
            user_id: ユーザーID（指定された場合はユーザーごとの閲覧回数も取得）

        Returns:
            閲覧統計情報のリスト
        """
        results = []
        for mechanism_id in mechanism_ids:
            stats = MechanismViewService.get_mechanism_views_stats(db, mechanism_id, user_id)
            results.append(stats)
        
        return results
