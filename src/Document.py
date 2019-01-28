## @file   Document.py
#  @brief  Contains functions for adding text to document.
#  @author Samuel Crawford
#  @date   1/28/2019

from docx import Document
from docx.shared import Inches, Pt

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
