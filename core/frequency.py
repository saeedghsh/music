"""A representation of Frequency"""
import operator
from dataclasses import dataclass
from functools import total_ordering
from math import isclose
from typing import Any


@total_ordering
@dataclass
class Frequency:
    """Frequency in Hz

    NOTE: by defining __eq__ and one other rich comparison ordering method (__lt__, __le__,
          __gt__, or __ge__), total_ordering decorator will automatically provide the rest.
    """

    value: float

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"Frequency must be non-zero and positive: {self.value}")

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.value} Hz"

    def __eq__(self, other: Any):
        if isinstance(other, Frequency):
            return isclose(self.value, other.value)
        if isinstance(other, (float, int)):
            return isclose(self.value, other)
        return NotImplemented

    def __lt__(self, other: Any):
        if isinstance(other, Frequency):
            return self.value < other.value
        if isinstance(other, (float, int)):
            return self.value < other
        return NotImplemented

    def _apply_operation(self, other: Any, operation):
        """support other of type Frequency, int and float"""
        if isinstance(other, (Frequency, int, float)):
            other_value = other.value if isinstance(other, Frequency) else other
            return Frequency(operation(self.value, other_value))
        return NotImplemented

    def __add__(self, other: Any):
        return self._apply_operation(other, operator.add)

    def __mul__(self, other: Any):
        if isinstance(other, (float, int)):
            return Frequency(self.value * other)
        return NotImplemented
