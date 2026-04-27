# WorshipList

Last Modified: 4/27/2026

## Description

This program automatically generates a chord chart for the songs being played
on a given week at my church. This is done through a GUI by running either
`make` or the executable in the `dist/` directory. More songs can be added to
the src/songs/ folder following the format outlined below.

To generate documentation, run `make doc` in the directory with the Makefile.
This will create two folders; the important files are html/index and
latex/refman.pdf for documentation.

## Song Files

Each song is stored as a text file with chords represented as Roman numerals,
where "I" corresponds to the first chord of the scale, "II" to the second, etc.
Lower case numerals denote minor chords, and "sus" following major chords
denotes suspended chords. Chords can also be preceded by "b" or "#" to indicate
that they are flat or sharp chords (i.e., not in the key provided),
respectively. The program then automatically translates these numerals to
standard chords in the specified key.

### Keywords

The song files also contain some custom symbols that are shorthand for some important functions, as follows:

| Keyword | Output |
|---|---|
|\||"\|"|
|x#|"x#" eg. "x2"|
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
4) Any chords wrapped in parentheses are meant to have a smaller text size.

## Contents

```
.
└── .github/
│   └── workflows/
│       │   main.yml
│
└── dist
│   └── src/
│   │   └── songs/
│   │
│   │   README.md
│   │   Settings.json
│   │   WorshipList.exe
│
└── src/
│   └── songs/
│   │   CommonSections.py
│   │   COMPILED_README.md
│   │   Document.py
│   │   GUI.py
│   │   Helpers.py
│   │   Main.py
│   │   README.md
│
│   .gitignore
│   Doxyfile
│   LICENSE
│   Makefile
│   README.md
|   requirements.txt
|   Settings.json
```

| Name | Description |
|---|---|
|.github/|Contains jobs for use with GitHub Actions|
|dist/|Contains the compiled version of the program with all necessary files|
|src/|Source folder for code and inputs|
|.gitignore|File for Git to ignore output files|
|Doxyfile|Configuration file for Doxygen|
|LICENSE|Contains terms for use and modification|
|Makefile|Contains commands for building|
|README.md|This file - Gives information about repo|
|requirements.txt|The required packages for using WorshipList|
|Settings.json|Contains the settings for the program (only output file path right now)|
