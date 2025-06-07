import pytest
from sqlalchemy.orm import Session

from backend.app.models.category import Category
from backend.app.schemas.category import CategoryCreate
from backend.app.services.category import CategoryService

def test_get_categories(db_session: Session, test_category: Category):
    """カテゴリー一覧取得のテスト"""
    categories = CategoryService.get_categories(db_session)
    # test_categoryフィクスチャによって1つのカテゴリが作成されているはず
    assert len(categories) == 1
    assert categories[0].id == test_category.id
    assert categories[0].name == test_category.name

def test_get_category_by_id(db_session: Session, test_category: Category):
    """IDによるカテゴリー取得のテスト"""
    category = CategoryService.get_category_by_id(db_session, test_category.id)
    assert category is not None
    assert category.id == test_category.id
    assert category.name == test_category.name

def test_get_category_by_id_not_found(db_session: Session):
    """存在しないIDによるカテゴリー取得のテスト"""
    category = CategoryService.get_category_by_id(db_session, 999)
    assert category is None

def test_get_category_by_name(db_session: Session, test_category: Category):
    """名前によるカテゴリー取得のテスト"""
    category = CategoryService.get_category_by_name(db_session, test_category.name)
    assert category is not None
    assert category.id == test_category.id
    assert category.name == test_category.name

def test_get_category_by_name_not_found(db_session: Session):
    """存在しない名前によるカテゴリー取得のテスト"""
    category = CategoryService.get_category_by_name(db_session, "存在しないカテゴリー")
    assert category is None

def test_create_category(db_session: Session):
    """カテゴリー作成のテスト"""
    category_data = CategoryCreate(name="新しいカテゴリー")
    category = CategoryService.create_category(db_session, category_data)
    assert category is not None
    assert category.name == category_data.name
    assert category.id is not None
    
    # データベースに保存されたことを確認
    db_category = CategoryService.get_category_by_name(db_session, name=category_data.name)
    assert db_category is not None
    assert db_category.name == category_data.name

def test_update_category(db_session: Session, test_category: Category):
    """カテゴリー更新のテスト"""
    update_data = CategoryCreate(name="更新されたカテゴリー")
    updated_category = CategoryService.update_category(db_session, test_category.id, update_data)
    assert updated_category is not None
    assert updated_category.id == test_category.id
    assert updated_category.name == update_data.name
    
    # データベースが更新されたことを確認
    db_category = CategoryService.get_category_by_id(db_session, category_id=test_category.id)
    assert db_category.name == update_data.name

def test_update_category_not_found(db_session: Session):
    """存在しないカテゴリーの更新テスト"""
    update_data = CategoryCreate(name="存在しないカテゴリー")
    updated_category = CategoryService.update_category(db_session, 999, update_data)
    assert updated_category is None

def test_delete_category(db_session: Session):
    """カテゴリー削除のテスト"""
    # 削除用のカテゴリーを作成
    category_data = CategoryCreate(name="削除用カテゴリー")
    category = CategoryService.create_category(db_session, category_data)
    
    # 削除を実行
    result = CategoryService.delete_category(db_session, category.id)
    assert result is True
    
    # データベースから削除されたことを確認
    db_category = CategoryService.get_category_by_id(db_session, category_id=category.id)
    assert db_category is None

def test_delete_category_not_found(db_session: Session):
    """存在しないカテゴリーの削除テスト"""
    result = CategoryService.delete_category(db_session, 999)
    assert result is False
