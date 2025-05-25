from datetime import datetime
from typing import Dict, Optional
from .models import Product, ProductCreate


class MemoryStorage:
    """メモリ上で商品データを管理するストレージクラス"""
    
    def __init__(self):
        self._products: Dict[int, Product] = {}
        self._next_id: int = 1
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """商品を作成してストレージに保存"""
        product = Product(
            id=self._next_id,
            name=product_data.name,
            price=product_data.price,
            created_at=datetime.now()
        )
        
        self._products[self._next_id] = product
        self._next_id += 1
        
        return product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """指定されたIDの商品を取得"""
        return self._products.get(product_id)
    
    def get_all_products(self) -> Dict[int, Product]:
        """全ての商品を取得（デバッグ用）"""
        return self._products.copy()
    
    def clear(self):
        """全ての商品データをクリア（テスト用）"""
        self._products.clear()
        self._next_id = 1


# グローバルストレージインスタンス
storage = MemoryStorage() 