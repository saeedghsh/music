# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import csv
import os
from typing import Dict, Tuple

import pytest

from core.frequency import Frequency
from core.notes import Note
from instruments.tar_instrument import tar_string

A4_FREQUENCY = Frequency(440)


def _load_notes_from_csv(filename: str) -> Tuple[dict, dict]:
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        notes: Dict[int, Dict[int, Note]] = {}
        frequencies: Dict[int, Dict[int, Frequency]] = {}
        for row in reader:
            string = int(row[0])
            fret = int(row[1])
            note = Note.from_name(row[2], A4_FREQUENCY)
            frequency = Frequency(float(row[3]))
            if string not in notes:
                notes[string] = {}
                frequencies[string] = {}
            notes[string][fret] = note
            frequencies[string][fret] = frequency
    return notes, frequencies


@pytest.mark.parametrize("base", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_strings(fret_count: int, base: str, a4_frequency: float):
    base_note = Note.from_name(base, Frequency(a4_frequency))
    result = tar_string(base_note, fret_count)
    assert isinstance(result, dict)
    assert len(result) == fret_count + 1
    assert result[0] == base_note


@pytest.mark.parametrize("fret_count", [24, 26, 29])
def test_tar_string_invalid_fret_counts(fret_count: int):
    base_note = Note.from_name("C4", A4_FREQUENCY)
    with pytest.raises(ValueError):
        tar_string(base_note, fret_count)


def test_tar_string_against_test_data_file():
    file_name = "test_data_tar_notes_C4-C4-G3-G3-C4-C3_A4_at_440.csv"
    dirpath = "tests/instruments"
    test_data_file_path = os.path.join(dirpath, file_name)
    string_to_base_map = {1: "C4", 2: "C4", 3: "G3", 4: "G3", 5: "C4", 6: "C3"}
    expected_notes, expected_frequencies = _load_notes_from_csv(test_data_file_path)
    for string_number, notes in expected_notes.items():
        actual_base_note = Note.from_name(string_to_base_map[string_number], A4_FREQUENCY)
        actual_notes = tar_string(actual_base_note, fret_count=28)
        for fret_number, expected_note in notes.items():
            expected_frequency = expected_frequencies[string_number][fret_number]
            actual_note = actual_notes[fret_number]
            assert actual_note == expected_note
            assert actual_note.frequency == expected_frequency


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
