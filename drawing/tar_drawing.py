"""Tar drawing utils"""
# pylint: disable=no-member
from typing import Dict, List, Sequence, Tuple

import cv2
import numpy as np

from core.notes import Note
from drawing.common import COLOR_BRG

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

FONT_SCALE = 0.5
FONT_THICKNESS = 1
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FRET_LABEL_COLOR = COLOR_BRG["black"]
FRET_LINE_COLOR = COLOR_BRG["black"]
FRET_LINE_THICKNESS = 2


def _draw_fret(image: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int]):
    cv2.line(image, pt1, pt2, FRET_LINE_COLOR, FRET_LINE_THICKNESS)


def _get_text_size(text: str) -> Sequence[int]:
    return cv2.getTextSize(  # skip baseline and only return (w, h)
        text, fontFace=FONT_FACE, fontScale=FONT_SCALE, thickness=FONT_THICKNESS
    )[0]


def _put_text(image: np.ndarray, text: str, position: Tuple[int, int], center: bool = False):
    pos = position
    if center:
        width, height = _get_text_size(text)
        pos = int(position[0] - width / 2), int(position[1] - height / 2)

    cv2.putText(
        image,
        text,
        pos,
        fontFace=FONT_FACE,
        fontScale=FONT_SCALE,
        color=FRET_LABEL_COLOR,
        thickness=FONT_THICKNESS,
    )


def _fret_label(note: Note) -> str:
    return f"{note.name}: {note.frequency.value:.2f} Hz"


def annotate_tar_image(string_notes: Dict[int, Note]) -> np.ndarray:
    """Annotate a tar image, show and/or save per argument setting"""
    if len(string_notes) != 28:
        raise NotImplementedError(
            "Currently only 27-fret count (28 including open-hand) is supported."
        )
    image = cv2.imread(INSTRUMENTS["tar"]["small_image"]["path"])
    col_min = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["min"]
    col_max = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["max"]
    fret_positions_row = INSTRUMENTS["tar"]["small_image"]["fret_position_row_27_fret"]
    for fret_number, row in fret_positions_row.items():
        _draw_fret(image, (col_min, row), (col_max, row))
        _put_text(image, _fret_label(string_notes[fret_number]), (col_max + 20, row))

    return image


def _max_text_width(texts: List[str]) -> int:
    return max(_get_text_size(text)[0] for text in texts)


def _length_ratio(base_note: Note, note: Note) -> float:
    """Returns the string ratio that produces 'note', if length of 1 produces 'base_note'

    NOTE: this ratio multiplied by the "string length" will yield the distance from saddle to fret
    """
    return base_note.frequency.value / note.frequency.value


def _length_label(base_note: Note, note: Note, string_length_mm: float) -> str:
    """NOTE: Ratio is of fret distance to saddle w.r.t string length.
    However, in practice, it's easier and hence more common to measure fret distance from nut
    Therefor the ratio is computed as 1-ratio before formatting it into text."""
    ratio = 1 - _length_ratio(base_note, note)
    label = f"{ratio * string_length_mm:.2f} mm"
    return label


def _draw_neck(image: np.ndarray, neck_size: Tuple[int, int], position: Tuple[int, int]):
    neck_width, neck_height = neck_size
    pos_x, pos_y = position
    x1, x2 = pos_x, pos_x + neck_width
    y1, y2 = pos_y, int(pos_y + neck_height)
    cv2.rectangle(image, (x1, y1), (x2, y2), COLOR_BRG["light_brown"], -1)
    x1, x2 = pos_x + int(neck_width / 3), pos_x + int(2 * neck_width / 3)
    cv2.rectangle(image, (x1, y1), (x2, y2), COLOR_BRG["dark_brown"], -1)


def _create_image(
    string: Dict[int, Note], string_length_mm: float, nut_to_saddle: int, neck_width: int
) -> Tuple[np.ndarray, Dict[str, int]]:
    base_note = string[0]
    max_fret_label_width = _max_text_width([_fret_label(note) for note in string.values()])
    max_length_label_width = _max_text_width(
        [_length_label(base_note, note, string_length_mm) for note in string.values()]
    )
    left_margin = int(1.5 * max_length_label_width)
    right_margin = int(1.5 * max_fret_label_width)
    top_margin = 2 * _get_text_size("x")[1]
    bottom_margin = top_margin
    img_height = nut_to_saddle + top_margin + bottom_margin
    img_width = neck_width + left_margin + right_margin
    image = np.ones((img_height, img_width, 3), dtype=np.uint8) * np.uint8(255)
    margin = {
        "left": left_margin,
        "right": right_margin,
        "top": top_margin,
        "bottom": bottom_margin,
    }
    return image, margin


def _neck_size(nut_to_saddle: int) -> Tuple[int, int]:
    neck_height = int(0.7 * nut_to_saddle)
    neck_width = int(0.05 * nut_to_saddle)
    return neck_width, neck_height


def _draw_nut(image: np.ndarray, margin: dict, neck_width: int):
    x1, x2 = margin["left"], margin["left"] + neck_width
    nut_y = margin["top"]
    cv2.line(image, (x1, nut_y), (x2, nut_y), FRET_LINE_COLOR, 2 * FRET_LINE_THICKNESS)
    _put_text(image, "NUT", (int((x1 + x2) / 2), nut_y), center=True)


def _draw_saddle(
    image: np.ndarray, margin: dict, neck_width: int, nut_to_saddle: int, string_length_mm: float
):
    x1, x2 = margin["left"], margin["left"] + neck_width
    saddle_y = margin["top"] + nut_to_saddle
    cv2.line(image, (x1, saddle_y), (x2, saddle_y), FRET_LINE_COLOR, 2 * FRET_LINE_THICKNESS)
    _put_text(image, "SADDLE", (int((x1 + x2) / 2), saddle_y), center=True)
    length_text = f"{string_length_mm:.2f} mm"
    length_text_x = margin["left"] - _get_text_size(length_text)[0]
    _put_text(image, length_text, (length_text_x, saddle_y))


def draw_tar(string: Dict[int, Note], string_length_mm: float = 660, nut_to_saddle: int = 1200):
    """Draw the neck of the tar, from nut to saddle, with frets and info"""
    neck_width, neck_height = _neck_size(nut_to_saddle)
    image, margin = _create_image(string, string_length_mm, nut_to_saddle, neck_width)
    _draw_neck(image, (neck_width, neck_height), (margin["left"], margin["top"]))
    _draw_nut(image, margin, neck_width)
    _draw_saddle(image, margin, neck_width, nut_to_saddle, string_length_mm)

    base_note = string[0]
    for fret_number, note in string.items():
        # ratio: (distance of fret from saddle / nut-to-saddle_distance)
        ratio = _length_ratio(base_note, note)
        fret_y = margin["top"] + int((1 - ratio) * nut_to_saddle)
        _draw_fret(image, (margin["left"], fret_y), (margin["left"] + neck_width, fret_y))
        text_x = margin["left"] + neck_width + int(neck_width / 10)
        _put_text(image, f"{fret_number} : {_fret_label(note)}", (text_x, fret_y))
        length_text = _length_label(base_note, note, string_length_mm)
        length_text_x = margin["left"] - _get_text_size(length_text)[0]
        _put_text(image, length_text, (length_text_x, fret_y))

    return image
