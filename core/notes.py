"""Musical note and utils"""
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple, Union

from core.accidentals import Accidental
from core.frequency import Frequency
from core.intervals import MusicalInterval
from core.octaves import Octave

STANDARD_NOTES_QUARTERTONE = [
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

CONVERSION_TO_STANDARD_NOTE = {
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


def _trailing_number(s: str) -> int:
    """Return an integer from the end of a string."""
    match = re.search(r"-?\d+$", s)
    if match:
        return int(match.group())
    raise ValueError(f"No integer found at the end of '{s}'")


def _validate_letter(letter: str):
    """validates that the note letter is valid"""
    if letter not in ["A", "B", "C", "D", "E", "F", "G"]:
        raise ValueError(f"Invalid note letter: {letter}")


def _decompose_name(name: str) -> Tuple[str, Accidental, Octave]:
    """Return (letter, accidental, octave) from the name

    It validates the name correctness.
    """
    # pylint: disable=fixme
    # TODO: B#9 is technically out of range, but this function does not notice it!

    def _pop_first(lst: list) -> str:
        return lst.pop(0) if len(lst) > 0 else ""

    octave = Octave.from_number(_trailing_number(name))

    name_wo_octave = list(name[: -len(str(octave))])

    letter = _pop_first(name_wo_octave)
    _validate_letter(letter)

    accidental_symbol = _pop_first(name_wo_octave)
    accidental = Accidental.from_symbol(accidental_symbol)

    if len(name_wo_octave) != 0:
        raise ValueError(f"name (wo octave) cannot be more that 2 char: {name_wo_octave}")

    return letter, accidental, octave


def _standardize_note(
    letter: str, accidental: Accidental, octave: Octave
) -> Tuple[str, Accidental, Octave]:
    """Return a standard note, given any input note

    Makes sure that the note belong set of "standard notes"
    """
    _ = _decompose_name(f"{letter}{accidental}{octave}")  # Validate name correctness

    name_wo_octave = f"{letter}{accidental}"
    new_octave = octave + 1 if name_wo_octave == "B#" else octave
    name_wo_octave_standard = CONVERSION_TO_STANDARD_NOTE.get(name_wo_octave, name_wo_octave)

    if len(name_wo_octave_standard) == 1:
        new_letter, new_accidental = name_wo_octave_standard, ""
    if len(name_wo_octave_standard) == 2:
        new_letter, new_accidental = name_wo_octave_standard[0], name_wo_octave_standard[1]

    return new_letter, Accidental.from_symbol(new_accidental), new_octave


def _compute_frequency(
    letter: str, accidental: Accidental, octave: Octave, a4_frequency: Frequency
) -> Frequency:
    """Calculate the frequency of a note."""
    # pylint: disable=invalid-name
    letter, accidental, octave = _standardize_note(letter, accidental, octave)
    note_index = STANDARD_NOTES_QUARTERTONE.index(f"{letter}{accidental}")
    A_index = STANDARD_NOTES_QUARTERTONE.index("A")
    quartertone_steps_from_A4 = note_index - A_index + (octave.number - 4) * 24
    return Frequency(a4_frequency.value * (2 ** (quartertone_steps_from_A4 / 24)))


@dataclass
class Note:
    """A representation of musical note with helper functions"""

    # pylint: disable=fixme
    # TODO: Except a4_frequency, all others could be optional at creation (use builder pattern?)

    name: str
    letter: str
    accidental: Accidental
    octave: Octave
    frequency: Frequency
    a4_frequency: Frequency

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}: {self.frequency} Hz"

    def __post_init__(self):
        letter, accidental, octave = _decompose_name(self.name)
        frequency = _compute_frequency(letter, accidental, octave, self.a4_frequency)
        if letter != self.letter:
            raise ValueError(f"Letter does not match the name: {letter} vs {self.name}")
        if accidental != self.accidental:
            raise ValueError(
                f"Accidental does not match the name: {accidental} vs {self.accidental}"
            )
        if octave != self.octave:
            raise ValueError(f"Octave does not match the name: {octave} vs {self.octave}")
        if frequency != self.frequency:
            raise ValueError(f"Frequency does not match the name: {frequency} vs {self.frequency}")

    @staticmethod
    def from_name(name: str, a4_frequency: Frequency) -> "Note":
        """Create and return an object of type Note from the given name"""
        letter, accidental, octave = _decompose_name(name)
        frequency = _compute_frequency(letter, accidental, octave, a4_frequency)
        return Note(name, letter, accidental, octave, frequency, a4_frequency)

    def _eq_to_frequency(self, other_frequency: Union[Frequency, int, float]) -> bool:
        return self.frequency == other_frequency

    def _eq_to_note(self, other: "Note") -> bool:
        return self._eq_to_frequency(other.frequency)

    def __eq__(self, other: Any) -> bool:
        type_dispatch: Dict[type, Callable] = {
            Frequency: self._eq_to_frequency,
            float: self._eq_to_frequency,
            int: self._eq_to_frequency,
            Note: self._eq_to_note,
        }
        other_type = type(other)
        if other_type not in type_dispatch:
            raise NotImplementedError(f"Type {other_type} is not supported for comparison")
        return type_dispatch[other_type](other)


def transposition_by_an_octave(note: Note) -> Note:
    """Transposes a note to an octave higher"""
    new_octave = note.octave + 1
    name = f"{note.letter}{note.accidental}{new_octave}"
    _ = _decompose_name(name)  # Validate name correctness
    frequency = Frequency(note.frequency.value * MusicalInterval.OCTAVE.value)
    return Note(name, note.letter, note.accidental, new_octave, frequency, note.a4_frequency)
