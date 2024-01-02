# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import csv
import os
import string
from math import isclose
from typing import Any, List, Tuple

import pytest

from core.accidentals import Accidental
from core.frequency import Frequency
from core.intervals import MusicalInterval
from core.notes import (
    STANDARD_NOTES,
    Note,
    _decompose_name,
    _standardize_note,
    _validate_letter,
    frequency_to_note,
    standard_notes,
)
from core.octaves import Octave

IS_CLOSE_ABS_TOL = 1e-10
A4_FREQUENCY = Frequency(440)


def _load_notes_from_csv(filename: str) -> List[Tuple[Note, Frequency]]:
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        return [
            (
                Note.from_name(row[2], A4_FREQUENCY),
                Frequency(float(row[3])),
            )
            for row in reader
        ]


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


@pytest.mark.parametrize("name", ["H2", "G#10", "D##4", "D^3", "8A", "Csharp4"])
def test_decompose_name_invalid(name: str):
    with pytest.raises(ValueError):
        _decompose_name(name)


@pytest.mark.parametrize(
    "actual, expected",
    [
        (("E", "#", 4), ("F", "", 4)),
        (("B", "#", 3), ("C", "", 4)),  # Note octave change
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
        _ = note == note_unsupported_type


@pytest.mark.parametrize("a4_frequency", [Frequency(100), Frequency(250), Frequency(440)])
@pytest.mark.parametrize(
    "added_value, actual_note_name, expected_note_name",
    [
        (MusicalInterval.OCTAVE, "A4", "A5"),
        (MusicalInterval.OCTAVE, "G#3", "G#4"),
        (MusicalInterval.OCTAVE, "Fs2", "Fs3"),
        (MusicalInterval.OCTAVE, "Dk-1", "Dk0"),
        (MusicalInterval.TONE, "A4", "B4"),
        (MusicalInterval.TONE, "B4", "C#5"),
        (MusicalInterval.TONE, "G#3", "A#3"),
        (MusicalInterval.TONE, "Ek2", "Fs2"),
        (MusicalInterval.TONE, "Dk-1", "Ek-1"),
        (MusicalInterval.SEMITONE, "A4", "A#4"),
        (MusicalInterval.SEMITONE, "B6", "C7"),
        (MusicalInterval.SEMITONE, "E6", "F6"),
        (MusicalInterval.QUARTERTONE, "A4", "As4"),
        (MusicalInterval.QUARTERTONE, "Bs6", "C7"),
        (MusicalInterval.QUARTERTONE, "Ek6", "E6"),
    ],
)
def test_note_add(
    added_value: MusicalInterval,
    actual_note_name: str,
    expected_note_name: str,
    a4_frequency: Frequency,
):
    actual_note = Note.from_name(actual_note_name, a4_frequency)
    expected_note = Note.from_name(expected_note_name, a4_frequency)
    assert actual_note + added_value == expected_note


@pytest.mark.parametrize("value_unsupported_type", [Frequency(100), 1, 0.0])
def test_note_add_not_implemented(value_unsupported_type: Any):
    note = Note.from_name("A0", A4_FREQUENCY)
    with pytest.raises(NotImplementedError):
        _ = note + value_unsupported_type


@pytest.mark.parametrize("a4_frequency", [Frequency(10), Frequency(100), Frequency(440)])
def test_note_from_name(a4_frequency: Frequency):
    note = Note.from_name("A4", a4_frequency)
    assert note.name == "A4"
    assert note.frequency == a4_frequency


@pytest.mark.parametrize("expected_frequency_distance", [-1.0, -0.5, 0.25, 1.0, 1.5])
def test_note_frequency_difference(expected_frequency_distance: float):
    file_name = "test_data_tar_notes_C4-C4-G3-G3-C4-C3_A4_at_440.csv"
    dirpath = "tests/instruments"
    test_data_file_path = os.path.join(dirpath, file_name)
    for note, frequency in _load_notes_from_csv(test_data_file_path):
        actual_frequency_distance = note.frequency_difference(
            Frequency(frequency.value - expected_frequency_distance)
        )
        assert isclose(
            actual_frequency_distance, expected_frequency_distance, abs_tol=IS_CLOSE_ABS_TOL
        )


@pytest.mark.parametrize("value_unsupported_type", [int(1), float(0.0)])
def test_note_frequency_difference_not_implemented(value_unsupported_type: Any):
    note = Note.from_name("A4", A4_FREQUENCY)
    with pytest.raises(NotImplementedError):
        _ = note.frequency_difference(value_unsupported_type)


@pytest.mark.parametrize("mode", ["natural", "semitone", "quartertone"])
@pytest.mark.parametrize("octave", [Octave.from_number(0), Octave.from_number(8)])
def test_standard_notes(mode: str, octave: Octave):
    names = STANDARD_NOTES[mode]
    notes = standard_notes(mode, octave, A4_FREQUENCY)
    assert len(names) == len(notes)
    for note in notes:
        assert note.octave == octave
        assert f"{note.letter}{str(note.accidental)}" in names


def test_standard_notes_invalid_mode():
    with pytest.raises(ValueError):
        standard_notes("wrong_mode", Octave.from_number(0), A4_FREQUENCY)


@pytest.mark.parametrize("frequency_error", [-1.0, -0.5, 0.25, 1.0, 1.5])
def test_frequency_to_note_quartertone(frequency_error: float):
    file_name = "test_data_tar_notes_C4-C4-G3-G3-C4-C3_A4_at_440.csv"
    dirpath = "tests/instruments"
    test_data_file_path = os.path.join(dirpath, file_name)
    for expected_note, expected_frequency in _load_notes_from_csv(test_data_file_path):
        actual_frequency = Frequency(expected_frequency.value + frequency_error)
        actual_note = frequency_to_note(actual_frequency, A4_FREQUENCY)
        assert expected_note == actual_note
        frequency_distance = actual_note.frequency_difference(actual_frequency)
        assert isclose(frequency_distance, -frequency_error, abs_tol=IS_CLOSE_ABS_TOL)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
