import pytest
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.models.like import Like

def test_database_connection(db_session: Session):
    """
    データベース接続のテスト
    """
    # データベースに接続できることを確認
    assert db_session is not None
    
    # トランザクションが機能することを確認
    db_session.begin()
    db_session.rollback()

def test_user_model(db_session: Session, test_user: User):
    """
    ユーザーモデルのテスト
    """
    # テストユーザーが正しく作成されていることを確認
    assert test_user.id is not None
    assert test_user.email == "test@example.com"
    assert test_user.password_hash == "hashed_password"
    
    # データベースからユーザーを取得できることを確認
    db_user = db_session.query(User).filter(User.id == test_user.id).first()
    assert db_user is not None
    assert db_user.email == test_user.email

def test_category_model(db_session: Session, test_category: Category):
    """
    カテゴリーモデルのテスト
    """
    # テストカテゴリーが正しく作成されていることを確認
    assert test_category.id is not None
    assert "テストカテゴリー" in test_category.name
    
    # データベースからカテゴリーを取得できることを確認
    db_category = db_session.query(Category).filter(Category.id == test_category.id).first()
    assert db_category is not None
    assert db_category.name == test_category.name

def test_mechanism_model(db_session: Session, test_mechanism: Mechanism, test_user: User, test_category: Category):
    """
    メカニズムモデルのテスト
    """
    # テストメカニズムが正しく作成されていることを確認
    assert test_mechanism.id is not None
    assert test_mechanism.title == "テストメカニズム"
    assert test_mechanism.description == "これはテスト用のメカニズムです"
    assert test_mechanism.reliability == 3
    assert test_mechanism.file_path == "/test/file.pdf"
    assert test_mechanism.thumbnail_path == "/test/thumbnail.jpg"
    assert test_mechanism.user_id == test_user.id
    
    # データベースからメカニズムを取得できることを確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.id == test_mechanism.id).first()
    assert db_mechanism is not None
    assert db_mechanism.title == test_mechanism.title
    
    # リレーションシップが正しく機能していることを確認
    assert db_mechanism.user.id == test_user.id
    assert len(db_mechanism.categories) == 1
    assert db_mechanism.categories[0].id == test_category.id

def test_like_model(db_session: Session, test_like: Like, test_user: User, test_mechanism: Mechanism):
    """
    いいねモデルのテスト
    """
    # テストいいねが正しく作成されていることを確認
    assert test_like.id is not None
    assert test_like.user_id == test_user.id
    assert test_like.mechanism_id == test_mechanism.id
    
    # データベースからいいねを取得できることを確認
    db_like = db_session.query(Like).filter(Like.id == test_like.id).first()
    assert db_like is not None
    assert db_like.user_id == test_like.user_id
    assert db_like.mechanism_id == test_like.mechanism_id
    
    # リレーションシップが正しく機能していることを確認
    assert db_like.user.id == test_user.id
    assert db_like.mechanism.id == test_mechanism.id

def test_relationship_user_mechanisms(db_session: Session, test_user: User, test_mechanism: Mechanism):
    """
    ユーザーとメカニズムのリレーションシップのテスト
    """
    # ユーザーからメカニズムを取得できることを確認
    db_user = db_session.query(User).filter(User.id == test_user.id).first()
    assert len(db_user.mechanisms) >= 1
    # テストメカニズムがユーザーのメカニズムリストに含まれていることを確認
    mechanism_ids = [m.id for m in db_user.mechanisms]
    assert test_mechanism.id in mechanism_ids

def test_relationship_mechanism_categories(db_session: Session, test_mechanism: Mechanism, test_category: Category):
    """
    メカニズムとカテゴリーのリレーションシップのテスト
    """
    # メカニズムからカテゴリーを取得できることを確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.id == test_mechanism.id).first()
    assert len(db_mechanism.categories) >= 1
    # テストカテゴリーがメカニズムのカテゴリーリストに含まれていることを確認
    category_ids = [c.id for c in db_mechanism.categories]
    assert test_category.id in category_ids
    
    # カテゴリーからメカニズムを取得できることを確認
    db_category = db_session.query(Category).filter(Category.id == test_category.id).first()
    assert len(db_category.mechanisms) >= 1
    # テストメカニズムがカテゴリーのメカニズムリストに含まれていることを確認
    mechanism_ids = [m.id for m in db_category.mechanisms]
    assert test_mechanism.id in mechanism_ids

def test_relationship_user_likes(db_session: Session, test_user: User, test_like: Like):
    """
    ユーザーといいねのリレーションシップのテスト
    """
    # ユーザーからいいねを取得できることを確認
    db_user = db_session.query(User).filter(User.id == test_user.id).first()
    assert len(db_user.likes) >= 1
    # テストいいねがユーザーのいいねリストに含まれていることを確認
    like_ids = [l.id for l in db_user.likes]
    assert test_like.id in like_ids

def test_relationship_mechanism_likes(db_session: Session, test_mechanism: Mechanism, test_like: Like):
    """
    メカニズムといいねのリレーションシップのテスト
    """
    # メカニズムからいいねを取得できることを確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.id == test_mechanism.id).first()
    assert len(db_mechanism.likes) >= 1
    # テストいいねがメカニズムのいいねリストに含まれていることを確認
    like_ids = [l.id for l in db_mechanism.likes]
    assert test_like.id in like_ids
