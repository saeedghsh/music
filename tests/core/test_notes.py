"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.frequency import Frequency
from core.notes import (
    Note,
    _decompose_note_name,
    _standardize_note,
    transposition_by_an_octave,
)

A4_FREQUENCY = Frequency(440)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("A4", ("A", "", 4)),
        ("G#3", ("G", "#", 3)),
        ("Fs2", ("F", "s", 2)),
        ("Dk-1", ("D", "k", -1)),
        ("Cb9", ("C", "b", 9)),
    ],
)
def test_decompose_note_name_valid(name, expected):
    assert _decompose_note_name(name) == expected, f"Incorrect decomposition for {name}"


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
def test_decompose_note_name_invalid(name):
    with pytest.raises(ValueError):
        _decompose_note_name(name)


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
    "letter, accidental, octave, expected",
    [
        ("E", "#", 4, ("F", "", 4)),
        ("B", "#", 3, ("C", "", 4)),  # Note octave change
        ("C", "b", 2, ("B", "", 2)),
        ("F", "k", 5, ("E", "s", 5)),
    ],
)
def test_standardize_note(letter, accidental, octave, expected):
    assert (
        _standardize_note(letter, accidental, octave) == expected
    ), f"Incorrect standardization for {letter}{accidental}{octave}"


@pytest.mark.parametrize(
    "letter, accidental, octave",
    [
        ("H", "", 4),  # Invalid letter
        ("C", "##", 3),  # Invalid accidental
        ("D", "s", -2),  # Invalid octave, assuming -1 to 9 is valid
    ],
)
def test_standardize_note_invalid(letter, accidental, octave):
    with pytest.raises(ValueError):
        _standardize_note(letter, accidental, octave)


def test_note_creation():
    note = Note("A4", "A", "", 4, A4_FREQUENCY, A4_FREQUENCY)
    assert note.name == "A4"
    assert note.letter == "A"
    assert note.accidental == ""
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
def test_note_from_name(a4_frequency):
    note = Note.from_name("A4", a4_frequency)
    assert note.name == "A4"
    assert note.frequency == a4_frequency


def test_note_eq():
    note1 = Note("A4", "A", "", 4, A4_FREQUENCY, A4_FREQUENCY)
    note2 = Note.from_name("A4", A4_FREQUENCY)
    note3 = Note("B4", "B", "", 4, Frequency(493.8833012561241), A4_FREQUENCY)
    assert note1 == note2
    assert note1 != note3
    assert note1 == "A4"
    assert note1 != "B4"
    assert note1 == 440.0
    assert note1 != 493.88


def test_note_eq_unsupported():
    note = Note("A4", "A", "", 4, A4_FREQUENCY, A4_FREQUENCY)
    with pytest.raises(NotImplementedError):
        # pylint: disable=pointless-statement
        # pylint: disable=use-implicit-booleaness-not-comparison
        note == {}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
