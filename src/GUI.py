## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   12/30/2021

import PySimpleGUI as sg

from datetime import date, timedelta
from pathlib import Path
from titlecase import titlecase

from Helpers import checkFileName, getValidSongs, validKeys


## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, a list of their keys, and the chord sheet file name.
def songGUI():
    numSongs = 4
    songs, keys = [""] * numSongs, [""] * numSongs
    makeNewWindow = True

    while True:
        if makeNewWindow:
            songsFromFile = getValidSongs()
            combo = []

            def songCombo(i, input=""):
                if input and input not in songsFromFile:
                    prepend = [input, ""]
                else:
                    prepend = [""]
                return sg.Combo(prepend + songsFromFile, input, 37, key=f"-SONG{i}-")

            def keyInput(i, input=""):
                return sg.InputText(input, (5, None), key=f"-KEY{i}-")

            # TODO? Maybe Combo isn't the best implementation
            for i in range(numSongs):
                if i < len(songs):
                    row = [songCombo(i, songs[i]), keyInput(i, keys[i])]
                else:
                    row = [songCombo(i), keyInput(i)]

                combo.append(row)

            # TODO: Implement using columns
            songDialogue = [[sg.Text("Song" + " " * 64 + "Key")]] + combo + \
                [[sg.Button("Change Number of Songs"), sg.Button("Add a New Song")],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Enter a filename:")],
                 [sg.InputText("", key="-FILENAME-")],
                 [sg.Button("OK"), sg.Button("Use Next Sunday"),
                  sg.Button("Quit")]
                 ]

            songWindow = sg.Window("WorshipList").Layout(songDialogue)

        button, values = songWindow.Read()
        makeNewWindow = True

        if button in {"Quit", None}:
            exit()
        else:
            songs, keys = [], []

            for i in range(numSongs):
                songs.append(values[f"-SONG{i}-"].strip())
                songWindow[f"-SONG{i}-"].update(songs[i])

                key = values[f"-KEY{i}-"].strip()
                if key:
                    key = key[0].upper() + key[1:].lower()
                keys.append(key)
                songWindow[f"-KEY{i}-"].update(key)

            if button == "Change Number of Songs":
                nonEmptyRows = [i for i in range(len(songs)) if songs[i] or keys[i]]
                newNS = numSongsGUI(nonEmptyRows)
                if newNS:
                    numSongs = newNS
                else:
                    makeNewWindow = False

            elif button == "Add a New Song":
                makeNewWindow = addSongGUI()

            else:
                if not checkSongGUI(songs, keys):
                    makeNewWindow = False
                    continue

                if button == "OK":
                    if checkFileName(values["-FILENAME-"]):
                        filename = values["-FILENAME-"]
                    else:
                        popupError("Invalid file name. Try again.")
                        continue
                elif button == "Use Next Sunday":
                    today = date.today()
                    nextSunday = today + timedelta(days=(6 - today.weekday()) % 7)
                    filename = f"LIFT Worship {nextSunday.strftime('%F')}"

                toDelete = [i for i, s in enumerate(songs) if not s]
                songWindow.close()

                def prune(xs):
                    return [x for i, x in enumerate(xs) if i not in toDelete]

                return prune(songs), prune(keys), filename

            if makeNewWindow:
                songWindow.close()


## @brief       Implements a GUI for entering the number of songs to generate.
#  @param[in] n The indices of GUI rows with a song and/or a key entered.
#  @return      Returns the user-entered number of songs.
def numSongsGUI(n):
    while True:
        button, numSongs = popupText("Enter the number of songs:")

        if button == "Cancel":
            return
        elif button == "OK":
            try:
                numSongs = int(numSongs)

                if numSongs > 0:
                    overwritten = sum(i >= numSongs for i in n)

                    if not overwritten:
                        return numSongs
                    elif overwritten == 1:
                        overwritten = "one entry"
                    else:
                        overwritten = f"{overwritten} entries"

                    delDialogue = [
                        [sg.Text(f"The number of songs entered will delete {overwritten}. Proceed anyways?")],
                        [sg.CloseButton("OK"), sg.CloseButton("Cancel")]
                    ]

                    delWindow = sg.Window("WorshipList").Layout(delDialogue)
                    button, _ = delWindow.Read()

                    if button == "Cancel":
                        return
                    elif button == "OK":
                        return numSongs

                else:
                    popupError("You must error a number greater than zero.")

            except ValueError:
                popupError("You must error a number greater than zero.")


## @brief   Adds a blank song file with the specified name.
def addSongGUI():
    songCreated = False
    while True:
        button, songName = popupText("Enter the name of the new song:")

        if button == "Cancel":
            return songCreated
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
                songCreated = True


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
