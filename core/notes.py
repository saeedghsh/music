"""Musical note and utils"""
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple, Union

from core.accidentals import Accidental
from core.frequency import Frequency
from core.intervals import MusicalInterval
from core.octaves import Octave

STANDARD_NOTES = {
    "natural": [
        "C",
        "D",
        "E",
        "F",
        "G",
        "A",
        "B",
    ],
    "semitone": [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ],
    "quartertone": [
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
    ],
}


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


def _letter_accidental_standard(letter_accidental: str) -> str:
    return CONVERSION_TO_STANDARD_NOTE.get(letter_accidental, letter_accidental)


def _index_in_standard_notes_list(letter_accidental: str) -> int:
    # pylint: disable=fixme
    # TODO: currently only supports standard notes with quartertone
    letter_accidental_standard = _letter_accidental_standard(letter_accidental)
    return STANDARD_NOTES["quartertone"].index(f"{letter_accidental_standard}")


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
    letter_accidental = list(name[: -len(str(octave))])
    letter = _pop_first(letter_accidental)
    _validate_letter(letter)
    accidental_symbol = _pop_first(letter_accidental)
    accidental = Accidental.from_symbol(accidental_symbol)
    if len(letter_accidental) != 0:
        raise ValueError(f"name (wo octave) cannot be more that 2 char: {letter_accidental}")
    return letter, accidental, octave


def _standardize_note(
    letter: str, accidental: Accidental, octave: Octave
) -> Tuple[str, Accidental, Octave]:
    """Return a standard note, given any input note

    Makes sure that the note belong set of "standard notes"
    """
    _ = _decompose_name(f"{letter}{accidental}{octave}")  # Validate name correctness
    letter_accidental = f"{letter}{accidental}"
    new_octave = octave + 1 if letter_accidental == "B#" else octave
    letter_accidental_standard = _letter_accidental_standard(letter_accidental)
    if len(letter_accidental_standard) == 1:
        new_letter, new_accidental = letter_accidental_standard, ""
    if len(letter_accidental_standard) == 2:
        new_letter, new_accidental = letter_accidental_standard[0], letter_accidental_standard[1]
    return new_letter, Accidental.from_symbol(new_accidental), new_octave


def _compute_frequency(
    letter: str, accidental: Accidental, octave: Octave, a4_frequency: Frequency
) -> Frequency:
    """Calculate the frequency of a note."""
    # pylint: disable=invalid-name
    letter, accidental, octave = _standardize_note(letter, accidental, octave)
    note_index = _index_in_standard_notes_list(f"{letter}{accidental}")
    A_index = _index_in_standard_notes_list("A")
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

    def __add__(self, other: Any) -> "Note":
        """Return a Note that is the transposed version of self by the specified interval"""
        if not isinstance(other, MusicalInterval):
            raise NotImplementedError(f"Type {type(other)} is not supported")

        if other == MusicalInterval.OCTAVE:
            quartertone_steps = 24
        if other == MusicalInterval.TONE:
            quartertone_steps = 4
        if other == MusicalInterval.SEMITONE:
            quartertone_steps = 2
        if other == MusicalInterval.QUARTERTONE:
            quartertone_steps = 1

        note_index = _index_in_standard_notes_list(f"{self.letter}{self.accidental}")
        if note_index + quartertone_steps >= len(STANDARD_NOTES["quartertone"]):
            new_octave = self.octave + 1
        else:
            new_octave = self.octave
        new_note_index = (note_index + quartertone_steps) % len(STANDARD_NOTES["quartertone"])
        new_name = f"{STANDARD_NOTES['quartertone'][new_note_index]}{new_octave.number}"
        new_letter, new_accidental, _ = _decompose_name(new_name)
        # computing the frequency this way has the advantage that it will be tested against
        # the _compute_frequency approach executed in the __post_init__
        frequency_ratio = MusicalInterval.QUARTERTONE.value**quartertone_steps
        new_frequency = Frequency(self.frequency.value * frequency_ratio)
        return Note(
            new_name, new_letter, new_accidental, new_octave, new_frequency, self.a4_frequency
        )


def standard_notes(mode: str, octave: Octave, a4_frequency: Frequency) -> List[Note]:
    """Return a list of standard notes"""
    if mode not in STANDARD_NOTES:
        raise ValueError(f"mode is not supported: {mode}")
    return [Note.from_name(f"{name}{octave.number}", a4_frequency) for name in STANDARD_NOTES[mode]]
