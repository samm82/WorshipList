## @file   Main.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   12/30/2021

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
    with Path("src/Settings.txt").open() as fp:
        filepath = Path(fp.readline().strip())

    print()

    if not filepath.is_dir():
        print("Can't find file path " + str(filepath))
        print("Make sure your file path is correct in Settings.txt")

    filepathDOCX = filepath / fileNameDOCX
    filepathPDF = filepath / fileNamePDF

    # Saves document as .docx
    try:
        doc.save(str(filepathDOCX))
        print("Chord sheet saved as .docx file.")
    except:
        # TODO: is this necessary?
        print("Unknown exception with saving .docx file.")

    # Saves document as .pdf
    if pdfWrite(filepathDOCX, filepathPDF):
        print("Chord sheet converted to PDF.")
    else:
        print("Error saving chord sheet as PDF.")

    print("Done.")


if __name__ == "__main__":
    main()
