"""Some drawing utils"""
from functools import partial
from typing import Tuple, Optional

import cv2
import numpy as np

# pylint: disable=no-member

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


# piano_keys = {
#     ("C", "", 0): 16.351597831287414,
#     ("C", "#", 0): 17.323914436054505,
#     ("D", "", 0): 18.354047994837977,
#     ("D", "#", 0): 19.445436482630058,
#     ("E", "", 0): 20.601722307054366,
#     ("F", "", 0): 21.826764464562746,
#     ("F", "#", 0): 23.12465141947715,
#     ("G", "", 0): 24.499714748859326,
#     ("G", "#", 0): 25.956543598746574,
#     ("A", "", 0): 27.5,
#     ("A", "#", 0): 29.13523509488062,
#     ("B", "", 0): 30.86770632850775,
#     ("C", "", 1): 32.70319566257483,
#     ("C", "#", 1): 34.64782887210901,
#     ("D", "", 1): 36.70809598967594,
#     ("D", "#", 1): 38.890872965260115,
#     ("E", "", 1): 41.20344461410875,
#     ("F", "", 1): 43.653528929125486,
#     ("F", "#", 1): 46.2493028389543,
#     ("G", "", 1): 48.999429497718666,
#     ("G", "#", 1): 51.91308719749314,
#     ("A", "", 1): 55.0,
#     ("A", "#", 1): 58.27047018976124,
#     ("B", "", 1): 61.7354126570155,
#     ("C", "", 2): 65.40639132514966,
#     ("C", "#", 2): 69.29565774421802,
#     ("D", "", 2): 73.41619197935188,
#     ("D", "#", 2): 77.78174593052023,
#     ("E", "", 2): 82.4068892282175,
#     ("F", "", 2): 87.30705785825097,
#     ("F", "#", 2): 92.4986056779086,
#     ("G", "", 2): 97.99885899543733,
#     ("G", "#", 2): 103.82617439498628,
#     ("A", "", 2): 110.0,
#     ("A", "#", 2): 116.54094037952248,
#     ("B", "", 2): 123.47082531403103,
#     ("C", "", 3): 130.8127826502993,
#     ("C", "#", 3): 138.59131548843604,
#     ("D", "", 3): 146.8323839587038,
#     ("D", "#", 3): 155.56349186104046,
#     ("E", "", 3): 164.81377845643496,
#     ("F", "", 3): 174.61411571650194,
#     ("F", "#", 3): 184.9972113558172,
#     ("G", "", 3): 195.99771799087463,
#     ("G", "#", 3): 207.65234878997256,
#     ("A", "", 3): 220.0,
#     ("A", "#", 3): 233.08188075904496,
#     ("B", "", 3): 246.94165062806206,
#     ("C", "", 4): 261.6255653005986,
#     ("C", "#", 4): 277.1826309768721,
#     ("D", "", 4): 293.6647679174076,
#     ("D", "#", 4): 311.1269837220809,
#     ("E", "", 4): 329.6275569128699,
#     ("F", "", 4): 349.2282314330039,
#     ("F", "#", 4): 369.9944227116344,
#     ("G", "", 4): 391.99543598174927,
#     ("G", "#", 4): 415.3046975799451,
#     ("A", "", 4): 440.0,
#     ("A", "#", 4): 466.1637615180899,
#     ("B", "", 4): 493.8833012561241,
#     ("C", "", 5): 523.2511306011972,
#     ("C", "#", 5): 554.3652619537442,
#     ("D", "", 5): 587.3295358348151,
#     ("D", "#", 5): 622.2539674441618,
#     ("E", "", 5): 659.2551138257398,
#     ("F", "", 5): 698.4564628660078,
#     ("F", "#", 5): 739.9888454232688,
#     ("G", "", 5): 783.9908719634985,
#     ("G", "#", 5): 830.6093951598903,
#     ("A", "", 5): 880.0,
#     ("A", "#", 5): 932.3275230361799,
#     ("B", "", 5): 987.7666025122483,
#     ("C", "", 6): 1046.5022612023945,
#     ("C", "#", 6): 1108.7305239074883,
#     ("D", "", 6): 1174.6590716696303,
#     ("D", "#", 6): 1244.5079348883237,
#     ("E", "", 6): 1318.5102276514797,
#     ("F", "", 6): 1396.9129257320155,
#     ("F", "#", 6): 1479.9776908465376,
#     ("G", "", 6): 1567.981743926997,
#     ("G", "#", 6): 1661.2187903197805,
#     ("A", "", 6): 1760.0,
#     ("A", "#", 6): 1864.6550460723597,
#     ("B", "", 6): 1975.533205024496,
#     ("C", "", 7): 2093.004522404789,
#     ("C", "#", 7): 2217.4610478149766,
#     ("D", "", 7): 2349.31814333926,
#     ("D", "#", 7): 2489.0158697766474,
#     ("E", "", 7): 2637.02045530296,
#     ("F", "", 7): 2793.825851464031,
#     ("F", "#", 7): 2959.955381693075,
#     ("G", "", 7): 3135.9634878539946,
#     ("G", "#", 7): 3322.437580639561,
#     ("A", "", 7): 3520.0,
#     ("A", "#", 7): 3729.3100921447194,
#     ("B", "", 7): 3951.066410048992,
# }


# draw_piano(keys=piano_keys, show=True, save=False)
