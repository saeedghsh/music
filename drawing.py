"""X"""
from functools import partial

import matplotlib.pyplot as plt
from matplotlib import patches

from music_instruments import generate_piano_keys


def _draw_key(
    axis: plt.Axes, x: float, y: float, w: float, h: float, color: str, label: str
):
    # pylint: disable=too-many-arguments
    face_color = color
    font_color = "black" if color == "white" else "white"
    fill_patch = color == "black"
    rect = patches.Rectangle(
        (x, y), w, h, edgecolor="black", facecolor=face_color, fill=fill_patch
    )
    axis.add_patch(rect)
    axis.annotate(
        label,
        (x + w / 2, y + h / 10),
        color=font_color,
        weight="bold",
        fontsize=8,
        ha="center",
        va="bottom",
        rotation="vertical",
    )


def _draw_keys(axis: plt.Axes, keys: dict):
    white_key_width = 1
    black_key_width = 0.6
    white_key_height = 5
    black_key_height = white_key_height / 2

    _draw_white_key = partial(
        _draw_key, axis=axis, w=white_key_width, h=white_key_height, color="white"
    )
    _draw_black_key = partial(
        _draw_key, axis=axis, w=black_key_width, h=black_key_height, color="black"
    )

    x = 0
    for key, freq in keys.items():
        note, accidental, octave = key
        label = f"{note}{accidental}{octave}: {freq:.2f} Hz"
        if accidental == "#":
            _draw_black_key(x=x - black_key_width / 2, y=black_key_height, label=label)
        else:
            _draw_white_key(x=x, y=0, label=label)
            x += white_key_width


def _draw_piano(keys: dict):
    _, axis = plt.subplots(figsize=(25, 5))
    white_key_count = len(keys) * (7 / 12)
    axis.set_xlim(0, white_key_count)
    axis.set_ylim(0, 5)
    axis.axis("off")
    _draw_keys(axis, keys)
    plt.tight_layout()
    plt.show()


_draw_piano(generate_piano_keys())
