## @file   GUI.py
#  @brief  Implements GUI for selecting songs.
#  @author Samuel Crawford
#  @date   6/18/2026

import PySimpleGUI as sg

import json
import pythoncom
import sys
import threading

from datetime import date, timedelta
from pathlib import Path
from titlecase import titlecase

from Document import docSetup, pdfWrite, writeSong
from GUI_Helpers import *
from Helpers import checkFileName, checkValidChord, getSetting, getSettings, \
    getValidSongs, reduceWhitespace, validKeys


## @brief  Implements GUI for retrieving songs and keys.
#  @return A list of songs, a list of their keys, and the chord sheet file name.
def songGUI():
    numSongs = 4
    songs, keys = [""] * numSongs, [""] * numSongs
    filename = ""
    makeNewWindow = True

    while True:
        if makeNewWindow:
            songsFromFile = getValidSongs()
            songColumnList: list = [sg.Text("Song")]
            keyColumnList: list = [sg.Text("Key")]

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
                [buttonRow(["Change Number of Songs", "Add a New Song", "Settings"]),
                 [sg.HorizontalSeparator()],
                 [sg.Text("Enter a filename:")],
                 [sg.InputText(filename, key="-FILENAME-")],
                 buttonRow(["OK", "Use Next Sunday", "Quit"])
                 ]
            ]

            songWindow = sg.Window("WorshipList").Layout(songDialogue)

        button, values = songWindow.Read()
        makeNewWindow = True

        if button in {"Quit", None}:
            sys.exit()
        else:
            songs, keys = [], []

            for i in range(numSongs):
                songs.append(values[f"-SONG{i}-"].strip())
                songWindow[f"-SONG{i}-"].update(songs[i])  # pyright: ignore[reportOptionalMemberAccess]

                key = values[f"-KEY{i}-"].strip()
                if key:
                    key = key[0].upper() + key[1:].lower()
                keys.append(key)
                songWindow[f"-KEY{i}-"].update(key)  # pyright: ignore[reportOptionalMemberAccess]

            if button == "Change Number of Songs":
                nonEmptyRows = [i for i in range(len(songs)) if songs[i] or keys[i]]
                newNS = numSongsGUI(nonEmptyRows)
                if newNS:
                    numSongs = newNS
                else:
                    makeNewWindow = False

            elif button == "Add a New Song":
                makeNewWindow = addSongGUI()

            elif button == "Settings":
                makeNewWindow = settingsGUI()

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
                    filename = f"{getSetting("CHURCH_NAME")} {nextSunday.strftime('%F')}"
                    makeNewWindow = True
                    continue

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


## @brief  Adds a song file with the specified name and sections.
#  @return A Boolean representing whether or not a song file was added.
def addSongGUI():
    NUM_LINES = 5
    sections = ["", "Verse", "Chorus", "Bridge", "V/Ch", "Intro", "Outro"]

    lColumn: list[list] = [[sg.Text("Name:")]]
    rColumn: list[list] = [[sg.InputText(key="-SONGNAME-")]]
    for i in range(NUM_LINES):
        lColumn.append([sg.Combo(sections, "", key=f"-SECTIONNAME{i}-")])
        rColumn.append([sg.InputText(key=f"-CHORDS{i}-")])

    dialogue = [
        [sg.Text("Add a song:")],
        [sg.Column(lColumn), sg.Column(rColumn)],
        buttonRow(["OK", "Cancel"])
    ]

    window = sg.Window("WorshipList").Layout(dialogue)

    ignoreInvalidChord = False
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
                filePath = Path(getSetting("SONG_PATH")) / f"{songName}.txt"

            if filePath.is_file():
                popupError("Song file already exists.")
                continue

            contents = [songName]
            goBack = False
            for i in range(int((len(values) - 1) / 2)):
                section = reduceWhitespace(values[f"-SECTIONNAME{i}-"])
                chords = reduceWhitespace(values[f"-CHORDS{i}-"])

                if chords and not ignoreInvalidChord:
                    for c in chords.split(" "):
                        if not checkValidChord(c):
                            button = popupWarn(f"Section \"{section}\" includes invalid chord \"{c}\".")
                            if button == "Go Back":
                                goBack = True
                                break
                            elif button == "Ignore All":
                                ignoreInvalidChord = True
                                break

                if goBack:
                    break

                if section:
                    if not chords and not ignoreEmptySection:
                        popupError(f"Section \"{section}\" has no chords defined.")
                        goBack = True
                        break
                    elif contents[-1].endswith("same"):
                        contents[-1] += f" {section}: {chords}"
                    else:
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
                            if contents[-1].endswith("same"):
                                contents[-1] = contents[-1][:-5]
                            elif not contents[-1].endswith("new"):
                                contents[-1] += " new"
                            contents[-1] += f" {chords}"

            if goBack:
                continue

            if len(contents) == 1:
                button = popupWarn("No sections defined for new song. Ignore?", False)
                if button == "Go Back":
                    continue

            with open(filePath, "w") as fp:
                fp.write("\n".join(contents))

            window.close()
            return True

        else:
            window.close()
            return False


