# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Any, Union

import pytest

from core.accidentals import Accidental, AccidentalNote
from core.intervals import MusicalInterval
from core.symbols import Symbol


def test_accidental_creation():
    accidental = Accidental("test", Symbol("x", "\u0041"), 1.5)
    assert accidental.name == "test"
    assert accidental.symbol.simplified == "x"
    assert accidental.frequency_ratio == 1.5
    assert str(accidental) == "x"


def test_accidental_creation_fail():
    with pytest.raises(ValueError):
        Accidental.from_name("wrong_name")
    with pytest.raises(ValueError):
        Accidental.from_symbol("%")


def test_accidental_comparison():
    # pylint: disable=pointless-statement
    AccidentalNote.SHARP.value == "sharp"
    AccidentalNote.SHARP.value == "#"
    AccidentalNote.SORI.value == "sori"
    AccidentalNote.SORI.value == "s"
    AccidentalNote.NATURAL.value == "natural"
    AccidentalNote.NATURAL.value == ""
    AccidentalNote.KORON.value == "koron"
    AccidentalNote.KORON.value == "k"
    AccidentalNote.FLAT.value == "flat"
    AccidentalNote.FLAT.value == "b"


def test_accidental_comparison_not_implemented():
    with pytest.raises(NotImplementedError):
        AccidentalNote.SHARP.value == 0  # pylint: disable=pointless-statement


def test_accidental_note_enum():
    sharp = AccidentalNote.SHARP.value
    assert isinstance(sharp, Accidental)
    assert sharp.name == "sharp"
    assert sharp.symbol == Symbol("#", "\u266F")
    assert sharp.frequency_ratio == MusicalInterval.SEMITONE.value


@pytest.mark.parametrize(
    "accidental",
    [
        Accidental("sharp", Symbol("#", "\u266F"), MusicalInterval.SEMITONE.value),
        "#",
        "sharp",
        "s",
        "sori",
        "",
        "natural",
        "k",
        "koron",
        "b",
        "flat",
    ],
)
def test_accidental_note_enum_validate_pass(accidental: Union[str, Accidental]):
    AccidentalNote.validate(accidental)


@pytest.mark.parametrize(
    "accidental",
    [
        "*",
        "sharp__",
        Accidental("un", Symbol("%", "xyz"), MusicalInterval.SEMITONE.value),
    ],
)
def test_accidental_note_enum_validate_fail(accidental: Any):
    with pytest.raises(ValueError):
        AccidentalNote.validate(accidental)


def test_accidental_note_enum_validate_note_implemented():
    with pytest.raises(NotImplementedError):
        AccidentalNote.validate(1)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
