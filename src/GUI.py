## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   1/10/2022

import PySimpleGUI as sg

from datetime import date, timedelta
from pathlib import Path
from titlecase import titlecase

from Helpers import checkFileName, getValidSongs, reduceWhitespace, validKeys


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


## @brief   Adds a song file with the specified name and sections.
def addSongGUI():
    NUM_LINES = 5
    sections = ["", "Verse", "Verse 1", "Verse 2", "Chorus", "Chorus 1",
                "Chorus 2", "Bridge", "Bridge 1", "Bridge 2"]

    lColumn = [[sg.Text("Name:")]]
    rColumn = [[sg.InputText(key="-SONGNAME-")]]
    for i in range(NUM_LINES):
        lColumn.append([sg.Combo(sections, "", key=f"-SECTIONNAME{i}-")])
        rColumn.append([sg.InputText(key=f"-CHORDS{i}-")])

    dialogue = [
        [sg.Text("Add a song:")],
        [sg.Column(lColumn), sg.Column(rColumn)],
        buttonRow(["OK", "Cancel"], False)
    ]

    window = sg.Window("WorshipList").Layout(dialogue)

    ignoreEmptySection = False

    while True:
        button, values = window.Read()

        if button == "OK":
            songName = titlecase(reduceWhitespace(values["-SONGNAME-"]))
            if not songName:
                popupError("Please enter a song name.")
                continue
            elif not checkFileName(songName):
                popupError("Invalid file name for a song.")
                continue
            else:
                filePath = Path(f"src/songs/{songName}.txt")

            if filePath.is_file():
                popupError("Song file already exists.")
                continue

            contents = [songName]
            goBack = False
            for i in range(int((len(values) - 1) / 2)):
                section = reduceWhitespace(values[f"-SECTIONNAME{i}-"])
                chords = reduceWhitespace(values[f"-CHORDS{i}-"])
                if section:
                    if not chords and not ignoreEmptySection:
                        popupError(f"Section \"{section}\" has no chords defined.")
                        goBack = True
                        break
                    contents.append(f"{section}: {chords}")

                else:
                    if chords:
                        if len(contents) == 1:
                            button = popupWarn(f"Line {i + 1} has no section name and will be ignored.")
                            if button == "Go Back":
                                goBack = True
                                break
                            elif button == "Ignore All":
                                ignoreEmptySection = True
                        else:
                            contents[-1] += f" new {chords}"

            if len(contents) == 1:
                button = popupWarn("No sections defined for new song. Ignore?", False)
                if button == "Go Back":
                    goBack = True

            if goBack:
                continue

            with open(filePath, "w") as fp:
                fp.write("\n".join(contents))

            window.close()
            return True

        else:
            window.close()
            return False


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
                    button = popupWarn(f"File for \"{song}\" has too few lines.")
                    if button == "Go Back":
                        return
                    elif button == "Ignore All":
                        ignoreEmptyFile = True
        else:
            if key and not ignoreDanglingKey:
                button = popupWarn(f"No song name entered for key \"{key}\".")
                if button == "Go Back":
                    return
                elif button == "Ignore All":
                    ignoreDanglingKey = True

    nonEmptySongs = [song for song in songs if song]
    if len(nonEmptySongs) != len(set(nonEmptySongs)):
        return popupError("Each song can only be selected once.")
    return True


## @brief         Defines a warning popup that provides the option to ignore.
#  @param[in] s   The warning string to be printed in dialogue box.
#  @param[in] all A Boolean representing if an "Ignore All" button should be created.
#  @return        The name of the button pressed.
def popupWarn(s, all=True):
    buttons = ["Go Back", "Ignore"]
    if all:
        buttons.append("Ignore All")

    dialogue = [[sg.Text(s)], buttonRow(buttons, True)]

    window = sg.Window("WorshipList").Layout(dialogue)
    return window.Read()[0]


## @brief       Defines a text input popup.
#  @param[in] s The prompt string to be printed in dialogue box.
#  @return      The name of the button pressed and the text entered.
def popupText(s):
    dialogue = [
        [sg.Text(s)],
        [sg.InputText("")],
        buttonRow(["OK", "Cancel"], True)
    ]

    window = sg.Window("WorshipList").Layout(dialogue)
    button, values = window.Read()
    return button, values[0]


## @brief       Defines an error popup that signifies incorrect input.
#  @param[in] s The error string to be printed in dialogue box.
def popupError(s):
    sg.Popup(s, title="Error")


## @brief           Creates a row of buttons.
#  @param[in] names A list of names for buttons and a Boolean for if they should close on press.
#  @param[in] close A Boolean representing if the window should be closed on a button press.
#  @return          A list of buttons.
def buttonRow(names, close):
    if close:
        return list(map(lambda n: sg.CloseButton(n), names))
    return list(map(lambda n: sg.Button(n), names))
