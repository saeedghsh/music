"""Musical Accidentals"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from core.intervals import MusicalInterval
from core.symbols import Symbol

SYMBOL_TO_NAME_MAP = {"#": "sharp", "s": "sori", "": "natural", "k": "koron", "b": "flat"}
SYMBOL_TO_INTERVAL_MAP = {
    "#": MusicalInterval.SEMITONE.value,
    "s": MusicalInterval.QUARTERTONE.value,
    "": 1,
    "k": 1 / MusicalInterval.QUARTERTONE.value,
    "b": 1 / MusicalInterval.SEMITONE.value,
}


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

    def __post_init__(self):
        if self.name not in SYMBOL_TO_NAME_MAP.values():
            raise ValueError(f"Invalid name {self.name}")
        if self.symbol.simplified not in SYMBOL_TO_NAME_MAP:
            raise ValueError(f"Invalid symbol {self.symbol}")
        if self.name != SYMBOL_TO_NAME_MAP[self.symbol.simplified]:
            raise ValueError(f"Symbol {self.symbol} and name {self.name} do not match")

    def __str__(self) -> str:
        return self.symbol.simplified

    def _eq_to_name(self, other_name: str) -> bool:
        return self.name == other_name

    def _eq_to_symbol(self, other_symbol: str) -> bool:
        return self.symbol == other_symbol

    def _eq_to_accidental(self, other: "Accidental") -> bool:
        return self.name == other.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return any([self._eq_to_name(other), self._eq_to_symbol(other)])
        if isinstance(other, Accidental):
            return self._eq_to_accidental(other)
        raise NotImplementedError(f"Type {type(other)} is not supported for comparison")

    @staticmethod
    def from_name(name: str) -> "Accidental":
        """Create and return an Accidental from the name"""
        if name not in SYMBOL_TO_NAME_MAP.values():
            raise ValueError(f"Cannot construct an Accidental by the name: {name}")
        accidental = getattr(AccidentalNote, name.upper())
        return accidental.value

    @staticmethod
    def from_symbol(symbol: str) -> "Accidental":
        """Create and return an Accidental from the symbol (single character)"""
        if symbol not in SYMBOL_TO_NAME_MAP:
            raise ValueError(f"Cannot construct an Accidental by the symbol: {symbol}")
        return Accidental.from_name(SYMBOL_TO_NAME_MAP[symbol])


class AccidentalNote(Enum):
    """An enum of common accidental"""

    SHARP = Accidental("sharp", Symbol("#", "\u266F"), MusicalInterval.SEMITONE.value)
    SORI = Accidental("sori", Symbol("s", "\U0001D1E9"), MusicalInterval.QUARTERTONE.value)
    NATURAL = Accidental("natural", Symbol("", ""), 1)
    KORON = Accidental("koron", Symbol("k", "\U0001D1EA"), 1 / MusicalInterval.QUARTERTONE.value)
    FLAT = Accidental("flat", Symbol("b", "\u266F"), 1 / MusicalInterval.SEMITONE.value)
