import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import time

from backend.app.models.mechanism_view import MechanismView
from backend.app.services.mechanism_view import MechanismViewService

def test_create_mechanism_view(db_session: Session, test_mechanism):
    """メカニズム閲覧履歴作成のテスト（5分間重複防止機能付き）"""
    # ユーザーIDありの場合（初回アクセス）
    mechanism_view, is_new = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_mechanism.user_id
    )
    
    assert mechanism_view is not None
    assert mechanism_view.mechanism_id == test_mechanism.id
    assert mechanism_view.user_id == test_mechanism.user_id
    assert is_new is True  # 新規作成
    
    # ユーザーIDなしの場合（匿名ユーザー）
    anonymous_view, is_new_anon = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None
    )
    
    assert anonymous_view is not None
    assert anonymous_view.mechanism_id == test_mechanism.id
    assert anonymous_view.user_id is None
    assert is_new_anon is True  # 新規作成

def test_duplicate_view_prevention(db_session: Session, test_mechanism, test_user):
    """5分間重複防止機能のテスト"""
    # 初回アクセス
    first_view, is_new_first = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    assert is_new_first is True  # 初回は新規作成
    first_view_id = first_view.id
    
    # 5分以内の再アクセス（重複防止されるべき）
    second_view, is_new_second = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    assert is_new_second is False  # 新規作成されない
    assert second_view.id == first_view_id  # 同じレコードが返される
    
    # 別のユーザーでは新規作成される
    from backend.app.models.user import User
    import time
    another_user = User(
        email=f"another_test_{time.time()}@example.com",
        password_hash="hashed_password"
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)
    
    third_view, is_new_third = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=another_user.id
    )
    
    assert is_new_third is True  # 別ユーザーは新規作成
    assert third_view.id != first_view_id  # 異なるレコード

def test_view_prevention_time_limit(db_session: Session, test_mechanism, test_user):
    """5分経過後の閲覧記録テスト（実際の待機なしでモック）"""
    # 初回アクセス
    first_view, is_new_first = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    assert is_new_first is True
    
    # 5分以上前の時刻に手動で更新（テスト用）
    six_minutes_ago = datetime.utcnow() - timedelta(minutes=6)
    first_view.viewed_at = six_minutes_ago
    db_session.commit()
    
    # 5分経過後のアクセス（新規作成されるべき）
    second_view, is_new_second = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    assert is_new_second is True  # 5分経過後は新規作成
    assert second_view.id != first_view.id  # 異なるレコード

def test_get_mechanism_views_count(db_session: Session, test_mechanism, test_user): # test_mechanism_view is not used due to cleanup
    """メカニズム総閲覧回数取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    
    # 閲覧履歴を1件作成 (test_userによる閲覧)
    view1, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id # test_userを使用
    )
    
    # 匿名ユーザーの閲覧履歴をもう1件追加
    view2, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None  # 匿名ユーザー
    )
    
    # 閲覧回数を取得
    views_count = MechanismViewService.get_mechanism_views_count(db_session, test_mechanism.id)
    
    # 合計2件の閲覧履歴があるはず
    assert views_count == 2

def test_get_user_mechanism_views_count(db_session: Session, test_mechanism, test_user): # test_mechanism_view is not used
    """特定ユーザーのメカニズム閲覧回数取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず

    # 同じユーザーの閲覧を2件追加（時間差を設けて重複防止を回避）
    view1, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 最初の閲覧を6分前に設定
    six_minutes_ago = datetime.utcnow() - timedelta(minutes=6)
    view1.viewed_at = six_minutes_ago
    db_session.commit()
    
    view2, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 匿名ユーザーの閲覧も1件追加
    view3, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None
    )
    
    # 特定ユーザーの閲覧回数を取得
    user_views_count = MechanismViewService.get_user_mechanism_views_count(
        db_session, 
        test_mechanism.id, 
        test_user.id
    )
    
    # テストユーザーの閲覧は2件のはず
    assert user_views_count == 2

def test_get_mechanism_views_stats(db_session: Session, test_mechanism, test_user): # test_mechanism_view is not used
    """メカニズム閲覧統計情報取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず

    # 同じユーザーの閲覧を2件追加（時間差を設けて重複防止を回避）
    view1, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 最初の閲覧を6分前に設定
    six_minutes_ago = datetime.utcnow() - timedelta(minutes=6)
    view1.viewed_at = six_minutes_ago
    db_session.commit()
    
    view2, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 匿名ユーザーの閲覧も1件追加
    view3, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None
    )
    
    # ユーザーIDを指定して統計情報を取得
    stats_with_user = MechanismViewService.get_mechanism_views_stats(
        db_session, 
        test_mechanism.id, 
        test_user.id
    )
    
    assert stats_with_user["mechanism_id"] == test_mechanism.id
    assert stats_with_user["total_views"] == 3  # 合計3件の閲覧
    assert stats_with_user["user_views"] == 2   # テストユーザーの閲覧は2件
    
    # ユーザーIDを指定せずに統計情報を取得
    stats_without_user = MechanismViewService.get_mechanism_views_stats(
        db_session, 
        test_mechanism.id
    )
    
    assert stats_without_user["mechanism_id"] == test_mechanism.id
    assert stats_without_user["total_views"] == 3  # 合計3件の閲覧
    assert "user_views" not in stats_without_user  # ユーザー閲覧数は含まれない

def test_get_mechanisms_views_stats(db_session: Session, test_mechanism, test_user): # test_mechanism_view is not used
    """複数メカニズムの閲覧統計情報取得のテスト"""
    # db_sessionのロールバック機能により、前のテストデータはクリアされているはず
    
    # 1つ目のメカニズム(test_mechanism)の閲覧履歴を1件追加
    view1, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 2つ目のメカニズムを作成
    from backend.app.models.mechanism import Mechanism
    import time
    second_mechanism = Mechanism(
        title=f"2つ目のテストメカニズム_{time.time()}", # Ensure unique title
        description="これは2つ目のテスト用メカニズムです",
        reliability=4,
        file_path="/test/file2.pdf",
        thumbnail_path="/test/thumbnail2.jpg",
        user_id=test_user.id
    )
    db_session.add(second_mechanism)
    db_session.commit()
    db_session.refresh(second_mechanism)
    
    # 2つ目のメカニズムの閲覧履歴を追加
    view2, _ = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=second_mechanism.id,
        user_id=test_user.id
    )
    
    # 複数メカニズムの統計情報を取得
    mechanism_ids = [test_mechanism.id, second_mechanism.id]
    stats = MechanismViewService.get_mechanisms_views_stats(
        db_session, 
        mechanism_ids, 
        test_user.id
    )
    
    assert len(stats) == 2
    
    # 1つ目のメカニズムの統計情報を確認
    first_stats = next(s for s in stats if s["mechanism_id"] == test_mechanism.id)
    assert first_stats["total_views"] == 1  # test_mechanism_viewの1件
    assert first_stats["user_views"] == 1   # テストユーザーの閲覧は1件
    
    # 2つ目のメカニズムの統計情報を確認
    second_stats = next(s for s in stats if s["mechanism_id"] == second_mechanism.id)
    assert second_stats["total_views"] == 1  # 追加した1件
    assert second_stats["user_views"] == 1   # テストユーザーの閲覧は1件
