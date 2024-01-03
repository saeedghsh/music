"""Piano drawing utils"""
# pylint: disable=no-member
from functools import partial
from typing import List

import cv2
import numpy as np

from core.frequency import Frequency
from core.notes import Note
from drawing.common import COLOR_BRG, pad_to_square, rotate_image

HEIGHT = WIDTH = 1000
CENTER = (HEIGHT // 2, WIDTH // 2)
RADIUS = int(0.48 * HEIGHT)
FONT_SCALE = HEIGHT / 1500
FONT_THICKNESS = 1
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
TEXT_RADIUS = 0.32 * HEIGHT


_get_text_size = partial(
    cv2.getTextSize, fontFace=FONT_FACE, fontScale=FONT_SCALE, thickness=FONT_THICKNESS
)
_put_text = partial(
    cv2.putText,
    fontFace=FONT_FACE,
    fontScale=FONT_SCALE,
    color=COLOR_BRG["black"],
    thickness=FONT_THICKNESS,
)


def _write_on_wedge(image: np.ndarray, angle: float, label: str):
    (text_width, text_height) = _get_text_size(label)[0]
    text_img = np.zeros((text_height + 1, text_width + 1, 3), dtype=np.uint8)
    text_img.fill(255)
    _put_text(text_img, label, (0, text_height))
    text_img = pad_to_square(text_img, np.uint8(255))
    # if inwards writing is desired angle=(np.pi - angle)
    rotated_image = rotate_image(image=text_img, angle=-angle, bg_color=255)
    x_pos = int(CENTER[0] + TEXT_RADIUS * np.cos(angle)) - rotated_image.shape[0] // 2
    y_pos = int(CENTER[1] + TEXT_RADIUS * np.sin(angle)) - rotated_image.shape[1] // 2
    row1, row2 = y_pos, y_pos + rotated_image.shape[0]
    col1, col2 = x_pos, x_pos + rotated_image.shape[1]
    # The use of mask performs a selective copy of the rotated_image to image to avoid the white
    # surrounding of each rotated_image overwrite the previous one. This implementation is very
    # simplistic and only works if color is black. The check is to safeguard for change of COLOR.
    # But since not really covered by tests, hence the "no cover" directive.
    if COLOR_BRG["black"] != (0, 0, 0):  # pragma: no cover
        image[row1:row2, col1:col2] = rotated_image
    else:
        mask = rotated_image < 200
        image[row1:row2, col1:col2][mask] = 0


def _draw_radius(image: np.ndarray, angle: float):
    end_x = int(CENTER[0] + RADIUS * np.cos(angle))
    end_y = int(CENTER[1] + RADIUS * np.sin(angle))
    cv2.line(image, CENTER, (end_x, end_y), COLOR_BRG["black"], 1)


def _print_a4_frequency(image: np.ndarray, frequency: Frequency):
    label = f"A4: {frequency.value} Hz"
    x_pos = WIDTH // 100
    y_pos = HEIGHT // 50
    _put_text(image, label, (x_pos, y_pos))


def draw_circle(notes: List[Note]) -> np.ndarray:
    """Create an image and draw notes on a circle"""
    image = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * np.uint8(255)
    angle_steps = 2 * np.pi / len(notes)
    cv2.circle(image, CENTER, RADIUS, COLOR_BRG["black"], 1)
    _print_a4_frequency(image, notes[0].a4_frequency)
    for i, note in enumerate(notes):
        angle = (i + 0.5) * angle_steps
        label = f"{i}: {note.name} - {note.frequency.value:.2f} Hz"
        # label = f"{i}: {note.name}"
        _write_on_wedge(image, angle, label)
    for i in range(len(notes)):
        angle = i * angle_steps
        _draw_radius(image, angle)
    return image
