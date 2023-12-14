# Playground for fiddle with musical notes

* Synthesizing all keys and notes of piano
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/pinao_keys_frquencies.png">
</p>

* Annotating the frets of Tar with note and frequency (string 1 version)
<p align="center">
    <img src="https://github.com/saeedghsh/musical_notes/blob/master/images/tar_small_1290x362_string1_annotated.jpg"  style="transform: rotate(90deg);">
</p>


### TODO
* [x] add a drawing of Tar and visaulize its notes and frequencies.

* [ ] make use of `Note` class everywhere; `instruments.py`, `drawing.py`
* [ ] add an entry point (`main.py`), from which can call drawing functions with proper CLI
* [ ] move `drawing.py` under `drawing` dir and make a file per instrument
* [ ] move `instruments.py` under `instruments` dir and make a file per instrument
* [ ] encapsulate each instrument into a `class` of `instrument`,
* [ ] fix issue with printing `sori` and `koron` symbols,
* [ ] right now the accidentals are printed as `{#,b,s,k}` (e.g. tar annotation) fix it so that proper symbols are printed
* [ ] use `Note.__str__` whereever note is printed, and make sure it is printer properly
* [ ] add test
* [ ] hookup the repo with gitbut CI
* [ ] Add Qt gui?
* [ ] extend to other instruments, start with Guitar and then Ney
* [ ] add audio and make it interactive?
* [ ] Add keys, scales and chords?


License
-------
```
Copyright (C) Saeed Gholami Shahbandi
```
 
NOTE: Portions of this code/project were developed with the assistance of ChatGPT, a product of OpenAI.  
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/3D_models/blob/master/LICENSE).
