## @file   Main.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   4/27/2026

import json
from pathlib import Path

from Document import docSetup, pdfWrite, writeSong
from GUI import songGUI


## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0
    print()

    # Gets list of songs, keys, and output filename from user
    songs, keys, filename = songGUI()
    fileNameDOCX, fileNamePDF = f"{filename}.docx", f"{filename}.pdf"

    # Writes each song
    for song, key in zip(songs, keys):
        doc, lineCount = writeSong(doc, lineCount, song, key)
        print(f"Wrote {song}.")

    # Gets output file directory from file
    with Path("Settings.json").open() as settings_json:
        settings = json.load(settings_json)
        outPath = Path(settings["OUTPUT_PATH"])

    print()

    if not outPath.is_dir():
        print("Can't find file path " + str(outPath))
        print("Make sure your file path is correct in Settings.json")

    outPathDOCX = outPath / fileNameDOCX
    outPathPDF = outPath / fileNamePDF

    # Saves document as .docx
    try:
        doc.save(str(outPathDOCX))
        print("Chord sheet saved as .docx file.")
    except:
        # TODO: is this necessary?
        print("Unknown exception with saving .docx file.")

    # Saves document as .pdf
    if pdfWrite(outPathDOCX, outPathPDF):
        print("Chord sheet converted to PDF.")
    else:
        print("Error saving chord sheet as PDF.")

    print("Done.")


if __name__ == "__main__":
    main()
