import os
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "メカニズム共有プラットフォーム（テスト）"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # テスト用データベース設定
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/mechanism_test_db"
    
    # JWT設定
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ファイルアップロード設定
    UPLOAD_DIR: str = "test_uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = ["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "jpg", "jpeg", "png", "gif"]
    
    # CORS設定
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # フロントエンドのURL
    ]
    
    class Config:
        env_file = ".env.test"
        case_sensitive = True

test_settings = TestSettings()
