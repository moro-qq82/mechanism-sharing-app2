from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="メカニズム共有プラットフォーム",
    description="物理的なメカニズムを可視化して共有するプラットフォーム",
    version="0.1.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uploadsディレクトリが存在しない場合は作成
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/files", exist_ok=True)
os.makedirs("uploads/thumbnails", exist_ok=True)

# 静的ファイルの設定
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "メカニズム共有プラットフォームAPI"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# 各ルーターをインポートして追加する
from backend.app.routers import category, like, auth, mechanism, mechanism_view, mechanism_download

app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
app.include_router(mechanism.router, prefix="/api/mechanisms", tags=["メカニズム"])
app.include_router(mechanism_view.router, prefix="/api/mechanisms", tags=["メカニズム閲覧"])
app.include_router(mechanism_download.router, prefix="/api/mechanisms", tags=["メカニズムダウンロード"])
app.include_router(category.router, prefix="/api/categories", tags=["カテゴリー"])
app.include_router(like.router, prefix="/api/likes", tags=["いいね"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
