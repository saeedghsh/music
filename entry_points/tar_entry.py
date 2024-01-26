"""Entry point for Tar"""

import argparse
import os
import sys
from typing import Sequence

from core.frequency import Frequency
from core.notes import Note
from drawing.common import save_image, show_image
from drawing.tar_drawing import annotate_tar_image, draw_tar
from instruments.tar_instrument import tar_string


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
        "--base-note",
        default="C4",
        type=str,
        help="The string's open-hand note",
    )
    parser.add_argument(
        "--a4-frequency",
        type=float,
        default=440,
        help="Frequency for the reference note A4",
    )
    parser.add_argument(
        "-p",
        "--print-out",
        action="store_true",
        help="Print out to terminal",
    )
    parser.add_argument(
        "--annotate",
        action="store_true",
        help="The visualization will be only the annotated version, otherwise drawing",
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
        help="Save the visualization to file (works only in combination with -f)",
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
    base_note = Note.from_name(args.base_note, Frequency(args.a4_frequency))
    string = tar_string(base_note, args.fret_count)

    if args.print_out:
        for fret_number, note in string.items():
            print(f"{fret_number}\t{note}")

    if args.save_to_file or args.visualize:
        # pylint: disable=fixme
        # TODO: This if is just for the sake of the smoke tests
        #       This function only supports 27 fret example as of now
        #       I should not be called except if being tested for save/show
        if args.annotate:
            image = annotate_tar_image(string)
        else:
            image = draw_tar(string)

    if args.save_to_file:
        save_image(image, args.file_path)
    if args.visualize:
        show_image(image, "Tar")
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
