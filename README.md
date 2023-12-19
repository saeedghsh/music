# Playground for fiddle with musical notes

* Synthesizing all keys and notes of piano
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/pinao_keys_frquencies.png">
</p>

* Annotating the frets of Tar with note and frequency (string 1 version)
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/tar_small_1290x362_string1_annotated.jpg"  style="transform: rotate(90deg);">
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

* [ ] add test
* [ ] hookup the repo with gitbut CI

* [ ] Add Setar Photo.
* [ ] Add Fret tying schema/drawing

* [ ] make note name validation a process separate from `Note.decompose_name`
* [ ] make use of `Note` class everywhere; `FrequencyCOmputer`, `instruments.py`, `drawing.py`
* [ ] add an entry point (`main.py`), from which can call drawing functions with proper CLI
* [ ] move `drawing.py` under `drawing` dir and make a file per instrument
* [ ] move `instruments.py` under `instruments` dir and make a file per instrument

* [ ] encapsulate each instrument into a `class` of `instrument`,
 
* [ ] `generate_tar_notes` only supports the tuning of `C-G-C`. generalize the tuning.
* [ ] Add common tuning for different keys ("Dastgah"): Wikipedia has a list (Double check)
* [ ] add "fret round" for Tar and Setar 
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


* [ ] add "fret string thickness" for Tar and Setar

* [ ] use `Note.__str__` whereever note is printed, and make sure it is printer properly
* [ ] use cv2 ot qt for piano drawing
* [ ] Add Qt gui?

* [ ] extend to other instruments, start with Guitar and then Ney
* [ ] add audio and make it interactive?
* [ ] Add keys, scales and chords?

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
* [Setar](https://fa.wikipedia.org/wiki/%D8%B3%D9%87%E2%80%8C%D8%AA%D8%A7%D8%B1) (Farsi entry).

# License
```
Copyright (C) Saeed Gholami Shahbandi
```
 
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/3D_models/blob/master/LICENSE).
