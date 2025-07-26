import pytest
from sqlalchemy.orm import Session
from fastapi import UploadFile
import io
from unittest.mock import patch, MagicMock
import time # For unique names

from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.schemas.mechanism import MechanismCreate, MechanismUpdate
from backend.app.services.mechanism import MechanismService

def test_get_mechanisms(db_session: Session, test_mechanism: Mechanism):
    """メカニズム一覧取得のテスト"""
    result = MechanismService.get_mechanisms(db_session) # Default: page=1, limit=10
    
    # test_mechanismフィクスチャによって1つのメカニズムが作成されているはず
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["page"] == 1
    assert result["limit"] == 10 # Default limit
    assert result["pages"] == 1
    
    # テスト用メカニズムが含まれていることを確認
    assert result["items"][0].id == test_mechanism.id
    assert result["items"][0].title == test_mechanism.title

def test_get_mechanisms_pagination(db_session: Session, test_user): # test_mechanismフィクスチャへの依存を削除
    """メカニズム一覧取得のページネーションテスト"""
    # 既存のメカニズムをクリアする（あるいは、テストDBを毎回クリーンにする設定があれば不要）
    # 今回は、テストの独立性を高めるために、このテスト専用のデータを投入する前にクリアする
    db_session.query(Mechanism).delete()
    db_session.commit()

    # 複数のメカニズムを作成
    mechanisms_data = []
    for i in range(15): # Create 15 mechanisms
        mechanism = Mechanism(
            title=f"Test Mechanism {i} {time.time()}", # Ensure unique titles
            description=f"Description {i}",
            reliability=i % 5 + 1,
            user_id=test_user.id,
            file_path=f"/test/file{i}.pdf",
            thumbnail_path=f"/test/thumb{i}.jpg"
        )
        mechanisms_data.append(mechanism)
    db_session.add_all(mechanisms_data)
    db_session.commit()
    for m in mechanisms_data:
        db_session.refresh(m)

    # 1ページ目、limit=5
    skip1 = (1 - 1) * 5
    result_page1_limit5 = MechanismService.get_mechanisms(db_session, skip=skip1, limit=5)
    assert result_page1_limit5["total"] == 15
    assert len(result_page1_limit5["items"]) == 5
    assert result_page1_limit5["page"] == 1
    assert result_page1_limit5["limit"] == 5
    assert result_page1_limit5["pages"] == 3 # 15 items / 5 per page = 3 pages

    # 2ページ目、limit=5
    skip2 = (2 - 1) * 5
    result_page2_limit5 = MechanismService.get_mechanisms(db_session, skip=skip2, limit=5)
    assert len(result_page2_limit5["items"]) == 5
    assert result_page2_limit5["page"] == 2

    # 3ページ目、limit=5
    skip3 = (3 - 1) * 5
    result_page3_limit5 = MechanismService.get_mechanisms(db_session, skip=skip3, limit=5)
    assert len(result_page3_limit5["items"]) == 5
    assert result_page3_limit5["page"] == 3
    
    # 存在しないページ
    skip4 = (4 - 1) * 5
    result_page4_limit5 = MechanismService.get_mechanisms(db_session, skip=skip4, limit=5)
    assert len(result_page4_limit5["items"]) == 0
    assert result_page4_limit5["page"] == 4
    assert result_page4_limit5["total"] == 15
    assert result_page4_limit5["pages"] == 3


def test_get_mechanism_by_id(db_session: Session, test_mechanism: Mechanism):
    """IDによるメカニズム取得のテスト"""
    mechanism = MechanismService.get_mechanism_by_id(db_session, test_mechanism.id)
    
    assert mechanism is not None
    assert mechanism.id == test_mechanism.id
    # フィクスチャが生成する実際の値と比較
    assert mechanism.title == test_mechanism.title 
    assert mechanism.description == test_mechanism.description
    assert mechanism.reliability == test_mechanism.reliability
    assert mechanism.file_path == test_mechanism.file_path
    assert mechanism.user_id == test_mechanism.user_id

def test_get_mechanism_by_id_not_found(db_session: Session):
    """存在しないIDによるメカニズム取得のテスト"""
    mechanism = MechanismService.get_mechanism_by_id(db_session, 999)
    assert mechanism is None

