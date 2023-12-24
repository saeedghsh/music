"""Test Tar entry point script"""
# pylint: disable=missing-function-docstring
import os

import pytest

from entry_points.tar import main


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_main_smoke_test(fret_count: int, string_number: int):
    args = [
        "--fret-count",
        str(fret_count),
        "--string-number",
        str(string_number),
    ]
    result = main(args)
    assert result == os.EX_OK


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
def test_main_file_save(tmp_path: str, string_number: int):
    output_file = os.path.join(tmp_path, "annotated_tar.png")
    args = [
        "--fret-count",
        str(27),
        "--string-number",
        str(string_number),
        "-s",
        "-f",
        output_file,
    ]
    result = main(args)
    assert result == os.EX_OK
    assert os.path.isfile(output_file), "File was not created"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
