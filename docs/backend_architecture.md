# バックエンド設計図

## アーキテクチャ図

```mermaid
classDiagram
    class Database {
        +Base
        +engine
        +SessionLocal
        +get_db()
    }
    
    class User {
        +id: Integer
        +email: String
        +password_hash: String
        +created_at: DateTime
        +updated_at: DateTime
        +mechanisms: Relationship
        +likes: Relationship
        +mechanism_views: Relationship
    }
    
    class Mechanism {
        +id: Integer
        +title: String
        +description: Text
        +reliability: Integer
        +file_path: String
        +thumbnail_path: String
        +user_id: Integer
        +created_at: DateTime
        +updated_at: DateTime
        +user: Relationship
        +categories: Relationship
        +likes: Relationship
        +views: Relationship
    }
    
    class Category {
        +id: Integer
        +name: String
        +created_at: DateTime
        +mechanisms: Relationship
    }
    
    class Like {
        +id: Integer
        +user_id: Integer
        +mechanism_id: Integer
        +created_at: DateTime
        +user: Relationship
        +mechanism: Relationship
    }
    
    class MechanismView {
        +id: Integer
        +mechanism_id: Integer
        +user_id: Integer
        +viewed_at: DateTime
        +user: Relationship
        +mechanism: Relationship
    }
    
    class UserSchema {
        +UserCreate
        +UserResponse
        +UserLogin
        +Token
        +TokenData
    }
    
    class MechanismSchema {
        +MechanismCreate
        +MechanismListResponse
        +MechanismDetailResponse
        +PaginatedMechanismResponse
    }
    
    class CategorySchema {
        +CategoryCreate
        +CategoryResponse
        +CategoryListResponse
    }
    
    class LikeSchema {
        +LikeResponse
    }
    
    class MechanismViewSchema {
        +MechanismViewBase
        +MechanismViewCreate
        +MechanismViewResponse
        +MechanismViewCount
        +MechanismViewsResponse
    }
    
    Database --> User
    Database --> Mechanism
    Database --> Category
    Database --> Like
    Database --> MechanismView
    
    User --> UserSchema
    Mechanism --> MechanismSchema
    Category --> CategorySchema
    Like --> LikeSchema
    MechanismView --> MechanismViewSchema
```

## アプリケーション構造

```
backend/
├── app/
│   ├── models/           # SQLAlchemyモデル
│   │   ├── user.py
│   │   ├── mechanism.py
│   │   ├── category.py
│   │   ├── like.py
│   │   └── mechanism_view.py
│   ├── schemas/          # Pydanticスキーマ
│   │   ├── user.py
│   │   ├── mechanism.py
│   │   ├── category.py
│   │   ├── like.py
│   │   └── mechanism_view.py
│   ├── routers/          # APIエンドポイント
│   │   ├── auth.py
│   │   ├── mechanism.py
│   │   ├── category.py
│   │   ├── like.py
│   │   └── mechanism_view.py
│   ├── services/         # ビジネスロジック
│   │   ├── auth.py
│   │   ├── mechanism.py
│   │   ├── category.py
│   │   ├── like.py
│   │   └── mechanism_view.py
│   ├── middlewares/      # ミドルウェア
│   │   └── auth.py
│   ├── utils/            # ユーティリティ関数
│   │   └── security.py
│   ├── database.py       # データベース設定
│   ├── config.py         # アプリケーション設定
│   └── main.py           # アプリケーションエントリーポイント
└── tests/                # テスト
    ├── test_auth.py
    ├── test_mechanism.py
    ├── test_category.py
    ├── test_like.py
    ├── test_mechanism_view.py
    └── test_mechanism_view_api.py
```

## データベースモデル

### User
- ユーザー情報を管理するモデル
- メールアドレスとパスワードハッシュを保存
- メカニズム、いいね、閲覧履歴への関連を持つ

### Mechanism
- メカニズム情報を管理するモデル
- タイトル、説明、信頼性レベル、ファイルパスなどを保存
- ユーザー、カテゴリー、いいね、閲覧履歴への関連を持つ

### Category
- カテゴリー情報を管理するモデル
- カテゴリー名を保存
- メカニズムへの関連を持つ

### Like
- いいね情報を管理するモデル
- ユーザーとメカニズムの関連を保存
- 一人のユーザーが同じメカニズムに複数回いいねできないようにユニーク制約を持つ

### MechanismView
- メカニズム閲覧履歴を管理するモデル
- メカニズムIDとユーザーID（匿名ユーザーの場合はNULL）を保存
- 閲覧日時を記録

## Pydanticスキーマ

### UserSchema
- UserCreate: ユーザー作成用スキーマ
- UserResponse: ユーザー情報表示用スキーマ
- UserLogin: ユーザー認証用スキーマ
- Token: トークン用スキーマ
- TokenData: トークンデータ用スキーマ

### MechanismSchema
- MechanismCreate: メカニズム作成用スキーマ
- MechanismListResponse: メカニズム一覧表示用スキーマ
- MechanismDetailResponse: メカニズム詳細表示用スキーマ
- PaginatedMechanismResponse: ページネーション用スキーマ

### CategorySchema
- CategoryCreate: カテゴリー作成用スキーマ
- CategoryResponse: カテゴリー情報表示用スキーマ
- CategoryListResponse: カテゴリー一覧表示用スキーマ

### LikeSchema
- LikeResponse: いいね情報表示用スキーマ

### MechanismViewSchema
- MechanismViewBase: メカニズム閲覧履歴の基本スキーマ
- MechanismViewCreate: メカニズム閲覧履歴作成用スキーマ
- MechanismViewResponse: メカニズム閲覧履歴レスポンス用スキーマ
- MechanismViewCount: メカニズム閲覧回数レスポンス用スキーマ
- MechanismViewsResponse: 複数メカニズムの閲覧回数レスポンス用スキーマ

## データフロー

1. クライアントからのリクエストがAPIエンドポイント（routers）に到達
2. ルーターがリクエストを適切なサービス（services）に転送
3. サービスがビジネスロジックを実行し、必要に応じてデータベースにアクセス
4. データベースからの結果をPydanticスキーマに変換して返却
5. レスポンスがクライアントに返される

## 認証フロー

1. ユーザーがログインリクエストを送信
2. パスワードが検証され、正しい場合はJWTトークンが生成
3. トークンがクライアントに返され、以降のリクエストに使用される
4. 保護されたエンドポイントでは、リクエストヘッダーからトークンを取得して検証
5. トークンが有効な場合、リクエストが処理される

## メカニズム閲覧回数記録フロー

1. ユーザーがメカニズム詳細画面にアクセス
2. フロントエンドがメカニズム詳細取得APIを呼び出し
3. メカニズム詳細取得後、閲覧履歴記録APIを呼び出し
4. バックエンドがユーザーID（匿名ユーザーの場合はNULL）とメカニズムIDを保存
5. 閲覧回数取得APIを呼び出して総閲覧回数とユーザー個人の閲覧回数を取得
6. フロントエンドが閲覧回数を表示
