from fastapi import FastAPI, HTTPException, status
from .models import ProductCreate, ProductResponse
from .storage import storage

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


@app.post("/items", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate):
    """商品を作成する
    
    Args:
        product_data: 商品作成データ
        
    Returns:
        作成された商品情報
        
    Raises:
        HTTPException: バリデーションエラーの場合
    """
    try:
        product = storage.create_product(product_data)
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            created_at=product.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"商品の作成に失敗しました: {str(e)}"
        )


@app.get("/items/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """指定されたIDの商品を取得する
    
    Args:
        product_id: 商品ID
        
    Returns:
        商品情報
        
    Raises:
        HTTPException: 商品が見つからない場合（404）
    """
    product = storage.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品ID {product_id} が見つかりません"
        )
    
    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        created_at=product.created_at
    ) 