# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import string
from typing import Any, Tuple

import pytest

from core.accidentals import Accidental
from core.frequency import Frequency
from core.notes import (
    STANDARD_NOTES,
    Note,
    _decompose_name,
    _standardize_note,
    _validate_letter,
    standard_notes,
    transposition_by_an_octave,
)
from core.octaves import Octave

A4_FREQUENCY = Frequency(440)


@pytest.mark.parametrize("letter", ["A", "B", "C", "D", "E", "F", "G"])
def test_validate_letter(letter: str):
    _validate_letter(letter)


@pytest.mark.parametrize("letter", list(string.ascii_letters.replace("ABCDEFG", "")))
def test_validate_letter_fail(letter: str):
    with pytest.raises(ValueError):
        _validate_letter(letter)


@pytest.mark.parametrize(
    "actual_name, expected_name, expected_accidental, expected_octave",
    [
        ("A4", "A", Accidental.from_symbol(""), 4),
        ("G#3", "G", Accidental.from_symbol("#"), 3),
        ("Fs2", "F", Accidental.from_symbol("s"), 2),
        ("Dk-1", "D", Accidental.from_symbol("k"), -1),
        ("Cb9", "C", Accidental.from_symbol("b"), 9),
    ],
)
def test_decompose_name_valid(
    actual_name: str, expected_name: str, expected_accidental: Accidental, expected_octave: int
):
    name, accidental, octave = _decompose_name(actual_name)
    assert name == expected_name, f"Incorrect name decomposition for {actual_name}"
    assert (
        accidental == expected_accidental
    ), f"Incorrect accidental decomposition for {actual_name}"
    assert octave == expected_octave, f"Incorrect octave decomposition for {actual_name}"


@pytest.mark.parametrize(
    "name",
    [
        "H2",  # Invalid letter
        "G#10",  # Octave out of range
        "D##4",  # Invalid accidental
        "D^3",  # Invalid accidental
        "8A",  # Incorrect format
        "Csharp4",  # Incorrect accidental format
    ],
)
def test_decompose_name_invalid(name: str):
    with pytest.raises(ValueError):
        _decompose_name(name)


@pytest.mark.parametrize("a4_frequency", [Frequency(100), Frequency(250), Frequency(440)])
@pytest.mark.parametrize(
    "actual_note_name, expected_note_name",
    [("A4", "A5"), ("G#3", "G#4"), ("Fs2", "Fs3"), ("Dk-1", "Dk0")],
)
def test_transposition_by_an_octave(
    actual_note_name: str, expected_note_name: str, a4_frequency: Frequency
):
    actual_note = Note.from_name(actual_note_name, a4_frequency)
    expected_note = Note.from_name(expected_note_name, a4_frequency)

    assert (
        transposition_by_an_octave(actual_note) == expected_note
    ), f"Incorrect transposition for {actual_note}"


@pytest.mark.parametrize(
    "actual, expected",
    [
        (("E", "#", 4), ("F", "", 4)),
        (("B", "#", 3), ("C", "", 4)),  # Note octave change in the next item
        (("C", "b", 2), ("B", "", 2)),
        (("F", "k", 5), ("E", "s", 5)),
    ],
)
def test_standardize_note(actual: Tuple[str, str, int], expected: Tuple[str, str, int]):
    letter = actual[0]
    accidental = Accidental.from_symbol(actual[1])
    octave = Octave.from_number(actual[2])
    assert (
        _standardize_note(letter, accidental, octave) == expected
    ), f"Incorrect standardization for {letter}{accidental}{octave}"


def test_note_creation():
    note = Note("A4", "A", Accidental.from_symbol(""), 4, A4_FREQUENCY, A4_FREQUENCY)
    assert note.name == "A4"
    assert note.letter == "A"
    assert note.accidental == ""
    assert note.accidental == Accidental.from_name("natural")
    assert note.octave == 4
    assert note.frequency == 440.0


def test_note_creation_fail():
    with pytest.raises(ValueError):
        Note("A4", "B", "", 4, Frequency(440.0), A4_FREQUENCY)
    with pytest.raises(ValueError):
        Note("A4", "A", "#", 4, Frequency(440.0), A4_FREQUENCY)
    with pytest.raises(ValueError):
        Note("A4", "A", "", 5, Frequency(440.0), A4_FREQUENCY)
    with pytest.raises(ValueError):
        Note("A4", "A", "", 4, Frequency(430.0), A4_FREQUENCY)
    with pytest.raises(ValueError):
        Note("A4", "A", "", 4, Frequency(440.0), A4_FREQUENCY * 2)


def test_note_str_repr():
    note = Note.from_name("A4", A4_FREQUENCY)
    assert str(note) == "A4"
    assert "A4: 440.0 Hz" in repr(note)


@pytest.mark.parametrize("a4_frequency", [Frequency(10), Frequency(100), Frequency(440)])
def test_note_from_name(a4_frequency: Frequency):
    note = Note.from_name("A4", a4_frequency)
    assert note.name == "A4"
    assert note.frequency == a4_frequency


def test_note_eq():
    note1 = Note("A4", "A", "", 4, A4_FREQUENCY, A4_FREQUENCY)
    note2 = Note.from_name("A4", A4_FREQUENCY)
    note3 = Note("B4", "B", "", 4, Frequency(493.8833012561241), A4_FREQUENCY)
    assert note1 == note2
    assert note1 != note3
    assert note1 == 440.0
    assert note1 == Frequency(440.0)
    assert note1 != 493.88
    assert note1 != Frequency(493.88)


@pytest.mark.parametrize("note_unsupported_type", [{}, "A4"])
def test_note_eq_unsupported(note_unsupported_type: Any):
    note = Note(
        "A4", "A", Accidental.from_symbol(""), Octave.from_number(4), A4_FREQUENCY, A4_FREQUENCY
    )
    with pytest.raises(NotImplementedError):
        # pylint: disable=pointless-statement
        # pylint: disable=use-implicit-booleaness-not-comparison
        note == note_unsupported_type


@pytest.mark.parametrize("mode", ["natural", "semitone", "quartertone"])
@pytest.mark.parametrize("octave", [Octave.from_number(0), Octave.from_number(8)])
def test_standard_notes(mode: str, octave: Octave):
    names = STANDARD_NOTES[mode]
    notes = standard_notes(mode, octave, A4_FREQUENCY)
    assert len(names) == len(notes)
    for note in notes:
        assert note.octave == octave
        assert f"{note.letter}{note.accidental.symbol.simplified}" in names


def test_standard_notes_invalid_mode():
    with pytest.raises(ValueError):
        standard_notes("wrong_mode", Octave.from_number(0), A4_FREQUENCY)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
