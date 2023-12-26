"""Visualize a Piano"""
import argparse
import os
import sys
from typing import Sequence

from drawing.tar_drawing import annotate_tar_image
from instruments.tar_instrument import (
    generate_tar_notes,
    print_tar_notes_and_frequencies,
)


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
    return parser.parse_args(argv)


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)
    string_notes = generate_tar_notes(args.fret_count, args.string_number)
    if args.print_out:
        print_tar_notes_and_frequencies(string_notes)
    if args.visualize or args.save_to_file:
        annotate_tar_image(string_notes, args.visualize, args.save_to_file, args.file_path)
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
