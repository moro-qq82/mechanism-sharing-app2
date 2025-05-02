
### issues (終了しても記載は残す)
01. メカニズム詳細画面で信頼性のレベルが数字表記だが、「妄想モデル」など信頼性定義文章を表示するようにしたい（テスト不要、画面で確認）
02. (backend)データベース設定の実装（テスト必要）
03. (backend)カテゴリー管理API実装（テスト必要）
04. (backend)いいね機能API実装（テスト必要）
05. (backend)認証機能実装その１：ユーザー登録API（テスト必要）
06. (backend)認証機能実装その２：ログインAPI（テスト必要）
07. (backend)認証機能実装その３：JWT認証ミドルウェア（テスト必要）
08. (backend)メカニズム管理API実装その１：メカニズム一覧取得API（テスト必要）
09. (backend)メカニズム管理API実装その２：メカニズム詳細取得API（テスト必要）
10. (backend)メカニズム管理API実装その３：メカニズム投稿API（ファイルアップロード含む）（テスト必要）
11. (backend)後回しにしたテスト実装の確認(test_auth.pyのendpoint)
12. (frontend)認証画面機能実装（テスト必要）
13. (frontend)共通コンポーネント実装（テスト必要）
14. (frontend)メカニズム一覧画面機能実装（テスト必要）
15. (frontend)メカニズム詳細画面機能実装（テスト必要）
16. (frontend)メカニズム投稿画面機能実装（テスト必要）
17. (frontend)APIとの連携実装
18. 統合テスト
19. 新規投稿画面でカテゴリ入力を別の画面からボタンクリックで入力できるようにしたい（テスト必要）

### completed
01. メカニズム詳細画面で信頼性のレベルが数字表記だが、「妄想モデル」など信頼性定義文章を表示するようにしたい（テスト不要、画面で確認）
   - 完了日時: 2025-04-29
   - 該当ファイル: 
     - frontend/src/utils/reliabilityUtils.ts
     - frontend/src/pages/MechanismDetailPage.tsx
02. (backend)データベース設定の実装（テスト必要）
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
03. (backend)カテゴリー管理API実装（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/services/category.py
     - backend/app/routers/category.py
     - backend/app/main.py
     - backend/tests/test_category.py
04. (backend)いいね機能API実装（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/services/like.py
     - backend/app/routers/like.py
     - backend/app/main.py
     - backend/tests/test_like.py
05. (backend)認証機能実装その１：ユーザー登録API（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/utils/security.py
     - backend/app/services/auth.py
     - backend/app/routers/auth.py
     - backend/app/main.py
     - backend/tests/test_auth.py
06. (backend)認証機能実装その２：ログインAPI（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/utils/security.py
     - backend/app/services/auth.py
     - backend/app/routers/auth.py
     - backend/app/main.py
     - backend/tests/test_auth.py
07. (backend)認証機能実装その３：JWT認証ミドルウェア（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/utils/security.py
     - backend/app/middlewares/auth.py
     - backend/tests/test_auth.py
08. (backend)メカニズム管理API実装その１：メカニズム一覧取得API（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/services/mechanism.py
     - backend/app/routers/mechanism.py
     - backend/app/main.py
     - backend/tests/test_mechanism.py
09. (backend)メカニズム管理API実装その２：メカニズム詳細取得API（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/app/services/mechanism.py
     - backend/app/routers/mechanism.py
     - backend/app/main.py
     - backend/tests/test_mechanism.py
10. (backend)メカニズム管理API実装その３：メカニズム投稿API（ファイルアップロード含む）（テスト必要）
    - 完了日時: 2025-04-29
    - 該当ファイル:
      - backend/app/services/mechanism.py
      - backend/app/routers/mechanism.py
      - backend/app/main.py
      - backend/tests/test_mechanism.py
      - uploads/files（ディレクトリ）
      - uploads/thumbnails（ディレクトリ）
11. (backend)後回しにしたテスト実装の確認(test_auth.pyのendpoint)
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - backend/tests/test_auth.py
12. (frontend)認証画面機能実装（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - frontend/src/types/auth.ts
     - frontend/src/services/api.ts
     - frontend/src/services/authService.ts
     - frontend/src/contexts/AuthContext.tsx
     - frontend/src/components/auth/LoginForm.tsx
     - frontend/src/components/auth/RegisterForm.tsx
     - frontend/src/components/auth/ProtectedRoute.tsx
     - frontend/src/components/layout/Navbar.tsx
     - frontend/src/components/layout/Layout.tsx
     - frontend/src/pages/LoginPage.tsx
     - frontend/src/pages/RegisterPage.tsx
     - frontend/src/App.tsx
     - frontend/src/__tests__/auth/LoginForm.test.tsx
     - frontend/src/__tests__/auth/RegisterForm.test.tsx
     - frontend/src/__tests__/auth/ProtectedRoute.test.tsx
     - frontend/src/__tests__/auth/AuthContext.test.tsx
     - frontend/src/__tests__/auth/authService.test.ts
13. (frontend)共通コンポーネント実装（テスト必要）
   - 完了日時: 2025-04-29
   - 該当ファイル:
     - frontend/src/components/common/Button.tsx
     - frontend/src/__tests__/common/Button.test.tsx
     - frontend/src/components/common/Input.tsx
     - frontend/src/__tests__/common/Input.test.tsx
     - frontend/src/components/common/TextArea.tsx
     - frontend/src/__tests__/common/TextArea.test.tsx
     - frontend/src/components/common/Select.tsx
     - frontend/src/__tests__/common/Select.test.tsx
     - frontend/src/components/common/FileUpload.tsx
     - frontend/src/__tests__/common/FileUpload.test.tsx
     - frontend/src/components/common/Pagination.tsx
     - frontend/src/__tests__/common/Pagination.test.tsx
     - frontend/src/components/common/Loading.tsx
     - frontend/src/__tests__/common/Loading.test.tsx
     - frontend/src/components/common/Header.tsx
     - frontend/src/__tests__/common/Header.test.tsx
     - frontend/src/components/common/Footer.tsx
     - frontend/src/__tests__/common/Footer.test.tsx
14. (frontend)メカニズム一覧画面機能実装（テスト必要）
   - 完了日時: 2025-05-02
   - 該当ファイル:
     - frontend/src/types/mechanism.ts
     - frontend/src/services/mechanismService.ts
     - frontend/src/pages/MechanismListPage.tsx
     - frontend/src/__tests__/pages/MechanismListPage.test.tsx
15. (frontend)メカニズム詳細画面機能実装（テスト必要）
   - 完了日時: 2025-05-02
   - 該当ファイル:
     - frontend/src/pages/MechanismDetailPage.tsx
     - frontend/src/__tests__/pages/MechanismDetailPage.test.tsx
16. (frontend)メカニズム投稿画面機能実装（テスト必要）
   - 完了日時: 2025-05-02
   - 該当ファイル:
     - frontend/src/pages/MechanismNewPage.tsx
     - frontend/src/__tests__/pages/MechanismNewPage.test.tsx
