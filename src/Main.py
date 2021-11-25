## @file   Main.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   11/24/2021

from pathlib import Path
from titlecase import titlecase

from Document  import docSetup, pdfWrite, writeSong
from GUI       import fileNameGUI, songGUI

## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0

    print()

    # Writes each song

    songs, keys = songGUI()
    fileNameDOCX, fileNamePDF = fileNameGUI()
    for i in range(len(songs)):
        songName, songFile = titlecase(songs[i]), titlecase(songs[i])
        doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        print("Wrote", songName + ".")

    # Get output file directory from file
    with Path("src/Settings.txt").open() as fp:
        filepath = Path(fp.readline().strip())

    print()

    if not filepath.is_dir():
        print("Can't find file path " + str(filepath))
        print("Make sure your file path is correct in Settings.txt")

    filepathDOCX = filepath / fileNameDOCX
    filepathPDF  = filepath / fileNamePDF

    # Saves document as .docx
    try:
        doc.save(str(filepathDOCX))
        print("Chord sheet saved as .docx file.")
    except:
        # TODO: is this necessary?
        print("Unknown exception with saving .docx file.")
    
    # Saves document as .pdf
    pdfWrite(filepathDOCX, filepathPDF)
    print("Chord sheet converted to PDF.")
    print("Done.")

main()