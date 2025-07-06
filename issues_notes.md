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
23. メカニズム詳細画面で「ファイルを表示」の隣にダウンロードボタンを配置したい
24. 投稿画面で投稿するボタンを押したときにスクロールしないとエラーが見えないことがある。投稿するボタンの下にエラーメッセージを表示したい（必須項目が記入されていません）
25. メカニズムごとにメカニズム詳細画面を開いた回数を記録できるようにする(個人ごと、総数)
26. backendのtest_auth.pyが単独テストではpassするが、backend全体テストでは一部failする
27. メカニズム詳細画面でファイルをダウンロードした回数を記録できるようにする（個人ごと、総数）
28. メカニズム一覧画面で、それぞれのメカニズム詳細がダウンロードされた回数の総数を表示できるようにする
29. メカニズム詳細画面で、ファイルをダウンロードした回数の総数を表示する

52. 背景画面とフォントをおしゃれにしたい
99. 新規投稿画面でカテゴリ入力を別の画面からボタンクリックで入力できるようにしたい（テスト必要）


### In process

### completed
27. メカニズム詳細画面でファイルをダウンロードした回数を記録できるようにする（個人ごと、総数）
   - 完了日時: 2025-07-06
   - 5分間重複防止機能を実装（同じユーザーが5分以内に同じメカニズムを再ダウンロードしてもカウントが増加しない仕組み）
   - 該当ファイル:
     - backend/app/models/mechanism_download.py - MechanismDownloadモデル作成
     - backend/app/schemas/mechanism_download.py - ダウンロード履歴のスキーマ定義
     - backend/app/services/mechanism_download.py - ダウンロード履歴のビジネスロジック
     - backend/app/routers/mechanism_download.py - ダウンロード履歴API
     - backend/tests/test_mechanism_download.py - ユニットテスト
     - backend/tests/test_mechanism_download_api.py - APIテスト
     - frontend/src/types/mechanism.ts - ダウンロード回数の型定義追加
     - frontend/src/services/mechanismService.ts - ダウンロード関連API呼び出し追加
     - frontend/src/pages/MechanismDetailPage.tsx - ダウンロードボタンクリック時のAPI呼び出し実装
     - migrations/versions/8079dc4a158a_add_mechanism_downloads_table_fixed.py - データベースマイグレーション
   - 機能: ダウンロード履歴記録、回数取得、一括取得API
   - 重複防止: 同じユーザーが5分以内に再ダウンロードしてもカウント増加しない
   - 認証状態対応: 認証あり・なし両方でダウンロード記録可能

28. メカニズム一覧画面で、それぞれのメカニズム詳細がダウンロードされた回数の総数を表示できるようにする
   - 完了日時: 2025-07-06
   - 該当ファイル:
     - frontend/src/pages/MechanismListPage.tsx - ダウンロード回数の一括取得・表示実装
   - 機能: メカニズム一覧でダウンロード回数を「ダウンロード X回」として表示
   - 実装: ページ読み込み時にダウンロード回数を一括取得し、各メカニズムカードに表示

29. メカニズム詳細画面で、ファイルをダウンロードした回数の総数を表示する
   - 完了日時: 2025-07-06
   - 該当ファイル:
     - frontend/src/pages/MechanismDetailPage.tsx - ダウンロード回数表示項目追加
   - 機能: 閲覧回数の下に「総ダウンロード回数」「あなたのダウンロード回数」を表示
   - 表示: 詳細画面読み込み時とダウンロード後にリアルタイム更新

25. メカニズムごとにメカニズム詳細画面を開いた回数を記録できるようにする(個人ごと、総数)
   - 完了日時: 2025-07-06
   - 5分間重複防止機能を実装（同じユーザーが5分以内に同じメカニズムを再度開いても閲覧回数が増加しない仕組み）
   - 該当ファイル:
     - backend/app/services/mechanism_view.py - 重複防止ロジックを追加
     - backend/app/routers/mechanism_view.py - APIレスポンスのステータスコード動的変更
     - backend/tests/test_mechanism_view.py - 新テストケース追加（test_duplicate_view_prevention, test_view_prevention_time_limit）
     - backend/tests/test_mechanism_view_api.py - APIテスト更新
   - バックエンド: MechanismViewService.create_mechanism_view メソッドの戻り値を(MechanismView, bool)に変更
   - API: 初回アクセス時は201 Created、5分以内の再アクセス時は200 OK を返却
   - テスト: 7個のユニットテストと2個のAPIテストが全て合格
   - 総閲覧回数が2ずつ増える問題を解決
26. backendのtest_auth.pyが単独テストではpassするが、backend全体テストでは一部failする
   - 完了日時: 2025-07-06
   - WSL環境側では問題なし
24. 投稿画面で投稿するボタンを押したときにスクロールしないとエラーが見えないことがある。投稿するボタンの下にエラーメッセージを表示したい（必須項目が記入されていません）
   - 完了日時: 2025-05-10
   - 該当ファイル:
     - frontend/src/pages/MechanismNewPage.tsx
     - frontend/src/__tests__/pages/MechanismNewPage.test.tsx
   - 投稿ボタンの下にエラーメッセージを表示するよう修正
   - 必須項目が記入されていない場合のエラーメッセージをリスト形式で表示
   - テストコードも更新して新しいUI構造に対応
23. メカニズム詳細画面で「ファイルを表示」の隣にダウンロードボタンを配置したい
   - 完了日時: 2025-05-10
   - 該当ファイル:
     - frontend/src/pages/MechanismDetailPage.tsx
     - frontend/src/__tests__/pages/MechanismDetailPage.test.tsx
   - 「ファイルを表示」ボタンの隣に「ダウンロード」ボタンを追加
   - ダウンロードボタンには`download`属性を指定し、ファイルを直接ダウンロードできるようにした
   - ボタンのスタイルは緑色にして、「ファイルを表示」ボタンと区別しやすくした
22. メカニズム一覧でタイルをクリックして詳細画面に遷移したい
   - 完了日時: 2025-05-10
   - 該当ファイル:
     - frontend/src/pages/MechanismListPage.tsx
   - タイル全体をLinkコンポーネントで囲み、クリック可能にした
   - タイトル部分のLinkを削除し、通常のテキストに変更した
   - カーソルポインタスタイルを追加して、クリック可能であることを視覚的に示した

21. サムネイル画像をpngとして登録したが、メカニズム一覧画面で表示されない
   - 完了日時: 2025-05-10
   - 該当ファイル:
     - frontend/src/utils/fileUtils.ts
     - frontend/src/pages/MechanismListPage.tsx
     - frontend/src/pages/MechanismDetailPage.tsx
   - clineのfileUtils.tsの修正が変だったので主導で修正した
20. メカニズム投稿できるが、詳細画面から「ファイルを表示」しても画像が表示されない（アップロードしたのはpngファイル）
   - 完了日時: 2025-05-10
   - 該当ファイル:
     - backend/app/main.py
     - frontend/src/pages/MechanismDetailPage.tsx
     - frontend/src/utils/fileUtils.ts
     - tests/integration/test_mechanism_integration.py
   - clineのfileUtils.tsの修正が変だったので主導で修正した
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
