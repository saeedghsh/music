from typing import Tuple
from notes_and_frequencies import frequency


def generate_all_notes(octave_range: Tuple[int, int] = (0, 9)) -> dict:
    """Generate all notes (including quadranttone) in give octave ranges"""
    notes = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["b", "k", "", "s", "#"]:
                notes[(note, accidental, octave)] = frequency(note, accidental, octave)
    return notes


def generate_piano_keys(octave_range: Tuple[int, int] = (0, 9)) -> dict:
    """Generate all notes for piano keys in give octave ranges"""
    keys = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["", "#"]:
                if f"{note}{accidental}" in ["E#", "B#"]:
                    continue
                key = (note, accidental, octave)
                keys[key] = frequency(*key)
    return keys
