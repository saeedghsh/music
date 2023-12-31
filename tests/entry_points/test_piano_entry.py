# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import subprocess

import pytest

from entry_points.piano_entry import main


def test_piano_entry_point_script_smoke_test():
    cmd = ["python3", "-m", "entry_points.piano_entry"]
    result = subprocess.run(cmd, capture_output=True, check=False)
    assert result.returncode == 0


def test_piano_entry_main_smoke_test():
    args = []
    result = main(args)
    assert result == os.EX_OK


def test_piano_entry_main_show(mocker):
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord("q"))
    mocker.patch("cv2.destroyAllWindows")
    args = ["-v"]
    result = main(args)
    assert result == os.EX_OK


def test_piano_entry_main_file_save(tmp_path: str):
    output_file = os.path.join(tmp_path, "piano.png")
    args = [
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
