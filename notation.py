"""X"""
from typing import Any, Tuple
from dataclasses import dataclass
from math import isclose
from functools import wraps

A4_FREQUENCY = 440  # Note reference: A4 = 440 Hz


# In this context a set of "standard notes" is defined as the following.
# An equal temperament tuning system, where the octave is divided into 24 equal
# parts (quadranttone), results in 24 notes. A set of "standard notes of
# quadranttones" is a set that maps bijectively to corresponding frequencies.
# * where "sharp" of a note and "flat" of another are the same note, opt for "sharp"
# * where "koron" of a note and "sori" of another are the same note, opt for "sori"
# * "E#" and "B#" are not considered as they are represented by "F" and "C"
STANDARD_NOTES_QUADRANTTONES = [
    "C",
    "Cs",
    "C#",
    "Dk",
    "D",
    "Ds",
    "D#",
    "Ek",
    "E",
    "Es",
    "F",
    "Fs",
    "F#",
    "Gk",
    "G",
    "Gs",
    "G#",
    "Ak",
    "A",
    "As",
    "A#",
    "Bk",
    "B",
    "Bs",
]


def _upper_lower_args(func):
    @wraps(func)
    def wrapper(note: str, accidental: str, octave: int) -> float:
        return func(note.upper(), accidental.lower(), octave)

    return wrapper


@_upper_lower_args
def _standardize_note(letter: str, accidental: str, octave: int) -> Tuple[str, int]:
    """Return a standard note, given any input note

    Makes sure that the note belong set of "standard notes"
    """
    conversion = {
        "E#": "F",
        "B#": "C",
        "Cb": "B",
        "Fb": "E",
        "Db": "C#",
        "Eb": "D#",
        "Gb": "F#",
        "Ab": "G#",
        "Bb": "A#",
        "Ck": "Bs",
        "Fk": "Es",
    }
    note = f"{letter}{accidental}"
    if note == "B#":
        octave += 1
    if note in conversion:
        note = conversion[note]
    # conversion.get(note, note)

    if len(note) == 1:
        letter, accidental = note, ""
    if len(note) == 2:
        letter, accidental = note[0], note[1]
    return letter, accidental, octave


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
    octave: int
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
    def compute_frequency(
        letter: str, accidental: str, octave: int, a4_frequency: float = A4_FREQUENCY
    ) -> float:
        """Calculate the frequency of a note."""
        # pylint: disable=invalid-name
        letter, accidental, octave = _standardize_note(letter, accidental, octave)
        note_index = STANDARD_NOTES_QUADRANTTONES.index(f"{letter}{accidental}")
        A_index = STANDARD_NOTES_QUADRANTTONES.index("A")
        quadranttone_steps_from_A4 = note_index - A_index + (octave - 4) * 24
        return a4_frequency * (2 ** (quadranttone_steps_from_A4 / 24))

    @staticmethod
    def transposition_by_an_octave(note_name: str) -> str:
        letter, accidental, octave = Note.decompose_name(note_name)
        new_octave = octave + 1
        return f"{letter}{accidental}{new_octave}"

    @staticmethod
    def decompose_name(name: str) -> Tuple[str, str, int]:
        """Return letter, accidental and octave from the name

        It also validates the name correctness thouroughly.
        """
        if not name[-1].isdigit():
            raise ValueError(f"Octave must be an number/int - note:{name}")
        octave = int(name[-1])
        if not -1 <= octave <= 9:
            raise ValueError(f"octave is out of range - note:{name}, octave:{octave}")

        if len(name[:-1]) == 1:
            letter, accidental = name[0].upper(), ""
        elif len(name[:-1]) == 2:
            letter, accidental = name[0].upper(), name[1].lower()
        else:
            raise ValueError(f"name cannot be more that 3 characters - note:{name}")

        if letter not in ["A", "B", "C", "D", "E", "F", "G"]:
            raise ValueError(f"invalid letter - note:{name}, letter:{letter}")
        if accidental not in ["#", "s", "", "k", "b"]:
            raise ValueError(
                f"invalid accidental - note:{name}, accidental:{accidental}"
            )

        return letter, accidental, octave

    @staticmethod
    def from_name(name: str, a4_frequency: float = A4_FREQUENCY) -> "Note":
        """Create and return an object of type Note from the given name"""
        letter, accidental, octave = Note.decompose_name(name)
        frequency = Note.compute_frequency(letter, accidental, octave, a4_frequency)
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
