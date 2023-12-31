# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import numpy as np
import pytest

from drawing.common import pad_to_square, rotate_image


@pytest.mark.parametrize("width", [101, 200, 300])
@pytest.mark.parametrize("height", [100, 201, 300])
@pytest.mark.parametrize("pad_value", [0, 100, 255])
def test_pad_to_square(width: int, height: int, pad_value: int):
    arr = np.random.rand(height, width, 3)
    padded_arr = pad_to_square(arr, pad_value)
    # check array sizes
    assert padded_arr.shape[0] == padded_arr.shape[1]
    assert padded_arr.shape[2] == 3
    # check padding (Note that pad size is computed conservatively rather than strictly)
    if padded_arr.shape[0] > arr.shape[0]:  # top and bottom
        pad_size = (padded_arr.shape[0] - arr.shape[0]) // 2
        if pad_size > 0:
            assert np.all(padded_arr[:pad_size, :, :] == pad_value)
            assert np.all(padded_arr[-pad_size:, :, :] == pad_value)
    elif padded_arr.shape[1] > arr.shape[1]:  # left and right
        pad_size = (padded_arr.shape[1] - arr.shape[1]) // 2
        if pad_size > 0:
            assert np.all(padded_arr[:, :pad_size, :] == pad_value)
            assert np.all(padded_arr[:, -pad_size:, :] == pad_value)


@pytest.mark.parametrize("height", [101, 200])
@pytest.mark.parametrize("width", [100, 201])
@pytest.mark.parametrize("angle", [np.pi / 6, 3 * np.pi / 2])
@pytest.mark.parametrize("bg_color", [0, 100, 255])
def test_rotate_image_smoke_test(height: int, width: int, angle: float, bg_color: int):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    rotated_image = rotate_image(image, angle, bg_color)
    assert rotated_image.shape == image.shape


@pytest.mark.parametrize("height", [101, 200])
@pytest.mark.parametrize("width", [100, 201])
@pytest.mark.parametrize("angle", [np.pi / 6, 3 * np.pi / 2])
@pytest.mark.parametrize("bg_color", [0, 255])
def test_rotate_image(height: int, width: int, angle: float, bg_color: int):
    # compare two images rotate by angle and (angle + 2*pi) and (angle - 2*pi)
    image = np.random.rand(height, width, 3).astype(np.uint8)
    rotated_image_1 = rotate_image(image, angle, bg_color)
    rotated_image_2 = rotate_image(image, angle + 2 * np.pi, bg_color)
    rotated_image_3 = rotate_image(image, angle - 2 * np.pi, bg_color)
    np.array_equal(rotated_image_1, rotated_image_2)
    np.array_equal(rotated_image_1, rotated_image_3)


@pytest.mark.parametrize("height", [101, 200])
@pytest.mark.parametrize("width", [100, 201])
@pytest.mark.parametrize("bg_color", [0, 255])
def test_rotate_image_180_degrees(height: int, width: int, bg_color: int):
    image = np.random.rand(height, width, 3).astype(np.uint8)
    expected = np.flip(np.flip(image, 0), 1)
    rotated_image_1 = rotate_image(image, np.pi, bg_color)
    rotated_image_2 = rotate_image(image, -np.pi, bg_color)
    np.array_equal(rotated_image_1, expected)
    np.array_equal(rotated_image_2, expected)


@pytest.mark.parametrize("height", [101, 200])
@pytest.mark.parametrize("width", [100, 201])
@pytest.mark.parametrize("bg_color", [0, 255])
def test_rotate_image_90_degrees(height: int, width: int, bg_color: int):
    image = np.random.rand(height, width, 3).astype(np.uint8)
    # rotate +90
    expected = np.flip(np.swapaxes(image, 0, 1), 0)
    rotated_image = rotate_image(image, np.pi / 2, bg_color)
    np.array_equal(rotated_image, expected)
    # rotate -90
    expected = np.flip(np.swapaxes(image, 0, 1), 1)
    rotated_image = rotate_image(image, np.pi / 2, bg_color)
    np.array_equal(rotated_image, expected)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
