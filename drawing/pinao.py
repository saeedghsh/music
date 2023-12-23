"""Piano drawing utils"""
# pylint: disable=no-member
from functools import partial
from typing import Tuple, Optional

import cv2
import numpy as np


_WHITE_KEY_HEIGHT = 300
_WHITE_KEY_WIDTH = int(0.1 * _WHITE_KEY_HEIGHT)
_WHITE_TEXT_X_OFFSET = int(0.4 * _WHITE_KEY_WIDTH)
_WHITE_TEXT_Y_OFFSET = -int(0.02 * _WHITE_KEY_HEIGHT)

_BLACK_KEY_WIDTH = int(0.08 * _WHITE_KEY_HEIGHT)
_BLACK_KEY_HEIGHT = int(0.5 * _WHITE_KEY_HEIGHT)
_BLACK_TEXT_X_OFFSET = int(0.3 * _BLACK_KEY_WIDTH)
_BLACK_TEXT_Y_OFFSET = -int(0.02 * _BLACK_KEY_HEIGHT)

_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
_FONT_SCALE = 0.0015 * _WHITE_KEY_HEIGHT


def _text_on_key(
    image: np.ndarray,
    text: str,
    posistion: Tuple[int],
    key_color: str,
    key_height: int,
):
    (text_width, text_height), _ = cv2.getTextSize(text, _FONT_FACE, _FONT_SCALE, 1)
    text_img = np.zeros((text_height + 1, text_width + 1, 3), dtype=np.uint8)
    if key_color == "black":
        text_color = (255, 255, 255)
        text_img.fill(0)
    if key_color == "white":
        text_color = (0, 0, 0)
        text_img.fill(255)
    cv2.putText(
        text_img,
        text,
        (0, text_height),
        _FONT_FACE,
        _FONT_SCALE,
        text_color,
        1,
        cv2.LINE_AA,
    )
    rotated_img = cv2.rotate(text_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    y_pos = posistion[1] + key_height - rotated_img.shape[0]
    image[
        y_pos : y_pos + rotated_img.shape[0],
        posistion[0] : posistion[0] + rotated_img.shape[1],
    ] = rotated_img


def _key_black(image: np.ndarray, x: int, label: str):
    _black_text = partial(_text_on_key, key_color="black", key_height=_BLACK_KEY_HEIGHT)
    pt1 = (x, 0)
    pt2 = (x + _BLACK_KEY_WIDTH, _BLACK_KEY_HEIGHT)
    cv2.rectangle(image, pt1, pt2, (0, 0, 0), -1)
    text_x = x + _BLACK_TEXT_X_OFFSET
    text_y = _BLACK_TEXT_Y_OFFSET
    _black_text(image, label, (text_x, text_y))


def _key_white(image: np.ndarray, x: int, label: str):
    _white_text = partial(_text_on_key, key_color="white", key_height=_WHITE_KEY_HEIGHT)
    pt1 = (x, 0)
    pt2 = (x + _WHITE_KEY_WIDTH, _WHITE_KEY_HEIGHT)
    cv2.rectangle(image, pt1, pt2, (0, 0, 0), 1)
    text_x = x + _WHITE_TEXT_X_OFFSET
    text_y = _WHITE_TEXT_Y_OFFSET
    _white_text(image, label, (text_x, text_y))


def _image_size(keys: dict) -> Tuple[int, int]:
    num_black_keys = len([_ for _, accidental, _ in keys if accidental == "#"])
    num_white_keys = len(keys) - num_black_keys
    piano_width = num_white_keys * _WHITE_KEY_WIDTH
    piano_height = _WHITE_KEY_HEIGHT
    return piano_width, piano_height


def _key_color(key: Tuple[str, str, int]) -> bool:
    _, accidental, _ = key
    return "black" if accidental == "#" else "white"


def _key_label(key: Tuple[str, str, int], freq) -> str:
    note, accidental, octave = key
    return f"{note}{accidental}{octave}: {freq:.2f} Hz"


def draw_piano(keys: dict, show: bool, save: bool, file_path: Optional[str]):
    """Create an image to draw the piano"""

    width, height = _image_size(keys)
    piano = np.ones((height, width, 3), dtype=np.uint8) * 255

    x = 0
    for key, freq in keys.items():
        if _key_color(key) == "white":
            _key_white(piano, x, _key_label(key, freq))
            x += _WHITE_KEY_WIDTH

    # Have to draw all blacks after whites,
    # otherwise drawing a white after black will upset the black
    x = 0
    for key, freq in keys.items():
        if _key_color(key) == "black":
            _key_black(piano, x - _BLACK_KEY_WIDTH // 2, _key_label(key, freq))
        else:
            x += _WHITE_KEY_WIDTH

    if save:
        if file_path is None:
            raise ValueError("Is save is True, file_path cannot be None")
        cv2.imwrite(file_path, piano)

    if show:
        cv2.imshow(f"{len(keys)} keys Piano", piano)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
