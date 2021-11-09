## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   11/9/2021

import PySimpleGUI as sg

from datetime import date, timedelta
from os.path import isfile

from Helpers import checkFileName, fileNameProcess, songNameProcess, validKeys

## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, and a list of their keys.
def songGUI():
    numSongs = 4
    while True:
        # Read list of songs from file
        file = open("src\\SongList.txt", "r")
        songsFromFile = file.readlines()
        file.close()
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
                    songs.append(values[i])
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

        numDialogue = [
            [sg.Text("Enter the number of songs:")],
            [sg.InputText("")],
            [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
        ]

        songWindow = sg.Window("WorshipList").Layout(numDialogue)
        button, values = songWindow.Read()
        numSong = values[0]

        if button == "Cancel":
            return
        else:
            try:
                if int(numSong) > 0:
                    return int(numSong)
                else:
                    popupError("You must error a number greater than zero.")
            except ValueError:
                popupError("You must error a number greater than zero.")


## @brief   Adds a blank song file with the specified name.
def addSongGUI():
    while True:

        songDialogue = [
            [sg.Text("Enter the name of the new song:")],
            [sg.InputText("")],
            [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
        ]

        songWindow = sg.Window("WorshipList").Layout(songDialogue)
        button, values = songWindow.Read()
        songName = values[0]

        if button == "Cancel":
            return
        else:
            fileName = fileNameProcess(songName)
            if not checkFileName(fileName):
                popupError("Invalid file name for a song.")
                continue
            else:
                filePath = "src\\songs\\" + fileNameProcess(songName) + ".txt"

            if isfile(filePath):
                popupError("Song file already exists.")
            else:
                songName = songNameProcess(songName)

                # Create new file with title
                with open(filePath, "w") as fp:
                    fp.write(songName)

                # Add new songs to song list
                with open("src\\SongList.txt", "r+") as fp:
                    songs = fp.readlines()
                    songs.append(songName + "\n")
                    songs.sort()
                    fp.seek(0)
                    fp.writelines(songs)
                break

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
        fileName = values[0]

        if button == "Cancel":
            exit()
        elif button == "Use Next Sunday":
            # Gets the next Sunday and formats it appropriately
            nextSunday = (date.today() + timedelta(days=(6-date.today().weekday())%7))
            return "LIFT Worship " + nextSunday.strftime("%F")
        elif checkFileName(fileName):
            return fileName
        else:
            popupError("Invalid file name. Try again.")

## @brief            Defines an error popup that signifies incorrect input.
#  @param[in] string The error string to be printed in dialogue box.
def popupError(string):
    sg.Popup(string, title="Error")