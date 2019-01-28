## @file   WorshipList.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   1/28/2019

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT

from sys import argv

from Document import docSetup
from GUI import songGUI
from MusicData import getChord, getNotes

## @brief The main function of the program that calls other programs.
def main():
    doc = docSetup()
    lineCount = 0

    # Writes each song

    if "gui" in argv:
        songs, keys = songGUI()
        for i in range(4):
            doc, lineCount = writeSong(doc, lineCount, songs[i].replace(" ", ""), keys[i])
    else:
        doc, lineCount = writeSong(doc, lineCount, "ThePassion", "D")
        doc, lineCount = writeSong(doc, lineCount, "Anointing", "B")
        doc, lineCount = writeSong(doc, lineCount, "OPraiseTheName", "B")
        doc, lineCount = writeSong(doc, lineCount, "DeathWasArrested", "B")

    doc.save('output.docx')

## @brief               Writes a song to doc.
#  @param[in] doc       The document being generated.
#  @param[in] lineCount A counter of how many lines have been printed.
#  @param[in] fileName  The name of the song file.
#  @param[in] oldKey    The original key of the song (manipulated in function).
#  @return              The document (doc) and line counter (lineCount).
def writeSong(doc, lineCount, fileName, oldKey):
    infile = open("src/songs/" + fileName + ".txt", "r")
    lines = infile.readlines()
    infile.close()

    # Converts key to uppercase

    key = oldKey[0].upper()
    if len(oldKey) > 1:
        key += oldKey[1]

    # Gets list of notes from getNotes(key)

    noteList = getNotes(key)

    # Adds page break if song will get cut off

    newLineLength = len(lines)
    for line in lines:
        if "new" in line.split():
            newLineLength += 1

    lineCount += newLineLength

    if lineCount > 16:
        p = doc.add_paragraph()
        run = p.add_run()
        run.add_break(WD_BREAK.PAGE)
    
    # Writes title

    p = doc.add_paragraph()
    title = p.add_run(lines[0].strip() + " ")
    title.font.size = Pt(36)
    title.underline = True

    titleKey = p.add_run("(" + key + ")")
    titleKey.font.size = Pt(20)
    titleKey.underline = True

    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)

    # Writes chords

    for i in range(1, len(lines)):
        line = lines[i].split()

        p = doc.add_paragraph()

        # Defines tab stops
        
        tab_stops = p.paragraph_format.tab_stops
        tab_stop = tab_stops.add_tab_stop(Inches(1.58), WD_TAB_ALIGNMENT.LEFT)

        # Adds section name

        if line[0][-1] == ":":
            p.add_run(line[0] + "\t")
            chordStart = 1
        else:
            p.add_run(line[0] + " " + line[1] + "\t")
            chordStart = 2

        # small = 0 -> normal size
        # small = 1 -> small size
        # small = 2 -> last small size

        small = 0

        # Adds all chords

        for chord in line[chordStart:]:
            if chord == "|":
                run = p.add_run("|  ")
            elif chord == "new":
                run = p.add_run("\n\t")
                lineCount += 1
            elif chord == "double":
                run = p.add_run("x 2  ")
            elif chord == "triple":
                run = p.add_run("x 3  ")
            elif "/" in chord:
                newChord = chord[:-1]
                run = p.add_run(getChord(noteList, newChord, fileName) + "/")
            elif "(" in chord:
                newChord = chord[1:]
                run = p.add_run("(" + getChord(noteList, newChord, fileName) + "  ")
                small = 1
            elif ")" in chord:
                newChord = chord[:-1]
                run = p.add_run(getChord(noteList, newChord, fileName) + ")  ")
                small = 2
            else:
                run = p.add_run(getChord(noteList, chord, fileName) + "  ")

            # Set font size for small text

            if small == 1:
                run.font.size = Pt(22)
            if small == 2:
                run.font.size = Pt(22)
                small = 0

        # Sets paragraph spacing

        if i != len(lines) - 1:
            p.paragraph_format.space_after = Pt(0)
        else:
            p.paragraph_format.space_after = Pt(10)

        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = Pt(36)

    return doc, lineCount

main()