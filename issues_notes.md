## 記載ルール
- issuesはユーザーが追記修正します。完了してもそのまま残します
- completedにされたissueはユーザーが確認後完了していなかったらIn processに移動します
- In processのissueはユーザーが完了を確認したら、Completedに移し、In processの方は削除します
- clineのタスク管理のためこれらのルールを運用します

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
17. (frontend)APIとの連携実装（テスト必要）
18. 統合テスト
19. ログイン後のトップページに「メカニズム一覧の取得に失敗しました」というエラーメッセージが出る
20. メカニズム投稿できるが、詳細画面から「ファイルを表示」しても画像が表示されない（アップロードしたのはpngファイル）
21. サムネイル画像をpngとして登録したが、メカニズム一覧画面で表示されない
22. メカニズム一覧でタイルをクリックして詳細画面に遷移したい
23. メカニズム詳細画面でファイルを表示したときに、ブラウザで表示できない拡張子の場合は自動でダウンロードさせたい
24. 投稿画面で投稿するボタンを押したときにスクロールしないとエラーが見えない。投稿するボタンの下にエラーメッセージを表示したい（必須項目が記入されていません）
25. メカニズムごとにメカニズム詳細画面を開いた回数を記録できるようにする
26. メカニズム詳細画面でファイルを表示した回数を記録できるようにする

99. 新規投稿画面でカテゴリ入力を別の画面からボタンクリックで入力できるようにしたい（テスト必要）


### In process
20. メカニズム投稿できるが、詳細画面から「ファイルを表示」しても画像が表示されない（アップロードしたのはpngファイル）
   - 完了日時: 2025-05-06
   - 該当ファイル:
     - backend/app/main.py
     - frontend/src/pages/MechanismDetailPage.tsx
     - frontend/src/utils/fileUtils.ts
     - tests/integration/test_mechanism_integration.py
   - 統合テストは通るが実際の起動画面では表示されていない
21. サムネイル画像をpngとして登録したが、メカニズム一覧画面で表示されない
   - 完了日時: 2025-05-04
   - 該当ファイル:
     - frontend/src/utils/fileUtils.ts
     - frontend/src/pages/MechanismListPage.tsx
     - frontend/src/pages/MechanismDetailPage.tsx


### completed



19. ログイン後のトップページに「メカニズム一覧の取得に失敗しました」というエラーメッセージが出る
   - 完了日時: 2025-05-04
   - 該当ファイル:
     - frontend/src/services/mechanismService.ts
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
17. (frontend)APIとの連携実装（テスト必要）
   - 完了日時: 2025-05-02
   - 該当ファイル:
     - frontend/src/__tests__/services/mechanismService.test.ts
     - frontend/src/__tests__/services/api.test.ts
18. 統合テスト
   - 完了日時: 2025-05-03
   - 該当ファイル:
     - tests/integration/conftest.py
     - tests/integration/test_auth_integration.py
     - tests/integration/test_category_integration.py
     - tests/integration/test_like_integration.py
     - tests/integration/test_mechanism_integration.py
     - tests/integration/test_frontend_backend_integration.py
     - tests/run_integration_tests.py
     - docs/docs_test_status.md
     - backend/app/routers/category.py
     - backend/app/routers/like.py
     - backend/app/schemas/like.py
