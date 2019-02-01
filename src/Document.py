## @file   Document.py
#  @brief  Contains functions for adding text to document.
#  @author Samuel Crawford
#  @date   1/28/2019

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT

from MusicData import getChord, getNotes

## @brief  Sets up an empty document.
#  @return The document.
def docSetup():
    doc = Document()
    
    # Defines margins

    section = doc.sections[0]
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # Defines default style

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(28)

    return doc

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

    doc = writeTitle(doc, lines[0], key)

    # Gets list of notes from getNotes(key)

    noteList = getNotes(key)

    # Writes the lines with chords

    for i in range(1, len(lines)):
        line = lines[i].split()
        end = i == len(lines) - 1

        doc, newLines = writeLine(doc, line, end, noteList, fileName)
        lineCount += newLines

    return doc, lineCount

## @brief            Writes a song title to the document.
#  @param[in] doc    The document to write to.
#  @param[in] title  The title to write to the document.
#  @param[in] key    The key of the song.
#  @return          The document.
def writeTitle(doc, title, key):
    p = doc.add_paragraph()
    title = p.add_run(title.strip() + " ")
    title.font.size = Pt(36)
    title.underline = True

    titleKey = p.add_run("(" + key + ")")
    titleKey.font.size = Pt(20)
    titleKey.underline = True

    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)

    return doc

## @brief           Writes a line to the document.
#  @param[in] doc   The document to write to.
#  @param[in] line  The line to write to the document.
#  @param[in] end   A boolean; True if line is the last line in the song.
#  @param[in] notes The list of valid notes.
#  @param[in] file  The file with the line to write.
#  @return          The document.
def writeLine(doc, line, end, notes, file):
    p = doc.add_paragraph()

    # Defines tab stops
    
    tab_stops = p.paragraph_format.tab_stops
    tab_stop = tab_stops.add_tab_stop(Inches(1.58), WD_TAB_ALIGNMENT.LEFT)

    p, chordStart = writeSection(p, line, 0)

    # small = 0 -> normal size
    # small = 1 -> small size
    # small = 2 -> last small size

    small      = 0
    extraLines = 0

    # Adds all chords

    for chord in line[chordStart:]:
        if chord == "|":
            run = p.add_run("|  ")
        elif chord == "new":
            run = p.add_run("\n\t")
            extraLines += 1
        elif chord == "double":
            run = p.add_run("x 2  ")
        elif chord == "triple":
            run = p.add_run("x 3  ")
        elif "/" in chord:
            newChord = chord[:-1]
            run = p.add_run(getChord(notes, newChord, file) + "/")
        elif "(" in chord:
            newChord = chord[1:]
            run = p.add_run("(" + getChord(notes, newChord, file) + "  ")
            small = 1
        elif ")" in chord:
            newChord = chord[:-1]
            run = p.add_run(getChord(notes, newChord, file) + ")  ")
            small = 2
        else:
            run = p.add_run(getChord(notes, chord, file) + "  ")

        # Set font size for small text

        if small == 1:
            run.font.size = Pt(22)
        if small == 2:
            run.font.size = Pt(22)
            small = 0

    # Sets paragraph spacing

    if end:
        p.paragraph_format.space_after = Pt(10)
    else:
        p.paragraph_format.space_after = Pt(0)

    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = Pt(36)

    return doc, extraLines

## @brief           Writes a section name to the document.
#  @param[in] p     The paragraph to write to.
#  @param[in] line  The line to get the section name from.
#  @param[in] start The index the chords start at.
#  @return          The paragraph and the index the chords start at.
def writeSection(p, line, start):
    if line[0][-1] == ":":
        p.add_run(line[0] + "\t")
        return p, start + 1
    else:
        p.add_run(line[0] + " " + line[1] + "\t")
        return p, start + 2
