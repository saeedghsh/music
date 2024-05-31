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


def test_musical_interval_as_quartertone_steps():
    assert MusicalInterval.as_quartertone_steps(MusicalInterval.OCTAVE) == 24
    assert MusicalInterval.as_quartertone_steps(MusicalInterval.TONE) == 4
    assert MusicalInterval.as_quartertone_steps(MusicalInterval.SEMITONE) == 2
    assert MusicalInterval.as_quartertone_steps(MusicalInterval.QUARTERTONE) == 1


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
