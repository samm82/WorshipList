## @file WorshipList.py
#  @brief Generates a worship chart from specifies songs and keys.
#  @author Samuel Crawford
#  @date 1/18/2019

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def main():
    doc = Document()
    doc = readSong(doc, "LionAndTheLamb", "G")

    doc.save('output.docx')

def readSong(doc, name, key):
    infile = open(name+".txt", "r")
    lines = infile.readlines()
    infile.close()

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

    print(lines)
    return doc

def getKey(key):
    # TODO: allow for lowercase key
    # TODO: allow for sharp/flat keys
    if key == "F":
        return ["A", "Bb", "C", "D", "E", "F", "G"]
    elif key == "C":
        return ["A", "B", "C", "D", "E", "F", "G"]
    elif key == "G":
        return ["A", "B", "C", "D", "E", "F#", "G"]
    elif key == "D":
        return ["A", "B", "C#", "D", "E", "F#", "G"]
    elif key == "A":
        return ["A", "B", "C#", "D", "E", "F#", "G#"]
    elif key == "E":
        return ["A", "B", "C#", "D#", "E", "F#", "G#"]
    elif key == "B":
        return ["A#", "B", "C#", "D#", "E", "F#", "G#"]
    else:
        # TODO: Convert to formal exception
        print("Wrong key")
        exit()

main()