# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
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


def test_accidental_note_enum():
    sharp = AccidentalNote.SHARP.value
    assert isinstance(sharp, Accidental)
    assert sharp.name == "sharp"
    assert sharp.symbol == Symbol("#", "\u266F")
    assert sharp.frequency_ratio == MusicalInterval.SEMITONE.value


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
