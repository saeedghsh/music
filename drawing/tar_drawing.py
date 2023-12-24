"""Tar drawing utils"""
# pylint: disable=no-member
from typing import Optional, Tuple, Dict

import cv2
import numpy as np

from core.notation import FrequencyComputer, Note

INSTRUMENTS: Dict[str, dict] = {
    "tar": {
        "small_image": {
            "path": "images/tar_small_1290x362.jpg",
            "fret_position_row_27_fret": {
                0: 162,
                1: 206,
                2: 230,
                3: 255,
                4: 295,
                5: 313,
                6: 333,
                7: 372,
                8: 398,
                9: 424,
                10: 448,
                11: 476,
                12: 494,
                13: 513,
                14: 540,
                15: 553,
                16: 568,
                17: 599,
                18: 618,
                19: 625,
                20: 638,
                21: 666,
                22: 679,
                23: 695,
                24: 716,
                25: 734,
                26: 752,
                27: 767,
            },
            "fret_position_col": {
                "min": 150,
                "max": 208,
            },
        },
        "large_image": {"path": "images/tar_large_3910x1097.jpg"},
    }
}

_COLOR = (0, 0, 0)

_FONT_SCALE = 0.5
_FONT_THICKNESS = 1
_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
_FRET_LABEL_COLOR = _COLOR
_FRET_LINE_THICKNESS = 2
_FRET_LINE_COLOR = _COLOR


def _draw_fret(image: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int]):
    cv2.line(image, pt1, pt2, _FRET_LINE_COLOR, _FRET_LINE_THICKNESS)


def _fret_label(string_notes: Dict[int, str], fret_number: int) -> str:
    note = string_notes[fret_number]
    letter, accidental, octave = Note.decompose_name(note)
    frequency = FrequencyComputer.compute_frequency(letter, accidental, octave)
    return f"{note}: {frequency:.2f} Hz"


def _print_fret_label(image: np.ndarray, label: str, position: Tuple[int, int]):
    cv2.putText(
        image,
        label,
        position,
        _FONT_FACE,
        _FONT_SCALE,
        _FRET_LABEL_COLOR,
        _FONT_THICKNESS,
    )


def annotate_tar_image(
    string_notes: Dict[int, str], show: bool, save: bool, file_path: Optional[str]
):
    """Annotate a tar image, show and/or save per argument setting"""
    if len(string_notes) != 28:
        raise NotImplementedError(
            "Curretnly only 27-fret count (28 including open-hand) is supported."
        )

    tar_img = cv2.imread(INSTRUMENTS["tar"]["small_image"]["path"])
    col_min = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["min"]
    col_max = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["max"]
    fret_positions_row = INSTRUMENTS["tar"]["small_image"]["fret_position_row_27_fret"]
    for fret_number, row in fret_positions_row.items():
        _draw_fret(tar_img, (col_min, row), (col_max, row))
        _print_fret_label(tar_img, _fret_label(string_notes, fret_number), (col_max + 20, row))

    if save:
        if file_path is None:
            raise ValueError("Is save is True, file_path cannot be None")
        cv2.imwrite(file_path, tar_img)

    if show:
        cv2.imshow("Annotated Tar", tar_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
