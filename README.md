# Playground for fiddle with musical notes

I wanted to redo the [frets](https://en.wikipedia.org/wiki/Fret) of my [Setar](https://en.wikipedia.org/wiki/Setar).
Common instructions are based on length of the [strings](https://en.wikipedia.org/wiki/String_(music)) and the distance of each fret from the [nut](https://en.wikipedia.org/wiki/Nut_(string_instrument)).
I don't like inaccuracies, so instead, I decided to find the accurate location of each fret based on the frquency.
To this end I needed to calculate the frequency of the [notes](https://en.wikipedia.org/wiki/Musical_note) corresponding to each fret.
Iranian music, and consequently the Setar, has [quarter tones](https://en.wikipedia.org/wiki/Quarter_tone) [accidentals](https://en.wikipedia.org/wiki/Accidental_(music)) ([Koron](https://en.wikipedia.org/wiki/Koron_(music)) and [Sori](https://en.wikipedia.org/wiki/Sori_(music))).
Therfore a hash-like table listing all notes available for conventional western musical instruments with [semitone](https://en.wikipedia.org/wiki/Semitone) granularity was not enough.
I started a python script to calculte the note frequencies for that purpose, ... and kinda got carried away... hence this repo.


## Example
Piano entry point:
```bash
python3 -m entry_points.piano -v
```


* Synthesizing all keys and notes of piano
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/pinao_keys_frquencies.png">
</p>

* Annotating the frets of Tar with note and frequency (string 1 version)
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/tar_small_1290x362_string1_annotated.jpg">
</p>


# TODO
```
Legend
* [ ] TODO
* [x] DONE
* [x] [d] DISCARD (temp and perm)
* [x] [p] PAUSED
* [x] [.] HALFASSED
```

### Imediate/Essential
* [ ] add test
* [ ] add entry points for Tar

### CI
* [ ] CI: hookup the repo with gitbut CI
* [x] CI: pylint
* [ ] CI: formatter
* [ ] CI: tests
* [ ] CI: make CI green

### Improve/Refactring
* [ ] `transposition_by_an_octave` to `transpose_by(interval: MusicalInterval, steps: int)`
* [ ] make note name validation a process separate from `Note.decompose_name`
* [ ] make use of `Note` class everywhere; `FrequencyCOmputer`, `instruments.py`, `drawing.py`
* [ ] move `drawing.py` under `drawing` dir and make a file per instrument
* [ ] encapsulate each instrument into a `class` of `instrument`,
* [ ] move `instruments.py` under `instruments` dir and make a file per instrument
* [ ] use `Note.__str__` whereever note is printed, and make sure it is printer properly
* [ ] use `cv2` (or `qt`) for piano drawing

### Improve/Extention
* [ ] `generate_tar_notes` only supports the tuning of `C-G-C`. generalize the tuning.
* [ ] add common tuning for different keys ("Dastgah"): Wikipedia has a list (Double check)
* [ ] add Setar Photo.
* [ ] add Fret tying schema/drawing
* [ ] add "fret round" for Tar and Setar
* [ ] add "fret string thickness" for Tar and Setar
  ```python
  # fret round count - 25 fret - according to Wikipedia ( Double check)
  {
    1:3,
    2:4,
    3:4,
    4:4,
    5:3,
    6:4,
    7:4,
    8:?,
    9:3,
    10:3,
    11:4,
    12:[3,4],
    13:4,
    14:3,
    15:4,
    16:3,
    17:3,
    18:4,
    19:?,
    20:[3,4],
    21:4,
    22:4,
    23:3,
    24:3,
    25:4,
    26:3,
    27:4,
    28:?,
  }
  ```

### Future Work
* [ ] Add Qt gui?
* [ ] extend to other instruments, start with Guitar and then Ney?
* [ ] add audio and make it interactive?
* [ ] Add keys, scales and chords?

### Done
* [x] add entry points for Piano
* [x] Add different fret count systems for Setar / Tar (25, 27, and 28)
* [x] change `accidental.unidoce_char` to `symbol` and find a better name for `accidental.shorthand`
* [x] make a enum for Octave.
* [x] make a enum for Accidentals.
* [x] [p] right now the accidentals are printed as `{#,b,s,k}` (e.g. tar annotation) fix it so that proper symbols are printed.
      This might be not feasible for koron and sori right now, but should be doable for sharp and flat.
* [x] Make frequency computer a separate class from note
* [x] [d] fix issue with printing `sori` and `koron` symbols,
        -> This turned to be much harder than I expected. Skipping for now        
* [x] add a drawing of Tar and visaulize its notes and frequencies.
* [x] `quartertone` -> `quartertone`

# Reference
* [Proposal to encode two accidentals for Iranian classical music](https://www.unicode.org/L2/L2020/20159-iran-music-symbols.pdf)
* Setar on Wikipedai: [Farsi entry]((https://fa.wikipedia.org/wiki/%D8%B3%D9%87%E2%80%8C%D8%AA%D8%A7%D8%B1)) and [English entry](https://en.wikipedia.org/wiki/Setar).

# License
```
Copyright (C) Saeed Gholami Shahbandi
```
 
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/3D_models/blob/master/LICENSE).
