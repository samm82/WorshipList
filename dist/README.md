# WorshipList
Last Modified: 12/31/2021

Last Compiled: 3/10/2022

## Description

This program automatically generates a chord chart for the songs being played on a given week at my church. More songs can be added to the src/songs/ folder following the format outlined below. Ensure that the program (WorshipList.exe) is in the same folder as the src/ folder before running.

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
