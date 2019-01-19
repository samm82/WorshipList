## @file WorshipList.py
#  @brief Generates a worship chart from specifies songs and keys.
#  @author Samuel Crawford
#  @date 1/18/2019

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def main():
    doc = Document()
    doc = writeSong(doc, "LionAndTheLamb", "G")

    doc.save('output.docx')

def writeSong(doc, name, key):
    infile = open(name+".txt", "r")
    lines = infile.readlines()
    infile.close()

    # Defines default style

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(28)

    # Writes title

    p = doc.add_paragraph()
    title = p.add_run(lines[0].strip() + " ")
    title.font.name = 'Calibri'
    title.font.size = Pt(36)
    title.underline = True

    titleKey = p.add_run("(" + key + ")")
    titleKey.font.name = 'Calibri'
    titleKey.font.size = Pt(20)
    titleKey.underline = True

    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Writes chords

    for i in lines[1:]:
        line = i.split()

        p = doc.add_paragraph()
        pClass = p.add_run(line[0])

        for chord in line[1:]:
            if chord == "|":
                p.add_run("|  ")
            elif chord == "double":
                # Might need spaces after
                p.add_run(" x 2")
            elif "/" in chord:
                newChord = chord[:-1]
                p.add_run(getChord(key, newChord) + "/")
            else:
                p.add_run(getChord(key, chord) + "  ")

    return doc

def getChord(key, num):
    # TODO: make more efficient
    # TODO: allow for lowercase key
    # TODO: allow for sharp/flat keys
    if key == "F":
        keyList = ["F", "G", "A", "Bb", "C", "D", "E"]
    elif key == "C":
        keyList = ["C", "D", "E", "F", "G", "A", "B"]
    elif key == "G":
        keyList = ["G", "A", "B", "C", "D", "E", "F#"]
    elif key == "D":
        keyList = ["D", "E", "F#", "G", "A", "B", "C#"]
    elif key == "A":
        keyList = ["A", "B", "C#", "D", "E", "F#", "G#"]
    elif key == "E":
        keyList = [ "E", "F#", "G#", "A", "B", "C#", "D#"]
    elif key == "B":
        keyList = ["B", "C#", "D#", "E", "F#", "G#", "A#"]
    else:
        # TODO: Convert to formal exception
        print("Wrong key")
        exit()

    minor = False
    if num.islower():
        minor = True

    num = num.lower()

    # TODO: make more efficient
    if num == "i":
        chord = keyList[0]
    elif num == "ii":
        chord = keyList[1]
    elif num == "iii":
        chord = keyList[2]
    elif num == "iv":
        chord = keyList[3]
    elif num == "v":
        chord = keyList[4]
    elif num == "vi":
        chord = keyList[5]
    elif num == "vii":
        chord = keyList[6]
    else:
        # TODO: Convert to formal exception
        print("Wrong chord")
        exit()

    if minor:
        chord += "m"

    return chord

main()