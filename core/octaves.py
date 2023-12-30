"""Octaves"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Sequence


@dataclass
class Octave:
    """An octave (perfect octave, the diapason) is the interval between one musical
    pitch and another with double its frequency"""

    name: str
    number: int

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return f"octave {self.number} {self.name}"

    def _eq_to_name(self, other_name: str) -> bool:
        return self.name == other_name

    def _eq_to_number(self, other_number: int) -> bool:
        return self.number == other_number

    def _eq_to_octave(self, other: "Octave") -> bool:
        return self.name == other.name and self.number == other.number

    def __eq__(self, other: Any) -> bool:
        type_dispatch: Dict[type, Callable] = {
            str: self._eq_to_name,
            int: self._eq_to_number,
            Octave: self._eq_to_octave,
        }
        other_type = type(other)
        if other_type not in type_dispatch:
            raise NotImplementedError(f"Type {other_type} is not supported for comparison")
        return type_dispatch[other_type](other)


class OctaveRegister(Enum):
    """An enum of common Octaves"""

    SUBSUBCONTRA = Octave("subsubcontra", -1)
    SUBCONTRA = Octave("sub-contra", 0)
    CONTRA = Octave("contra", 1)
    GREAT = Octave("great", 2)
    SMALL = Octave("small", 3)
    ONELINED = Octave("one-lined", 4)
    TWOLINED = Octave("two-lined", 5)
    THREELINED = Octave("three-lined", 6)
    FOURLINED = Octave("four-lined", 7)
    FIVELINED = Octave("five-lined", 8)
    SIXLINED = Octave("six-lined", 9)

    @staticmethod
    def _octave_range() -> Sequence[int]:
        """Return a list of octave range as integer values"""
        return [octave.value.number for octave in OctaveRegister]

    @staticmethod
    def validate(octave: int):
        """Check if input octave is in range"""
        octave_range = OctaveRegister._octave_range()
        if not octave_range[0] <= octave <= octave_range[-1]:
            raise ValueError(f"value {octave} is out of bound: {octave_range}")
