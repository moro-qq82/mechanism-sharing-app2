# データベース設計図

## ER図

```mermaid
erDiagram
    USERS {
        int id PK
        string email
        string password_hash
        datetime created_at
        datetime updated_at
    }
    
    MECHANISMS {
        int id PK
        string title
        text description
        int reliability
        string file_path
        string thumbnail_path
        int user_id FK
        datetime created_at
        datetime updated_at
    }
    
    CATEGORIES {
        int id PK
        string name
        datetime created_at
    }
    
    LIKES {
        int id PK
        int user_id FK
        int mechanism_id FK
        datetime created_at
    }
    
    MECHANISM_CATEGORIES {
        int mechanism_id PK,FK
        int category_id PK,FK
    }
    
    USERS ||--o{ MECHANISMS : "creates"
    USERS ||--o{ LIKES : "gives"
    MECHANISMS ||--o{ LIKES : "receives"
    MECHANISMS ||--o{ MECHANISM_CATEGORIES : "has"
    CATEGORIES ||--o{ MECHANISM_CATEGORIES : "belongs to"
```

## テーブル定義

### users テーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | Integer | PK, index | ユーザーID |
| email | String | unique, index, not null | メールアドレス |
| password_hash | String | not null | パスワードハッシュ |
| created_at | DateTime | not null, default=now() | 作成日時 |
| updated_at | DateTime | not null, default=now(), onupdate=now() | 更新日時 |

### mechanisms テーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | Integer | PK, index | メカニズムID |
| title | String | not null | タイトル |
| description | Text | not null | 説明 |
| reliability | Integer | not null | 信頼性レベル (1-5) |
| file_path | String | not null | ファイルパス |
| thumbnail_path | String | nullable | サムネイルパス |
| user_id | Integer | FK(users.id), not null | 投稿者ID |
| created_at | DateTime | not null, default=now() | 作成日時 |
| updated_at | DateTime | not null, default=now(), onupdate=now() | 更新日時 |

### categories テーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | Integer | PK, index | カテゴリーID |
| name | String | unique, not null | カテゴリー名 |
| created_at | DateTime | not null, default=now() | 作成日時 |

### likes テーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | Integer | PK, index | いいねID |
| user_id | Integer | FK(users.id), not null | ユーザーID |
| mechanism_id | Integer | FK(mechanisms.id), not null | メカニズムID |
| created_at | DateTime | not null, default=now() | 作成日時 |

**ユニーク制約**: (user_id, mechanism_id) - 一人のユーザーが同じメカニズムに複数回いいねできないようにする制約

### mechanism_categories テーブル (中間テーブル)
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| mechanism_id | Integer | PK, FK(mechanisms.id) | メカニズムID |
| category_id | Integer | PK, FK(categories.id) | カテゴリーID |

## リレーションシップ

- User (1) - (0..*) Mechanism: ユーザーは複数のメカニズムを投稿できる
- User (1) - (0..*) Like: ユーザーは複数のいいねを付けられる
- Mechanism (1) - (0..*) Like: メカニズムは複数のいいねを受け取れる
- Mechanism (0..*) - (0..*) Category: メカニズムと複数のカテゴリーは多対多の関係
