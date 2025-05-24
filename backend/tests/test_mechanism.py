import pytest
from sqlalchemy.orm import Session
from fastapi import UploadFile
import io
from unittest.mock import patch, MagicMock

from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.schemas.mechanism import MechanismCreate
from backend.app.services.mechanism import MechanismService

def test_get_mechanisms(db_session: Session, test_mechanism: Mechanism):
    """メカニズム一覧取得のテスト"""
    result = MechanismService.get_mechanisms(db_session)
    
    assert result["total"] >= 1
    assert len(result["items"]) >= 1
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["pages"] >= 1
    
    # テスト用メカニズムが含まれていることを確認
    assert any(mechanism.id == test_mechanism.id for mechanism in result["items"])

def test_get_mechanism_by_id(db_session: Session, test_mechanism: Mechanism):
    """IDによるメカニズム取得のテスト"""
    mechanism = MechanismService.get_mechanism_by_id(db_session, test_mechanism.id)
    
    assert mechanism is not None
    assert mechanism.id == test_mechanism.id
    assert mechanism.title == test_mechanism.title
    assert mechanism.description == test_mechanism.description
    assert mechanism.reliability == test_mechanism.reliability
    assert mechanism.file_path == test_mechanism.file_path
    assert mechanism.user_id == test_mechanism.user_id

def test_get_mechanism_by_id_not_found(db_session: Session):
    """存在しないIDによるメカニズム取得のテスト"""
    mechanism = MechanismService.get_mechanism_by_id(db_session, 999)
    assert mechanism is None

def test_get_likes_count(db_session: Session, test_mechanism: Mechanism, test_like):
    """いいね数取得のテスト"""
    likes_count = MechanismService.get_likes_count(db_session, test_mechanism.id)
    assert likes_count == 1

def test_get_likes_count_no_likes(db_session: Session, test_mechanism: Mechanism):
    """いいねがない場合のいいね数取得のテスト"""
    # テスト用いいねを削除
    from backend.app.models.like import Like
    db_session.query(Like).filter(Like.mechanism_id == test_mechanism.id).delete()
    db_session.commit()
    
    likes_count = MechanismService.get_likes_count(db_session, test_mechanism.id)
    assert likes_count == 0

@patch('backend.app.services.mechanism.os.makedirs')
@patch('backend.app.services.mechanism.open')
@patch('backend.app.services.mechanism.shutil.copyfileobj')
def test_save_upload_file(mock_copyfileobj, mock_open, mock_makedirs):
    """ファイル保存のテスト"""
    # モックの設定
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test content")
    
    # 関数を呼び出し
    with patch('backend.app.services.mechanism.uuid.uuid4', return_value="test-uuid"):
        file_path = MechanismService.save_upload_file(mock_file, "test_folder")
    
    # アサーション
    mock_makedirs.assert_called_once_with("test_folder", exist_ok=True)
    mock_open.assert_called_once()
    mock_copyfileobj.assert_called_once()
    assert "test-uuid.pdf" in file_path

def test_get_or_create_categories_existing(db_session: Session, test_category: Category):
    """既存のカテゴリー取得のテスト"""
    categories = MechanismService.get_or_create_categories(db_session, [test_category.name])
    
    assert len(categories) == 1
    assert categories[0].id == test_category.id
    assert categories[0].name == test_category.name

def test_get_or_create_categories_new(db_session: Session):
    """新規カテゴリー作成のテスト"""
    category_name = "新しいカテゴリー"
    categories = MechanismService.get_or_create_categories(db_session, [category_name])
    
    assert len(categories) == 1
    assert categories[0].name == category_name
    
    # データベースに保存されたことを確認
    db_category = db_session.query(Category).filter(Category.name == category_name).first()
    assert db_category is not None
    assert db_category.name == category_name

def test_get_or_create_categories_mixed(db_session: Session, test_category: Category):
    """既存と新規が混在するカテゴリー取得・作成のテスト"""
    new_category_name = "新しいカテゴリー2"
    categories = MechanismService.get_or_create_categories(db_session, [test_category.name, new_category_name])
    
    assert len(categories) == 2
    assert any(category.name == test_category.name for category in categories)
    assert any(category.name == new_category_name for category in categories)

def test_get_or_create_categories_empty(db_session: Session):
    """空のカテゴリーリストのテスト"""
    categories = MechanismService.get_or_create_categories(db_session, [])
    assert len(categories) == 0

def test_get_or_create_categories_whitespace(db_session: Session):
    """空白のみのカテゴリー名のテスト"""
    categories = MechanismService.get_or_create_categories(db_session, ["  ", ""])
    assert len(categories) == 0

@patch('backend.app.services.mechanism.MechanismService.get_or_create_categories')
def test_create_mechanism(mock_get_or_create_categories, db_session: Session, test_user):
    """メカニズム作成のテスト"""
    # モックの設定
    # IDを指定せずにCategoryオブジェクトを作成（データベースが自動的にIDを割り当てる）
    test_categories = [Category(name="テストカテゴリー")]
    mock_get_or_create_categories.return_value = test_categories
    
    # テストデータ
    mechanism_data = MechanismCreate(
        title="新しいメカニズム",
        description="これは新しいメカニズムです",
        reliability=4,
        categories=["テストカテゴリー"]
    )
    
    # 関数を呼び出し
    mechanism = MechanismService.create_mechanism(
        db=db_session,
        mechanism=mechanism_data,
        user_id=test_user.id,
        file_path="/test/new_file.pdf",
        thumbnail_path="/test/new_thumbnail.jpg"
    )
    
    # アサーション
    assert mechanism is not None
    assert mechanism.title == mechanism_data.title
    assert mechanism.description == mechanism_data.description
    assert mechanism.reliability == mechanism_data.reliability
    assert mechanism.file_path == "/test/new_file.pdf"
    assert mechanism.thumbnail_path == "/test/new_thumbnail.jpg"
    assert mechanism.user_id == test_user.id
    assert mechanism.categories == test_categories
    
    # データベースに保存されたことを確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.title == mechanism_data.title).first()
    assert db_mechanism is not None
    assert db_mechanism.id == mechanism.id
