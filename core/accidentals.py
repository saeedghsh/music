"""Musical Accidentals"""
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


class AccidentalNote(Enum):
    """An enum of common accidental"""

    SHARP = Accidental("sharp", Symbol("#", "\u266F"), MusicalInterval.SEMITONE.value)
    SORI = Accidental("sori", Symbol("s", "\U0001D1E9"), MusicalInterval.QUARTERTONE.value)
    NATURAL = Accidental("natural", Symbol("", ""), 1)
    KORON = Accidental("koron", Symbol("k", "\U0001D1EA"), 1 / MusicalInterval.QUARTERTONE.value)
    FLAT = Accidental("flat", Symbol("b", "\u266F"), 1 / MusicalInterval.SEMITONE.value)
