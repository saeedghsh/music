# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

from core.symbols import Symbol


def test_symbol_creation():
    sym = Symbol(simplified="A", unicode="\u0041")
    assert sym.simplified == "A"
    assert sym.unicode == "\u0041"


def test_symbol_comparison():
    sym1 = Symbol(simplified="A", unicode="\u0041")
    sym2 = Symbol(simplified="A", unicode="\u0041")
    sym3 = Symbol(simplified="B", unicode="\u0042")
    assert sym1 == sym2
    assert sym1 == "A"
    assert sym1 != sym3
    assert sym1 != "B"


def test_symbol_comparison_not_implemented():
    s = Symbol(simplified="A", unicode="\u0041")
    with pytest.raises(NotImplementedError):
        s == 0  # pylint: disable=pointless-statement


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
