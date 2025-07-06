import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.app.models.mechanism_download import MechanismDownload
from backend.app.services.mechanism_download import MechanismDownloadService
@pytest.fixture
def db_session(TestingSessionLocal):
    """テスト用データベースセッション"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # テスト後にデータをクリーンアップ
        db.query(MechanismDownload).delete()
        db.commit()
        db.close()


class TestMechanismDownloadService:
    """MechanismDownloadServiceのテストクラス"""

    def test_create_mechanism_download_success(self, db_session: Session):
        """ダウンロード履歴の作成が成功することをテスト"""
        mechanism_id = 1
        user_id = 1
        
        # ダウンロード履歴を作成
        download, is_new = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, user_id
        )
        
        # 結果を検証
        assert download is not None
        assert download.mechanism_id == mechanism_id
        assert download.user_id == user_id
        assert download.downloaded_at is not None
        assert is_new is True
        
        # データベースに保存されているかを検証
        db_download = db_session.query(MechanismDownload).filter(
            MechanismDownload.id == download.id
        ).first()
        assert db_download is not None
        assert db_download.mechanism_id == mechanism_id
        assert db_download.user_id == user_id

    def test_create_mechanism_download_without_user(self, db_session: Session):
        """ユーザーIDなしでダウンロード履歴を作成できることをテスト"""
        mechanism_id = 1
        
        # ユーザーIDなしでダウンロード履歴を作成
        download, is_new = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, None
        )
        
        # 結果を検証
        assert download is not None
        assert download.mechanism_id == mechanism_id
        assert download.user_id is None
        assert download.downloaded_at is not None
        assert is_new is True

    def test_duplicate_download_prevention(self, db_session: Session):
        """5分以内の重複ダウンロードが防止されることをテスト"""
        mechanism_id = 1
        user_id = 1
        
        # 最初のダウンロード履歴を作成
        first_download, is_new1 = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, user_id
        )
        
        # 同じユーザーが同じメカニズムを再度ダウンロード（5分以内）
        second_download, is_new2 = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, user_id
        )
        
        # 結果を検証
        assert first_download is not None
        assert second_download is not None
        assert is_new1 is True
        assert is_new2 is False  # 新規作成されていない
        assert first_download.id == second_download.id  # 同じレコード

    def test_download_prevention_time_limit(self, db_session: Session):
        """5分経過後は新しいダウンロード履歴が作成されることをテスト"""
        mechanism_id = 1
        user_id = 1
        
        # 最初のダウンロード履歴を作成
        first_download, is_new1 = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, user_id
        )
        
        # 5分前の時刻に手動で設定（テスト用）
        six_minutes_ago = datetime.utcnow() - timedelta(minutes=6)
        first_download.downloaded_at = six_minutes_ago
        db_session.commit()
        
        # 5分経過後に再度ダウンロード
        second_download, is_new2 = MechanismDownloadService.create_mechanism_download(
            db_session, mechanism_id, user_id
        )
        
        # 結果を検証
        assert first_download is not None
        assert second_download is not None
        assert is_new1 is True
        assert is_new2 is True  # 新規作成されている
        assert first_download.id != second_download.id  # 異なるレコード

    def test_get_mechanism_downloads_count(self, db_session: Session):
        """メカニズムの総ダウンロード回数を正しく取得できることをテスト"""
        mechanism_id = 1
        
        # 初期状態では0回
        count = MechanismDownloadService.get_mechanism_downloads_count(db_session, mechanism_id)
        assert count == 0
        
        # ダウンロード履歴を複数作成
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, 1)
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, 2)
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, None)
        
        # ダウンロード回数を取得
        count = MechanismDownloadService.get_mechanism_downloads_count(db_session, mechanism_id)
        assert count == 3

    def test_get_user_mechanism_downloads_count(self, db_session: Session):
        """特定ユーザーのメカニズムダウンロード回数を正しく取得できることをテスト"""
        mechanism_id = 1
        user_id = 1
        
        # 初期状態では0回
        count = MechanismDownloadService.get_user_mechanism_downloads_count(
            db_session, mechanism_id, user_id
        )
        assert count == 0
        
        # 特定ユーザーのダウンロード履歴を作成
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, user_id)
        
        # 他のユーザーのダウンロード履歴も作成
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, 2)
        
        # 特定ユーザーのダウンロード回数を取得
        count = MechanismDownloadService.get_user_mechanism_downloads_count(
            db_session, mechanism_id, user_id
        )
        assert count == 1

    def test_get_mechanism_downloads_stats(self, db_session: Session):
        """メカニズムのダウンロード統計情報を正しく取得できることをテスト"""
        mechanism_id = 1
        user_id = 1
        
        # ダウンロード履歴を作成
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, user_id)
        MechanismDownloadService.create_mechanism_download(db_session, mechanism_id, 2)
        
        # ユーザーIDありの統計情報を取得
        stats = MechanismDownloadService.get_mechanism_downloads_stats(
            db_session, mechanism_id, user_id
        )
        
        # 結果を検証
        assert stats["mechanism_id"] == mechanism_id
        assert stats["total_downloads"] == 2
        assert stats["user_downloads"] == 1
        
        # ユーザーIDなしの統計情報を取得
        stats_without_user = MechanismDownloadService.get_mechanism_downloads_stats(
            db_session, mechanism_id
        )
        
        # 結果を検証
        assert stats_without_user["mechanism_id"] == mechanism_id
        assert stats_without_user["total_downloads"] == 2
        assert "user_downloads" not in stats_without_user

    def test_get_mechanisms_downloads_stats(self, db_session: Session):
        """複数メカニズムのダウンロード統計情報を正しく取得できることをテスト"""
        mechanism_ids = [1, 2]
        user_id = 1
        
        # メカニズム1のダウンロード履歴を作成
        MechanismDownloadService.create_mechanism_download(db_session, 1, user_id)
        MechanismDownloadService.create_mechanism_download(db_session, 1, 2)
        
        # メカニズム2のダウンロード履歴を作成
        MechanismDownloadService.create_mechanism_download(db_session, 2, user_id)
        
        # 複数メカニズムの統計情報を取得
        stats_list = MechanismDownloadService.get_mechanisms_downloads_stats(
            db_session, mechanism_ids, user_id
        )
        
        # 結果を検証
        assert len(stats_list) == 2
        
        # メカニズム1の統計
        mechanism1_stats = stats_list[0]
        assert mechanism1_stats["mechanism_id"] == 1
        assert mechanism1_stats["total_downloads"] == 2
        assert mechanism1_stats["user_downloads"] == 1
        
        # メカニズム2の統計
        mechanism2_stats = stats_list[1]
        assert mechanism2_stats["mechanism_id"] == 2
        assert mechanism2_stats["total_downloads"] == 1
        assert mechanism2_stats["user_downloads"] == 1