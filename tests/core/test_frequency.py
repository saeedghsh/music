"""Test Piano entry point script"""
# pylint: disable=missing-function-docstring
import pytest

from core.frequency import Frequency


def test_frequency_creation():
    freq = Frequency(50.0)
    assert freq.value == 50.0
    assert str(freq) == "50.0"
    assert repr(freq) == "50.0 Hz"


def test_frequency_creation_fail():
    with pytest.raises(ValueError):
        Frequency(-1.0)
    with pytest.raises(ValueError):
        Frequency(0.0)


def test_frequency_equality():
    freq1 = Frequency(50.0)
    freq2 = Frequency(50.000000001)
    freq3 = Frequency(50.1)
    assert freq1 == freq2
    assert freq1 != freq3
    assert freq1 == 50.0
    assert freq1 != 50.1
    assert freq1.__eq__("50") is NotImplemented  # pylint: disable=unnecessary-dunder-call


def test_frequency_less_than():
    freq1 = Frequency(50.0)
    freq2 = Frequency(50.1)
    assert freq1 < freq2
    assert freq1 < 50.1
    assert freq1.__lt__("50") is NotImplemented  # pylint: disable=unnecessary-dunder-call


def test_frequency_add():
    freq1 = Frequency(50.0)
    freq2 = Frequency(20.0)
    assert freq1 + freq2 == 70
    assert freq1 + 20.0 == 70
    assert freq1.__add__("50") is NotImplemented  # pylint: disable=unnecessary-dunder-call


def test_frequency_mul():
    freq1 = Frequency(50.0)
    freq2 = Frequency(20.0)
    assert freq1 * 2 == 100
    assert freq1.__mul__("2") is NotImplemented  # pylint: disable=unnecessary-dunder-call
    assert freq1.__mul__(freq2) is NotImplemented  # pylint: disable=unnecessary-dunder-call


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
