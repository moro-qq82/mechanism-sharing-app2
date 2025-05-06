# メカニズム共有プラットフォーム

物理的なメカニズムを可視化して共有し、ユーザー間でインタラクションを行うためのWebアプリケーションです。

## プロジェクト概要

このプラットフォームでは、ユーザーが様々な物理的メカニズムに関する情報を投稿・共有し、他のユーザーと知識を交換することができます。各メカニズムには信頼性レベルが設定され、「妄想モデル」（理論的な仮説段階）から「教科書に記載」（学術的に確立）まで、5段階の信頼性レベルでメカニズムを区別することができます。

### 主要機能

- ユーザー登録・認証
- メカニズムの投稿・閲覧
- カテゴリーによる分類
- 信頼性レベルの設定
- いいね機能によるインタラクション

## 技術スタック

### フロントエンド
- React 19
- TypeScript
- Tailwind CSS
- React Router
- React Query
- Axios

### バックエンド
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- JWT認証
- Bcrypt（パスワードハッシュ化）

### データベース
- PostgreSQL

## 開発環境のセットアップ

### 前提条件
- Node.js 18以上
- Python 3.10以上
- PostgreSQL 14以上

### バックエンドのセットアップ

1. リポジトリをクローン
   ```
   git clone <repository-url>
   cd mechanism_sharing_app
   ```

2. 仮想環境を作成して有効化
   ```
   python -m venv venv
   # Windowsの場合
   venv\Scripts\activate
   # macOS/Linuxの場合
   source venv/bin/activate
   ```

3. 依存関係をインストール
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. PostgreSQLデータベースを作成
   ```
   createdb mechanism_db
   ```

5. ルートディレクトリで開発サーバーを起動
   ```
   cd ..
   uvicorn backend.app.main:app --reload
   ```

### フロントエンドのセットアップ

1. 依存関係をインストール
   ```
   cd frontend
   npm install
   ```

2. 開発サーバーを起動
   ```
   npm start
   ```

## 使用方法

1. ブラウザで以下のURLにアクセス
   - フロントエンド: http://localhost:3000
   - バックエンドAPI: http://localhost:8000
   - Swagger UI（API ドキュメント）: http://localhost:8000/docs

2. アカウントを作成してログイン

3. メカニズムの閲覧・投稿・評価を行う

## プロジェクト構造

詳細なプロジェクト構造については、[docs/context.md](docs/context.md)を参照してください。

## 開発ステータス

現在、このプロジェクトはMVP（Minimum Viable Product）開発フェーズにあります。基本的なプロジェクト構造とデータモデルが整備されており、APIエンドポイントの実装とフロントエンドの機能実装を進めている段階です。

詳細な開発計画については、[mvp-development-plan.md](mvp-development-plan.md)を参照してください。

## ドキュメント

- [要件定義書](requirements-doc.md)
- [詳細設計書](detailed-design-doc.md)
- [MVP開発計画](mvp-development-plan.md)
- [開発コンテキスト](docs/context.md)
- [変更履歴](docs/CHANGELOG.md)
- [課題リスト](issues_notes.md)

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
