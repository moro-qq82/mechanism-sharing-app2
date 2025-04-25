# メカニズム共有プラットフォーム詳細設計書（MVP版）

## 1. システムアーキテクチャ

### 1.1 全体アーキテクチャ

```
+------------------+      +------------------+      +------------------+
|                  |      |                  |      |                  |
|  クライアント     |<---->|  APIサーバー     |<---->|  データベース    |
|  (React)         |      |  (FastAPI)      |      |  (PostgreSQL)    |
|                  |      |                  |      |                  |
+------------------+      +------------------+      +------------------+
                                   ^
                                   |
                                   v
                          +------------------+
                          |                  |
                          |  ストレージ      |
                          |  (ローカル)      |
                          |                  |
                          +------------------+
```

### 1.2 技術スタック

#### フロントエンド
- React: UIコンポーネントライブラリ
- TypeScript: 型安全な開発のための言語
- Tailwind CSS: スタイリングフレームワーク
- Axios: HTTP通信ライブラリ
- React Router: ルーティングライブラリ
- React Query: データフェッチングライブラリ

#### バックエンド
- Python: プログラミング言語
- FastAPI: Webフレームワーク
- SQLAlchemy: ORMライブラリ
- Pydantic: データバリデーションライブラリ
- JWT: 認証トークン
- Bcrypt: パスワードハッシュ化

#### データベース
- PostgreSQL: リレーショナルデータベース

#### インフラ
- ローカル開発環境（将来的にはAzureへ移行）

## 2. データベース設計

### 2.1 ER図

```
+---------------+       +---------------+       +---------------+
|    Users      |       |  Mechanisms   |       |    Likes      |
+---------------+       +---------------+       +---------------+
| id (PK)       |       | id (PK)       |       | id (PK)       |
| email         |       | title         |       | user_id (FK)  |
| password_hash |       | description   |       | mechanism_id  |
| created_at    |       | reliability   |       | created_at    |
| updated_at    |       | file_path     |       +---------------+
+---------------+       | thumbnail_path|
                        | user_id (FK)  |       +---------------+
                        | created_at    |       |  Categories   |
                        | updated_at    |       +---------------+
                        +---------------+       | id (PK)       |
                                |               | name          |
                                |               | created_at    |
                                v               +---------------+
                        +---------------+              ^
                        | MechanismCat  |              |
                        +---------------+              |
                        | mechanism_id  |--------------|
                        | category_id   |
                        +---------------+
```

### 2.2 テーブル定義

#### Usersテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | SERIAL | PRIMARY KEY | ユーザーID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | メールアドレス |
| password_hash | VARCHAR(255) | NOT NULL | ハッシュ化されたパスワード |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新日時 |

#### Mechanismsテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | SERIAL | PRIMARY KEY | メカニズムID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | NOT NULL | 説明文 |
| reliability | INTEGER | NOT NULL | 信頼性レベル（1-5） |
| file_path | VARCHAR(255) | NOT NULL | ファイルパス |
| thumbnail_path | VARCHAR(255) | NULL | サムネイルパス |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | 投稿ユーザーID |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新日時 |

#### Categoriesテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | SERIAL | PRIMARY KEY | カテゴリーID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | カテゴリー名 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |

#### MechanismCategoriesテーブル（中間テーブル）
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| mechanism_id | INTEGER | FOREIGN KEY, NOT NULL | メカニズムID |
| category_id | INTEGER | FOREIGN KEY, NOT NULL | カテゴリーID |
| PRIMARY KEY | | (mechanism_id, category_id) | 複合主キー |

#### Likesテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | SERIAL | PRIMARY KEY | いいねID |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | ユーザーID |
| mechanism_id | INTEGER | FOREIGN KEY, NOT NULL | メカニズムID |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |
| UNIQUE | | (user_id, mechanism_id) | 一人一回のいいね制約 |

## 3. API設計

### 3.1 認証API

#### ユーザー登録
- エンドポイント: `/api/auth/register`
- メソッド: POST
- リクエストボディ:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- レスポンス:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2025-04-25T14:30:00Z"
  }
  ```

#### ログイン
- エンドポイント: `/api/auth/login`
- メソッド: POST
- リクエストボディ:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- レスポンス:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "user@example.com"
    }
  }
  ```

### 3.2 メカニズムAPI

#### メカニズム一覧取得
- エンドポイント: `/api/mechanisms`
- メソッド: GET
- クエリパラメータ:
  - `page`: ページ番号（デフォルト: 1）
  - `limit`: 1ページあたりの件数（デフォルト: 10）