def test_get_likes_count(db_session: Session, test_mechanism: Mechanism, test_user): # test_like is not needed if we create like here
    """いいね数取得のテスト"""
    # この時点ではいいねは0のはず
    assert MechanismService.get_likes_count(db_session, test_mechanism.id) == 0
    
    # いいねを作成
    from backend.app.models.like import Like
    like = Like(user_id=test_user.id, mechanism_id=test_mechanism.id)
    db_session.add(like)
    db_session.commit()

    likes_count = MechanismService.get_likes_count(db_session, test_mechanism.id)
    assert likes_count == 1

def test_get_likes_count_no_likes(db_session: Session, test_mechanism: Mechanism): # test_like fixture is not used
    """いいねがない場合のいいね数取得のテスト"""
    # test_mechanismが作成された時点では、関連するLikeはないはず
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
    category_name = f"新しいカテゴリー_{time.time()}" # Ensure unique name
    categories = MechanismService.get_or_create_categories(db_session, [category_name])
    
    assert len(categories) == 1
    assert categories[0].name == category_name
    
    # データベースに保存されたことを確認
    db_category = db_session.query(Category).filter(Category.name == category_name).first()
    assert db_category is not None
    assert db_category.name == category_name

def test_get_or_create_categories_mixed(db_session: Session, test_category: Category):
    """既存と新規が混在するカテゴリー取得・作成のテスト"""
    new_category_name = f"新しいカテゴリー2_{time.time()}" # Ensure unique name
    categories = MechanismService.get_or_create_categories(db_session, [test_category.name, new_category_name])
    
    assert len(categories) == 2
    found_existing = any(cat.name == test_category.name and cat.id == test_category.id for cat in categories)
    found_new = any(cat.name == new_category_name for cat in categories)
    assert found_existing
    assert found_new


def test_get_or_create_categories_empty(db_session: Session):
    """空のカテゴリーリストのテスト"""
    categories = MechanismService.get_or_create_categories(db_session, [])
    assert len(categories) == 0

def test_get_or_create_categories_whitespace(db_session: Session):
    """空白のみのカテゴリー名のテスト"""
    categories = MechanismService.get_or_create_categories(db_session, ["  ", ""])
    assert len(categories) == 0

