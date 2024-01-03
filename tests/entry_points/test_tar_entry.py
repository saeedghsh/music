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


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_smoke_test(fret_count: int, base_note: str, a4_frequency: float):
    args = [
        "--fret-count",
        str(fret_count),
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_smoke_test_print_out(fret_count: int, base_note: str, a4_frequency: float):
    args = [
        "--fret-count",
        str(fret_count),
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
        "--print-out",
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_show_annotate(mocker, base_note: str, a4_frequency: float):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = [
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
        "--visualize",
        "--annotate",
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("fret_count", [25, 28])
def test_tar_entry_main_show_annotate_not_implemented(mocker, fret_count: int):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = [
        "--fret-count",
        str(fret_count),
        "--visualize",
        "--annotate",
    ]
    with pytest.raises(NotImplementedError):
        main(args)


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_file_save_annotate(tmp_path: str, base_note: str, a4_frequency: float):
    output_file = os.path.join(tmp_path, "annotated_tar.png")
    args = [
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
        "--save-to-file",
        "--annotate",
        "--file-path",
        output_file,
    ]
    result = main(args)
    assert result == os.EX_OK
    assert os.path.isfile(output_file)


def test_tar_entry_main_file_save_without_file_path():
    args = [
        "--base-note",
        "A3",
        "--a4-frequency",
        "440",
        "--save-to-file",
    ]
    with pytest.raises(ValueError):
        main(args)


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_show_draw(mocker, base_note: str, fret_count: int, a4_frequency: float):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = [
        "--fret-count",
        str(fret_count),
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
        "--visualize",
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("base_note", ["A3", "A#2", "Bk5", "Gs1"])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
@pytest.mark.parametrize("a4_frequency", [2, 270, 440])
def test_tar_entry_main_file_save_draw(
    tmp_path: str, base_note: str, fret_count: int, a4_frequency: float
):
    output_file = os.path.join(tmp_path, "annotated_tar.png")
    args = [
        "--fret-count",
        str(fret_count),
        "--base-note",
        base_note,
        "--a4-frequency",
        str(a4_frequency),
        "--save-to-file",
        "--file-path",
        output_file,
    ]
    result = main(args)
    assert result == os.EX_OK
    assert os.path.isfile(output_file)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
