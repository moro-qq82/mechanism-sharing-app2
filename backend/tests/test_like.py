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
    # 確実に存在しないメカニズムIDを使用
    non_existent_mechanism_id = 99999
    like = LikeService.get_like(db_session, test_user.id, non_existent_mechanism_id)
    assert like is None

def test_create_like(db_session: Session, test_user, test_mechanism): # test_mechanism is a new mechanism from fixture
    """いいね作成のテスト"""
    # test_mechanism フィクスチャによって新しいメカニズムが提供される
    # そのメカニズムにいいねをする
    like = LikeService.create_like(db_session, test_user.id, test_mechanism.id)
    assert like is not None
    assert like.user_id == test_user.id
    assert like.mechanism_id == test_mechanism.id
    
    # データベースに保存されたことを確認
    db_like = LikeService.get_like(db_session, test_user.id, test_mechanism.id)
    assert db_like is not None
    assert db_like.user_id == test_user.id
    assert db_like.mechanism_id == test_mechanism.id

def test_delete_like(db_session: Session, test_user, test_mechanism): # test_mechanism is a new mechanism from fixture
    """いいね削除のテスト"""
    # test_mechanism フィクスチャによって新しいメカニズムが提供される
    # そのメカニズムにいいねを作成
    like = LikeService.create_like(db_session, test_user.id, test_mechanism.id)
    assert like is not None # Ensure like was created before attempting delete
    
    # 削除を実行
    result = LikeService.delete_like(db_session, test_user.id, test_mechanism.id)
    assert result is True
    
    # データベースから削除されたことを確認
    db_like = LikeService.get_like(db_session, test_user.id, test_mechanism.id)
    assert db_like is None

def test_delete_like_not_found(db_session: Session, test_user): # Removed test_mechanism as it's not directly used for non_existent
    """存在しないいいねの削除テスト"""
    # 存在しないメカニズムIDを使用
    non_existent_mechanism_id = 99999
    
    # 削除を実行
    result = LikeService.delete_like(db_session, test_user.id, non_existent_mechanism_id)
    assert result is False

