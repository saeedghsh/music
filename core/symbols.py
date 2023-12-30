"""Symbols"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Symbol:
    """A representation for musical symbols"""

    simplified: str
    unicode: str

    def _eq_to_simplified(self, other_simplified: str) -> bool:
        return self.simplified == other_simplified

    def _eq_to_symbol(self, other: "Symbol") -> bool:
        return self.simplified == other.simplified

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self._eq_to_simplified(other)
        if isinstance(other, Symbol):
            return self._eq_to_symbol(other)
        raise NotImplementedError(f"Type {type(other)} is not supported for comparison")
