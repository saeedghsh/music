"""The common musical intervals"""

from enum import Enum


class MusicalInterval(Enum):
    """An enum of common intervals expressed as frequency ratio"""

    OCTAVE = 2 ** (12 / 12)  # 2
    TONE = 2 ** (1 / 6)  # 8 ** (1/24)
    SEMITONE = 2 ** (1 / 12)  # 4 ** (1/24)
    QUARTERTONE = 2 ** (1 / 24)  # 2 ** (1/24)

    @staticmethod
    def as_quartertone_steps(interval: "MusicalInterval") -> int:
        """Return quartertone step count corresponding to the interval"""
        return {
            MusicalInterval.OCTAVE: 24,
            MusicalInterval.TONE: 4,
            MusicalInterval.SEMITONE: 2,
            MusicalInterval.QUARTERTONE: 1,
        }[interval]
