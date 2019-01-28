## @file   Document.py
#  @brief  Contains functions for adding text to document.
#  @author Samuel Crawford
#  @date   1/28/2019

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT

from MusicData import getChord

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