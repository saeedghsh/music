"""Entry point for circle of notes"""
import argparse
import os
import sys
from typing import Sequence

from core.frequency import Frequency
from core.notes import STANDARD_NOTES_QUARTERTONE, Note
from drawing.circle_of_notes_drawing import draw_circle
from drawing.common import save_image, show_image


def _parse_arguments(argv: Sequence[str]):
    parser = argparse.ArgumentParser(description="Circle of notes entry point")
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--save-to-file",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--file-path",
        type=str,
        required=False,
        help="for saving",
    )
    parser.add_argument(
        "-o",
        "--octave",
        type=int,
        default=0,
        help="Octave",
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
    notes = [
        Note.from_name(f"{name}{args.octave}", Frequency(args.a4_frequency))
        for name in STANDARD_NOTES_QUARTERTONE
    ]
    image = draw_circle(notes)
    if args.save_to_file:
        save_image(image, args.file_path)
    if args.visualize:
        show_image(image, "Circle of Notes")
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
