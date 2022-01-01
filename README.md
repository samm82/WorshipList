# WorshipList
Last Modified: 12/31/2021

## Description

Whenever I'm on worship at LIFT Church, I have to create a chord chart for the songs we're playing that week, so I made a program to automate that process. This program 
automatically generates that chord chart. This is done through a GUI, by running `make`.

To generate documentation, run `make doc` in the directory with the Makefile. This will create two folders; the important files are html/index 
and latex/refman.pdf for documentation.

## Song Files

Each song is stored as a text file with chords represented as Roman numerals, where "I" corresponds to the first chord of the scale, "II" to the 
second, etc. Lower case numerals denote minor chords. The program then automatically translates these numerals to standard chords, depending on 
the key specified. 

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
│   │   │   Settings.txt
│   │
│   │   README.md
│   │   WorshipList.exe
│
└── src/
│   └── songs/
│   │   COMPILED_README.md
│   │   Document.py
│   │   GUI.py
│   │   Helpers.py
│   │   Main.py
│   │   README.md
│   │   Settings.txt
│
│   .gitignore
│   Doxyfile
│   LICENSE
│   Makefile
│   README.md
|   requirements.txt
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
