"""Visualize a Piano"""
import sys
from typing import Sequence
import argparse

from instruments.instruments import generate_piano_keys
from drawing.drawing import draw_piano


def _parse_arguments(argv: Sequence[str]):
    parser = argparse.ArgumentParser(description="Piano entry point")
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="If specified, will visualize",
    )
    return parser.parse_args(argv)


def _main(argv: Sequence[str]):
    arguments = _parse_arguments(argv)
    piano_keys = generate_piano_keys()
    if arguments.visualize:
        draw_piano(piano_keys)


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
