# WorshipList
Last Modified: 3/17/2019

## Description

Every week for worship at LIFT Church, I have to create a chord chart for the four songs we're playing that week. This program automatically 
generates that chord chart. This can be done by the GUI (by running `make gui`) or semi-manually from the `main()` function (by running `make`). 
Semi-manually generating the document is mainly for ease of testing without having to enter each song/key every time, but can be used if you 
would like.

To generate documentation, run `make doc` in the directory with the Makefile. This will create two folders; the important files are html/index 
and latex/refman.pdf for documentation.

NOTE: Making with the GUI currently uses an absolute file path in `Main.py` on my system - if you are using this program, you will have to modify 
it.

## Song Files

Each song is stored as a text file with chords represented as Roman numerals, where "I" corresponds to the first chord of the scale, "II" to the 
second, etc. Lower case numerals denote minor chords. The program then automatically translates these numerals to standard chords, depending on 
the key specified. 

### Keywords

The song files also contain some custom symbols that are shorthand for some important functions, as follows:

| Keyword | Output |
|---|---|
|\||"\|"|
|double|"x 2"|
|triple|"x 3"|
|new|Splits a line into two lines, preserving tab stops|
|same|Denotes that two sections should appear on the same line|
|/|Denotes a chord over a bass note|
|(|"(" and denotes beginning of small text|
|)|")" and denotes end of small text|

### Assumptions

Some assumptions for how the song files are formatted:
1) The first line in the file is the title of the song, properly formatted. (eg. "Lion and the Lamb")
2) Each section (chorus, verse, bridge, etc.) is on a new line, with the first entry being the entry name and a colon. (eg. "V/Ch:")
3) The longest section name (currently) is the length of "Bridge 2:" when implemented in Word.
4) The maximum number of words in a section (currently) is three. (eg. "Ch 2 End:")
5) Any chord with a bass note has a space after the slash. (eg. "I/ III")
6) Any chords wrapped in parentheses are meant to have a smaller text size.

## Contents

```
.
└── src/
│   │   Document.py
│   │   GUI.py  
│   │   Main.py
│   │   MusicData.py
│   │   README.md  
│   │
│   └── songs/
│   
│   .gitignore
│   Doxyfile
│   Makefile
│   README.md
```

| Name | Description |
|---|---|
|src/|Source folder for code and inputs|
|.gitignore|File for Git to ignore output files|
|Doxyfile|Configuration file for Doxygen|
|Makefile|Contains commands for building|
|README.md|This file - Gives information about repo|
