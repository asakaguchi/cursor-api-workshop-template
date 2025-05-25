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


def test_create_product_with_valid_data_returns_201(client):
    """有効なデータで商品作成が成功することをテスト"""
    # Arrange
    product_data = {
        "name": "テスト商品",
        "price": 1000.0
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["name"] == "テスト商品"
    assert response_data["price"] == 1000.0
    assert "created_at" in response_data


def test_create_product_with_empty_name_returns_422(client):
    """商品名が空の場合にバリデーションエラーが返されることをテスト"""
    # Arrange
    product_data = {
        "name": "",
        "price": 1000.0
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 422


def test_create_product_with_negative_price_returns_422(client):
    """価格が負の値の場合にバリデーションエラーが返されることをテスト"""
    # Arrange
    product_data = {
        "name": "テスト商品",
        "price": -100.0
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 422


def test_create_product_with_zero_price_returns_422(client):
    """価格が0の場合にバリデーションエラーが返されることをテスト"""
    # Arrange
    product_data = {
        "name": "テスト商品",
        "price": 0.0
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 422


def test_create_product_with_missing_name_returns_422(client):
    """商品名が欠けている場合にバリデーションエラーが返されることをテスト"""
    # Arrange
    product_data = {
        "price": 1000.0
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 422


def test_create_product_with_missing_price_returns_422(client):
    """価格が欠けている場合にバリデーションエラーが返されることをテスト"""
    # Arrange
    product_data = {
        "name": "テスト商品"
    }
    
    # Act
    response = client.post("/items", json=product_data)
    
    # Assert
    assert response.status_code == 422


def test_create_multiple_products_increments_id(client):
    """複数の商品を作成した場合にIDが自動インクリメントされることをテスト"""
    # Arrange
    product_data_1 = {"name": "商品1", "price": 1000.0}
    product_data_2 = {"name": "商品2", "price": 2000.0}
    
    # Act
    response_1 = client.post("/items", json=product_data_1)
    response_2 = client.post("/items", json=product_data_2)
    
    # Assert
    assert response_1.status_code == 201
    assert response_2.status_code == 201
    assert response_1.json()["id"] == 1
    assert response_2.json()["id"] == 2 