## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   6/1/2019

from Document  import docSetup, pdfWrite, writeSong
from GUI       import fileNameGUI, songGUI

## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0

    print()

    # Writes each song

    songs, keys = songGUI()
    date = fileNameGUI()
    for i in range(4):
        songName, songFile = songs[i], songs[i]
        for char in [' ', ',', "'", "(", ")"]:
            songFile = songFile.replace(char, "")
        doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        print("Wrote", songName + ".")
    file = "C:\\Users\\samcr\\OneDrive\\Documents\\LIFT\\LIFT Worship " + date

    print()

    # Saves document as .docx
    doc.save(file + ".docx")
    print("Chord sheet saved as docx.")
    
    # Saves document as .pdf
    pdfWrite(file)
    print("Chord sheet converted to PDF.")
    print("Done.")

main()