"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import os
import pytest

from entry_points.piano import main


def test_main_smoke_test():
    args = []
    result = main(args)
    assert result == os.EX_OK


def test_main_file_save(tmp_path: str):
    output_file = os.path.join(tmp_path, "piano.png")
    args = [
        "-s",
        "-f",
        output_file,
    ]
    result = main(args)
    assert result == os.EX_OK
    assert os.path.isfile(output_file), "File was not created"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
