## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   3/2/2019

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
            songFile = songs[i].replace(" ", "")
            songFile = songFile.replace(",", "")
            songFile = songFile.replace("'", "")
            doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        doc.save("C:\\Users\\samcr\\OneDrive\\Documents\\LIFT\\LIFT Worship " + date + ".docx")
    else:
        doc, lineCount = writeSong(doc, lineCount, "JesusWeLoveYou", "B")
        doc, lineCount = writeSong(doc, lineCount, "HallelujahHereBelow", "C")
        doc, lineCount = writeSong(doc, lineCount, "WhatABeautifulName", "D")
        doc, lineCount = writeSong(doc, lineCount, "IWillBoastInChrist", "A")

        # doc, lineCount = writeSong(doc, lineCount, "GloriousDay", "D")
        # doc, lineCount = writeSong(doc, lineCount, "Anointing", "B")
        # doc, lineCount = writeSong(doc, lineCount, "LetThereBeLight", "B")
        # doc, lineCount = writeSong(doc, lineCount, "ThePassion", "B")
        doc.save('output.docx')

main()