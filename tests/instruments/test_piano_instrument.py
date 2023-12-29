"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

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
    for _, note in keys.items():
        assert note.letter in ["C", "D", "E", "F", "G", "A", "B"], f"Invalid note {note.letter}"
        if note.letter in ["E", "B"]:
            assert (
                note.accidental != "#"
            ), f"Invalid accidental {note.accidental} for note {note.letter}"
    assert len(keys) == expected_keys_count, f"Expected {expected_keys_count} keys, got {len(keys)}"


def test_generate_piano_keys_invalid_range():
    with pytest.raises(ValueError):
        generate_piano_keys((3, 2), a4_frequency=1)  # Start is greater than end


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
