from fastapi import FastAPI
from .models import ProductResponse

app = FastAPI(
    title="商品管理API",
    description="商品の登録と取得を行うAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {"message": "商品管理API is running"}


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy"} 