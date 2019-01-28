## @file   MusicData.py
#  @brief  Contains helper functions for getting list of notes in key and chords.
#  @author Samuel Crawford
#  @date   1/26/2019

class FileError(Exception):
    pass

class ParamError(Exception):
    pass

## @brief  Gets a list of valid keys.
#  @return A list of valid keys.
def validKeys():
    return ['F','F#','Gb','G','G#','Ab','A','A#','Bb','B','C','C#','Db','D','D#','Eb','E']

## @brief         Gets a list of notes in the given key.
#  @param[in] key The key of the song.
#  @return        A list of notes in the given key.
#  @throw         ParamError if the key isn't valid.
def getNotes(key):
    # Defines standard lists

    notesSharp = ['F','F#','G','G#','A','A#','B','C','C#','D','D#','E','F','F#','G','G#','A','A#','B','C','C#','D','D#','E']
    notesFlat  = ['F','Gb','G','Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B','C','Db','D','Eb','E']

    # Checks if key is valid

    if key not in validKeys():
        raise ParamError("The key \"" + key + "\" isn't recognized.")

    if len(key) > 1:
        if key[1] == "#":
            notes = notesSharp
        elif key[1] == "b":
            notes = notesFlat
    elif key in ["C", "F"]:
        notes = notesFlat
    else:
        notes = notesSharp

    # Gets notes of the major scale started at the given key

    noteList = []
    note = notes.index(key)
    for i in list(range(7)):
        noteList.append(notes[note])
        if i == 2:
            note += 1
        else:
            note += 2

    return noteList

## @brief              Gets chord from Roman numeral based on list of notes.
#  @param[in] noteList A list of notes in the key of the song.
#  @param[in] num      The Roman numeral from the song file.
#  @param[in] fileName The name of file with student information.
#  @return             The chord converted from the Roman numeral.
#  @throw              FileError if the chord isn't valid.
def getChord(noteList, num, fileName):
    lowerNum = num.lower()
    numList = ["i", "ii", "iii", "iv", "v", "vi", "vii"]

    # Checks if chord is valid, and retrieves it from list if it is
    if lowerNum not in numList:
        raise FileError("The chord \"" + num + "\" in the " + fileName + " file isn't recognized.")
    else:
        chord = noteList[numList.index(lowerNum)]

    # Handles if chord is minor
    if num.islower():
        chord += "m"

    return chord
