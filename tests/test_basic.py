import pytest
from fastapi.testclient import TestClient
from product_api import app, storage


@pytest.fixture
def client():
    """テスト用のFastAPIクライアント"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """各テスト前にストレージをクリア"""
    storage.clear()
    yield
    storage.clear()


def test_root_endpoint(client):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "商品管理API is running"}


def test_health_check(client):
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_storage_basic_operations():
    """ストレージの基本操作テスト"""
    from product_api.models import ProductCreate
    
    # 商品作成データ
    product_data = ProductCreate(name="テスト商品", price=1000.0)
    
    # 商品作成
    product = storage.create_product(product_data)
    assert product.id == 1
    assert product.name == "テスト商品"
    assert product.price == 1000.0
    assert product.created_at is not None
    
    # 商品取得
    retrieved_product = storage.get_product(1)
    assert retrieved_product is not None
    assert retrieved_product.id == 1
    assert retrieved_product.name == "テスト商品"
    
    # 存在しない商品
    non_existent = storage.get_product(999)
    assert non_existent is None 