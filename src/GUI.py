## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   12/27/2021

import PySimpleGUI as sg

from datetime import date, timedelta
from pathlib import Path
from titlecase import titlecase

from Helpers import checkFileName, getValidSongs, validKeys


## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, and a list of their keys.
def songGUI():
    numSongs = 4
    songs, keys = ["" for _ in range(numSongs)], ["" for _ in range(numSongs)]

    while True:
        songsFromFile = getValidSongs()
        combo = []

        def songCombo(input=""):
            if input and input not in songsFromFile:
                return sg.Combo([input, ""] + songsFromFile, input)
            return sg.Combo([""] + songsFromFile, input)

        def keyInput(input=""):
            return sg.InputText(input, (5, None))

        # TODO? Maybe Combo isn't the best implementation
        for i in range(numSongs):
            if i < len(songs):
                row = [songCombo(songs[i]), keyInput(keys[i])]
            else:
                row = [songCombo(), keyInput()]

            combo.append(row)

        songDialogue = [[sg.Text("Song" + " " * 43 + "Key")]] + combo + \
            [[sg.CloseButton("OK"), sg.CloseButton("Number of Songs"),
              sg.CloseButton("Add a Song"), sg.CloseButton("Quit")]]

        songWindow = sg.Window("WorshipList").Layout(songDialogue)
        button, values = songWindow.Read()

        if button == "Quit":
            exit()
        else:
            songs, keys = [], []
            for i in range(len(values)):
                if i % 2 == 0:
                    songs.append(values[i].strip())
                else:
                    key = values[i].strip()
                    if key:
                        key = key[0].upper() + key[1:].lower()
                    keys.append(key)

            if button == "Number of Songs":
                def lastEntry(x):
                    return next((i for i, j in enumerate(x) if j), 0)

                newNS = numSongsGUI(max(lastEntry(songs), lastEntry(keys)))
                if newNS:
                    numSongs = newNS

            elif button == "Add a Song":
                addSongGUI()
            elif button == "OK":
                if checkSongGUI(songs, keys):
                    toDelete = [i for i, s in enumerate(songs) if not s]
                    prune = lambda xs: [x for i, x in enumerate(xs) if i not in toDelete]  # noqa: E731
                    return prune(songs), prune(keys)


## @brief  Implements a GUI for entering the number of songs to generate.
#  @return Returns the entered number of songs.
def numSongsGUI(lastEntry):
    while True:
        button, numSongs = popupText("Enter the number of songs:")

        if button == "Cancel":
            return
        else:
            try:
                numSongs = int(numSongs)
            except ValueError:
                popupError("You must error a number greater than zero.")

            if int(numSongs) > 0:
                if numSongs <= lastEntry:
                    delDialogue = [
                        [sg.Text("The number of songs entered will delete at least one entry. Proceed anyways?")],
                        [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
                    ]

                    delWindow = sg.Window("WorshipList").Layout(delDialogue)
                    button, values = delWindow.Read()

                    if button == "Cancel":
                        return
                return numSongs

            else:
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
                filePath = Path(f"src/songs/{songName}.txt")

            if filePath.is_file():
                popupError("Song file already exists.")
            else:
                # Create new file with title
                with open(filePath, "w") as fp:
                    fp.write(songName)


## @brief            Ensures output of song GUI is valid.
#  @param[in] songs  The song inputs.
#  @param[in] keys   The key inputs.
#  @return           True if the output is valid and None otherwise.
def checkSongGUI(songs, keys):
    ignoreAll = False

    if not any(songs):
        return popupError("You must select at least one song.")

    validSongs = getValidSongs()
    for song, key in zip(songs, keys):
        if song:
            if song not in validSongs:
                return popupError(f"\"{song}\" not found in the songs directory.")
            elif not key:
                return popupError(f"No key specified for \"{song}\".")
            elif key not in validKeys:
                return popupError(f"\"{key}\" is not a valid key.")
        else:
            if key and not ignoreAll:
                noSongName = [
                    [sg.Text(f"No song name entered for key \"{key}\".")],
                    [sg.CloseButton("Go Back"), sg.CloseButton("Ignore"),
                     sg.CloseButton("Ignore All")]
                ]

                window = sg.Window("WorshipList").Layout(noSongName)
                button, _ = window.Read()
                if button == "Go Back":
                    return
                elif button == "Ignore All":
                    ignoreAll = True

    nonEmptySongs = [song for song in songs if song]
    if len(nonEmptySongs) != len(set(nonEmptySongs)):
        return popupError("Each song can only be selected once.")

    return True


## @brief  Implements GUI for retrieving the file name.
#  @return The file name.
def fileNameGUI():
    while True:

        deleteDialogue = [
            [sg.Text("Enter a filename:")],
            [sg.InputText("")],
            [sg.CloseButton("OK"), sg.CloseButton("Use Next Sunday"),
             sg.CloseButton("Cancel")]
        ]

        deleteWindow = sg.Window("WorshipList").Layout(deleteDialogue)
        button, values = deleteWindow.Read()

        if button == "Cancel":
            exit()
        elif button == "Use Next Sunday":
            # Gets the next Sunday and formats it appropriately
            today = date.today()
            nextSunday = today + timedelta(days=(6 - today.weekday()) % 7)
            filename = f"LIFT Worship {nextSunday.strftime('%F')}"
        elif checkFileName(values[0]):
            filename = values[0]
        else:
            popupError("Invalid file name. Try again.")

        return f"{filename}.docx", f"{filename}.pdf"


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