@patch('backend.app.services.mechanism.MechanismService.get_or_create_categories')
def test_create_mechanism_with_mock(mock_get_or_create_categories, db_session: Session, test_user):
    """メカニズム作成のテスト（get_or_create_categoriesをモック）"""
    # モックの設定
    mock_category_name = f"モックテストカテゴリー_{time.time()}"
    # Categoryオブジェクトを作成するが、IDはDB割り当てなのでNoneのまま
    mock_categories_returned = [Category(name=mock_category_name)] 
    mock_get_or_create_categories.return_value = mock_categories_returned
    
    # テストデータ
    mechanism_data = MechanismCreate(
        title=f"新しいメカニズム_{time.time()}", # Ensure unique title
        description="これは新しいメカニズムです",
        reliability=4,
        categories=[mock_category_name] # モックが返すカテゴリ名と一致させる
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
    mock_get_or_create_categories.assert_called_once_with(db_session, [mock_category_name])
    assert mechanism is not None
    assert mechanism.title == mechanism_data.title
    assert mechanism.description == mechanism_data.description
    assert mechanism.reliability == mechanism_data.reliability
    assert mechanism.file_path == "/test/new_file.pdf"
    assert mechanism.thumbnail_path == "/test/new_thumbnail.jpg"
    assert mechanism.user_id == test_user.id
    
    # モックが返したカテゴリが実際に設定されているか確認
    # 注意: mock_categories_returnedのCategoryオブジェクトはIDがないため、名前で比較
    assert len(mechanism.categories) == 1
    assert mechanism.categories[0].name == mock_category_name 
    
    # データベースに保存されたことを確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.id == mechanism.id).first()
    assert db_mechanism is not None
    assert db_mechanism.title == mechanism_data.title
    assert len(db_mechanism.categories) == 1
    assert db_mechanism.categories[0].name == mock_category_name


def test_create_mechanism_no_mock(db_session: Session, test_user):
    """メカニズム作成のテスト（get_or_create_categoriesをモックしない）"""
    category_name1 = f"実カテゴリー1_{time.time()}"
    category_name2 = f"実カテゴリー2_{time.time()}"
    
    # テストデータ
    mechanism_data = MechanismCreate(
        title=f"モックなしメカニズム_{time.time()}", # Ensure unique title
        description="これはモックなしの新しいメカニズムです",
        reliability=3,
        categories=[category_name1, category_name2]
    )
    
    # 関数を呼び出し
    mechanism = MechanismService.create_mechanism(
        db=db_session,
        mechanism=mechanism_data,
        user_id=test_user.id,
        file_path="/test/no_mock_file.pdf",
        thumbnail_path="/test/no_mock_thumbnail.jpg"
    )
    
    # アサーション
    assert mechanism is not None
    assert mechanism.title == mechanism_data.title
    assert mechanism.user_id == test_user.id
    
    # カテゴリーが正しく作成または取得され、関連付けられていることを確認
    assert len(mechanism.categories) == 2
    created_category_names = sorted([cat.name for cat in mechanism.categories])
    expected_category_names = sorted([category_name1, category_name2])
    assert created_category_names == expected_category_names
    
    # データベースからメカニズムを再取得して確認
    db_mechanism = db_session.query(Mechanism).filter(Mechanism.id == mechanism.id).first()
    assert db_mechanism is not None
    assert len(db_mechanism.categories) == 2
    db_category_names = sorted([cat.name for cat in db_mechanism.categories])
    assert db_category_names == expected_category_names

    # カテゴリーがデータベースに存在することを確認
    cat1_db = db_session.query(Category).filter(Category.name == category_name1).first()
    cat2_db = db_session.query(Category).filter(Category.name == category_name2).first()
    assert cat1_db is not None
    assert cat2_db is not None

def test_update_mechanism_success(db_session: Session, test_mechanism: Mechanism, test_user):
    """メカニズム編集成功のテスト（投稿者本人）"""
    # 更新データ
    update_data = MechanismUpdate(
        title="更新されたタイトル",
        description="更新された説明",
        reliability=5,
        categories=["更新カテゴリー1", "更新カテゴリー2"]
    )
    
    # メカニズムを更新（投稿者本人）
    updated_mechanism = MechanismService.update_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        mechanism_update=update_data,
        current_user_id=test_mechanism.user_id
    )
    
    # アサーション
    assert updated_mechanism is not None
    assert updated_mechanism.id == test_mechanism.id
    assert updated_mechanism.title == "更新されたタイトル"
    assert updated_mechanism.description == "更新された説明"
    assert updated_mechanism.reliability == 5
    assert len(updated_mechanism.categories) == 2
    
    # カテゴリー名を確認
    category_names = sorted([cat.name for cat in updated_mechanism.categories])
    assert category_names == ["更新カテゴリー1", "更新カテゴリー2"]

def test_update_mechanism_partial_update(db_session: Session, test_mechanism: Mechanism):
    """メカニズム部分編集のテスト"""
    original_title = test_mechanism.title
    original_description = test_mechanism.description
    
    # 一部のフィールドのみ更新
    update_data = MechanismUpdate(reliability=4)
    
    updated_mechanism = MechanismService.update_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        mechanism_update=update_data,
        current_user_id=test_mechanism.user_id
    )
    
    # アサーション
    assert updated_mechanism is not None
    assert updated_mechanism.title == original_title  # 変更されていない
    assert updated_mechanism.description == original_description  # 変更されていない
    assert updated_mechanism.reliability == 4  # 変更された

def test_update_mechanism_not_owner(db_session: Session, test_mechanism: Mechanism, test_user):
    """メカニズム編集失敗のテスト（投稿者以外）"""
    # 別のユーザーを作成
    from backend.app.models.user import User
    another_user = User(
        email=f"another_{time.time()}@example.com",
        password_hash="hashedpassword"
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)
    
    update_data = MechanismUpdate(title="不正な更新")
    
    # 投稿者以外のユーザーで更新を試行
    updated_mechanism = MechanismService.update_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        mechanism_update=update_data,
        current_user_id=another_user.id
    )
    
    # 更新は失敗すべき
    assert updated_mechanism is None

def test_update_mechanism_not_found(db_session: Session, test_user):
    """存在しないメカニズムの編集テスト"""
    update_data = MechanismUpdate(title="存在しないメカニズム")
    
    updated_mechanism = MechanismService.update_mechanism(
        db=db_session,
        mechanism_id=999,  # 存在しないID
        mechanism_update=update_data,
        current_user_id=test_user.id
    )
    
    # 更新は失敗すべき
    assert updated_mechanism is None

