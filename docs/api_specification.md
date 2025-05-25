# 商品管理API仕様書

## 概要
商品の登録と取得を行うREST APIです。メモリ上でデータを管理し、FastAPIフレームワークを使用して実装されています。

## ベースURL
```
http://localhost:8000
```

## エンドポイント一覧

### 1. ヘルスチェック

#### GET /
アプリケーションの動作確認用エンドポイント

**レスポンス**
- ステータスコード: 200
- Content-Type: application/json

```json
{
  "message": "商品管理API is running"
}
```

#### GET /health
ヘルスチェック用エンドポイント

**レスポンス**
- ステータスコード: 200
- Content-Type: application/json

```json
{
  "status": "healthy"
}
```

### 2. 商品作成

#### POST /items
新しい商品を作成します。

**リクエスト**
- Content-Type: application/json

```json
{
  "name": "商品名",
  "price": 1000.0
}
```

**リクエストパラメータ**
| フィールド | 型 | 必須 | 制約 | 説明 |
|-----------|----|----|------|------|
| name | string | ✓ | 1文字以上 | 商品名 |
| price | number | ✓ | 0より大きい | 商品価格 |

**レスポンス**
- ステータスコード: 201 Created
- Content-Type: application/json

```json
{
  "id": 1,
  "name": "商品名",
  "price": 1000.0,
  "created_at": "2025-05-26T01:38:25.930765"
}
```

**エラーレスポンス**
- ステータスコード: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

### 3. 商品取得

#### GET /items/{id}
指定されたIDの商品情報を取得します。

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|----|----|------|
| id | integer | ✓ | 商品ID |

**レスポンス**
- ステータスコード: 200 OK
- Content-Type: application/json

```json
{
  "id": 1,
  "name": "商品名",
  "price": 1000.0,
  "created_at": "2025-05-26T01:38:25.930765"
}
```

**エラーレスポンス**

商品が見つからない場合:
- ステータスコード: 404 Not Found

```json
{
  "detail": "商品ID 999 が見つかりません"
}
```

無効なID形式の場合:
- ステータスコード: 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "product_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "invalid"
    }
  ]
}
```

## データモデル

### Product
商品情報を表すデータモデル

| フィールド | 型 | 説明 |
|-----------|----|----|
| id | integer | 商品ID（自動生成） |
| name | string | 商品名 |
| price | number | 商品価格 |
| created_at | string (ISO 8601) | 作成日時（自動生成） |

## HTTPステータスコード

| コード | 説明 |
|-------|------|
| 200 | OK - 取得成功 |
| 201 | Created - 作成成功 |
| 404 | Not Found - リソースが見つからない |
| 422 | Unprocessable Entity - バリデーションエラー |

## 使用例

### 商品作成の例
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "サンプル商品", "price": 1500.0}'
```

### 商品取得の例
```bash
curl -X GET "http://localhost:8000/items/1"
```

## 制限事項

- データはメモリ上に保存されるため、アプリケーション再起動時にデータは失われます
- 同時接続数やリクエスト頻度に関する制限は設けていません
- 商品の更新・削除機能は提供していません

## バージョン情報

- API バージョン: 1.0.0
- FastAPI バージョン: 0.104.1
- Python バージョン: 3.11+ 