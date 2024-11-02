# tabs2music
Converts guitar tabs (.txt) into audio (.wav)


## Getting started
1. Run `pip install tabs2music`
2. Download a soundfont, such as [this](https://drive.google.com/drive/folders/1rUSSwPpzpxl2Tg8Jn3kWqOimlxZZPAjN?usp=sharing) one
3. You're done!

To use the library, you should use the `run` function. The `run` function takes the following parameters:
- tabs_path: a path to the .txt file containing the tabs input. The name of the file will be the song's name.
- audio_save_path: a path to the directory the .midi and .wav files will be saved to.
- soundfont_path: a path to the soundfont file.
- save_midi (optional, default=False): if True, the .midi file will be saved, otherwise it is deleted.
- play_midi (optional, default=False): if True, the .midi file will be played via the terminal on creation, otherwise nothing is played.
- tempo (optional, default=120): measured in bpm, changes the speed of the song.

Here is a minimal example that doesn't override the optional values: 
`run("/path/to/song.txt", "/path/to/save/", "/path/with/soundfont.sf2")`

Here is an example that overrides all of the optional values: 
`run("/path/to/song.txt", "/path/to/save/", "/path/with/soundfont.sf2", save_midi=True, play_midi=True, tempo=200)`


## How to write a tabs file
### Tuning a guitar string
Every guitar tab has six lines, one for each of the six strings on the guitar. However feel free to add more or less "strings", as the code doesn't care how many you want to add. Every string is written on its own line, and must follow a certain pattern, which can be split into two parts: 
1. **The string's tuning:** A string's tuning is defined by combing a note with an octave number (no spaces in between). So "E2", "G#3", and "Db4" are all valid tunings.
2. **The string's notes:** After the string's tuning comes the notes to be played on the string. This section must begin with "|-", and must end with "-|", where the "|"s represent the start/end of a bar, and the "-"s provide a space in between every other note for easier reading. So a single bar in 4/4 might look like "|-1-2-3-4-|". To make more than one bar, you simply continue this pattern, like "|-1-2-3-4-|-2-3-4-5-|" for two bars.

Now lets put these two halves together. Here is an example of a string tuned to E2, the standard tuning used on the lowest guitar string, with enough notes for a bar in 4/4. Please note the formatting/spaces, it must be followed as well: "E2 |-1-2-3-4-|".

### Allowed notation
Once you have defined a string, you can start writing notes to be played on that string. Each note is surrounded by a "-", which makes it a bit easier to read the tabs. This can already be seen above in the section [Creating a guitar string](#creating-a-guitar-string). Here are the currently supported options:
- **A number:** When writing a number, this indicates the fret to play on the string.
- **A note extension** (~)**:** After a note has been played (indicated by a number), each "~" directly after it will extend the note for as many "~"s used. Here is an example that plays an open low E for four beats: "E2 |-0-~-~-~-|".
- **A rest** (-)**:** This is used when neither a number or "~" are specified. It simply doesn't play anything on the string for a single beat.


## Example tabs file
Copy and paste this into a .txt file, its the background guitar for "All in the Waiting" by Buckethead.

```
E4 |-3-----2-------2-|-3-----2-------2-|-2-----0-------0-|-2-----0-------0-|-2-----3-------3-|-2-----3-------3-|-3-----2-------2-|-3-----2-------2-|
B3 |---3-----3---3---|---3-----3---3---|---3-----3---3---|---3-----3---3---|---3-----3---3---|---3-----3---3---|---3-----3---3---|---3-----3---3---|
G3 |-----0-----0-----|-----0-----0-----|-----0-----0-----|-----0-----0-----|-----0-----0-----|-----0-----0-----|-----0-----0-----|-----0-----0-----|
D3 |-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|
A2 |-----------------|-----------------|-2-~-~-~-~-~-~-~-|-2-~-~-~-~-~-~-~-|-3-~-~-~-~-~-~-~-|-3-~-~-~-~-~-~-~-|-----------------|-----------------|
E2 |-3-~-~-~-~-~-~-~-|-3-~-~-~-~-~-~-~-|-----------------|-----------------|-----------------|-----------------|-3-~-~-~-~-~-~-~-|-3-~-~-~-~-~-~-~-|
```


## Upcoming features:
1. Enforce more things with the tab's construction
    - a given bar is in the same time signature for all strings (equal length of notes)
2. More note timing flexibility (ex: triplets)
3. Need to add soundfont to support hammer ons (h), pull offs (p), sliding up (/) and down (\\), bending up (b) and down (r), and vibrato (v)
4. Capo
5. When on the website, make tabs also downloadable