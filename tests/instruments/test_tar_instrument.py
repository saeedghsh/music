# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import csv
import os
from typing import Dict, Tuple

import pytest

from core.frequency import Frequency
from core.notes import Note
from instruments.tar_instrument import generate_tar_string, generate_tar_strings

A4_FREQUENCY = Frequency(440)


@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_generate_tar_string_valid_fret_counts(fret_count: int):
    result = generate_tar_string(fret_count=fret_count, string_number=1, a4_frequency=A4_FREQUENCY)
    assert isinstance(result, dict)


@pytest.mark.parametrize("fret_count", [24, 26, 29])
def test_generate_tar_string_invalid_fret_counts(fret_count: int):
    with pytest.raises(ValueError):
        generate_tar_string(fret_count=fret_count, string_number=1, a4_frequency=A4_FREQUENCY)


@pytest.mark.parametrize("string_number", [0, 7])
def test_generate_tar_string_invalid_string_numbers(string_number: int):
    with pytest.raises(ValueError):
        generate_tar_string(fret_count=27, string_number=string_number, a4_frequency=A4_FREQUENCY)


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


def test_generate_tar_strings_against_test_data_file():
    file_name = "test_data_tar_notes_C4-C4-G3-G3-C4-C3_A4_at_440.csv"
    dirpath = "tests/instruments"
    test_data_file_path = os.path.join(dirpath, file_name)
    expected_notes, expected_frequencies = _load_notes_from_csv(test_data_file_path)
    actual_notes = generate_tar_strings(28, A4_FREQUENCY)
    for string_number, notes in actual_notes.items():
        for fret_number, actual_note in notes.items():
            assert actual_note == expected_notes[string_number][fret_number]
            assert actual_note.frequency == expected_frequencies[string_number][fret_number]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
