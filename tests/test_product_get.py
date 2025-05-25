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


def test_get_existing_product_returns_200(client):
    """存在する商品の取得が成功することをテスト"""
    # Arrange - 商品を事前に作成
    product_data = {"name": "テスト商品", "price": 1500.0}
    create_response = client.post("/items", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]
    
    # Act
    response = client.get(f"/items/{product_id}")
    
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == product_id
    assert response_data["name"] == "テスト商品"
    assert response_data["price"] == 1500.0
    assert "created_at" in response_data


def test_get_non_existent_product_returns_404(client):
    """存在しない商品の取得で404エラーが返されることをテスト"""
    # Arrange
    non_existent_id = 999
    
    # Act
    response = client.get(f"/items/{non_existent_id}")
    
    # Assert
    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data


def test_get_product_with_invalid_id_type_returns_422(client):
    """無効なID形式で422エラーが返されることをテスト"""
    # Arrange
    invalid_id = "invalid"
    
    # Act
    response = client.get(f"/items/{invalid_id}")
    
    # Assert
    assert response.status_code == 422


def test_get_product_with_negative_id_returns_404(client):
    """負のIDで404エラーが返されることをテスト"""
    # Arrange
    negative_id = -1
    
    # Act
    response = client.get(f"/items/{negative_id}")
    
    # Assert
    assert response.status_code == 404


def test_get_product_with_zero_id_returns_404(client):
    """ID=0で404エラーが返されることをテスト"""
    # Arrange
    zero_id = 0
    
    # Act
    response = client.get(f"/items/{zero_id}")
    
    # Assert
    assert response.status_code == 404


def test_get_multiple_products_returns_correct_data(client):
    """複数の商品を作成して正しく取得できることをテスト"""
    # Arrange - 複数の商品を作成
    product_data_1 = {"name": "商品1", "price": 1000.0}
    product_data_2 = {"name": "商品2", "price": 2000.0}
    
    create_response_1 = client.post("/items", json=product_data_1)
    create_response_2 = client.post("/items", json=product_data_2)
    
    assert create_response_1.status_code == 201
    assert create_response_2.status_code == 201
    
    product_id_1 = create_response_1.json()["id"]
    product_id_2 = create_response_2.json()["id"]
    
    # Act
    response_1 = client.get(f"/items/{product_id_1}")
    response_2 = client.get(f"/items/{product_id_2}")
    
    # Assert
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    
    data_1 = response_1.json()
    data_2 = response_2.json()
    
    assert data_1["id"] == product_id_1
    assert data_1["name"] == "商品1"
    assert data_1["price"] == 1000.0
    
    assert data_2["id"] == product_id_2
    assert data_2["name"] == "商品2"
    assert data_2["price"] == 2000.0


def test_get_product_json_response_format(client):
    """レスポンスのJSON形式が正しいことをテスト"""
    # Arrange
    product_data = {"name": "フォーマットテスト商品", "price": 999.99}
    create_response = client.post("/items", json=product_data)
    product_id = create_response.json()["id"]
    
    # Act
    response = client.get(f"/items/{product_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    response_data = response.json()
    required_fields = ["id", "name", "price", "created_at"]
    for field in required_fields:
        assert field in response_data
    
    # データ型の確認
    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["name"], str)
    assert isinstance(response_data["price"], (int, float))
    assert isinstance(response_data["created_at"], str) 