def test_update_mechanism_categories_only(db_session: Session, test_mechanism: Mechanism):
    """カテゴリーのみ更新のテスト"""
    original_title = test_mechanism.title
    
    update_data = MechanismUpdate(categories=["新カテゴリー"])
    
    updated_mechanism = MechanismService.update_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        mechanism_update=update_data,
        current_user_id=test_mechanism.user_id
    )
    
    # アサーション
    assert updated_mechanism is not None
    assert updated_mechanism.title == original_title  # 変更されていない
    assert len(updated_mechanism.categories) == 1
    assert updated_mechanism.categories[0].name == "新カテゴリー"

def test_delete_mechanism_success(db_session: Session, test_mechanism: Mechanism):
    """メカニズム削除成功のテスト（投稿者本人）"""
    mechanism_id = test_mechanism.id
    user_id = test_mechanism.user_id
    
    # メカニズムを削除（投稿者本人）
    success = MechanismService.delete_mechanism(
        db=db_session,
        mechanism_id=mechanism_id,
        current_user_id=user_id,
        is_admin=False
    )
    
    # 削除が成功することを確認
    assert success is True
    
    # データベースから削除されていることを確認
    deleted_mechanism = db_session.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
    assert deleted_mechanism is None

def test_delete_mechanism_not_owner(db_session: Session, test_mechanism: Mechanism):
    """メカニズム削除失敗のテスト（投稿者以外）"""
    # 別のユーザーを作成
    from backend.app.models.user import User
    another_user = User(
        email=f"another_{time.time()}@example.com",
        password_hash="hashedpassword"
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)
    
    # 投稿者以外のユーザーで削除を試行
    success = MechanismService.delete_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        current_user_id=another_user.id,
        is_admin=False
    )
    
    # 削除は失敗すべき
    assert success is False
    
    # メカニズムがまだ存在することを確認
    mechanism = db_session.query(Mechanism).filter(Mechanism.id == test_mechanism.id).first()
    assert mechanism is not None

def test_delete_mechanism_not_found(db_session: Session, test_user):
    """存在しないメカニズムの削除テスト"""
    success = MechanismService.delete_mechanism(
        db=db_session,
        mechanism_id=999,  # 存在しないID
        current_user_id=test_user.id,
        is_admin=False
    )
    
    # 削除は失敗すべき
    assert success is False

def test_delete_mechanism_admin_success(db_session: Session, test_mechanism: Mechanism):
    """admin権限でのメカニズム削除成功テスト"""
    # adminユーザーを作成
    from backend.app.models.user import User
    admin_user = User(
        email=f"admin_{time.time()}@example.com",
        password_hash="hashedpassword",
        is_admin=True
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    
    mechanism_id = test_mechanism.id
    
    # admin権限でメカニズムを削除（投稿者以外）
    success = MechanismService.delete_mechanism(
        db=db_session,
        mechanism_id=mechanism_id,
        current_user_id=admin_user.id,
        is_admin=True
    )
    
    # 削除が成功することを確認
    assert success is True
    
    # データベースから削除されていることを確認
    deleted_mechanism = db_session.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
    assert deleted_mechanism is None

def test_delete_mechanism_non_admin_failure(db_session: Session, test_mechanism: Mechanism):
    """非admin権限での他人のメカニズム削除失敗テスト"""
    # 一般ユーザーを作成
    from backend.app.models.user import User
    regular_user = User(
        email=f"regular_{time.time()}@example.com",
        password_hash="hashedpassword",
        is_admin=False
    )
    db_session.add(regular_user)
    db_session.commit()
    db_session.refresh(regular_user)
    
    # 一般ユーザーが他人のメカニズムを削除しようとする
    success = MechanismService.delete_mechanism(
        db=db_session,
        mechanism_id=test_mechanism.id,
        current_user_id=regular_user.id,
        is_admin=False
    )
    
    # 削除は失敗すべき
    assert success is False
    
    # メカニズムがまだ存在することを確認
    mechanism = db_session.query(Mechanism).filter(Mechanism.id == test_mechanism.id).first()
    assert mechanism is not None
