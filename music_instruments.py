from typing import Tuple, Dict
from notes_and_frequencies import compute_frequency


def generate_all_notes(octave_range: Tuple[int, int] = (0, 9)) -> dict:
    """Generate all notes (including quadranttone) in give octave ranges"""
    notes = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["b", "k", "", "s", "#"]:
                notes[(note, accidental, octave)] = compute_frequency(note, accidental, octave)
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
                keys[key] = compute_frequency(*key)
    return keys


def shit_string(string: Dict[int, str], new_base_note: str) -> Dict[int, str]:
    """Return 
    
    Assuming the frets are the same across the neck of the instrument for all the strings
    """

    new_string = string
    return new_string


def generate_tar_notes(): # -> Dict[int, Dict[int, Note]]:
    """Tar and Setar"""
    # strings = {string_number: [] for string_number in range(1, 7)}
    string1 = {
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
    }
    string2 = string1
    string3 = {} # "G3"
    string4 = {} # "G3"

    string5 = string1
    string6 = {
        i: f"{}"
        for i, note in enumerate(string1.items())
    }
    return string1, string2, string3, string4, string5, string6
