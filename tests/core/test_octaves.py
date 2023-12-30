# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Union

import pytest

from core.octaves import Octave, OctaveRegister


def test_octave_creation():
    octave = Octave("great", 2)
    assert octave.name == "great"
    assert octave.number == 2


def test_octave_str_repr():
    octave = Octave("great", 2)
    assert str(octave) == "2"
    assert repr(octave) == "octave 2 great"


@pytest.mark.parametrize(
    "other, expected",
    [
        ("great", True),
        ("small", False),
        (2, True),
        (3, False),
        (Octave("great", 2), True),
        (Octave("small", 3), False),
    ],
)
def test_octave_eq(other: Union[str, int, Octave], expected: bool):
    octave = Octave("great", 2)
    assert (octave == other) == expected, f"Incorrect equality comparison with {other}"


def test_octave_eq_unsupported():
    octave = Octave("great", 2)
    with pytest.raises(NotImplementedError):
        octave == float(2)  # pylint: disable=expression-not-assigned


def test_octave_register():
    assert OctaveRegister.GREAT.value == Octave("great", 2)
    assert OctaveRegister.SMALL.value.number == 3


def test_octave_register_validate():
    for octave in range(-1, 10):
        OctaveRegister.validate(octave)
    for octave in range(10, 20):
        with pytest.raises(ValueError):
            OctaveRegister.validate(octave)
    for octave in range(-10, -2):
        with pytest.raises(ValueError):
            OctaveRegister.validate(octave)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
