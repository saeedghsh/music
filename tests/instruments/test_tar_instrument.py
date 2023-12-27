"""Test Tar entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.notation import (
    compute_frequency,
    decompose_note_name,
    transposition_by_an_octave,
)
from instruments.tar_instrument import generate_tar_notes, print_string_notes


def test_print_string_notes(mocker):
    mocked_print = mocker.patch("builtins.print")
    string_notes = {
        0: "E4",
        1: "F4",
    }
    expected_calls = [
        (0, "E4", compute_frequency(*decompose_note_name("E4"))),
        (1, "F4", compute_frequency(*decompose_note_name("F4"))),
    ]
    print_string_notes(string_notes)
    assert mocked_print.call_count == len(expected_calls)
    for call, (fret_number, note_name, frequency) in zip(
        mocked_print.call_args_list, expected_calls
    ):
        args, _ = call
        expected_string = f"{fret_number}\t{note_name}:\t{frequency} Hz"
        assert (
            args[0] == expected_string
        ), f"Expected print: '{expected_string}', but got: '{args[0]}'"


@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_generate_tar_notes_valid_fret_counts(fret_count):
    result = generate_tar_notes(fret_count=fret_count, string_number=1)
    assert isinstance(result, dict)


@pytest.mark.parametrize("fret_count", [24, 26, 29])
def test_generate_tar_notes_invalid_fret_counts(fret_count):
    with pytest.raises(ValueError):
        generate_tar_notes(fret_count=fret_count, string_number=1)


@pytest.mark.parametrize("string_number", [0, 7])
def test_generate_tar_notes_invalid_string_numbers(string_number):
    with pytest.raises(ValueError):
        generate_tar_notes(fret_count=27, string_number=string_number)


def test_generate_tar_notes_sixth_string_transposition():
    base_notes = generate_tar_notes(fret_count=27, string_number=1)
    transposed_notes = generate_tar_notes(fret_count=27, string_number=6)

    for fret, note in base_notes.items():
        expected_transposed_note = transposition_by_an_octave(note)
        assert (
            transposed_notes[fret] == expected_transposed_note
        ), f"Incorrect transposition for fret {fret}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
