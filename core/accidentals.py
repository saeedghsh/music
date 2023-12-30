"""The basic musical notations and notions"""
from dataclasses import dataclass
from enum import Enum

from core.intervals import MusicalInterval
from core.symbols import Symbol


@dataclass
class Accidental:

    """Accidentals are symbols that pair with a notes to create new notes.
    Three common accidentals are:
    * the sharp: half-step higher,
    * the flat: half-step lower,
    * the natural.
    In Iranian music:
    * the sori: quarter-step higher
    * the koron: quarter-step lower"""

    name: str
    symbol: Symbol
    frequency_ratio: float

    def __str__(self) -> str:
        return self.symbol.simplified


class AccidentalSymbol(Enum):
    """An enum of symbols of common accidental"""

    SHARP = Symbol("#", "\u266F")
    SORI = Symbol("s", "\U0001D1E9")
    NATURAL = Symbol("", "")
    KORON = Symbol("k", "\U0001D1EA")
    FLAT = Symbol("b", "\u266F")


class AccidentalNote(Enum):
    """An enum of common accidental"""

    SHARP = Accidental("sharp", AccidentalSymbol.SHARP.value, MusicalInterval.SEMITONE.value)
    SORI = Accidental("sori", AccidentalSymbol.SORI.value, MusicalInterval.QUARTERTONE.value)
    NATURAL = Accidental("natural", AccidentalSymbol.NATURAL.value, 1)
    KORON = Accidental("koron", AccidentalSymbol.KORON.value, 1 / MusicalInterval.QUARTERTONE.value)
    FLAT = Accidental("flat", AccidentalSymbol.FLAT.value, 1 / MusicalInterval.SEMITONE.value)
