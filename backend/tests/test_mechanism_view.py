import pytest
from sqlalchemy.orm import Session

from backend.app.models.mechanism_view import MechanismView
from backend.app.services.mechanism_view import MechanismViewService

def test_create_mechanism_view(db_session: Session, test_mechanism):
    """メカニズム閲覧履歴作成のテスト"""
    # ユーザーIDありの場合
    mechanism_view = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_mechanism.user_id
    )
    
    assert mechanism_view is not None
    assert mechanism_view.mechanism_id == test_mechanism.id
    assert mechanism_view.user_id == test_mechanism.user_id
    
    # ユーザーIDなしの場合（匿名ユーザー）
    anonymous_view = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None
    )
    
    assert anonymous_view is not None
    assert anonymous_view.mechanism_id == test_mechanism.id
    assert anonymous_view.user_id is None

def test_get_mechanism_views_count(db_session: Session, test_mechanism, test_mechanism_view):
    """メカニズム総閲覧回数取得のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).filter(MechanismView.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    # 閲覧履歴を1件作成
    test_view = MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_mechanism.user_id
    )
    
    # 匿名ユーザーの閲覧履歴をもう1件追加
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=None  # 匿名ユーザー
    )
    
    # 閲覧回数を取得
    views_count = MechanismViewService.get_mechanism_views_count(db_session, test_mechanism.id)
    
    # 合計2件の閲覧履歴があるはず
    assert views_count == 2

def test_get_user_mechanism_views_count(db_session: Session, test_mechanism, test_user, test_mechanism_view):
    """特定ユーザーのメカニズム閲覧回数取得のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).filter(MechanismView.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    # 同じユーザーの閲覧を2件追加
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 匿名ユーザーの閲覧も1件追加
    MechanismViewService.create_mechanism_view(
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

def test_get_mechanism_views_stats(db_session: Session, test_mechanism, test_user, test_mechanism_view):
    """メカニズム閲覧統計情報取得のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).filter(MechanismView.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    # 同じユーザーの閲覧を2件追加
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 匿名ユーザーの閲覧も1件追加
    MechanismViewService.create_mechanism_view(
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

def test_get_mechanisms_views_stats(db_session: Session, test_mechanism, test_user, test_mechanism_view):
    """複数メカニズムの閲覧統計情報取得のテスト"""
    # テスト前にデータベースをクリーンアップ
    db_session.query(MechanismView).delete()
    db_session.commit()
    
    # 1つ目のメカニズムの閲覧履歴を1件追加
    MechanismViewService.create_mechanism_view(
        db=db_session,
        mechanism_id=test_mechanism.id,
        user_id=test_user.id
    )
    
    # 2つ目のメカニズムを作成
    from backend.app.models.mechanism import Mechanism
    second_mechanism = Mechanism(
        title="2つ目のテストメカニズム",
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
    MechanismViewService.create_mechanism_view(
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
