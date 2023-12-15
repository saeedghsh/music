from typing import Tuple
from notation import Note


def generate_all_notes(octave_range: Tuple[int, int] = (0, 9)) -> dict:
    """Generate all notes (including quadranttone) in give octave ranges"""
    notes = {}
    for octave in range(*octave_range):
        for note in ["C", "D", "E", "F", "G", "A", "B"]:
            for accidental in ["b", "k", "", "s", "#"]:
                notes[(note, accidental, octave)] = Note.compute_frequency(
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
                keys[key] = Note.compute_frequency(*key)
    return keys


def generate_tar_notes():  # -> Dict[int, Dict[int, Note]]:
    """Tar and Setar"""
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
    string3 = {
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
    }  # "G3"
    string4 = string3
    string5 = string1
    string6 = {
        fret_number: Note.transposition_by_an_octave(note)
        for fret_number, note in string1.items()
    }
    return {1: string1, 2: string2, 3: string3, 4: string4, 5: string5, 6: string6}


def _print_tar_notes_and_frequencies(string_number: int):
    if string_number not in range(1, 7):
        raise ValueError("Tar/Setar strings should be numbered 1-6")

    tar_strings = generate_tar_notes()
    string_notes = tar_strings[string_number]
    for fret_number, note_name in string_notes.items():
        letter, accidental, octave = Note.decompose_name(note_name)
        frequency = Note.compute_frequency(letter, accidental, octave)
        print(f"{fret_number}\t{note_name}:\t{frequency} Hz")


_print_tar_notes_and_frequencies(string_number=1)
