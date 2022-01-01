## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   1/1/2022

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
            songColumnList = [sg.Text("Song")]
            keyColumnList = [sg.Text("Key")]

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
                    songColumnList.append(songCombo(i, songs[i]))
                    keyColumnList.append(keyInput(i, keys[i]))
                else:
                    songColumnList.append(songCombo(i))
                    keyColumnList.append(keyInput(i))

            songDialogue = [
                [sg.Column([[s] for s in songColumnList]),
                 sg.Column([[k] for k in keyColumnList])],
                [buttonRow(["Change Number of Songs", "Add a New Song"], False),
                 [sg.HorizontalSeparator()],
                 [sg.Text("Enter a filename:")],
                 [sg.InputText("", key="-FILENAME-")],
                 buttonRow(["OK", "Use Next Sunday", "Quit"], False)
                 ]
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

                songWindow.close()
                toDelete = [i for i, s in enumerate(songs) if not s]

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
                        buttonRow(["OK", "Cancel"], True)
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
        if songCreated:
            button, songName = popupText("Enter the name of the next song to add:")
        else:
            button, songName = popupText("Enter the name of the new song:")

        if button == "OK":
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
        else:
            return songCreated


## @brief            Ensures output of song GUI is valid.
#  @param[in] songs  The song inputs.
#  @param[in] keys   The key inputs.
#  @return           True if the output is valid and None otherwise.
def checkSongGUI(songs, keys):
    if not any(songs):
        return popupError("You must select at least one song.")

    ignoreEmptyFile = False
    ignoreDanglingKey = False

    validSongs = getValidSongs()
    for song, key in zip(songs, keys):
        if song:
            if song not in validSongs:
                return popupError(f"\"{song}\" not found in the songs directory.")
            elif not key:
                return popupError(f"No key specified for \"{song}\".")
            elif key not in validKeys:
                return popupError(f"\"{key}\" is not a valid key.")

            with Path(f"src/songs/{song}.txt").open() as fp:
                if len(fp.readlines()) == 1 and not ignoreEmptyFile:
                    emptyFile = [
                        [sg.Text(f"File for \"{song}\" has too few lines.")],
                        buttonRow(["Go Back", "Ignore", "Ignore All"], True)
                    ]

                    window = sg.Window("WorshipList").Layout(emptyFile)
                    button, _ = window.Read()
                    if button == "Go Back":
                        return
                    elif button == "Ignore All":
                        ignoreEmptyFile = True
        else:
            if key and not ignoreDanglingKey:
                noSongName = [
                    [sg.Text(f"No song name entered for key \"{key}\".")],
                    buttonRow(["Go Back", "Ignore", "Ignore All"], True)
                ]

                window = sg.Window("WorshipList").Layout(noSongName)
                button, _ = window.Read()
                if button == "Go Back":
                    return
                elif button == "Ignore All":
                    ignoreDanglingKey = True

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
        buttonRow(["OK", "Cancel"], True)
    ]

    window = sg.Window("WorshipList").Layout(dialogue)
    button, values = window.Read()
    return button, values[0]


## @brief            Defines an error popup that signifies incorrect input.
#  @param[in] string The error string to be printed in dialogue box.
def popupError(string):
    sg.Popup(string, title="Error")


## @brief     Creates a row of buttons.
#  @param[in] A list of names for buttons and a Boolean for if they should close on press.
#  @return    A list of buttons.
def buttonRow(names, close):
    if close:
        return list(map(lambda n: sg.CloseButton(n), names))
    return list(map(lambda n: sg.Button(n), names))
