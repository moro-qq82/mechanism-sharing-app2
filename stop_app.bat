@echo off
chcp 65001
echo ========================================
echo メカニズム共有プラットフォーム停止中...
echo ========================================

REM Node.jsプロセス（React開発サーバー）を停止
echo フロントエンドサーバーを停止中...
taskkill /f /im node.exe 2>nul
if %ERRORLEVEL% EQU 0 (
    echo フロントエンドサーバーを停止しました。
) else (
    echo フロントエンドサーバーは実行されていませんでした。
)

REM Pythonプロセス（FastAPIサーバー）を停止
echo バックエンドサーバーを停止中...
taskkill /f /im python.exe 2>nul
if %ERRORLEVEL% EQU 0 (
    echo バックエンドサーバーを停止しました。
) else (
    echo バックエンドサーバーは実行されていませんでした。
)

REM uvicornプロセスも停止（念のため）
taskkill /f /im uvicorn.exe 2>nul

echo.
echo ========================================
echo アプリケーションを停止しました。
echo ========================================
echo.
pause