def test_get_mechanism_likes_count(db_session: Session, test_user, test_mechanism):
    """メカニズムのいいね数取得テスト"""
    # まず、このメカニズムにいいねがないことを確認 (test_likeフィクスチャはここでは使わない)
    initial_count = LikeService.get_mechanism_likes_count(db_session, test_mechanism.id)
    assert initial_count == 0

    # test_user が test_mechanism にいいねをする
    LikeService.create_like(db_session, test_user.id, test_mechanism.id)
    count_after_first_like = LikeService.get_mechanism_likes_count(db_session, test_mechanism.id)
    assert count_after_first_like == 1
    
    # 新しいユーザーを作成してそのユーザーでもいいねする
    from backend.app.models.user import User
    import time
    unique_email = f"another_user_{time.time()}@example.com"
    new_user = User(
        email=unique_email, # Ensure unique email
        password_hash="another_hashed_password"
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    # 新しいユーザーでいいねする
    LikeService.create_like(db_session, new_user.id, test_mechanism.id)
    
    # いいね数が増えたことを確認
    new_count = LikeService.get_mechanism_likes_count(db_session, test_mechanism.id)
    assert new_count == 2

def test_get_user_liked_mechanisms(db_session: Session, test_user, test_mechanism): # Removed test_like
    """ユーザーがいいねしたメカニズム一覧取得テスト"""
    # test_user が test_mechanism にいいねをする
    LikeService.create_like(db_session, test_user.id, test_mechanism.id)

    # 新しいメカニズムを作成 (test_mechanismとは別)
    import time
    unique_title = f"もう一つのテストメカニズム_{time.time()}"
    another_mechanism = Mechanism(
        title=unique_title,
        description="これはもう一つのテスト用のメカニズムです",
        reliability=1,
        file_path="/test/another_file.pdf",
        thumbnail_path="/test/another_thumbnail.jpg",
        user_id=test_user.id # test_userがオーナー
    )
    db_session.add(another_mechanism)
    db_session.commit()
    db_session.refresh(another_mechanism)
    
    # 新しいメカニズムにも test_user がいいねする
    LikeService.create_like(db_session, test_user.id, another_mechanism.id)
    
    # ユーザーがいいねしたメカニズム一覧を取得
    liked_mechanisms = LikeService.get_user_liked_mechanisms(db_session, test_user.id)
    
    # 2つのメカニズムがいいねされていることを確認
    assert len(liked_mechanisms) == 2
    
    # いいねしたメカニズムのIDが含まれていることを確認
    mechanism_ids = [m.id for m in liked_mechanisms]
    assert test_mechanism.id in mechanism_ids
    assert another_mechanism.id in mechanism_ids

def test_get_popular_mechanisms(db_session: Session, test_user, test_mechanism): # Removed test_like
    """人気のメカニズム取得テスト"""
    # テストの独立性を高めるために、既存のLikeとMechanismデータをクリア
    # (test_mechanismフィクスチャが作るものは除く、あるいはフィクスチャ自体を使わないようにする方がよりクリーン)
    # 今回は、このテスト関数内で作成するデータのみに依存するように、関連データを削除します。
    # ただし、test_mechanismフィクスチャが作るものは残し、それ以外のものを制御します。
    # より厳密には、テスト開始時に全クリアが望ましいが、影響範囲を考慮し限定的に対応。
    # test_mechanism以外のMechanismと、全てのLikeを削除してみる。
    db_session.query(Like).delete()
    # test_mechanism.id 以外の Mechanism を削除 (フィクスチャで作成されたものは残す)
    db_session.query(Mechanism).filter(Mechanism.id != test_mechanism.id).delete()
    db_session.commit()


    # test_mechanism はフィクスチャから提供される (いいねはまだないはず)
    # 上記のクリア処理により、test_mechanism に関連する Like も消えているはずなので再作成の必要性を確認
    # → test_mechanism自体は残しているので、このテストケース内で test_mechanism へのいいねを能動的に行う

    # 新しいユーザーを2人作成
    from backend.app.models.user import User
    import time
    new_user1 = User(email=f"user1_{time.time()}@example.com", password_hash="hash1")
    new_user2 = User(email=f"user2_{time.time()}@example.com", password_hash="hash2")
    db_session.add_all([new_user1, new_user2])
    db_session.commit()
    db_session.refresh(new_user1)
    db_session.refresh(new_user2)
    
    # test_mechanism に3つのいいねをつける (test_user, new_user1, new_user2)
    LikeService.create_like(db_session, test_user.id, test_mechanism.id)
    LikeService.create_like(db_session, new_user1.id, test_mechanism.id)
    LikeService.create_like(db_session, new_user2.id, test_mechanism.id)

    # 別のメカニズムを作成し、1つのいいねをつける
    another_mechanism = Mechanism(
        title=f"あまり人気のないメカニズム_{time.time()}",
        description="いいねが少ない",
        reliability=2,
        file_path="/test/less_popular_file.pdf", # 追加
        thumbnail_path="/test/less_popular_thumbnail.jpg", # 追加
        user_id=test_user.id
    )
    db_session.add(another_mechanism)
    db_session.commit()
    db_session.refresh(another_mechanism)
    LikeService.create_like(db_session, test_user.id, another_mechanism.id)
    
    # 人気のメカニズムを取得 (上位1件)
    popular_mechanisms = LikeService.get_popular_mechanisms(db_session, limit=1)
    
    # 結果が1件返されることを確認
    assert len(popular_mechanisms) == 1
    
    # 最初の結果が最もいいね数の多いメカニズム(test_mechanism)であることを確認
    # popular_mechanisms[0] は (Mechanism, like_count) の形式であることを期待
    assert len(popular_mechanisms[0]) == 2 # 要素が2つあることを確認
    most_popular_mechanism = popular_mechanisms[0][0]
    likes_count = popular_mechanisms[0][1]

    assert isinstance(most_popular_mechanism, Mechanism) # 最初の要素がMechanismオブジェクトであることを確認
    assert isinstance(likes_count, int) # 2番目の要素が整数であることを確認
    assert most_popular_mechanism.id == test_mechanism.id
    assert likes_count == 3

    # 上位2件を取得してみる
    popular_mechanisms_top2 = LikeService.get_popular_mechanisms(db_session, limit=2)
    assert len(popular_mechanisms_top2) == 2
    assert popular_mechanisms_top2[0][0].id == test_mechanism.id # 1番目は test_mechanism (3いいね)
    assert popular_mechanisms_top2[0][1] == 3
    assert popular_mechanisms_top2[1][0].id == another_mechanism.id # 2番目は another_mechanism (1いいね)
    assert popular_mechanisms_top2[1][1] == 1