- レスポンス:
  ```json
  {
    "items": [
      {
        "id": 1,
        "title": "サンプルメカニズム",
        "description": "これはサンプルメカニズムです",
        "reliability": 3,
        "thumbnail_path": "/thumbnails/sample.jpg",
        "user": {
          "id": 1,
          "email": "user@example.com"
        },
        "categories": ["機械", "電子"],
        "likes_count": 5,
        "created_at": "2025-04-25T14:30:00Z"
      },
      ...
    ],
    "total": 100,
    "page": 1,
    "limit": 10,
    "pages": 10
  }
  ```

#### メカニズム詳細取得
- エンドポイント: `/api/mechanisms/{mechanism_id}`
- メソッド: GET
- レスポンス:
  ```json
  {
    "id": 1,
    "title": "サンプルメカニズム",
    "description": "これはサンプルメカニズムです",
    "reliability": 3,
    "file_path": "/files/sample.pdf",
    "thumbnail_path": "/thumbnails/sample.jpg",
    "user": {
      "id": 1,
      "email": "user@example.com"
    },
    "categories": ["機械", "電子"],
    "likes_count": 5,
    "created_at": "2025-04-25T14:30:00Z",
    "updated_at": "2025-04-25T14:30:00Z"
  }
  ```

#### メカニズム投稿
- エンドポイント: `/api/mechanisms`
- メソッド: POST
- 認証: 必須
- リクエスト: multipart/form-data
  - `title`: タイトル
  - `description`: 説明文
  - `reliability`: 信頼性レベル（1-5）
  - `categories`: カテゴリー（カンマ区切り）
  - `file`: アップロードファイル
  - `thumbnail`: サムネイル画像（オプション）
- レスポンス:
  ```json
  {
    "id": 1,
    "title": "新規メカニズム",
    "description": "これは新規メカニズムです",
    "reliability": 3,
    "file_path": "/files/new.pdf",
    "thumbnail_path": "/thumbnails/new.jpg",
    "user_id": 1,
    "categories": ["機械", "電子"],
    "created_at": "2025-04-25T14:30:00Z",
    "updated_at": "2025-04-25T14:30:00Z"
  }
  ```

### 3.3 カテゴリーAPI

#### カテゴリー一覧取得
- エンドポイント: `/api/categories`
- メソッド: GET
- レスポンス:
  ```json
  [
    {
      "id": 1,
      "name": "機械"
    },
    {
      "id": 2,
      "name": "電子"
    },
    ...
  ]
  ```

### 3.4 いいねAPI

#### いいね追加
- エンドポイント: `/api/mechanisms/{mechanism_id}/like`
- メソッド: POST
- 認証: 必須
- レスポンス:
  ```json
  {
    "mechanism_id": 1,
    "likes_count": 6
  }
  ```

#### いいね削除
- エンドポイント: `/api/mechanisms/{mechanism_id}/like`
- メソッド: DELETE
- 認証: 必須
- レスポンス:
  ```json
  {
    "mechanism_id": 1,
    "likes_count": 5
  }
  ```

## 4. 画面設計

### 4.1 画面一覧

| 画面名 | URL | 説明 |
|-------|-----|------|
| ログイン画面 | /login | ユーザーログイン |
| 新規登録画面 | /register | ユーザー新規登録 |
| メカニズム一覧画面 | / | メカニズム一覧表示 |
| メカニズム詳細画面 | /mechanisms/{id} | メカニズム詳細表示 |
| メカニズム投稿画面 | /mechanisms/new | 新規メカニズム投稿 |

### 4.2 画面遷移図

```
+---------------+     +---------------+
|  ログイン画面  |<--->| 新規登録画面  |
+---------------+     +---------------+
        |
        v
+---------------+     +---------------+     +---------------+
|  メカニズム   |---->|  メカニズム   |<----|  メカニズム   |
|  一覧画面     |     |  詳細画面     |     |  投稿画面     |
+---------------+     +---------------+     +---------------+
```

### 4.3 各画面の詳細

#### 4.3.1 ログイン画面
- コンポーネント:
  - メールアドレス入力フィールド
  - パスワード入力フィールド
  - ログインボタン
  - 新規登録リンク

#### 4.3.2 新規登録画面
- コンポーネント:
  - メールアドレス入力フィールド
  - パスワード入力フィールド
  - パスワード確認入力フィールド
  - 登録ボタン
  - ログインリンク

#### 4.3.3 メカニズム一覧画面
- コンポーネント:
  - ヘッダー（ログイン状態、新規投稿ボタン）
  - メカニズムカードリスト
    - サムネイル
    - タイトル
    - 信頼性レベル表示
    - カテゴリータグ
    - いいね数
  - メカニズム詳細サムネイル
  - ページネーション

#### 4.3.4 メカニズム詳細画面
- コンポーネント:
  - ヘッダー
  - メカニズム情報
    - タイトル
    - 説明文
    - 信頼性レベル表示
    - カテゴリータグ
    - 投稿者情報
    - 投稿日時
  - ファイルビューア/ダウンロードリンク
  - いいねボタン
  - いいね数表示

