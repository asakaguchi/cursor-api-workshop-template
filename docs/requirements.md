# 商品管理API要件

## 機能要件
- 商品の登録と取得
- 商品フィールド：id(Integer)、商品名(String)、価格(Float)、作成日(Datetime)
- メモリ上でデータ保持（DBは使用しない）

## API仕様
- GET /items/{id}：商品取得
- POST /items：商品作成

## 技術要件
- FastAPIフレームワーク使用
- JSONレスポンス形式
- エラーハンドリング実装
- テストコード必須