from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
import os
import shutil
from fastapi import UploadFile
import uuid

from backend.app.models.mechanism import Mechanism
from backend.app.models.category import Category
from backend.app.models.like import Like
from backend.app.schemas.mechanism import MechanismCreate, MechanismUpdate

class MechanismService:
    """
    メカニズム関連のビジネスロジックを提供するサービスクラス
    """

    @staticmethod
    def get_mechanisms(db: Session, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        メカニズム一覧を取得する

        Args:
            db: データベースセッション
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            メカニズムのリストとページネーション情報を含む辞書
        """
        # 総件数を取得
        total = db.query(func.count(Mechanism.id)).scalar()
        
        # メカニズムを取得
        mechanisms = db.query(Mechanism).order_by(Mechanism.created_at.desc()).offset(skip).limit(limit).all()
        
        # ページ数を計算
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        # 現在のページを計算
        page = skip // limit + 1 if limit > 0 else 1
        
        return {
            "items": mechanisms,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }

    @staticmethod
    def get_mechanism_by_id(db: Session, mechanism_id: int) -> Optional[Mechanism]:
        """
        IDによりメカニズムを取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            メカニズムオブジェクト、存在しない場合はNone
        """
        return db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()

    @staticmethod
    def get_likes_count(db: Session, mechanism_id: int) -> int:
        """
        メカニズムのいいね数を取得する

        Args:
            db: データベースセッション
            mechanism_id: メカニズムID

        Returns:
            いいね数
        """
        return db.query(func.count(Like.id)).filter(Like.mechanism_id == mechanism_id).scalar()

    @staticmethod
    def save_upload_file(upload_file: UploadFile, folder: str) -> str:
        """
        アップロードされたファイルを保存する

        Args:
            upload_file: アップロードされたファイル
            folder: 保存先フォルダ

        Returns:
            保存されたファイルのパス
        """
        # 保存先フォルダが存在しない場合は作成
        os.makedirs(folder, exist_ok=True)
        
        # ファイル名を一意にするためにUUIDを使用
        file_extension = os.path.splitext(upload_file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(folder, file_name)
        
        # ファイルを保存
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        return file_path

    @staticmethod
    def get_or_create_categories(db: Session, category_names: List[str]) -> List[Category]:
        """
        カテゴリー名のリストから、既存のカテゴリーを取得または新規作成する

        Args:
            db: データベースセッション
            category_names: カテゴリー名のリスト

        Returns:
            カテゴリーオブジェクトのリスト
        """
        categories = []
        for name in category_names:
            # 空文字列やNoneの場合はスキップ
            if not name or not name.strip():
                continue
                
            # カテゴリー名を正規化
            name = name.strip()
            
            # 既存のカテゴリーを検索
            category = db.query(Category).filter(Category.name == name).first()
            
            # 存在しない場合は新規作成
            if not category:
                category = Category(name=name)
                db.add(category)
                db.commit()
                db.refresh(category)
            
            categories.append(category)
        
        return categories

    @staticmethod
    def create_mechanism(
        db: Session, 
        mechanism: MechanismCreate, 
        user_id: int,
        file_path: str,
        thumbnail_path: Optional[str] = None
    ) -> Mechanism:
        """
        新しいメカニズムを作成する

        Args:
            db: データベースセッション
            mechanism: 作成するメカニズムのデータ
            user_id: 投稿ユーザーID
            file_path: 保存されたファイルのパス
            thumbnail_path: 保存されたサムネイルのパス（オプション）

        Returns:
            作成されたメカニズムオブジェクト
        """
        # カテゴリーを取得または作成
        categories = MechanismService.get_or_create_categories(db, mechanism.categories)
        
        # メカニズムを作成
        db_mechanism = Mechanism(
            title=mechanism.title,
            description=mechanism.description,
            reliability=mechanism.reliability,
            file_path=file_path,
            thumbnail_path=thumbnail_path,
            user_id=user_id
        )
        
        # カテゴリーを関連付け
        db_mechanism.categories = categories
        
        # データベースに保存
        db.add(db_mechanism)
        db.commit()
        db.refresh(db_mechanism)
        
        return db_mechanism

    @staticmethod
    def update_mechanism(
        db: Session,
        mechanism_id: int,
        mechanism_update: MechanismUpdate,
        current_user_id: int
    ) -> Optional[Mechanism]:
        """
        メカニズムを更新する

        Args:
            db: データベースセッション
            mechanism_id: 更新するメカニズムのID
            mechanism_update: 更新データ
            current_user_id: 現在のユーザーID

        Returns:
            更新されたメカニズムオブジェクト、権限がない場合やメカニズムが存在しない場合はNone
        """
        # メカニズムを取得
        mechanism = db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
        if not mechanism:
            return None
        
        # 投稿者本人かどうかを確認
        if mechanism.user_id != current_user_id:
            return None
        
        # 更新可能なフィールドのみ更新
        update_data = mechanism_update.model_dump(exclude_unset=True)
        
        # カテゴリーが指定されている場合は個別に処理
        if 'categories' in update_data:
            categories = MechanismService.get_or_create_categories(db, update_data['categories'])
            mechanism.categories = categories
            del update_data['categories']
        
        # その他のフィールドを更新
        for field, value in update_data.items():
            setattr(mechanism, field, value)
        
        db.commit()
        db.refresh(mechanism)
        
        return mechanism

    @staticmethod
    def delete_mechanism(
        db: Session,
        mechanism_id: int,
        current_user_id: int,
        is_admin: bool = False
    ) -> bool:
        """
        メカニズムを削除する

        Args:
            db: データベースセッション
            mechanism_id: 削除するメカニズムのID
            current_user_id: 現在のユーザーID
            is_admin: 現在のユーザーがadminかどうか

        Returns:
            削除成功の場合True、権限がない場合やメカニズムが存在しない場合はFalse
        """
        # メカニズムを取得
        mechanism = db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()
        if not mechanism:
            return False
        
        # 投稿者本人またはadminかどうかを確認
        if mechanism.user_id != current_user_id and not is_admin:
            return False
        
        # メカニズムを削除（関連データも自動削除される）
        db.delete(mechanism)
        db.commit()
        
        return True
