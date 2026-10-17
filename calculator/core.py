"""四則演算などの基本関数と、文字列の数式を安全に評価する evaluate()。"""

import ast
import math
import operator

Number = int | float


def add(a: Number, b: Number) -> Number:
    return a + b


def subtract(a: Number, b: Number) -> Number:
    return a - b


def multiply(a: Number, b: Number) -> Number:
    return a * b


def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ZeroDivisionError("0 で割ることはできません")
    return a / b


def power(base: Number, exponent: Number) -> Number:
    return base**exponent


def sqrt(x: Number) -> float:
    if x < 0:
        raise ValueError("負の数の平方根は計算できません")
    return math.sqrt(x)


def factorial(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("階乗は整数にのみ定義されています")
    if n < 0:
        raise ValueError("負の数の階乗は計算できません")
    return math.factorial(n)


_BINARY_OPS = {
    ast.Add: add,
    ast.Sub: subtract,
    ast.Mult: multiply,
    ast.Div: divide,
    ast.Pow: power,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS = {
    "sqrt": sqrt,
    "factorial": factorial,
    "abs": abs,
}

_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def evaluate(expression: str) -> Number:
    """数式文字列を評価して結果を返す。

    eval() は使わず、AST を辿って許可された演算・関数・定数のみを計算する。
    例: evaluate("2 * (3 + 4)") -> 14
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"数式の構文が正しくありません: {expression!r}") from exc
    return _eval_node(tree.body)


def _eval_node(node: ast.AST) -> Number:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError(f"数値以外の値は使えません: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op = _BINARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"未対応の演算子です: {type(node.op).__name__}")
        return op(_eval_node(node.left), _eval_node(node.right))

    if isinstance(node, ast.UnaryOp):
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"未対応の演算子です: {type(node.op).__name__}")
        return op(_eval_node(node.operand))

    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"未定義の名前です: {node.id}")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ValueError("未対応の関数呼び出しです")
        if node.keywords:
            raise ValueError("キーワード引数は使えません")
        args = [_eval_node(arg) for arg in node.args]
        return _FUNCTIONS[node.func.id](*args)

    raise ValueError(f"未対応の式です: {type(node).__name__}")
