## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   11/11/2019

import PySimpleGUI as sg

from Helpers import fileNameProcess, songNameProcess, validKeys

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

## @brief   Adds a blank song file.
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
            songGUI()
        else:
            # Try to write blank song file
            filePath = "src\\songs\\" + fileNameProcess(songName) + ".txt"
            try:
                file = open(filePath, "r")
                file.close()
                popupError("Song file already exists.")
            except:
                songName = songNameProcess(songName)
                file = open(filePath, "w")
                file.write(songName)
                file.close()

                # Add to song list
                file = open("src\\SongList.txt", "r+")
                songs = file.readlines()
                songs.append(songName + "\n")
                songs.sort()
                file.seek(0)
                file.writelines(songs)
                file.close()
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
#  @return           A (verified) list of songs and their keys.
def popupError(string):
    errorDialgue = [
        [sg.Text(string)], 
        [sg.CloseButton("OK")]
    ]

    songWindow = sg.Window("Error").Layout(errorDialgue)
    button, values = songWindow.Read()

## @brief  Implements GUI for retrieving the date.
#  @return The date.
def fileNameGUI():
    invalid = True
    while invalid:

        fileDialogue = [
            [sg.Text("Enter the date in MM-DD-YY format (eg. 2-13-19):")],
            [sg.InputText("")],
            [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
        ]

        fileWindow = sg.Window("WorshipList").Layout(fileDialogue)
        button, values = fileWindow.Read()
        date = values[0]

        if button != "OK":
            exit()
        else:
            invalid = checkFileNameGUI(date)

    return date

## @brief           Checks output of GUI to ensure correct outputs.
#  @param[in] date  The date.
#  @return          True if the date is invalid, otherwise false.
def checkFileNameGUI(date):
    for char in date:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']:
            popupError("Characters can only be numerals or hyphens (-).")
            return True

    if len(date) < 6:
        popupError("The date must be at least six characters long.")
        return True   
    elif len(date) > 8:
        popupError("The date must be at most eight characters long.")
        return True  

    return False