"""Representation of the Piano"""
from typing import Tuple

from core.notation import compute_frequency


def generate_piano_keys(octave_range: Tuple[int, int], a4_frequency: float) -> dict:
    """Generate all notes for piano keys in give octave ranges

    NOTE: start of octave_range is inclusive and end of it is exclusive
    """
    # pylint: disable=fixme
    # TODO: this implementation does not generate any standard piano (i.e. 88-97-108 keys)
    if octave_range[0] >= octave_range[1]:
        raise ValueError("Upper range must be greater than lower range")
    keys = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["", "#"]:
                if f"{note}{accidental}" in ["E#", "B#"]:
                    continue
                key = (note, accidental, octave)
                keys[key] = compute_frequency(*key, a4_frequency)
    return keys
