"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.accidentals import Accidental, AccidentalNote, AccidentalSymbol
from core.frequency import Frequency
from core.intervals import MusicalInterval
from core.symbols import Symbol

A4_FREQUENCY = Frequency(440)


def test_accidental_creation():
    accidental = Accidental("test", Symbol("x", "\u0041"), 1.5)
    assert accidental.name == "test"
    assert accidental.symbol.simplified == "x"
    assert accidental.frequency_ratio == 1.5
    assert str(accidental) == "x"


def test_accidental_symbol_enum():
    assert AccidentalSymbol.SHARP.value.simplified == "#"
    assert AccidentalSymbol.FLAT.value.simplified == "b"


def test_accidental_note_enum():
    sharp = AccidentalNote.SHARP.value
    assert isinstance(sharp, Accidental)
    assert sharp.name == "sharp"
    assert sharp.symbol == AccidentalSymbol.SHARP.value
    assert sharp.frequency_ratio == MusicalInterval.SEMITONE.value


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
