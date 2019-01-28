## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   1/27/2019

import PySimpleGUI as sg

from MusicData import validKeys

## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, and a list of their keys.
def songGUI():
    songList = [
        "Select a song...", # Default entry
        "Anointing",
        "Death Was Arrested",
        "Glorious Day",
        "Great Are You Lord",
        "Heaven Come",
        "Let There Be Light",
        "Lion and the Lamb",
        "O Praise the Name",
        "Resurrecting",
        "Spirit of the Living God",
        "The Passion",
        "Who You Say I Am"
    ]

    invalid = True
    while invalid:

        songDialogue = [
            # Maybe InputCombo isn't the best implementation
            [sg.Text("Song                                           Key")],
            [sg.InputCombo(songList), sg.InputText("  ", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("  ", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("  ", size=(5, None))],
            [sg.InputCombo(songList), sg.InputText("  ", size=(5, None))],
            [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
        ]

        songWindow = sg.Window("WorshipList").Layout(songDialogue)
        button, values = songWindow.Read()

        songs, keys = [], []
        for i in range(len(values)):
            if i % 2 == 0:
                songs.append(values[i])
            else:
                key = values[i]
                key = key.strip()
                if len(key) == 1:
                    key = key.upper()
                else:
                    key = key[0].upper() + key[1].lower()
                keys.append(key)

        invalid = checkGUI(button, songs, keys)

    return songs, keys

## @brief            Checks output of GUI to ensure correct outputs.
#  @param[in] button The button input.
#  @param[in] songs  The song inputs.
#  @param[in] keys   The key inputs.
#  @return           A (verified) list of songs and their keys.
def checkGUI(button, songs, keys):
    if button == "Cancel":
        exit()

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

## @brief            Defines an error popup that signifies incorrec input.
#  @param[in] string The error string to be printed in dialogue box.
#  @return           A (verified) list of songs and their keys.
def popupError(string):
    errorDialgue = [
        [sg.Text(string)], 
        [sg.CloseButton("OK")]
    ]

    songWindow = sg.Window("Error").Layout(errorDialgue)
    button, values = songWindow.Read()
