"""Musical Accidentals"""
from dataclasses import dataclass
from enum import Enum
from typing import Union

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

    @staticmethod
    def _validate_by_symbol(symbol: str) -> bool:
        return symbol in [accidental.value.symbol.simplified for accidental in AccidentalNote]

    @staticmethod
    def _validate_by_name(name: str) -> bool:
        return name in [accidental.value.name for accidental in AccidentalNote]

    @staticmethod
    def _validate_by_accidental(accidental: Accidental) -> bool:
        return AccidentalNote._validate_by_name(accidental.name)

    @staticmethod
    def validate(accidental: Union[Accidental, str]):
        """Check if accidental is valid"""
        accidental_type = type(accidental)
        if accidental_type is Accidental:
            valid = AccidentalNote._validate_by_accidental(accidental)
        elif accidental_type is str:
            valid = any(
                [
                    AccidentalNote._validate_by_name(accidental),
                    AccidentalNote._validate_by_symbol(accidental),
                ]
            )
        else:
            raise NotImplementedError(f"Type {accidental_type} is not supported for validation")
        if not valid:
            raise ValueError(f"Accidental {accidental} is un-identifiable")
