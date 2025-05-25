"""
テストモジュールがproduct_apiパッケージをインポートできるようにするヘルパー。
setup.py developを実行せずに、開発中のコードをテストできます。
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import product_api