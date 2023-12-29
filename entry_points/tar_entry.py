"""Visualize a Piano"""
import argparse
import os
import sys
from typing import Sequence

from core.frequency import Frequency
from drawing.tar_drawing import annotate_tar_image
from instruments.tar_instrument import generate_tar_string


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
        "-p",
        "--print-out",
        action="store_true",
        help="Print out to terminal",
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
        "-f",
        "--file-path",
        type=str,
        required=False,
        help="for saving",
    )
    parser.add_argument(
        "-a4",
        "--a4-frequency",
        type=float,
        default=440,
        help="Frequency for the reference note A4",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)
    string_notes = generate_tar_string(
        args.fret_count, args.string_number, Frequency(args.a4_frequency)
    )
    if args.print_out:
        for fret_number, note in string_notes.items():
            print(f"{fret_number}\t{note}")
    if args.visualize or args.save_to_file:
        annotate_tar_image(string_notes, args.visualize, args.save_to_file, args.file_path)
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
