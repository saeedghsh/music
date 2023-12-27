"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.notation import compute_frequency
from instruments.piano_instrument import generate_piano_keys


def test_generate_piano_keys_default():
    keys = generate_piano_keys()
    assert len(keys) > 0, "No keys generated"
    for key, freq in keys.items():
        assert len(key) == 3
        note, accidental, octave = key

        assert note in ["C", "D", "E", "F", "G", "A", "B"], f"Invalid note {note}"
        if note in ["E", "B"]:
            assert accidental != "#", f"Invalid accidental {accidental} for note {note}"

        expected_frequency = compute_frequency(note, accidental, octave)
        assert (
            freq == expected_frequency
        ), f"Incorrect frequency for {key}: {freq} vs {expected_frequency}"


@pytest.mark.parametrize(
    "octave_range, expected_count",
    [
        ((0, 1), 12),  # 12 keys in one octave
        ((1, 3), 24),  # 24 keys in two octaves
    ],
)
def test_generate_piano_keys_ranges(octave_range, expected_count):
    keys = generate_piano_keys(octave_range)
    assert len(keys) == expected_count, f"Expected {expected_count} keys, got {len(keys)}"


def test_generate_piano_keys_invalid_range():
    with pytest.raises(ValueError):
        generate_piano_keys((3, 2))  # Start is greater than end


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
