# 商品管理API

FastAPIを使用した商品管理REST APIです。商品の登録と取得機能を提供します。

## 機能

- ✅ 商品の作成（POST /items）
- ✅ 商品の取得（GET /items/{id}）
- ✅ ヘルスチェック（GET /health）
- ✅ 包括的なバリデーション
- ✅ 適切なエラーハンドリング
- ✅ 自動ID生成・タイムスタンプ付与

## 技術スタック

- **フレームワーク**: FastAPI 0.104.1
- **言語**: Python 3.11+
- **バリデーション**: Pydantic 2.5.0
- **テスト**: pytest 7.4.3
- **サーバー**: Uvicorn 0.24.0
- **データ保存**: インメモリ

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
uvicorn product_api.main:app --reload --port 8000
```

### 3. API仕様の確認

ブラウザで以下にアクセス:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API使用例

### 商品作成

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "サンプル商品", "price": 1500.0}'
```

**レスポンス:**
```json
{
  "id": 1,
  "name": "サンプル商品",
  "price": 1500.0,
  "created_at": "2025-05-26T01:45:05.431810"
}
```

### 商品取得

```bash
curl -X GET "http://localhost:8000/items/1"
```

**レスポンス:**
```json
{
  "id": 1,
  "name": "サンプル商品",
  "price": 1500.0,
  "created_at": "2025-05-26T01:45:05.431810"
}
```

### ヘルスチェック

```bash
curl -X GET "http://localhost:8000/health"
```

**レスポンス:**
```json
{
  "status": "healthy"
}
```

## テスト実行

### 全テスト実行

```bash
python -m pytest tests/ -v
```

### カバレッジ付きテスト実行

```bash
python -m pytest tests/ --cov=product_api --cov-report=html
```

### 特定のテストファイル実行

```bash
# 基本テスト
python -m pytest tests/test_basic.py -v

# 商品作成テスト
python -m pytest tests/test_product_create.py -v

# 商品取得テスト
python -m pytest tests/test_product_get.py -v

# 統合テスト
python -m pytest tests/test_integration.py -v
```

## プロジェクト構造

```
product-api/
├── product_api/          # アプリケーションコード
│   ├── __init__.py
│   ├── main.py          # FastAPIアプリケーション
│   ├── models.py        # Pydanticモデル
│   └── storage.py       # データストレージ
├── tests/               # テストコード
│   ├── __init__.py
│   ├── context.py       # テスト用インポート
│   ├── test_basic.py    # 基本機能テスト
│   ├── test_product_create.py  # 商品作成テスト
│   ├── test_product_get.py     # 商品取得テスト
│   └── test_integration.py     # 統合テスト
├── docs/                # ドキュメント
│   ├── requirements.md  # 要件定義
│   └── api_specification.md  # API仕様書
├── requirements.txt     # 依存関係
├── pyproject.toml      # プロジェクト設定
└── README.md           # このファイル
```

## 開発フロー

このプロジェクトはTDD（テスト駆動開発）アプローチで開発されました：

1. **Task 1**: プロジェクト基盤構築
2. **Task 2**: 商品作成API実装
3. **Task 3**: 商品取得API実装
4. **Task 4**: 統合テストと最終調整

各タスクでRed-Green-Refactorサイクルを実践し、包括的なテストスイートを構築しました。

## テスト結果

- **総テスト数**: 24テスト
- **成功率**: 100% (24/24)
- **カバレッジ**: 主要ビジネスロジック100%

## API仕様

詳細なAPI仕様については [docs/api_specification.md](docs/api_specification.md) を参照してください。

## 制限事項

- データはメモリ上に保存されるため、アプリケーション再起動時にデータは失われます
- 商品の更新・削除機能は提供していません
- 認証・認可機能は実装していません

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。
