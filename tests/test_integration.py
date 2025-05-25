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


def test_complete_product_lifecycle(client):
    """商品の完全なライフサイクルをテスト（作成→取得）"""
    # Arrange
    product_data = {
        "name": "統合テスト商品",
        "price": 3000.0
    }
    
    # Act & Assert - 商品作成
    create_response = client.post("/items", json=product_data)
    assert create_response.status_code == 201
    
    created_product = create_response.json()
    assert created_product["name"] == "統合テスト商品"
    assert created_product["price"] == 3000.0
    assert created_product["id"] == 1
    assert "created_at" in created_product
    
    # Act & Assert - 商品取得
    product_id = created_product["id"]
    get_response = client.get(f"/items/{product_id}")
    assert get_response.status_code == 200
    
    retrieved_product = get_response.json()
    assert retrieved_product == created_product


def test_multiple_products_workflow(client):
    """複数商品の作成と取得のワークフローをテスト"""
    # Arrange
    products_data = [
        {"name": "商品A", "price": 1000.0},
        {"name": "商品B", "price": 2000.0},
        {"name": "商品C", "price": 3000.0}
    ]
    
    created_products = []
    
    # Act - 複数商品の作成
    for product_data in products_data:
        response = client.post("/items", json=product_data)
        assert response.status_code == 201
        created_products.append(response.json())
    
    # Assert - IDの連続性確認
    for i, product in enumerate(created_products):
        assert product["id"] == i + 1
    
    # Act & Assert - 各商品の取得確認
    for i, expected_product in enumerate(created_products):
        response = client.get(f"/items/{i + 1}")
        assert response.status_code == 200
        retrieved_product = response.json()
        assert retrieved_product == expected_product


def test_error_handling_consistency(client):
    """エラーハンドリングの一貫性をテスト"""
    # 商品作成のバリデーションエラー
    invalid_create_data = {"name": "", "price": -100.0}
    create_response = client.post("/items", json=invalid_create_data)
    assert create_response.status_code == 422
    assert "detail" in create_response.json()
    
    # 存在しない商品の取得エラー
    get_response = client.get("/items/999")
    assert get_response.status_code == 404
    assert "detail" in get_response.json()
    
    # 無効なIDでの取得エラー
    invalid_id_response = client.get("/items/invalid")
    assert invalid_id_response.status_code == 422
    assert "detail" in invalid_id_response.json()


def test_api_response_format_consistency(client):
    """APIレスポンス形式の一貫性をテスト"""
    # 商品作成
    product_data = {"name": "フォーマット確認商品", "price": 1500.0}
    create_response = client.post("/items", json=product_data)
    
    # 作成レスポンスの形式確認
    assert create_response.status_code == 201
    assert create_response.headers["content-type"] == "application/json"
    
    created_product = create_response.json()
    required_fields = ["id", "name", "price", "created_at"]
    for field in required_fields:
        assert field in created_product
    
    # 取得レスポンスの形式確認
    get_response = client.get(f"/items/{created_product['id']}")
    assert get_response.status_code == 200
    assert get_response.headers["content-type"] == "application/json"
    
    retrieved_product = get_response.json()
    for field in required_fields:
        assert field in retrieved_product
    
    # 両レスポンスの一致確認
    assert created_product == retrieved_product


def test_concurrent_operations_simulation(client):
    """並行操作のシミュレーションテスト"""
    # 複数の商品を短時間で作成
    products = []
    for i in range(5):
        product_data = {"name": f"並行テスト商品{i+1}", "price": (i+1) * 1000.0}
        response = client.post("/items", json=product_data)
        assert response.status_code == 201
        products.append(response.json())
    
    # 全ての商品が正しく作成されていることを確認
    for i, product in enumerate(products):
        assert product["id"] == i + 1
        assert product["name"] == f"並行テスト商品{i+1}"
        assert product["price"] == (i+1) * 1000.0
    
    # 全ての商品が正しく取得できることを確認
    for i in range(5):
        response = client.get(f"/items/{i+1}")
        assert response.status_code == 200
        retrieved_product = response.json()
        assert retrieved_product == products[i]


def test_edge_cases_handling(client):
    """エッジケースの処理をテスト"""
    # 最小値での商品作成
    min_product = {"name": "a", "price": 0.01}
    response = client.post("/items", json=min_product)
    assert response.status_code == 201
    
    # 大きな値での商品作成
    large_product = {"name": "大きな価格の商品", "price": 999999.99}
    response = client.post("/items", json=large_product)
    assert response.status_code == 201
    
    # 日本語文字での商品作成
    japanese_product = {"name": "日本語商品名テスト", "price": 1000.0}
    response = client.post("/items", json=japanese_product)
    assert response.status_code == 201
    
    # 作成した商品の取得確認
    for product_id in [1, 2, 3]:
        response = client.get(f"/items/{product_id}")
        assert response.status_code == 200


def test_health_endpoints_integration(client):
    """ヘルスチェックエンドポイントとの統合テスト"""
    # ヘルスチェック
    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "healthy"}
    
    # ルートエンドポイント
    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json() == {"message": "商品管理API is running"}
    
    # 商品作成後もヘルスチェックが正常
    product_data = {"name": "ヘルステスト商品", "price": 1000.0}
    client.post("/items", json=product_data)
    
    health_response_after = client.get("/health")
    assert health_response_after.status_code == 200
    assert health_response_after.json() == {"status": "healthy"} 