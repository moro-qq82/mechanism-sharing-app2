# フロントエンド設計図

## コンポーネント構造図

```mermaid
classDiagram
    class App {
        +render()
    }
    
    class LoginPage {
        +render()
    }
    
    class RegisterPage {
        +render()
    }
    
    class MechanismListPage {
        +render()
    }
    
    class MechanismDetailPage {
        -mechanism: Object
        +render()
    }
    
    class MechanismNewPage {
        +render()
    }
    
    class ReliabilityUtils {
        +getReliabilityLabel(level: number): string
        +getReliabilityColorClass(level: number): string
    }
    
    App --> LoginPage
    App --> RegisterPage
    App --> MechanismListPage
    App --> MechanismDetailPage
    App --> MechanismNewPage
    MechanismDetailPage --> ReliabilityUtils
```

## ページコンポーネント

### App
- メインのアプリケーションコンポーネント
- React Routerを使用してルーティングを管理
- 各ページへのルートを定義

### LoginPage
- ユーザーログイン機能を提供
- メールアドレスとパスワードによる認証

### RegisterPage
- 新規ユーザー登録機能を提供
- メールアドレスとパスワードによるアカウント作成

### MechanismListPage
- メカニズム一覧を表示
- フィルタリングやソート機能を提供（予定）

### MechanismDetailPage
- 特定のメカニズムの詳細情報を表示
- メカニズムのタイトル、説明、信頼性、カテゴリー、ファイル情報などを表示
- いいね機能を提供

### MechanismNewPage
- 新しいメカニズムを投稿するためのフォームを提供
- タイトル、説明、信頼性レベル、カテゴリー、ファイルのアップロード機能

## ユーティリティ

### ReliabilityUtils
- 信頼性レベルに関する機能を提供
- 信頼性レベルを数値から文字列に変換する関数
- 信頼性レベルに応じた背景色とテキスト色のクラス名を返す関数

## コンポーネントディレクトリ構造

```
frontend/src/
├── components/
│   ├── auth/         # 認証関連コンポーネント
│   ├── common/       # 共通コンポーネント
│   ├── layout/       # レイアウト関連コンポーネント
│   └── mechanism/    # メカニズム関連コンポーネント
├── contexts/         # Reactコンテキスト
├── hooks/            # カスタムフック
├── pages/            # ページコンポーネント
├── services/         # APIサービス
├── types/            # 型定義
└── utils/            # ユーティリティ関数
```

## データフロー

1. ユーザーがアプリケーションにアクセス
2. App.tsxがルーティングを処理し、適切なページコンポーネントをレンダリング
3. ページコンポーネントが必要に応じてAPIサービスを使用してバックエンドからデータを取得
4. 取得したデータをコンポーネントの状態として保存し、UIをレンダリング
5. ユーザーのアクションに応じて、APIサービスを通じてバックエンドにデータを送信

## 認証フロー

1. ユーザーがLoginPageまたはRegisterPageでフォームを送信
2. APIサービスがバックエンドに認証リクエストを送信
3. 認証成功時、トークンをローカルストレージに保存
4. 認証が必要なページでは、トークンを使用してAPIリクエストを認証
