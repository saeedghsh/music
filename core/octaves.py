"""Octaves"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict

NUMBER_TO_NAME_MAP = {
    -1: "subsubcontra",
    0: "subcontra",
    1: "contra",
    2: "great",
    3: "small",
    4: "onelined",
    5: "twolined",
    6: "threelined",
    7: "fourlined",
    8: "fivelined",
    9: "sixlined",
}


@dataclass
class Octave:
    """An octave (perfect octave, the diapason) is the interval between one musical
    pitch and another with double its frequency"""

    name: str
    number: int

    def __post_init__(self):
        if self.name not in NUMBER_TO_NAME_MAP.values():
            raise ValueError(f"Invalid name {self.name}")
        if self.number not in NUMBER_TO_NAME_MAP:
            raise ValueError(f"Invalid number {self.number}")
        if self.name != NUMBER_TO_NAME_MAP[self.number]:
            raise ValueError(f"Number {self.number} and name {self.name} for not match")

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

    def __add__(self, other: Any):
        if isinstance(other, int):
            return Octave.from_number(self.number + other)
        raise NotImplementedError(f"Type {type(other)} is not supported for add")

    @staticmethod
    def from_name(name: str) -> "Octave":
        """Return an Octave object from name"""
        if name not in NUMBER_TO_NAME_MAP.values():
            raise ValueError(f"Name {name} is not a valid Octave name")
        octave = getattr(OctaveRegister, name.upper())
        return octave.value

    @staticmethod
    def from_number(number: int) -> "Octave":
        """Return an Octave object from name"""
        if number not in NUMBER_TO_NAME_MAP:
            raise ValueError(f"Number {number} is not a valid Octave")
        return Octave.from_name(NUMBER_TO_NAME_MAP[number])

    @staticmethod
    def validate(octave: int):
        """Check if input octave is in range

        NOTE: since Octave objects are validated at constructions, not need to support Octave type
        """
        octave_range = list(NUMBER_TO_NAME_MAP.keys())
        if not octave_range[0] <= octave <= octave_range[-1]:
            raise ValueError(f"value {octave} is out of bound: {octave_range}")


class OctaveRegister(Enum):
    """An enum of common Octaves"""

    SUBSUBCONTRA = Octave("subsubcontra", -1)
    SUBCONTRA = Octave("subcontra", 0)
    CONTRA = Octave("contra", 1)
    GREAT = Octave("great", 2)
    SMALL = Octave("small", 3)
    ONELINED = Octave("onelined", 4)
    TWOLINED = Octave("twolined", 5)
    THREELINED = Octave("threelined", 6)
    FOURLINED = Octave("fourlined", 7)
    FIVELINED = Octave("fivelined", 8)
    SIXLINED = Octave("sixlined", 9)
