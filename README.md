# Playground for fiddling with musical notes

[![GPLv3 License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/saeedghsh/music/blob/master/LICENSE)  
[![black](https://github.com/saeedghsh/music/actions/workflows/formatting.yml/badge.svg?branch=master)](https://github.com/saeedghsh/music/actions/workflows/formatting.yml)
[![pylint](https://github.com/saeedghsh/music/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/saeedghsh/music/actions/workflows/pylint.yml)
[![pytest](https://github.com/saeedghsh/music/actions/workflows/pytest.yml/badge.svg?branch=master)](https://github.com/saeedghsh/music/actions/workflows/pytest.yml)
[![pytest-cov](https://github.com/saeedghsh/music/actions/workflows/pytest-cov.yml/badge.svg?branch=master)](https://github.com/saeedghsh/music/actions/workflows/pytest-cov.yml)
[![mypy](https://github.com/saeedghsh/music/actions/workflows/type-check.yml/badge.svg?branch=master)](https://github.com/saeedghsh/music/actions/workflows/type-check.yml)

I wanted to redo the [frets](https://en.wikipedia.org/wiki/Fret) of my [Setar](https://en.wikipedia.org/wiki/Setar).
Common instructions are based on length of the [strings](https://en.wikipedia.org/wiki/String_(music)) and the distance of each fret from the [nut](https://en.wikipedia.org/wiki/Nut_(string_instrument)).
I don't like inaccuracies, so instead, I decided to find the accurate location of each fret based on the frequency.
To this end I needed to calculate the frequency of the [notes](https://en.wikipedia.org/wiki/Musical_note) corresponding to each fret.  

Iranian music, and consequently the Setar, has [quarter tones](https://en.wikipedia.org/wiki/Quarter_tone) [accidentals](https://en.wikipedia.org/wiki/Accidental_(music)) ([Koron](https://en.wikipedia.org/wiki/Koron_(music)) and [Sori](https://en.wikipedia.org/wiki/Sori_(music))).
Therefor a hash-like table listing all notes available for conventional western musical instruments with [semitone](https://en.wikipedia.org/wiki/Semitone) granularity was not enough.
I started a python script to calculate the note frequencies for that purpose, ... and kinda got carried away... hence this repo.

## Example
Entry point examples:
```bash
$ python3 -m entry_points.piano_entry -v
$ python3 -m entry_points.piano_entry -s -f <path-to-save-file>

$ python3 -m entry_points.tar_entry --fret-count 27 --string-number 1 -p
$ python3 -m entry_points.tar_entry --fret-count 27 --string-number 1 -v
$ python3 -m entry_points.tar_entry --fret-count 27 --string-number 1 -s -f <path-to-save-file>
```

* Piano entry point output:
<p align="center">
    <img src="https://github.com/saeedghsh/music/blob/master/images/pinao_keys_frequencies.png">
</p>

* Tar entry point output:
    <details>
        <summary> print-out</summary>

        ```bash
        0	C4:	261.6255653005986 Hz
        1	C#4:	277.1826309768721 Hz
        2	Dk4:	285.30470202322215 Hz
        3	D4:	293.6647679174076 Hz
        4	Eb4:	311.1269837220809 Hz
        5	Ek4:	320.24370022528126 Hz
        6	E4:	329.6275569128699 Hz
        7	F4:	349.2282314330039 Hz
        8	Fs4:	359.46139971304194 Hz
        9	F#4:	369.9944227116344 Hz
        10	Gk4:	380.83608684270297 Hz
        11	G4:	391.99543598174927 Hz
        12	Ab4:	415.3046975799451 Hz
        13	Ak4:	427.4740541075866 Hz
        14	A4:	440.0 Hz
        15	Bb4:	466.1637615180899 Hz
        16	Bk4:	479.82340237271336 Hz
        17	B4:	493.8833012561241 Hz
        18	C5:	523.2511306011972 Hz
        19	C#5:	554.3652619537442 Hz
        20	Dk5:	570.6094040464443 Hz
        21	D5:	587.3295358348151 Hz
        22	Eb5:	622.2539674441618 Hz
        23	Ek5:	640.4874004505624 Hz
        24	E5:	659.2551138257398 Hz
        25	F5:	698.4564628660078 Hz
        26	F#5:	739.9888454232688 Hz
        27	G5:	783.9908719634985 Hz
        ```

    </details>

<p align="center">
    <img src="https://github.com/saeedghsh/music/blob/master/images/tar_small_1290x362_string1_annotated.png" height="500">
</p>

## Tests, coverage, linter, formatter, static type check
```bash
$ black . --check
$ isort . --check-only
$ mypy . --explicit-package-bases
$ pylint $(git ls-files '*.py')
$ pytest
$ pytest --cov=. # $ pytest --cov=. --cov-report html; firefox htmlcov/index.html
```

# TODO

### Improve/Refactoring
* [ ] split `core/notation`, maybe into `notation`, `frequency`, etc. ...
* [ ] make note name validation a process separate from `decompose_note_name`
* [ ] uniform the function signatures and the way they operate for stuff under `instruments.py`
* [ ] `transposition_by_an_octave` to `transpose_by(interval: MusicalInterval, steps: int)`.
      This is a prerequisite for an easy implementation of the "tuning variation" on Tar/Setar.
* [ ] a mapping function between note and frequency, given the base note frequency.
* [ ] a mapping function between ratio of string length to ratio of resulting frequencies (are they the same?)
* [ ] fix all TODOs in the code. `pylint` is currently suppress so not to flag them, remove suppressions.
* [ ] right now we only annotate tar in drawing, should we draw something wo/ existing photos?
* [ ] `drawing` module is not actually tested and only covered through entry point unit tests. Add unittest for that.

### Documentations
* [ ] add Setar Photo.
* [ ] add Fret tying schema/drawing
* [ ] add "fret string thickness" for Tar and Setar
* [ ] add "fret round" for Tar and Setar
```python
  # fret round count for Setar - 25 fret - according to Wikipedia (double check)
  {
    1:3, 2:4, 3:4, 4:4, 5:3, 6:4, 7:4, 8:?, 9:3, 10:3,
    11:4, 12:[3,4], 13:4, 14:3, 15:4, 16:3, 17:3, 18:4, 19:?, 20:[3,4],
    21:4, 22:4, 23:3, 24:3, 25:4, 26:3, 27:4, 28:?,
  }
```

### Future Work
* [ ] `tar_string` only supports the tuning of `C4-C4-G3-G3-C4-C3`. generalize the tuning.
* [ ] add common tuning for different keys ("Dastgah"): Wikipedia has a list (Double check)
* [ ] Add keys, scales and chords?
* [ ] Add Qt gui?
* [ ] extend to other instruments, start with Guitar and then Ney?
* [ ] add audio and make it interactive?

# Reference
* Proposal to encode two accidentals for Iranian classical music: [Unicode proposal](https://www.unicode.org/L2/L2020/20159-iran-music-symbols.pdf).
* Setar on Wikipedia: [Farsi entry]((https://fa.wikipedia.org/wiki/%D8%B3%D9%87%E2%80%8C%D8%AA%D8%A7%D8%B1)) and [English entry](https://en.wikipedia.org/wiki/Setar).

# License
```
Copyright (C) Saeed Gholami Shahbandi
```
 
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/music/blob/master/LICENSE).
