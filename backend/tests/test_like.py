import pytest
from sqlalchemy.orm import Session

from backend.app.models.like import Like
from backend.app.models.mechanism import Mechanism
from backend.app.services.like import LikeService

def test_get_like(db_session: Session, test_like: Like):
    """特定のいいねを取得するテスト"""
    like = LikeService.get_like(db_session, test_like.user_id, test_like.mechanism_id)
    assert like is not None
    assert like.id == test_like.id
    assert like.user_id == test_like.user_id
    assert like.mechanism_id == test_like.mechanism_id

def test_get_like_not_found(db_session: Session, test_user, test_mechanism):
    """存在しないいいねを取得するテスト"""
    # 別のメカニズムIDを使用
    non_existent_mechanism_id = test_mechanism.id + 1
    like = LikeService.get_like(db_session, test_user.id, non_existent_mechanism_id)
    assert like is None

def test_create_like(db_session: Session, test_user, test_mechanism):
    """いいね作成のテスト"""
    # 新しいメカニズムを作成してそれにいいねする
    new_mechanism = Mechanism(
        title="新しいテストメカニズム",
        description="これは新しいテスト用のメカニズムです",
        reliability=2,
        file_path="/test/new_file.pdf",
        thumbnail_path="/test/new_thumbnail.jpg",
        user_id=test_user.id
    )
    db_session.add(new_mechanism)
    db_session.commit()
    db_session.refresh(new_mechanism)
    
    # いいねを作成
    like = LikeService.create_like(db_session, test_user.id, new_mechanism.id)
    assert like is not None
    assert like.user_id == test_user.id
    assert like.mechanism_id == new_mechanism.id
    
    # データベースに保存されたことを確認
    db_like = LikeService.get_like(db_session, test_user.id, new_mechanism.id)
    assert db_like is not None
    assert db_like.user_id == test_user.id
    assert db_like.mechanism_id == new_mechanism.id

def test_delete_like(db_session: Session, test_user, test_mechanism):
    """いいね削除のテスト"""
    # 新しいメカニズムを作成してそれにいいねする
    new_mechanism = Mechanism(
        title="削除テスト用メカニズム",
        description="これは削除テスト用のメカニズムです",
        reliability=2,
        file_path="/test/delete_test_file.pdf",
        thumbnail_path="/test/delete_test_thumbnail.jpg",
        user_id=test_user.id
    )
    db_session.add(new_mechanism)
    db_session.commit()
    db_session.refresh(new_mechanism)
    
    # 新しいメカニズムにいいねを作成
    like = LikeService.create_like(db_session, test_user.id, new_mechanism.id)
    
    # 削除を実行
    result = LikeService.delete_like(db_session, test_user.id, new_mechanism.id)
    assert result is True
    
    # データベースから削除されたことを確認
    db_like = LikeService.get_like(db_session, test_user.id, new_mechanism.id)
    assert db_like is None

def test_delete_like_not_found(db_session: Session, test_user, test_mechanism):
    """存在しないいいねの削除テスト"""
    # 存在しないメカニズムIDを使用
    # 実際にデータベースに存在しない大きな値を使用
    non_existent_mechanism_id = 99999
    
    # 削除を実行
    result = LikeService.delete_like(db_session, test_user.id, non_existent_mechanism_id)
    assert result is False

def test_get_mechanism_likes_count(db_session: Session, test_like: Like, test_user, test_mechanism):
    """メカニズムのいいね数取得テスト"""
    # 既存のいいねがあるので、カウントは1以上
    count = LikeService.get_mechanism_likes_count(db_session, test_mechanism.id)
    assert count >= 1
    
    # 新しいユーザーを作成してそのユーザーでもいいねする
    from backend.app.models.user import User
    new_user = User(
        email="another@example.com",
        password_hash="another_hashed_password"
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    # 新しいユーザーでいいねする
    LikeService.create_like(db_session, new_user.id, test_mechanism.id)
    
    # いいね数が増えたことを確認
    new_count = LikeService.get_mechanism_likes_count(db_session, test_mechanism.id)
    assert new_count == count + 1

def test_get_user_liked_mechanisms(db_session: Session, test_user, test_mechanism, test_like: Like):
    """ユーザーがいいねしたメカニズム一覧取得テスト"""
    # 新しいメカニズムを作成
    new_mechanism = Mechanism(
        title="もう一つのテストメカニズム",
        description="これはもう一つのテスト用のメカニズムです",
        reliability=1,
        file_path="/test/another_file.pdf",
        thumbnail_path="/test/another_thumbnail.jpg",
        user_id=test_user.id
    )
    db_session.add(new_mechanism)
    db_session.commit()
    db_session.refresh(new_mechanism)
    
    # 新しいメカニズムにもいいねする
    LikeService.create_like(db_session, test_user.id, new_mechanism.id)
    
    # ユーザーがいいねしたメカニズム一覧を取得
    liked_mechanisms = LikeService.get_user_liked_mechanisms(db_session, test_user.id)
    
    # 少なくとも2つのメカニズムがいいねされていることを確認
    assert len(liked_mechanisms) >= 2
    
    # いいねしたメカニズムのIDが含まれていることを確認
    mechanism_ids = [m.id for m in liked_mechanisms]
    assert test_mechanism.id in mechanism_ids
    assert new_mechanism.id in mechanism_ids

def test_get_popular_mechanisms(db_session: Session, test_user, test_mechanism, test_like: Like):
    """人気のメカニズム取得テスト"""
    # 新しいメカニズムを作成
    new_mechanism = Mechanism(
        title="人気のテストメカニズム",
        description="これは人気のテスト用のメカニズムです",
        reliability=5,
        file_path="/test/popular_file.pdf",
        thumbnail_path="/test/popular_thumbnail.jpg",
        user_id=test_user.id
    )
    db_session.add(new_mechanism)
    db_session.commit()
    db_session.refresh(new_mechanism)
    
    # 新しいユーザーを作成
    from backend.app.models.user import User
    new_user1 = User(email="user1@example.com", password_hash="hash1")
    new_user2 = User(email="user2@example.com", password_hash="hash2")
    db_session.add_all([new_user1, new_user2])
    db_session.commit()
    db_session.refresh(new_user1)
    db_session.refresh(new_user2)
    
    # 新しいメカニズムに複数のいいねをつける
    LikeService.create_like(db_session, test_user.id, new_mechanism.id)
    LikeService.create_like(db_session, new_user1.id, new_mechanism.id)
    LikeService.create_like(db_session, new_user2.id, new_mechanism.id)
    
    # 人気のメカニズムを取得
    popular_mechanisms = LikeService.get_popular_mechanisms(db_session, limit=2)
    
    # 結果が返されることを確認
    assert len(popular_mechanisms) > 0
    
    # 最初の結果が最もいいね数の多いメカニズムであることを確認
    most_popular_mechanism, likes_count = popular_mechanisms[0]
    assert most_popular_mechanism.id == new_mechanism.id
    assert likes_count >= 3  # 少なくとも3つのいいねがあるはず
