"""Representation of the Tar"""
from typing import Dict, Sequence

from core.notation import Note, transposition_by_an_octave


def _fret_numbers(fret_count: int) -> Sequence[int]:
    if fret_count not in [25, 27, 28]:
        raise ValueError(f"Valid values for fret count are [25, 27, 28], provided: {fret_count}")
    if fret_count == 25:
        fret_numbers = [n for n in range(0, 28) if n not in [8, 19]]
    if fret_count == 27:
        fret_numbers = list(range(0, 28))
    if fret_count == 28:
        fret_numbers = list(range(0, 29))
    return fret_numbers


def _tar_strings(fret_count: int, a4_frequency: float) -> Dict[int, Dict[int, Note]]:
    string_1_28_fret = {
        0: Note.from_name("C4", a4_frequency),
        1: Note.from_name("C#4", a4_frequency),
        2: Note.from_name("Dk4", a4_frequency),
        3: Note.from_name("D4", a4_frequency),
        4: Note.from_name("Eb4", a4_frequency),
        5: Note.from_name("Ek4", a4_frequency),
        6: Note.from_name("E4", a4_frequency),
        7: Note.from_name("F4", a4_frequency),
        8: Note.from_name("Fs4", a4_frequency),
        9: Note.from_name("F#4", a4_frequency),
        10: Note.from_name("Gk4", a4_frequency),
        11: Note.from_name("G4", a4_frequency),
        12: Note.from_name("Ab4", a4_frequency),
        13: Note.from_name("Ak4", a4_frequency),
        14: Note.from_name("A4", a4_frequency),
        15: Note.from_name("Bb4", a4_frequency),
        16: Note.from_name("Bk4", a4_frequency),
        17: Note.from_name("B4", a4_frequency),
        18: Note.from_name("C5", a4_frequency),
        19: Note.from_name("C#5", a4_frequency),
        20: Note.from_name("Dk5", a4_frequency),
        21: Note.from_name("D5", a4_frequency),
        22: Note.from_name("Eb5", a4_frequency),
        23: Note.from_name("Ek5", a4_frequency),
        24: Note.from_name("E5", a4_frequency),
        25: Note.from_name("F5", a4_frequency),
        26: Note.from_name("F#5", a4_frequency),
        27: Note.from_name("G5", a4_frequency),
        28: Note.from_name("G#5", a4_frequency),
    }
    string_3_28_fret = {
        0: Note.from_name("G3", a4_frequency),
        1: Note.from_name("G#3", a4_frequency),
        2: Note.from_name("Ak3", a4_frequency),
        3: Note.from_name("A3", a4_frequency),
        4: Note.from_name("Bb3", a4_frequency),
        5: Note.from_name("Bk3", a4_frequency),
        6: Note.from_name("B3", a4_frequency),
        7: Note.from_name("C4", a4_frequency),
        8: Note.from_name("Cs4", a4_frequency),
        9: Note.from_name("C#4", a4_frequency),
        10: Note.from_name("Dk4", a4_frequency),
        11: Note.from_name("D4", a4_frequency),
        12: Note.from_name("Eb4", a4_frequency),
        13: Note.from_name("Ek4", a4_frequency),
        14: Note.from_name("E4", a4_frequency),
        15: Note.from_name("F4", a4_frequency),
        16: Note.from_name("Fs4", a4_frequency),
        17: Note.from_name("F#4", a4_frequency),
        18: Note.from_name("G4", a4_frequency),
        19: Note.from_name("G#4", a4_frequency),
        20: Note.from_name("Ak4", a4_frequency),
        21: Note.from_name("A4", a4_frequency),
        22: Note.from_name("Bb4", a4_frequency),
        23: Note.from_name("Bk4", a4_frequency),
        24: Note.from_name("B4", a4_frequency),
        25: Note.from_name("C5", a4_frequency),
        26: Note.from_name("C#5", a4_frequency),
        27: Note.from_name("D5", a4_frequency),
        28: Note.from_name("D#5", a4_frequency),
    }
    fret_numbers = _fret_numbers(fret_count)
    strings = {}
    strings[1] = {
        fret_number: note
        for fret_number, note in string_1_28_fret.items()
        if fret_number in fret_numbers
    }
    strings[3] = {
        fret_number: note
        for fret_number, note in string_3_28_fret.items()
        if fret_number in fret_numbers
    }
    strings[2] = strings[1]
    strings[4] = strings[3]
    strings[5] = strings[1]
    strings[6] = {
        fret_number: transposition_by_an_octave(note) for fret_number, note in strings[1].items()
    }
    return strings


def tar_string(fret_count: int, string_number: int, a4_frequency: float) -> Dict[int, Note]:
    """Tar and Setar"""
    if string_number not in [1, 2, 3, 4, 5, 6]:
        raise ValueError(
            f"Valid values for string number are [1, ..., 6], provided: {string_number}"
        )
    strings = _tar_strings(fret_count, a4_frequency)
    return strings[string_number]
