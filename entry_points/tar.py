"""Visualize a Piano"""
import sys
from typing import Sequence
import argparse

from core.notation import Note, FrequencyComputer
from instruments.instruments import generate_tar_notes
from drawing.drawing import draw_tar_notes_and_frequencies


def _print_tar_notes_and_frequencies(tar_strings: dict, string_number: int):
    # TODO: move this to instrument.tar
    if string_number not in range(1, 7):
        raise ValueError("Tar/Setar strings should be numbered 1-6")
    string_notes = tar_strings[string_number]
    for fret_number, note_name in string_notes.items():
        letter, accidental, octave = Note.decompose_name(note_name)
        frequency = FrequencyComputer.compute_frequency(letter, accidental, octave)
        print(f"{fret_number}\t{note_name}:\t{frequency} Hz")


def _parse_arguments(argv: Sequence[str]):
    parser = argparse.ArgumentParser(description="Piano entry point")
    parser.add_argument(
        "--fret-count",
        type=int,
        choices=[25, 27, 28],
        default=27,
        help="Number of frets on the neck",
    )
    parser.add_argument(
        "--string-number",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        default=1,
        help="The string number",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Visualize",
    )
    parser.add_argument(
        "-s",
        "--save-to-file",
        action="store_true",
        help="Save the visualization to file (works only in combination with -v)",
    )
    parser.add_argument(
        "-p",
        "--print-out",
        action="store_true",
        help="Print out to terminal",
    )
    return parser.parse_args(argv)


def _main(argv: Sequence[str]):
    arguments = _parse_arguments(argv)
    tar_strings = generate_tar_notes(arguments.fret_count)

    if arguments.print_out:
        _print_tar_notes_and_frequencies(
            tar_strings, string_number=arguments.string_number
        )

    if arguments.visualize:
        draw_tar_notes_and_frequencies(
            tar_strings,
            string_number=arguments.string_number,
            save_to_file=arguments.save_to_file,
        )


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
