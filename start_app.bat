@echo off
chcp 932
echo ========================================
echo メカニズム共有プラットフォーム起動中...
echo ========================================

REM 現在のディレクトリを保存
set ORIGINAL_DIR=%CD%

@REM REM バックエンドの仮想環境を確認・作成
@REM echo.
@REM echo [0/4] バックエンドの仮想環境を確認中...
@REM cd /d "%~dp0"
@REM if not exist ".venv" (
@REM     echo 仮想環境が見つかりません。.venv を作成します...
@REM     uv venv .venv
@REM     if %ERRORLEVEL% NEQ 0 (
@REM         echo エラー: 仮想環境の作成に失敗しました。
@REM         pause
@REM         exit /b 1
@REM     )
@REM     echo 仮想環境の作成が完了しました。
@REM ) else (
@REM     echo 仮想環境は既に存在します。
@REM )

@REM REM バックエンドの依存関係をインストール（初回のみ）
@REM echo.
@REM echo [1/4] バックエンドの依存関係を確認中...
@REM cd /d "%~dp0"
@REM if not exist "requirements_installed.flag" (
@REM     echo バックエンドの依存関係をインストール中...
@REM     REM 仮想環境を有効化
@REM     call .venv\Scripts\activate
@REM     uv pip install -r backend\requirements.txt
@REM     if %ERRORLEVEL% EQU 0 (
@REM         echo. > requirements_installed.flag
@REM         echo バックエンドの依存関係のインストールが完了しました。
@REM     ) else (
@REM         echo エラー: バックエンドの依存関係のインストールに失敗しました。
@REM         pause
@REM         exit /b 1
@REM     )
@REM ) else (
@REM     echo バックエンドの依存関係は既にインストール済みです。
@REM )

@REM REM フロントエンドの依存関係をインストール（初回のみ）
@REM echo.
@REM echo [2/4] フロントエンドの依存関係を確認中...
@REM cd /d "%~dp0\frontend"
@REM if not exist "node_modules" (
@REM     echo フロントエンドの依存関係をインストール中...
@REM     npm install
@REM     if %ERRORLEVEL% NEQ 0 (
@REM         echo エラー: フロントエンドの依存関係のインストールに失敗しました。
@REM         pause
@REM         exit /b 1
@REM     )
@REM     echo フロントエンドの依存関係のインストールが完了しました。
@REM ) else (
@REM     echo フロントエンドの依存関係は既にインストール済みです。
@REM )

@REM REM プロジェクトルートに戻る
@REM cd /d "%~dp0"

@REM REM データベースマイグレーション実行
@REM echo.
@REM echo [3/4] データベースマイグレーションを実行中...
@REM ".venv\Scripts\alembic.exe" upgrade head
@REM if %ERRORLEVEL% NEQ 0 (
@REM     echo 警告: データベースマイグレーションでエラーが発生しました。
@REM     echo データベースが正しく設定されているか確認してください。
@REM     echo 続行しますか？ (Y/N)
@REM     set /p CONTINUE=
@REM     if /i not "%CONTINUE%"=="Y" (
@REM         pause
@REM         exit /b 1
@REM     )
@REM )

REM バックエンドサーバーを起動（バックグラウンド）
echo.
echo [4/4] サーバーを起動中...
echo バックエンドサーバーを起動しています...
call .venv\Scripts\activate
start "Backend Server" cmd /c "uvicorn backend.app.main:app --reload"

REM 少し待機してからフロントエンドを起動
timeout /t 3 /nobreak >nul

echo フロントエンドサーバーを起動しています...
cd /d "%~dp0\frontend"
start "Frontend Server" cmd /c "npm start"

REM 元のディレクトリに戻る
cd /d "%ORIGINAL_DIR%"

echo.
echo ========================================
echo アプリケーションが起動しました！
echo ========================================
echo.
echo アクセス先:
echo - フロントエンド: http://localhost:3000
echo - バックエンドAPI: http://localhost:8000
echo - API ドキュメント: http://localhost:8000/docs
echo.
echo サーバーを停止するには、各ターミナルウィンドウで Ctrl+C を押してください。
echo.
echo ブラウザが自動で開かない場合は、手動で http://localhost:3000 にアクセスしてください。
echo.
pause
