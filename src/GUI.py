## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   11/24/2021

import PySimpleGUI as sg

from datetime import date, timedelta
from os import listdir
from pathlib import Path
from titlecase import titlecase

from Helpers import checkFileName, validKeys

## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, and a list of their keys.
def songGUI():
    numSongs = 4
    while True:
        
        # Get list of songs from songs directory
        # [:-4] removes ".txt" from filenames
        songsFromFile = [song[:-4] for song in listdir(Path("src/songs"))]
        songsFromFile.sort()
        songList = ["Select a song..."] + songsFromFile

        # TODO? Maybe InputCombo isn't the best implementation
        songDialogue = [[sg.Text("Song                                           Key")]] + \
            [[sg.InputCombo(songList), sg.InputText("", size=(5, None))] for _ in range(numSongs)] + \
            [[sg.CloseButton("OK"), sg.CloseButton("Number of Songs"), sg.CloseButton("Add a Song"), sg.CloseButton("Cancel")]]

        songWindow = sg.Window("WorshipList").Layout(songDialogue)
        button, values = songWindow.Read()

        if button == "Cancel":
            exit()
        elif button == "Number of Songs":
            numSongs = numSongsGUI()
        elif button == "Add a Song":
            addSongGUI()
        else:
            songs, keys = [], []
            for i in range(len(values)):
                if i % 2 == 0:
                    songs.append(values[i].strip())
                else:
                    key = values[i].strip()
                    if len(key):
                        key = key[0].upper() + key[1:].lower()
                    keys.append(key)

            # TODO: Better way to implement this?
            verifiedOutput = checkSongGUI(songs, keys)
            if verifiedOutput:
                break

    return verifiedOutput[0], verifiedOutput[1]

def numSongsGUI():
    while True:

        button, numSongs = popupText("Enter the number of songs:")

        if button == "Cancel":
            return
        else:
            try:
                if int(numSongs) > 0:
                    return int(numSongs)
                else:
                    popupError("You must error a number greater than zero.")
            except ValueError:
                popupError("You must error a number greater than zero.")

## @brief   Adds a blank song file with the specified name.
def addSongGUI():
    while True:

        button, songName = popupText("Enter the name of the new song:")

        if button == "Cancel":
            return
        else:
            songName = titlecase(songName)
            if not checkFileName(songName):
                popupError("Invalid file name for a song.")
                continue
            else:
                filePath = Path("src/songs/" + songName + ".txt")

            if filePath.is_file():
                popupError("Song file already exists.")
            else:
                # Create new file with title
                with open(filePath, "w") as fp:
                    fp.write(songName)

## @brief            Checks output of GUI to ensure correct outputs and removes empty song fields.
#  @param[in] songs  The song inputs.
#  @param[in] keys   The key inputs.
#  @return           The updated output if valid, otherwise False.
def checkSongGUI(songs, keys):

    def rmEmptySongsKeys(xs):
        return [xs[i] for i in range(len(xs)) if songs[i] and keys[i]]

    songs, keys = rmEmptySongsKeys(songs), rmEmptySongsKeys(keys)

    if not len(songs):
        popupError("You must select at least one song.")
        return False

    for key in keys:
        if key not in validKeys():
            popupError("You must select a valid key for each song.")
            return False

    if len(songs) != len(set(songs)):
        popupError("Each song can only be selected once.")
        return False

    return songs, keys

## @brief  Implements GUI for retrieving the file name.
#  @return The file name.
def fileNameGUI():
    while True:

        fileDialogue = [
            [sg.Text("Enter a filename:")],
            [sg.InputText("")],
            [sg.CloseButton("OK"), sg.CloseButton("Use Next Sunday"), sg.CloseButton("Cancel")]
        ]

        fileWindow = sg.Window("WorshipList").Layout(fileDialogue)
        button, values = fileWindow.Read()

        if button == "Cancel":
            exit()
        elif button == "Use Next Sunday":
            # Gets the next Sunday and formats it appropriately
            nextSunday = (date.today() + timedelta(days=(6-date.today().weekday())%7))
            filename =  "LIFT Worship " + nextSunday.strftime("%F")
        elif checkFileName(values[0]):
            filename = values[0]
        else:
            popupError("Invalid file name. Try again.")

        return filename + ".docx", filename + ".pdf"

## @brief            Defines a text input popup.
#  @param[in] string The prompt string to be printed in dialogue box.
#  @return           The name of the button pressed and the text entered.
def popupText(string):
    dialogue = [
        [sg.Text(string)],
        [sg.InputText("")],
        [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
    ]

    window = sg.Window("WorshipList").Layout(dialogue)
    button, values = window.Read()
    return button, values[0]

## @brief            Defines an error popup that signifies incorrect input.
#  @param[in] string The error string to be printed in dialogue box.
def popupError(string):
    sg.Popup(string, title="Error")
