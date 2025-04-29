
### issues
1. メカニズム詳細画面で信頼性のレベルが数字表記だが、「妄想モデル」など信頼性定義文章を表示するようにしたい（テスト不要、画面で確認）
2. (backend)データベース設定の実装（テスト必要）
3. (backend)カテゴリー管理API実装（テスト必要）
4. (backend)いいね機能API実装（テスト必要）
5. (backend)認証機能実装その１：ユーザー登録API（テスト必要）
6. (backend)認証機能実装その２：ログインAPI（テスト必要）
7. (backend)認証機能実装その３：JWT認証ミドルウェア（テスト必要）
8. (backend)メカニズム管理API実装その１：メカニズム一覧取得API（テスト必要）
9. (backend)メカニズム管理API実装その２：メカニズム詳細取得API（テスト必要）
10. (backend)メカニズム管理API実装その３：メカニズム投稿API（ファイルアップロード含む）（テスト必要）
11. (frontend)認証画面機能実装
12. (frontend)共通コンポーネント実装
13. (frontend)メカニズム一覧画面機能実装
14. (frontend)メカニズム詳細画面機能実装
15. (frontend)メカニズム投稿画面機能実装
16. 新規投稿画面でカテゴリ入力を別の画面からボタンクリックで入力できるようにしたい（テスト必要）
17. (frontend)APIとの連携実装
18. 統合テスト

### completed
1. メカニズム詳細画面で信頼性のレベルが数字表記だが、「妄想モデル」など信頼性定義文章を表示するようにしたい（テスト不要、画面で確認）
   - 完了日時: 2025-04-29
   - 該当ファイル: 
     - frontend/src/utils/reliabilityUtils.ts
     - frontend/src/pages/MechanismDetailPage.tsx
2. (backend)データベース設定の実装（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/database.py
     - backend/app/config.py
     - backend/app/config_test.py
     - backend/app/database_test.py
     - backend/tests/conftest.py
     - backend/tests/test_database.py
     - alembic.ini
     - migrations/env.py
     - migrations/versions/ab1384850060_initial_migration.py
