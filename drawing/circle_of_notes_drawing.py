"""Piano drawing utils"""
# pylint: disable=no-member
from functools import partial
from typing import List

import cv2
import numpy as np

from core.notes import Note
from drawing.common import pad_to_square, rotate_image

COLOR = (0, 0, 0)
HEIGHT = WIDTH = 1000
CENTER = (HEIGHT // 2, WIDTH // 2)
RADIUS = int(0.48 * HEIGHT)
FONT_SCALE = HEIGHT / 1500
FONT_THICKNESS = 1
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
TEXT_RADIUS = 0.4 * HEIGHT


_get_text_size = partial(
    cv2.getTextSize, fontFace=FONT_FACE, fontScale=FONT_SCALE, thickness=FONT_THICKNESS
)
_put_text = partial(
    cv2.putText, fontFace=FONT_FACE, fontScale=FONT_SCALE, color=COLOR, thickness=FONT_THICKNESS
)


def _text_on_wedge(image: np.ndarray, angle: float, label: str):
    (text_width, text_height) = _get_text_size(label)[0]
    text_img = np.zeros((text_height + 1, text_width + 1, 3), dtype=np.uint8)
    text_img.fill(255)
    _put_text(text_img, label, (0, text_height))
    text_img = pad_to_square(text_img, np.uint8(255))
    # if inwards writing is desired angle=(np.pi - angle)
    rotated_img = rotate_image(image=text_img, angle=-angle, bg_color=255)
    x_pos = int(CENTER[0] + TEXT_RADIUS * np.cos(angle)) - rotated_img.shape[0] // 2
    y_pos = int(CENTER[1] + TEXT_RADIUS * np.sin(angle)) - rotated_img.shape[1] // 2
    image[
        y_pos : y_pos + rotated_img.shape[0],
        x_pos : x_pos + rotated_img.shape[1],
    ] = rotated_img


def _draw_radius(image: np.ndarray, angle: float):
    end_x = int(CENTER[0] + RADIUS * np.cos(angle))
    end_y = int(CENTER[1] + RADIUS * np.sin(angle))
    cv2.line(image, CENTER, (end_x, end_y), COLOR, 1)


def draw_circle(notes: List[Note]) -> np.ndarray:
    """Create an image and draw notes on a circle"""
    image = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * np.uint8(255)
    angle_steps = 2 * np.pi / len(notes)
    cv2.circle(image, CENTER, RADIUS, COLOR, 1)
    for i, note in enumerate(notes):
        angle = (i + 0.5) * angle_steps
        label = f"{i}: {note.name}"
        _text_on_wedge(image, angle, label)
    for i in range(len(notes)):
        angle = i * angle_steps
        _draw_radius(image, angle)
    return image
