## @file WorshipList.py
#  @brief Generates a worship chart from specifies songs and keys.
#  @author Samuel Crawford
#  @date 1/18/2019

from docx import Document

def main():
    doc = Document()
    doc = readSong(doc, "LionAndTheLamb", "G")

    doc.save('output.docx')

def readSong(doc, name, key):
    infile = open(name+".txt", "r")
    lines = infile.readlines()
    infile.close()

    doc.add_heading(lines[0].strip(), 0)

    print(lines)
    return doc

main()