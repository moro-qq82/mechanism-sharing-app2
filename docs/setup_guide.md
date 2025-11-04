# 別環境での立ち上げ手順

このドキュメントでは、プロジェクトを新しいマシンやクラウド環境で再現する際の流れをまとめます。リポジトリに含まれる `scripts/bootstrap.sh` は、依存関係の種類や必要になりそうなコマンドを自動で提案する補助ツールです。まずはスクリプトを実行し、結果を基に各ステップを進めてください。

## 前提ツール

- Git 2.40 以上
- Node.js 18 以上（`package.json` が存在する場合）
- npm / pnpm / yarn / bun のいずれか（リポジトリのロックファイルに従う）
- Python 3.10 以上（`pyproject.toml` や `requirements.txt` を検出した場合）
- Docker (Compose plugin を含む) — `docker-compose.yml` または `compose.yaml` が存在する場合
- `jq`（`package.json` からスクリプト名を自動抽出するため。未導入でもスクリプトは動作し、手動確認のメッセージが表示されます）

## セットアップフロー

1. **リポジトリの取得**
   ```bash
   git clone <repository-url>
   cd mechanism-sharing-app2
   ```

2. **補助スクリプトの実行**
   ```bash
   ./scripts/bootstrap.sh
   ```
   - スクリプトは `.env` ファイルの有無、Node.js/Python の依存関係、Docker コンポーズ、マイグレーション、テストコマンドの候補などを表示します。
   - ここで表示されたコマンドを順番にこなすのが最短経路です。

3. **環境変数の準備**
   - `.env.example` や `.env.local` が検出された場合は、案内に従って `.env` を作成します。
   - どの値が必要かわからない場合は、アプリの README や環境変数を参照するソースコードを確認してください。

4. **依存関係のインストール**
   - Node.js プロジェクトなら、ロックファイルに合わせて `pnpm install` / `yarn install` / `npm ci` などを実行します。
   - Python プロジェクトなら、`poetry install` / `pipenv install` / `python3 -m venv .venv && pip install -r requirements.txt` のような案内が出ます。
   - Docker コンテナが案内された場合、`docker compose up --build` もしくは `docker-compose up --build` を利用します。

5. **データベースやマイグレーション**
   - `prisma/schema.prisma` を検出した場合は `pnpm prisma migrate deploy` などのコマンドが提示されます。
   - `migrations/` ディレクトリがある場合は、採用フレームワーク（Django, Rails, etc.）のマイグレーション手順に従ってください。

6. **アプリケーションの起動**
   - `package.json` 内に `dev` スクリプトがあれば `npm run dev` などで開発サーバーが起動できます。
   - Docker を使う場合は、Compose で立ち上げた後にログを確認し、サービスが正しく稼働しているか確認してください。

7. **テストの実行**
   - Node.js の場合、`scripts.bootstrap.sh` が `pnpm test` や `npm test` などを案内します。
   - Python の場合、`pytest` ディレクトリを検知すると `pytest` の実行を促します。
   - その他のテストがある場合は `Makefile` や CI 設定ファイルを参照してください。

## トラブルシューティング

- **jq がないと言われる**: `sudo apt-get install jq` や `brew install jq` などで導入するか、`package.json` をテキストエディタで開いて `scripts` の内容を確認してください。
- **pnpm や yarn がないと言われる**: `npm install -g pnpm` / `npm install -g yarn` のように npm 経由で導入するのが簡単です。
- **Docker Compose のコマンドが失敗する**: Docker Engine の再起動や、`docker compose version` でプラグインが有効になっているか確認してください。古い環境では `docker-compose` コマンドを利用します。
- **マイグレーションがうまくいかない**: DB 接続文字列が `.env` に正しく設定されているか確認し、必要であれば `scripts/bootstrap.sh` を再実行して抜け漏れがないかチェックしてください。

## スクリプトの挙動カスタマイズ

`scripts/bootstrap.sh` は検出した情報を標準出力に整形して表示するだけで、破壊的な操作は行いません。プロジェクト固有のフレームワーク（例: Django, Rails, NestJS など）に合わせて案内を追加したい場合は、該当ディレクトリや設定ファイルの存在チェックを追記してください。コメントは英語で記述する運用を推奨しています。
