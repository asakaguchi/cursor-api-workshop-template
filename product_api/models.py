from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """商品作成用のリクエストモデル"""
    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="価格")


class Product(BaseModel):
    """商品データモデル"""
    id: int = Field(..., description="商品ID")
    name: str = Field(..., description="商品名")
    price: float = Field(..., description="価格")
    created_at: datetime = Field(..., description="作成日時")


class ProductResponse(BaseModel):
    """商品レスポンス用モデル"""
    id: int
    name: str
    price: float
    created_at: datetime 