#### 4.3.5 メカニズム投稿画面
- コンポーネント:
  - ヘッダー
  - 投稿フォーム
    - タイトル入力フィールド
    - 説明文入力エリア
    - 信頼性レベル選択
    - カテゴリー入力（複数選択可能）
    - ファイルアップロード
    - サムネイルアップロード
  - 投稿ボタン
  - キャンセルボタン

## 5. コンポーネント設計

### 5.1 フロントエンドコンポーネント構成

```
src/
├── components/
│   ├── common/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── TextArea.tsx
│   │   ├── Select.tsx
│   │   ├── FileUpload.tsx
│   │   ├── Pagination.tsx
│   │   └── Loading.tsx
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── mechanism/
│   │   ├── MechanismCard.tsx
│   │   ├── MechanismList.tsx
│   │   ├── MechanismDetail.tsx
│   │   ├── MechanismForm.tsx
│   │   ├── ReliabilityBadge.tsx
│   │   ├── CategoryTag.tsx
│   │   └── LikeButton.tsx
│   └── layout/
│       └── MainLayout.tsx
├── pages/
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── MechanismListPage.tsx
│   ├── MechanismDetailPage.tsx
│   └── MechanismNewPage.tsx
├── services/
│   ├── api.ts
│   ├── auth.ts
│   ├── mechanism.ts
│   └── category.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useMechanisms.ts
│   └── useCategories.ts
├── contexts/
│   └── AuthContext.tsx
├── types/
│   ├── User.ts
│   ├── Mechanism.ts
│   └── Category.ts
├── utils/
│   ├── formatDate.ts
│   └── fileHelpers.ts
├── App.tsx
└── index.tsx
```

### 5.2 バックエンドコンポーネント構成

```
app/
├── main.py
├── config.py
├── database.py
├── models/
│   ├── user.py
│   ├── mechanism.py
│   ├── category.py
│   └── like.py
├── schemas/
│   ├── user.py
│   ├── mechanism.py
│   ├── category.py
│   └── like.py
├── routers/
│   ├── auth.py
│   ├── mechanism.py
│   ├── category.py
│   └── like.py
├── services/
│   ├── auth.py
│   ├── mechanism.py
│   ├── category.py
│   └── file.py
├── middlewares/
│   └── auth.py
└── utils/
    ├── security.py
    └── pagination.py
```

## 6. セキュリティ設計

### 6.1 認証・認可

- JWT（JSON Web Token）を使用した認証
- パスワードはbcryptでハッシュ化して保存
- 認証が必要なAPIエンドポイントにはミドルウェアで保護

### 6.2 XSS対策

- Reactの仕組みによるエスケープ処理
- Content-Security-Policy（CSP）ヘッダーの設定

### 6.3 CSRF対策

- SameSite属性付きのCookieを使用
- Double Submit Cookie パターンの実装

### 6.4 その他のセキュリティ対策

- HTTPS通信の強制
- 適切なHTTPヘッダーの設定
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block

## 7. デプロイメント設計

### 7.1 開発環境

- ローカル環境での開発
  - フロントエンド: npm start (localhost:3000)
  - バックエンド: uvicorn main:app --reload (localhost:8000)
  - データベース: ローカルPostgreSQL

### 7.2 本番環境（将来的）

- Azure App Service
- Azure Database for PostgreSQL
- Azure Blob Storage（ファイル保存用）

## 8. テスト計画

### 8.1 単体テスト

- フロントエンド: Jest + React Testing Library
- バックエンド: pytest

### 8.2 統合テスト

- APIエンドポイントのテスト
- フロントエンド・バックエンド連携テスト

### 8.3 E2Eテスト

- Cypress を使用したE2Eテスト

## 9. 実装スケジュール

### フェーズ1: 基盤構築（2週間）
- プロジェクト設定
- データベース設計・構築
- 認証システム実装

### フェーズ2: コア機能実装（3週間）
- メカニズム投稿機能
- メカニズム表示機能
- いいね機能

### フェーズ3: UI/UX改善（2週間）
- デザイン調整
- レスポンシブ対応
- パフォーマンス最適化

### フェーズ4: テスト・デバッグ（1週間）
- 単体テスト
- 統合テスト
- バグ修正

## 10. 今後の拡張計画

MVPリリース後、以下の機能を順次実装予定：

1. LDAP認証
2. プロフィール管理機能の拡充
3. ソート・フィルター機能
4. コメント機能
5. ダウンロード機能
6. シェア機能
7. 閲覧数の計測・表示
8. 時系列データの可視化
9. バックアップ体制の構築
