## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   1/21/2020

import PySimpleGUI as sg

from datetime import date, timedelta
from os.path import isfile

from Helpers import checkFileName, fileNameProcess, songNameProcess, validKeys

## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, and a list of their keys.
def songGUI():
    invalid = True
    while invalid:
        # Read list of songs from file
        file = open("src\\SongList.txt", "r")
        songsFromFile = file.readlines()
        file.close()
        songList = ["Select a song..."] + songsFromFile

        songDialogue = [
            # Maybe InputCombo isn't the best implementation
            [sg.Text("Song                                           Key")],
            [sg.InputCombo(songList), sg.InputText("", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("", size=(5, None))],
            [sg.CloseButton("OK"), sg.CloseButton("Add a Song"), sg.CloseButton("Cancel")]
        ]

        songWindow = sg.Window("WorshipList").Layout(songDialogue)
        button, values = songWindow.Read()

        if button == "Cancel":
            exit()
        elif button == "Add a Song":
            addSongGUI()
        else:
            songs, keys = [], []
            for i in range(len(values)):
                if i % 2 == 0:
                    songs.append(values[i])
                else:
                    key = values[i]
                    key = key.strip()
                    if len(key) == 1:
                        key = key.upper()
                    elif len(key) == 2:
                        key = key[0].upper() + key[1].lower()
                    keys.append(key)

            invalid = checkSongGUI(songs, keys)

    return songs, keys

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

## @brief            Checks output of GUI to ensure correct outputs.
#  @param[in] songs  The song inputs.
#  @param[in] keys   The key inputs.
#  @return           True if the outputs are invalid, otherwise false.
def checkSongGUI(songs, keys):
    for song in songs:
        if song == "Select a song...":
            popupError("You must select a song for all four options.")
            return True

    for key in keys:
        if key not in validKeys():
            popupError("You must select a valid key for all four options.")
            return True

    if len(songs) != len(set(songs)):
        popupError("Each song can only be selected once.")
        return True

    return False

## @brief            Defines an error popup that signifies incorrect input.
#  @param[in] string The error string to be printed in dialogue box.
def popupError(string):
    errorDialgue = [
        [sg.Text(string)], 
        [sg.CloseButton("OK")]
    ]

    errorWindow = sg.Window("Error").Layout(errorDialgue)
    errorWindow.Read()

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
