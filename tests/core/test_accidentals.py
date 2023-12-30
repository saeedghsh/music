# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

from core.accidentals import Accidental, AccidentalNote
from core.intervals import MusicalInterval
from core.symbols import Symbol


def test_accidental_creation():
    sharp_symbol = Symbol("#", "\u266F")
    accidental = Accidental("sharp", sharp_symbol, 1.0)
    assert accidental.name == "sharp"
    assert accidental.symbol.simplified == "#"
    assert accidental.frequency_ratio == 1.0

    assert str(accidental) == "#"


def test_accidental_creation_fail():
    sharp_symbol = Symbol("#", "\u266F")
    bad_symbol = Symbol("%", "xyz")
    with pytest.raises(ValueError):
        Accidental("wrong_name", sharp_symbol, 1.0)
    with pytest.raises(ValueError):
        Accidental("sharp", bad_symbol, 1.0)
    with pytest.raises(ValueError):
        Accidental("flat", sharp_symbol, 1.0)  # name-symbol mismatch


@pytest.mark.parametrize("name", ["sharp", "sori", "natural", "koron", "flat"])
def test_accidental_from_name(name: str):
    Accidental.from_name(name)


@pytest.mark.parametrize("name", ["sharp_", "sori_", "natural_", "koron_", "flat_"])
def test_accidental_from_name_invalid(name: str):
    with pytest.raises(ValueError):
        Accidental.from_name(name)


@pytest.mark.parametrize("symbol", ["#", "s", "", "k", "b"])
def test_accidental_from_symbol(symbol: str):
    Accidental.from_symbol(symbol)


@pytest.mark.parametrize("symbol", ["%", "*", "-", "@", "!"])
def test_accidental_from_symbol_invalid(symbol: str):
    with pytest.raises(ValueError):
        Accidental.from_symbol(symbol)


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


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
