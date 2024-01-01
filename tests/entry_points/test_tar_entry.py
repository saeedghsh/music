# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import subprocess

import pytest

from entry_points.tar_entry import main


def test_tar_entry_point_script_smoke_test():
    cmd = ["python3", "-m", "entry_points.tar_entry"]
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode == 0


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_tar_entry_main_smoke_test(fret_count: int, string_number: int):
    args_base = [
        "--fret-count",
        str(fret_count),
        "--string-number",
        str(string_number),
    ]
    result = main(args_base)
    assert result == os.EX_OK


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_tar_entry_main_smoke_test_print_out(fret_count: int, string_number: int):
    args_base = [
        "--fret-count",
        str(fret_count),
        "--string-number",
        str(string_number),
        "-p",
    ]
    result = main(args_base)
    assert result == os.EX_OK


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
def test_tar_entry_main_show(mocker, string_number: int):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = [
        "--fret-count",
        str(27),
        "--string-number",
        str(string_number),
        "-v",
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("fret_count", [25, 28])
def test_tar_entry_main_show_not_implemented(mocker, fret_count: int, string_number: int):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = [
        "--fret-count",
        str(fret_count),
        "--string-number",
        str(string_number),
        "-v",
    ]
    with pytest.raises(NotImplementedError):
        main(args)


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
def test_tar_entry_main_file_save(tmp_path: str, string_number: int):
    output_file = os.path.join(tmp_path, "annotated_tar.png")
    args = [
        "--fret-count",
        str(27),
        "--string-number",
        str(string_number),
        "-s",
    ]
    with pytest.raises(ValueError):
        main(args)

    args.extend(["-f", output_file])
    result = main(args)
    assert result == os.EX_OK
    assert os.path.isfile(output_file)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
