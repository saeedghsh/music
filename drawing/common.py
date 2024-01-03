"""Piano drawing utils"""
# pylint: disable=no-member
from typing import Optional, Union

import cv2
import numpy as np

COLOR_BRG = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "light_brown": (205, 222, 239),
    "dark_brown": (33, 67, 101),
}


def pad_to_square(image: np.ndarray, pad_value: Union[int, np.uint8]) -> np.ndarray:
    """Return a copy of the image that is padded to be square(i.e. h=w)"""
    height, width, _ = image.shape
    if height == width:
        return image
    top = bottom = left = right = 0
    diff = abs(height - width)
    if height > width:
        left = right = diff // 2
        right += diff % 2
    else:
        top = bottom = diff // 2
        bottom += diff % 2
    return np.pad(
        image, ((top, bottom), (left, right), (0, 0)), "constant", constant_values=pad_value
    )


def _rad_to_deg(rad: float) -> float:
    return 180 * rad / np.pi


def rotate_image(image: np.ndarray, angle: float, bg_color: int):
    """Rotate an image by an arbitrary angle.
    image_size is (h,w,3) and angle is in radian
    """
    height, width, _ = image.shape
    image_center = tuple(np.array([width, height]) / 2)
    rotation = cv2.getRotationMatrix2D(image_center, _rad_to_deg(angle), 1.0)
    result = cv2.warpAffine(
        image,
        rotation,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderValue=(bg_color, bg_color, bg_color),
    )
    return result


def show_image(image: np.ndarray, window_name: str = ""):
    """Show image"""
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_image(image: np.ndarray, file_path: Optional[str]):
    """Save image to specified path using"""
    if file_path is None:
        raise ValueError("file_path cannot be None")
    cv2.imwrite(file_path, image)
