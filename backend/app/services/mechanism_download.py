from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta

from backend.app.models.mechanism_download import MechanismDownload
from backend.app.schemas.mechanism_download import MechanismDownloadCreate

class MechanismDownloadService:
    """
    メカニズムダウンロード履歴関連のビジネスロジックを提供するサービスクラス
    """

    @staticmethod
    def create_mechanism_download(db: Session, mechanism_id: int, user_id: Optional[int] = None) -> Tuple[MechanismDownload, bool]:
        """
        メカニズムダウンロード履歴を作成する（5分間の重複防止機能付き）

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID（ログインしていない場合はNone）

        Returns:
            (MechanismDownload, is_new): ダウンロード履歴オブジェクトと新規作成されたかのフラグ
        """
        # 5分前の時刻を計算
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        
        # 5分以内の同じユーザー・メカニズムのダウンロード履歴をチェック
        recent_download = db.query(MechanismDownload).filter(
            MechanismDownload.mechanism_id == mechanism_id,
            MechanismDownload.user_id == user_id,
            MechanismDownload.downloaded_at >= five_minutes_ago
        ).order_by(desc(MechanismDownload.downloaded_at)).first()
        
        # 5分以内にダウンロード履歴がある場合は既存のレコードを返す
        if recent_download:
            return recent_download, False
        
        # 5分以内にダウンロード履歴がない場合は新規作成
        db_mechanism_download = MechanismDownload(
            mechanism_id=mechanism_id,
            user_id=user_id
        )
        
        # データベースに保存
        db.add(db_mechanism_download)
        db.commit()
        db.refresh(db_mechanism_download)
        
        return db_mechanism_download, True

    @staticmethod
    def get_mechanism_downloads_count(db: Session, mechanism_id: int) -> int:
        """
        メカニズムの総ダウンロード回数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            ダウンロード回数
        """
        return db.query(func.count(MechanismDownload.id)).filter(MechanismDownload.mechanism_id == mechanism_id).scalar()

    @staticmethod
    def get_user_mechanism_downloads_count(db: Session, mechanism_id: int, user_id: int) -> int:
        """
        特定ユーザーのメカニズムダウンロード回数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID

        Returns:
            ダウンロード回数
        """
        return db.query(func.count(MechanismDownload.id)).filter(
            MechanismDownload.mechanism_id == mechanism_id,
            MechanismDownload.user_id == user_id
        ).scalar()

    @staticmethod
    def get_mechanism_downloads_stats(db: Session, mechanism_id: int, user_id: Optional[int] = None) -> Dict[str, int]:
        """
        メカニズムのダウンロード統計情報を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID
            user_id: ユーザーID（指定された場合はユーザーごとのダウンロード回数も取得）

        Returns:
            ダウンロード統計情報（総ダウンロード回数とユーザーごとのダウンロード回数）
        """
        # 総ダウンロード回数を取得
        total_downloads = MechanismDownloadService.get_mechanism_downloads_count(db, mechanism_id)
        
        # レスポンス用の辞書を作成
        result = {
            "mechanism_id": mechanism_id,
            "total_downloads": total_downloads
        }
        
        # ユーザーIDが指定されている場合はユーザーごとのダウンロード回数も取得
        if user_id:
            user_downloads = MechanismDownloadService.get_user_mechanism_downloads_count(db, mechanism_id, user_id)
            result["user_downloads"] = user_downloads
        
        return result

    @staticmethod
    def get_mechanisms_downloads_stats(db: Session, mechanism_ids: List[int], user_id: Optional[int] = None) -> List[Dict[str, int]]:
        """
        複数メカニズムのダウンロード統計情報を取得する

        Args:
            db: データベースセッション
            mechanism_ids: メカニズムIDのリスト
            user_id: ユーザーID（指定された場合はユーザーごとのダウンロード回数も取得）

        Returns:
            ダウンロード統計情報のリスト
        """
        results = []
        for mechanism_id in mechanism_ids:
            stats = MechanismDownloadService.get_mechanism_downloads_stats(db, mechanism_id, user_id)
            results.append(stats)
        
        return results