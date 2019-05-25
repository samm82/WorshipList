## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   5/25/2019

from sys import argv

from Document  import docSetup, pdfWrite, writeSong
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
            songFile = songs[i]
            for char in [' ', ',', "'", "(", ")"]:
                songFile = songFile.replace(char, "")
            doc, lineCount = writeSong(doc, lineCount, songFile, keys[i])
        file = "C:\\Users\\samcr\\OneDrive\\Documents\\LIFT\\LIFT Worship " + date
    else:
        doc, lineCount = writeSong(doc, lineCount, "JesusWeLoveYou", "B")
        doc, lineCount = writeSong(doc, lineCount, "HallelujahHereBelow", "C")
        doc, lineCount = writeSong(doc, lineCount, "WhatABeautifulName", "D")
        doc, lineCount = writeSong(doc, lineCount, "WholeHeartHoldMeNow", "E")

        # doc, lineCount = writeSong(doc, lineCount, "GloriousDay", "D")
        # doc, lineCount = writeSong(doc, lineCount, "Anointing", "B")
        # doc, lineCount = writeSong(doc, lineCount, "LetThereBeLight", "B")
        # doc, lineCount = writeSong(doc, lineCount, "ThePassion", "B")
        file = "C:\\Users\\samcr\\Desktop\\Programming\\WorshipList\\output"

    # Saves document as .docx
    doc.save(file + ".docx")
    
    # Saves document as .pdf
    pdfWrite(file)

main()