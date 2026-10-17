import math

import pytest

from calculator import (
    add,
    divide,
    evaluate,
    factorial,
    multiply,
    power,
    sqrt,
    subtract,
)


class TestBasicOperations:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [(1, 2, 3), (-1, 1, 0), (0.1, 0.2, 0.3), (0, 0, 0)],
    )
    def test_add(self, a, b, expected):
        assert add(a, b) == pytest.approx(expected)

    def test_subtract(self):
        assert subtract(10, 4) == 6
        assert subtract(4, 10) == -6

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 2.5) == -5.0

    def test_divide(self):
        assert divide(10, 4) == 2.5
        assert divide(-9, 3) == -3

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

    def test_power(self):
        assert power(2, 10) == 1024
        assert power(4, 0.5) == 2.0
        assert power(2, -1) == 0.5


class TestSqrt:
    def test_sqrt(self):
        assert sqrt(9) == 3.0
        assert sqrt(2) == pytest.approx(1.41421356)

    def test_sqrt_negative(self):
        with pytest.raises(ValueError):
            sqrt(-1)


class TestFactorial:
    @pytest.mark.parametrize(("n", "expected"), [(0, 1), (1, 1), (5, 120), (10, 3628800)])
    def test_factorial(self, n, expected):
        assert factorial(n) == expected

    def test_factorial_negative(self):
        with pytest.raises(ValueError):
            factorial(-3)

    @pytest.mark.parametrize("value", [2.5, "3", True])
    def test_factorial_non_integer(self, value):
        with pytest.raises(TypeError):
            factorial(value)


class TestEvaluate:
    @pytest.mark.parametrize(
        ("expression", "expected"),
        [
            ("1 + 2", 3),
            ("2 * (3 + 4)", 14),
            ("10 / 4", 2.5),
            ("2 ** 3 ** 2", 512),
            ("-5 + +3", -2),
            ("7 % 3", 1),
            ("7 // 2", 3),
            ("sqrt(16) + factorial(3)", 10),
            ("abs(-4.5)", 4.5),
            ("1 + 2 * 3 - 4 / 2", 5),
        ],
    )
    def test_evaluate(self, expression, expected):
        assert evaluate(expression) == pytest.approx(expected)

    def test_constants(self):
        assert evaluate("pi") == pytest.approx(math.pi)
        assert evaluate("2 * e") == pytest.approx(2 * math.e)

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            evaluate("1 / 0")

    @pytest.mark.parametrize("expression", ["1 +", "(2 * 3", ""])
    def test_syntax_error(self, expression):
        with pytest.raises(ValueError):
            evaluate(expression)

    @pytest.mark.parametrize(
        "expression",
        [
            "__import__('os').system('ls')",
            "open('file.txt')",
            "x + 1",
            "'abc'",
            "True + 1",
            "[1, 2]",
            "1 < 2",
            "sqrt(x=4)",
            "math.sqrt(4)",
        ],
    )
    def test_rejects_unsafe_or_unsupported(self, expression):
        with pytest.raises(ValueError):
            evaluate(expression)
