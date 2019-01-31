## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   1/31/2019

from sys import argv

from Document  import docSetup, writeSong
from GUI       import fileNameGUI, songGUI

## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0

    # Writes each song

    if "gui" in argv:
        songs, keys = songGUI()
        date = fileNameGUI()
        for i in range(4):
            doc, lineCount = writeSong(doc, lineCount, songs[i].replace(" ", ""), keys[i])
        doc.save("C:\\Users\\samcr\\OneDrive\\Documents\\LIFT\\LIFT Worship " + date + ".docx")
    else:
        doc, lineCount = writeSong(doc, lineCount, "ThePassion", "D")
        doc, lineCount = writeSong(doc, lineCount, "Anointing", "B")
        doc, lineCount = writeSong(doc, lineCount, "OPraiseTheName", "B")
        doc, lineCount = writeSong(doc, lineCount, "DeathWasArrested", "B")
        doc.save('output.docx')

main()