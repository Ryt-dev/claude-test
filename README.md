# claude-test

Python 製の簡単な数式計算ライブラリ `calculator` です。

## 使い方

```python
from calculator import add, divide, sqrt, evaluate

add(1, 2)                     # 3
divide(10, 4)                 # 2.5
sqrt(16)                      # 4.0
evaluate("2 * (3 + 4)")       # 14
evaluate("sqrt(16) + pi")     # 7.141592...
```

`evaluate()` は `eval()` を使わず AST を解析して計算するため、
四則演算・`**`・`%`・`//`、関数 `sqrt` / `factorial` / `abs`、定数 `pi` / `e` 以外は受け付けません。

## テスト

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```
