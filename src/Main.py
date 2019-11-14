## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   11/14/2019

from Document  import docSetup, pdfWrite, writeSong
from GUI       import fileNameGUI, songGUI
from Helpers   import fileNameProcess, songNameProcess

## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0

    print()

    # Writes each song

    songs, keys = songGUI()
    date = fileNameGUI()
    for i in range(4):
        songName, songFile = songNameProcess(songs[i]), fileNameProcess(songs[i])
        doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        print("Wrote", songName + ".")

    # Get output file directory from file
    f = open("src\\Settings.txt", "r")
    path = f.read().strip()
    f.close()

    file = path + "LIFT Worship " + date

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