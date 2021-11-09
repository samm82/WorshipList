## @file   Main.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   11/9/2021

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
    fileName = fileNameGUI()
    for i in range(len(songs)):
        songName, songFile = titlecase(songs[i]), titlecase(songs[i])
        doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        print("Wrote", songName + ".")

    # Get output file directory from file
    with open("src\\Settings.txt", "r") as fp:
        file = fp.read().strip() + fileName

    print()

    # Saves document as .docx
    try:
        doc.save(file + ".docx")
        print("Chord sheet saved as docx.")
    except:
        print("Can't find file path " + file)
        print("Make sure your file path is correct in Settings.txt")
    
    # Saves document as .pdf
    pdfWrite(file)
    print("Chord sheet converted to PDF.")
    print("Done.")

main()