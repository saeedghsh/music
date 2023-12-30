# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Union

import pytest

from core.octaves import Octave, OctaveRegister


def test_octave_creation():
    octave = Octave("great", 2)
    assert octave.name == "great"
    assert octave.number == 2


def test_octave_from_name():
    subsubcontra = Octave.from_name("subsubcontra")
    assert subsubcontra.name == "subsubcontra"
    assert subsubcontra.number == -1
    great = Octave.from_name("great")
    assert great.name == "great"
    assert great.number == 2


def test_octave_from_name_invalid():
    with pytest.raises(ValueError):
        Octave.from_name("wrong_name")


def test_octave_from_number():
    subsubcontra = Octave.from_number(-1)
    assert subsubcontra.name == "subsubcontra"
    assert subsubcontra.number == -1
    great = Octave.from_number(2)
    assert great.name == "great"
    assert great.number == 2


def test_octave_from_number_invalid():
    with pytest.raises(ValueError):
        Octave.from_number(-5)


@pytest.mark.parametrize(
    "name, number",
    [
        ("wrong_name", 0),
        ("small", -5),  # wrong number
        ("small", 0),  # name and number mismatch
    ],
)
def test_octave_creation_invalid(name: str, number: int):
    with pytest.raises(ValueError):
        Octave(name, number)


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


def test_octave_eq_not_implemented():
    octave = Octave("great", 2)
    with pytest.raises(NotImplementedError):
        octave == float(2)  # pylint: disable=expression-not-assigned


def test_octave_add():
    octave_1 = Octave("contra", 1)
    octave_2 = Octave("great", 2)
    octave_9 = Octave("sixlined", 9)
    assert octave_1 + 1 == octave_2
    assert octave_1 + 8 == octave_9
    assert octave_2 + 7 == octave_9


def test_octave_add_not_implemented():
    # pylint: disable=expression-not-assigned, pointless-statement
    octave = Octave("great", 2)
    with pytest.raises(NotImplementedError):
        octave + float(2)
    with pytest.raises(NotImplementedError):
        octave + octave


def test_octave_validate():
    for octave in range(-1, 10):
        Octave.validate(octave)
    for octave in range(10, 20):
        with pytest.raises(ValueError):
            Octave.validate(octave)
    for octave in range(-10, -2):
        with pytest.raises(ValueError):
            Octave.validate(octave)


def test_octave_register():
    assert OctaveRegister.GREAT.value == Octave("great", 2)
    assert OctaveRegister.SMALL.value.number == 3


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