## @brief Allows the user to view and change settings.
def settingsGUI():
    ## @brief           Formats a given settings key for use in dialogues.
    #  @param[in] s     The settings key to format.
    #  @param[in] title A Boolean representing if the key should be in titlecase.
    #  @return          The key in natural language in lowercase if title is False.
    def processSettingKey(s: str, title: bool) -> str:
        s = s.replace("_", " ")
        return titlecase(s) if title else s.lower()

    lColumn: list[list] = []
    rColumn: list[list] = []
    for key, val in getSettings().items():
        lColumn.append([sg.Text(processSettingKey(key, True) + ":")])
        rColumn.append([sg.InputText(key=key, default_text=val),
                        sg.FolderBrowse() if "PATH" in key else sg.VPush()])

    dialogue = [
        [sg.Text("Settings")],
        [sg.Column(lColumn), sg.Column(rColumn)],
        buttonRow(["OK", "Cancel"])
    ]

    window = sg.Window("WorshipList").Layout(dialogue)

    while True:
        button, values = window.Read()
        # The folder browsers populate the text fields
        # Don't check the browser values since they're either unpopulated or redundant
        del values["Browse"]
        del values["Browse0"]

        validSettings = True
        if button == "OK":
            for key, val in values.items():
                lowerKey = processSettingKey(key, False)
                if not val:
                    popupError(f"Please enter a{"n" if lowerKey[0] in "aeiou" else ""} {lowerKey}.")
                    validSettings = False
                if val and ("PATH" in key and not Path(val).is_dir() or
                            "NAME" in key and not checkFileName(val)):
                    popupError(f"Please enter a valid {lowerKey}.")
                    validSettings = False

            if validSettings:
                with Path("Settings.json").open("w") as settings_json:
                    settings_json.write(json.dumps(values, indent=4))
                break
        else:
            break

    window.close()


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

            songPath = Path(getSetting("SONG_PATH"))
            with (songPath / f"{song}.txt").open() as fp:
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

    # nonEmptySongs = [song for song in songs if song]
    # if len(nonEmptySongs) != len(set(nonEmptySongs)):
    #     return popupError("Each song can only be selected once.")
    return True


## @brief  Displays the progress of output to the user.
def statusGUI(songs: list[str], keys: list[str], filename: str):
    lines = [f"Writing {song}..." for song in songs] + [
        "", "Saving chord sheet as .docx file...", "Converting chord sheet to PDF..."]

    lColumn: list[list[sg.Text]] = [[sg.Text(line)] for line in lines]
    rColumn: list[list[sg.Text]] = [[sg.Text(" ", key=f"song{i}")]
                                    for i in range(len(songs))] + [
                                        [sg.Text(" ")], [sg.Text(" ", key="docx")],
                                        [sg.Text(" ", key="pdf")]]

    dialogue = [
        [sg.Column(lColumn), sg.Column(rColumn)],
        buttonRow(["OK", "Cancel"])
    ]

    window = sg.Window("WorshipList", dialogue, finalize=True)
    window["OK"].update(disabled=True)  # pyright: ignore[reportOptionalMemberAccess]

    ## @brief          Updates the status icon for a given work item.
    #  @param[in] key  The key for the given item to update.
    #  @param[in] val  The new status for the given item (represented by a symbol).
    def updateStatus(key: str, val: str):
        window[key].update(val)  # pyright: ignore[reportArgumentType, reportOptionalMemberAccess]

    ## @brief  Defines the thread that outputs chord sheets.
    def outputChordSheetThread():
        pythoncom.CoInitialize()
        doc = docSetup()
        lineCount = 0

        # Gets output file directory from settings
        outPath = Path(getSetting("OUTPUT_PATH"))
        fileNameDOCX, fileNamePDF = f"{filename}.docx", f"{filename}.pdf"

        outPathDOCX = outPath / fileNameDOCX
        outPathPDF = outPath / fileNamePDF

        if not outPath.is_dir():
            popupError(f"Can't find file path {str(outPath)}.\n"
                       "Make sure your file path is correct in Settings.")

        # Writes each song
        updateStatus("song0", sg.SYMBOL_HOURGLASS)
        for i, (song, key) in enumerate(zip(songs, keys)):
            doc, lineCount = writeSong(doc, lineCount, song, key)
            updateStatus(f"song{i}", sg.SYMBOL_CHECK)
            updateStatus("docx" if i + 1 == len(songs) else f"song{i + 1}", sg.SYMBOL_HOURGLASS)

        # Saves document as .docx
        try:
            doc.save(str(outPathDOCX))
            updateStatus("docx", sg.SYMBOL_CHECK)
        except:
            # TODO: is this necessary?
            updateStatus("docx", sg.SYMBOL_X)

        # Saves document as .pdf
        updateStatus("pdf", sg.SYMBOL_HOURGLASS)
        if pdfWrite(outPathDOCX, outPathPDF):
            updateStatus("pdf", sg.SYMBOL_CHECK)
        else:
            updateStatus("pdf", sg.SYMBOL_X)

        window["OK"].update(disabled=False)  # pyright: ignore[reportOptionalMemberAccess]

    threading.Thread(target=outputChordSheetThread, daemon=True).start()

    while True:
        event, _ = window.Read()

        if event == sg.WIN_CLOSED or event in {"OK", "Cancel"}:
            break
        window.refresh()

    window.close()
