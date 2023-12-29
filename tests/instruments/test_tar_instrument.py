"""Test Tar entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.notation import transposition_by_an_octave
from instruments.tar_instrument import tar_string


@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_tar_string_valid_fret_counts(fret_count):
    result = tar_string(fret_count=fret_count, string_number=1, a4_frequency=440)
    assert isinstance(result, dict)


@pytest.mark.parametrize("fret_count", [24, 26, 29])
def test_tar_string_invalid_fret_counts(fret_count):
    with pytest.raises(ValueError):
        tar_string(fret_count=fret_count, string_number=1, a4_frequency=440)


@pytest.mark.parametrize("string_number", [0, 7])
def test_tar_string_invalid_string_numbers(string_number):
    with pytest.raises(ValueError):
        tar_string(fret_count=27, string_number=string_number, a4_frequency=440)


def test_tar_string_sixth_string_transposition():
    base_notes = tar_string(fret_count=27, string_number=1, a4_frequency=440)
    transposed_notes = tar_string(fret_count=27, string_number=6, a4_frequency=440)

    for fret, note in base_notes.items():
        expected_transposed_note = transposition_by_an_octave(note)
        assert (
            transposed_notes[fret] == expected_transposed_note
        ), f"Incorrect transposition for fret {fret}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
