"""Representation of the Tar"""

from typing import Dict, Sequence

from core.intervals import MusicalInterval
from core.notes import Note

# The music interval from each fret to previous, lower pitched, fret.
# Fret=0 (base-note/open-hand) has no previous to have differential interval.
FRET_DIFFERENTIAL_INTERVAL = {
    1: MusicalInterval.SEMITONE,
    2: MusicalInterval.QUARTERTONE,
    3: MusicalInterval.QUARTERTONE,
    4: MusicalInterval.SEMITONE,
    5: MusicalInterval.QUARTERTONE,
    6: MusicalInterval.QUARTERTONE,
    7: MusicalInterval.SEMITONE,
    8: MusicalInterval.QUARTERTONE,
    9: MusicalInterval.QUARTERTONE,
    10: MusicalInterval.QUARTERTONE,
    11: MusicalInterval.QUARTERTONE,
    12: MusicalInterval.SEMITONE,
    13: MusicalInterval.QUARTERTONE,
    14: MusicalInterval.QUARTERTONE,
    15: MusicalInterval.SEMITONE,
    16: MusicalInterval.QUARTERTONE,
    17: MusicalInterval.QUARTERTONE,
    18: MusicalInterval.SEMITONE,
    19: MusicalInterval.SEMITONE,
    20: MusicalInterval.QUARTERTONE,
    21: MusicalInterval.QUARTERTONE,
    22: MusicalInterval.SEMITONE,
    23: MusicalInterval.QUARTERTONE,
    24: MusicalInterval.QUARTERTONE,
    25: MusicalInterval.SEMITONE,
    26: MusicalInterval.SEMITONE,
    27: MusicalInterval.SEMITONE,
    28: MusicalInterval.SEMITONE,
}


def _fret_indices(fret_count: int) -> Sequence[int]:
    if fret_count == 25:
        fret_indices = [n for n in range(0, 28) if n not in [8, 19]]
    elif fret_count == 27:
        fret_indices = list(range(0, 28))
    elif fret_count == 28:
        fret_indices = list(range(0, 29))
    else:
        raise ValueError(f"Valid values for fret count are [25, 27, 28], provided: {fret_count}")
    return fret_indices


def tar_string(base_note: Note, fret_count: int) -> Dict[int, Note]:
    """Return a String that is a dict of (frets_number, fret_note).

    NOTE: Fret zero is the open-hand and does not count in the total fret counts.
          Returning dict has (fret_count + 1) entries.
    NOTE: Depending on the fret_count, the fret numbers does not include the whole range.
          See: _fret_indices()."""
    notes = {0: base_note}
    for i in range(1, 29):
        notes[i] = notes[i - 1] + FRET_DIFFERENTIAL_INTERVAL[i]

    return {
        fret_number: note
        for fret_number, note in notes.items()
        if fret_number in _fret_indices(fret_count)
    }
