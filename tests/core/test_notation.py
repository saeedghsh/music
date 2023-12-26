"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
from math import isclose

import pytest

from core.notation import (
    Accidental,
    AccidentalNote,
    AccidentalSymbol,
    MusicalInterval,
    Note,
    Octave,
    OctaveRegister,
    Symbol,
    conversion_to_standard_note,
    decompose_note_name,
    standard_notes_quartertones,
    standardize_note,
    transposition_by_an_octave,
)


def test_musical_interval_values():
    assert isclose(MusicalInterval.OCTAVE.value, 2 ** (12 / 12))
    assert isclose(MusicalInterval.TONE.value, 2 ** (1 / 6))
    assert isclose(MusicalInterval.SEMITONE.value, 2 ** (1 / 12))
    assert isclose(MusicalInterval.QUARTERTONE.value, 2 ** (1 / 24))


def test_symbol_creation():
    sym = Symbol(simplified="A", unicode="\u0041")
    assert sym.simplified == "A"
    assert sym.unicode == "\u0041"


def test_symbol_comparison():
    sym1 = Symbol(simplified="A", unicode="\u0041")
    sym2 = Symbol(simplified="A", unicode="\u0041")
    sym3 = Symbol(simplified="B", unicode="\u0042")
    assert sym1 == sym2
    assert sym1 != sym3


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
def test_octave_eq(other, expected):
    octave = Octave("great", 2)
    assert (octave == other) == expected, f"Incorrect equality comparison with {other}"


def test_octave_eq_unsupported():
    octave = Octave("great", 2)
    with pytest.raises(NotImplementedError):
        octave == float(2)  # pylint: disable=expression-not-assigned


def test_octave_register():
    assert OctaveRegister.GREAT.value == Octave("great", 2)
    assert OctaveRegister.SMALL.value.number == 3


@pytest.mark.parametrize(
    "name, expected",
    [
        ("A4", ("A", "", 4)),
        ("G#3", ("G", "#", 3)),
        ("Fs2", ("F", "s", 2)),
        ("Dk-1", ("D", "k", -1)),
        ("Cb9", ("C", "b", 9)),
    ],
)
def test_decompose_note_name_valid(name, expected):
    assert decompose_note_name(name) == expected, f"Incorrect decomposition for {name}"


@pytest.mark.parametrize(
    "name",
    [
        "H2",  # Invalid letter
        "G#10",  # Octave out of range
        "D##4",  # Invalid accidental
        "8A",  # Incorrect format
        "Csharp4",  # Incorrect accidental format
    ],
)
def test_decompose_note_name_invalid(name):
    with pytest.raises(ValueError):
        decompose_note_name(name)


@pytest.mark.parametrize(
    "note_name, expected", [("A4", "A5"), ("G#3", "G#4"), ("Fs2", "Fs3"), ("Dk-1", "Dk0")]
)
def test_transposition_by_an_octave(note_name, expected):
    assert (
        transposition_by_an_octave(note_name) == expected
    ), f"Incorrect transposition for {note_name}"


@pytest.mark.parametrize(
    "note_name",
    [
        "G#10",  # Octave out of range after transposition
        "H2",  # Invalid letter
        "Csharp4",  # Incorrect accidental format
    ],
)
def test_transposition_by_an_octave_invalid(note_name):
    with pytest.raises(ValueError):
        transposition_by_an_octave(note_name)


def test_standard_notes_quartertones():
    expected_notes = [
        "C",
        "Cs",
        "C#",
        "Dk",
        "D",
        "Ds",
        "D#",
        "Ek",
        "E",
        "Es",
        "F",
        "Fs",
        "F#",
        "Gk",
        "G",
        "Gs",
        "G#",
        "Ak",
        "A",
        "As",
        "A#",
        "Bk",
        "B",
        "Bs",
    ]
    assert standard_notes_quartertones() == expected_notes


def test_conversion_to_standard_note():
    expected_conversions = {
        "E#": "F",
        "B#": "C",
        "Cb": "B",
        "Fb": "E",
        "Db": "C#",
        "Eb": "D#",
        "Gb": "F#",
        "Ab": "G#",
        "Bb": "A#",
        "Ck": "Bs",
        "Fk": "Es",
    }

    assert conversion_to_standard_note() == expected_conversions


@pytest.mark.parametrize(
    "letter, accidental, octave, expected",
    [
        ("E", "#", 4, ("F", "", 4)),
        ("B", "#", 3, ("C", "", 4)),  # Note octave change
        ("C", "b", 2, ("B", "", 2)),
        ("F", "k", 5, ("E", "s", 5)),
    ],
)
def test_standardize_note(letter, accidental, octave, expected):
    assert (
        standardize_note(letter, accidental, octave) == expected
    ), f"Incorrect standardization for {letter}{accidental}{octave}"


@pytest.mark.parametrize(
    "letter, accidental, octave",
    [
        ("H", "", 4),  # Invalid letter
        ("C", "##", 3),  # Invalid accidental
        ("D", "s", -2),  # Invalid octave, assuming -1 to 9 is valid
    ],
)
def test_standardize_note_invalid(letter, accidental, octave):
    with pytest.raises(ValueError):
        standardize_note(letter, accidental, octave)


def test_note_creation():
    note = Note("A4", "A", "", 4, 440.0)
    assert note.name == "A4"
    assert note.letter == "A"
    assert note.accidental == ""
    assert note.octave == 4
    assert isclose(note.frequency, 440.0)


def test_note_str_repr():
    note = Note("A4", "A", "", 4, 440.0)
    assert str(note) == "A4"
    assert "Note A4 - 440.0 Hz" in repr(note)


def test_note_from_name():
    note = Note.from_name("A4")
    assert note.name == "A4"
    assert note.frequency == 440.0


def test_note_eq():
    note1 = Note("A4", "A", "", 4, 440.0)
    note2 = Note.from_name("A4")
    note3 = Note("B4", "B", "", 4, 493.88)
    assert note1 == note2
    assert note1 != note3
    assert note1 == "A4"
    assert note1 != "B4"
    assert note1 == 440.0
    assert note1 != 493.88


def test_note_eq_unsupported():
    note = Note("A4", "A", "", 4, 440.0)
    with pytest.raises(NotImplementedError):
        # pylint: disable=pointless-statement
        # pylint: disable=use-implicit-booleaness-not-comparison
        note == {}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
