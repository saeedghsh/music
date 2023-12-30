# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from math import isclose

import pytest

from core.notes import MusicalInterval


def test_musical_interval_values():
    assert isclose(MusicalInterval.OCTAVE.value, 2 ** (12 / 12))
    assert isclose(MusicalInterval.TONE.value, 2 ** (1 / 6))
    assert isclose(MusicalInterval.SEMITONE.value, 2 ** (1 / 12))
    assert isclose(MusicalInterval.QUARTERTONE.value, 2 ** (1 / 24))


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
