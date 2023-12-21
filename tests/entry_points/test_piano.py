"""Test Tar entry point script"""
import os
import pytest

from entry_points.piano import main


def test_main_smoke_test():
    # pylint: disable=missing-function-docstring
    args = []
    result = main(args)
    assert result == os.EX_OK


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
