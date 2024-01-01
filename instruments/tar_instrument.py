"""Representation of the Tar"""
from typing import Dict, Sequence

from core.frequency import Frequency
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
    if fret_count not in [25, 27, 28]:
        raise ValueError(f"Valid values for fret count are [25, 27, 28], provided: {fret_count}")
    if fret_count == 25:
        fret_numbers = [n for n in range(0, 28) if n not in [8, 19]]
    if fret_count == 27:
        fret_numbers = list(range(0, 28))
    if fret_count == 28:
        fret_numbers = list(range(0, 29))
    return fret_numbers


def _tar_string(base_note: Note) -> Dict[int, Note]:
    notes = {0: base_note}
    for i in range(1, 29):
        notes[i] = notes[i - 1] + FRET_DIFFERENTIAL_INTERVAL[i]
    return notes


def _drop_fret(notes: Dict[int, Note], fret_count: int) -> Dict[int, Note]:
    return {
        fret_number: note
        for fret_number, note in notes.items()
        if fret_number in _fret_indices(fret_count)
    }


def generate_tar_strings(fret_count: int, a4_frequency: Frequency) -> Dict[int, Dict[int, Note]]:
    """Return a dict of (string_number, String).
    Where String is a dict of (frets_number, fret_note).
    NOTE: Depending on the fret_count, the fret numbers does not include the whole range.
          See: _fret_indices()."""
    strings = {}
    strings[1] = _drop_fret(_tar_string(Note.from_name("C4", a4_frequency)), fret_count)
    strings[2] = _drop_fret(_tar_string(Note.from_name("C4", a4_frequency)), fret_count)
    strings[3] = _drop_fret(_tar_string(Note.from_name("G3", a4_frequency)), fret_count)
    strings[4] = _drop_fret(_tar_string(Note.from_name("G3", a4_frequency)), fret_count)
    strings[5] = _drop_fret(_tar_string(Note.from_name("C4", a4_frequency)), fret_count)
    strings[6] = _drop_fret(_tar_string(Note.from_name("C3", a4_frequency)), fret_count)
    return strings
