import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "メカニズム共有プラットフォーム"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # データベース設定
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/mechanism_db"
    
    # JWT設定
    SECRET_KEY: str = "your-secret-key"  # 本番環境では環境変数から取得する
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ファイルアップロード設定
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = ["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "jpg", "jpeg", "png", "gif"]
    
    # CORS設定
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # フロントエンドのURL
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
