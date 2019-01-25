# WorshipList
Last Modified: 1/25/2019

## Description

Every week for worship at LIFT Church, I have to manually create a chord chart for the four songs we're playing that week. This program automatically generates that chord chart. This is currently done semi-manually from the `main()` function (mainly for ease of testing), but will eventually be updated to ask for user input.

## Song Files

Each song is stored as a text file with chords represented as Roman numerals, where "I" corresponds to the first chord of the scale, "II" to the second, etc. Lower case numerals denote minor chords. The program than automatically translates these numerals to standard chords, depending on the key specified. 

### Keywords

The song files also contain some custom symbols, some of which correspond to exactly what they are, such as "|", "(", and ")". Others are shorthand for some key functions, as follows:

| Keyword | Output |
|---|---|
|double|x 2|
|triple|x 3|
|new|Splits a line into two lines, preserving tab stops|
|/|Denotes a chord over a bass note (with proper spacing)|

### Assumptions

Some assumptions for how the song files are formatted:
1) The first line in the file is the title of the song, properly formatted. (eg. "Lion and the Lamb")
2) Each section (chorus, verse, bridge, etc.) is on a new line, with the first entry being the entry name and a colon. (eg. "V/Ch:")
3) The longest section name (currently) is the length of "Bridge 2:" when implemented in Word.
4) Any chord with a bass note has a space after the slash. (eg. "D/ F#")

## Contents

**songs**
: Directory of songs, with chords stored as Roman numerals.

WorshipList.py
: The actual program that outputs the chord chart as `output.docx`.

README.md
: This file.