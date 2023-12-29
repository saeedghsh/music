"""Test Tar entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.frequency import Frequency
from core.notation import transposition_by_an_octave
from instruments.tar_instrument import generate_tar_string

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


def test_generate_tar_string_sixth_string_transposition():
    base_notes = generate_tar_string(fret_count=27, string_number=1, a4_frequency=A4_FREQUENCY)
    transposed_notes = generate_tar_string(
        fret_count=27, string_number=6, a4_frequency=A4_FREQUENCY
    )

    for fret, note in base_notes.items():
        expected_transposed_note = transposition_by_an_octave(note)
        assert (
            transposed_notes[fret] == expected_transposed_note
        ), f"Incorrect transposition for fret {fret}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
