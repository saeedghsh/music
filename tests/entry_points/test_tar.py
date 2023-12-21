"""Test Tar entry point script"""
import os
import pytest

from entry_points.tar import main


@pytest.mark.parametrize("string_number", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("fret_count", [25, 27, 28])
def test_main_smoke_test(fret_count: int, string_number: int):
    # pylint: disable=missing-function-docstring
    args = [
        "--fret-count",
        str(fret_count),
        "--string-number",
        str(string_number),
    ]
    result = main(args)
    assert result == os.EX_OK


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
