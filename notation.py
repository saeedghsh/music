"""X"""
from typing import Any, Tuple
from dataclasses import dataclass
from math import isclose

from notes_and_frequencies import compute_frequency

A4_FREQUENCY = 440  # Note reference: A4 = 440 Hz


@dataclass
class Accidental:
    """Accidentals are symbols that pair with a notes to create new notes.
    Three common accidentals are:
    * the sharp: half-step higher,
    * the flat: half-step lower,
    * the natural.
    In Iranian music:
    * the sori: quarter-step higher
    * the koron: quarter-step lower"""

    name: str
    short_hand: str
    unicode_cha: str
    frequency_ratio: float

    def __str__(self) -> str:
        return self.short_hand


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
        type_dispatch = {
            str: self._eq_to_name,
            int: self._eq_to_number,
            Octave: self._eq_to_octave,
        }
        other_type = type(other)
        if other_type not in type_dispatch.keys():
            raise NotImplementedError(
                f"Type {other_type} is not supported for comparison"
            )
        return type_dispatch[other_type](other)


@dataclass
class Note:
    name: str
    letter: str
    accidental: str
    octave: Octave
    frequency: float

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Note {self.name} - {self.frequency} Hz"

    def __post_init__(self):
        letter, accidental, octave = self.decompose_name(self.name)
        assert letter == self.letter
        assert accidental == self.accidental
        assert octave == self.octave

    @staticmethod
    def decompose_name(name: str) -> Tuple[str, str, int]:
        """Return letter, accidental and octave from the name

        It also validates the name correctness thouroughly.
        """
        if not name[-1].isdigit():
            raise ValueError("Last char of name must be octave as a number (int)")
        octave = name[-1]
        if not -1 <= octave <= 0:
            raise ValueError("octave is out of range")

        if len(name[:-1]) == 1:
            letter, accidental = name[0].upper(), ""
        elif len(name[:-1]) == 1:
            letter, accidental = name[0].upper(), name[1].lower()
        else:
            raise ValueError("Length name cannot be more that 3 characters")

        if letter not in ["A", "B", "C", "D", "E", "F", "G"]:
            raise ValueError("letter is invalid")
        if accidental not in ["#", "s", "", "k", "b"]:
            raise ValueError("accidental is invalid")

        return letter, accidental, octave

    @staticmethod
    def from_name(name: str, a4_frequency: float = A4_FREQUENCY) -> "Note":
        """Create and return an object of type Note from the given name"""
        letter, accidental, octave = Note.decompose_name(name)
        frequency = compute_frequency(letter, accidental, octave, a4_frequency)
        return Note(name, letter, accidental, octave, frequency)

    def _eq_to_name(self, other_name: str) -> bool:
        # TODO: Should convert self and other both to a standard form
        # for instance to make sure E# == F is True
        return self.name == other_name

    def _eq_to_frequency(self, other_frequency: float) -> bool:
        return isclose(self.frequency, other_frequency)

    def _eq_to_note(self, other: "Note") -> bool:
        return self._eq_to_name(other.name) and self._eq_to_frequency(other.frequency)

    def __eq__(self, other: Any) -> bool:
        type_dispatch = {
            str: self._eq_to_name,
            float: self._eq_to_frequency,
            Note: self._eq_to_note,
        }
        other_type = type(other)
        if other_type not in type_dispatch.keys():
            raise NotImplementedError(
                f"Type {other_type} is not supported for comparison"
            )
        return type_dispatch[other_type](other)


FREQUENCY_RATIO = {
    "octave": 2 ** (12 / 12),  # 2
    "tone": 2 ** (1 / 6),  # 8 ** (1/24)
    "semitone": 2 ** (1 / 12),  # 4 ** (1/24)
    "quadranttone": 2 ** (1 / 24),  # 2 ** (1/24)
}


ACCIDENTALS = {
    "sharp": Accidental("sharp", "#", "\u266F", FREQUENCY_RATIO["semitone"]),
    "sori": Accidental("sori", "s", "\U0001D1E9", FREQUENCY_RATIO["quadranttone"]),
    "natural": Accidental("natural", "", "", 1),
    "koron": Accidental(
        "koron", "k", "\U0001D1EA", 1 / FREQUENCY_RATIO["quadranttone"]
    ),
    "flat": Accidental("flat", "b", "\u266F", 1 / FREQUENCY_RATIO["semitone"]),
}

OCTAVES = {
    -1: Octave("subsubcontra", -1),
    0: Octave("sub-contra", 0),
    1: Octave("contra", 1),
    2: Octave("great", 2),
    3: Octave("small", 3),
    4: Octave("one-lined", 4),
    5: Octave("two-lined", 5),
    6: Octave("three-lined", 6),
    7: Octave("four-lined", 7),
    8: Octave("five-lined", 8),
    9: Octave("six-lined", 9),
}
