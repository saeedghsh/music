from typing import Tuple, Dict
from notation import Note, FrequencyComputer


def generate_all_notes(octave_range: Tuple[int, int] = (0, 9)) -> dict:
    """Generate all notes (including quartertone) in give octave ranges"""
    notes = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["b", "k", "", "s", "#"]:
                notes[(note, accidental, octave)] = FrequencyComputer.compute_frequency(
                    note, accidental, octave
                )
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
                keys[key] = FrequencyComputer.compute_frequency(*key)
    return keys


def generate_tar_notes(fret_count: int = 27) -> Dict[int, Dict[int, str]]:
    """Tar and Setar"""
    if fret_count not in [25, 27, 28]:
        raise ValueError(
            f"Valid values for fret count are [25, 27, 28], provided: {fret_count}"
        )
    string_1_28_fret = {
        0: "C4",
        1: "C#4",
        2: "Dk4",
        3: "D4",
        4: "Eb4",
        5: "Ek4",
        6: "E4",
        7: "F4",
        8: "Fs4",
        9: "F#4",
        10: "Gk4",
        11: "G4",
        12: "Ab4",
        13: "Ak4",
        14: "A4",
        15: "Bb4",
        16: "Bk4",
        17: "B4",
        18: "C5",
        19: "C#5",
        20: "Dk5",
        21: "D5",
        22: "Eb5",
        23: "Ek5",
        24: "E5",
        25: "F5",
        26: "F#5",
        27: "G5",
        28: "G#5",
    }
    string_3_28_fret = {
        0: "G3",
        1: "G#3",
        2: "Ak3",
        3: "A3",
        4: "Bb3",
        5: "Bk3",
        6: "B3",
        7: "C4",
        8: "Cs4",
        9: "C#4",
        10: "Dk4",
        11: "D4",
        12: "Eb4",
        13: "Ek4",
        14: "E4",
        15: "F4",
        16: "Fs4",
        17: "F#4",
        18: "G4",
        19: "G#4",
        20: "Ak4",
        21: "A4",
        22: "Bb4",
        23: "Bk4",
        24: "B4",
        25: "C5",
        26: "C#5",
        27: "D5",
        28: "D#5",
    }
    if fret_count == 25:
        fret_numbers = [n for n in range(0, 28) if n not in [8, 19]]
    if fret_count == 27:
        fret_numbers = list(range(0, 28))
    if fret_count == 28:
        fret_numbers = list(range(0, 29))

    strings = {}
    strings[1] = {
        fret_number: fret_note
        for fret_number, fret_note in string_1_28_fret.items()
        if fret_number in fret_numbers
    }
    strings[3] = {
        fret_number: fret_note
        for fret_number, fret_note in string_3_28_fret.items()
        if fret_number in fret_numbers
    }
    strings[2] = strings[1]
    strings[4] = strings[3]
    strings[5] = strings[1]
    strings[6] = {
        fret_number: Note.transposition_by_an_octave(note)
        for fret_number, note in strings[1].items()
    }
    return strings
