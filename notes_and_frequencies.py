"""X"""
from typing import Tuple
from functools import wraps
from notation import A4_FREQUENCY

# In this context a set of "standard notes" is defined as the following.
# An equal temperament tuning system, where the octave is divided into 24 equal
# parts (quadranttone), results in 24 notes. A set of "standard notes of
# quadranttones" is a set that maps bijectively to corresponding frequencies.
# * where "sharp" of a note and "flat" of another are the same note, opt for "sharp"
# * where "koron" of a note and "sori" of another are the same note, opt for "sori"
# * "E#" and "B#" are not considered as they are represented by "F" and "C"
STANDARD_NOTES_QUADRANTTONES = [
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


def _upper_lower_args(func):
    @wraps(func)
    def wrapper(note: str, accidental: str, octave: int) -> float:
        return func(note.upper(), accidental.lower(), octave)

    return wrapper


@_upper_lower_args
def _standardize_note(note: str, accidental: str, octave: int) -> Tuple[str, int]:
    """Return a standard note, given any input note

    Makes sure that the note belong set of "standard notes"
    """
    conversion = {
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
    full_note = f"{note}{accidental}"
    if full_note == "B#":
        octave += 1
    if full_note in conversion:
        full_note = conversion[full_note]
    return full_note, octave


def compute_frequency(
    note: str, accidental: str, octave: int, a4_frequency: float = A4_FREQUENCY
) -> float:
    """Calculate the frequency of a note."""
    # pylint: disable=invalid-name
    full_note, octave = _standardize_note(note, accidental, octave)
    note_index = STANDARD_NOTES_QUADRANTTONES.index(full_note)
    A_index = STANDARD_NOTES_QUADRANTTONES.index("A")
    quadranttone_steps_from_A4 = note_index - A_index + (octave - 4) * 24
    return a4_frequency * (2 ** (quadranttone_steps_from_A4 / 24))
