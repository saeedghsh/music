# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import csv
import os
from typing import Dict, Tuple

import pytest

from core.frequency import Frequency
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
        notes_names: Dict[int, Dict[int, str]] = {}
        notes_frequency: Dict[int, Dict[int, str]] = {}
        for row in reader:
            string_str, fret_str, name, frequency = row
            string, fret = int(string_str), int(fret_str)
            if string not in notes_names:
                notes_names[string] = {}
                notes_frequency[string] = {}
            notes_names[string][fret] = name
            notes_frequency[string][fret] = frequency
    return notes_names, notes_frequency


def test_generate_tar_strings_against_test_data_file():
    file_name = "test_data_tar_notes_C4-C4-G3-G3-C4-C3_A4_at_440.csv"
    dirpath = "tests/instruments"
    test_data_file_path = os.path.join(dirpath, file_name)
    names_on_file, frequencies_on_file = _load_notes_from_csv(test_data_file_path)
    actual_string_notes = generate_tar_strings(28, Frequency(440))
    for string_number, notes in actual_string_notes.items():
        for fret_number, note in notes.items():
            actual_note_name = f"{note.name}"
            actual_note_frequency = f"{note.frequency.value:.2f}"
            expected_note_name = names_on_file[string_number][fret_number]
            expected_note_frequency = frequencies_on_file[string_number][fret_number]
            assert expected_note_name == actual_note_name
            assert expected_note_frequency == actual_note_frequency


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
