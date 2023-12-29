"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.notation import compute_frequency
from instruments.piano_instrument import generate_piano_keys


@pytest.mark.parametrize(
    "octave_range, expected_keys_count, a4_frequency",
    [
        ((0, 1), 12, 440),  # 12 keys in one octave
        ((1, 3), 24, 440),  # 24 keys in two octaves
        ((1, 3), 24, 100),  # different a4_frequency
    ],
)
def test_generate_piano_keys(octave_range, expected_keys_count, a4_frequency):
    keys = generate_piano_keys(octave_range, a4_frequency)
    assert len(keys) > 0, "No keys generated"
    for key, freq in keys.items():
        assert len(key) == 3
        note, accidental, octave = key

        assert note in ["C", "D", "E", "F", "G", "A", "B"], f"Invalid note {note}"
        if note in ["E", "B"]:
            assert accidental != "#", f"Invalid accidental {accidental} for note {note}"

        expected_frequency = compute_frequency(note, accidental, octave, a4_frequency)
        assert (
            freq == expected_frequency
        ), f"Incorrect frequency for {key}: {freq} vs {expected_frequency}"
    assert len(keys) == expected_keys_count, f"Expected {expected_keys_count} keys, got {len(keys)}"


def test_generate_piano_keys_invalid_range():
    with pytest.raises(ValueError):
        generate_piano_keys((3, 2), a4_frequency=1)  # Start is greater than end


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
