## @file   Helpers.py
#  @brief  Contains helper functions for the modules.
#  @author Samuel Crawford
#  @date   12/27/2021

from os import listdir
from pathlib import Path
from pathvalidate import is_valid_filename

sharpNotes = ['F','F#','G','G#','A','A#','B','C','C#','D','D#','E'] * 2  # noqa: E231
flatNotes = ['F','Gb','G','Ab','A','Bb','B','C','Db','D','Eb','E'] * 2  # noqa: E231
validKeys = set(sharpNotes + flatNotes)


## @brief   Exception for if a file is incorrectly formatted (invalid chord).
class FileError(Exception):
    pass


## @brief   Exception for an invalid parameter (key).
#  @details GUI automatically checks this - only used when not using GUI.
class ParamError(Exception):
    pass


## @brief           Checks a file name to ensure it is valid.
#  @param[in] name  The file name.
#  @return          True if the name is valid, otherwise False.
def checkFileName(name):
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    return is_valid_filename(name) and name not in reserved


## @brief   Gets a list of valid songs from the song directory.
#  @return  A list of all valid songs.
def getValidSongs():
    # [:-4] removes ".txt" from filenames
    return sorted([s[:-4] for s in listdir(Path("src/songs"))])


## @brief         Gets a list of notes in the given key.
#  @param[in] key The key of the song.
#  @return        A list of notes in the given key.
#  @throw         ParamError if the key isn't valid.
def getNotes(key):
    # Checks if key is valid

    if key not in validKeys:
        raise ParamError("The key \"" + key + "\" isn't recognized.")

    if len(key) > 1:
        if key[1] == "#":
            notes = sharpNotes
        elif key[1] == "b":
            notes = flatNotes
    elif key in ["C", "F"]:
        notes = flatNotes
    else:
        notes = sharpNotes

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
        raise FileError(f"The chord \"{num}\" in {fileName} isn't recognized.")
    else:
        chord = noteList[numList.index(lowerNum)]

    # Handles if chord is minor
    if num.islower():
        chord += "m"

    return chord
