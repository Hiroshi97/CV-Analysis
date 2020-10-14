import io
import pdfminer
from pdfminer.converter import *
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdevice import PDFDevice
import PyPDF2

#PyMuPDF
import fitz

#InvisibleTextFilter
from InvisibleTextFilter import InvisibleTextFilter

import base64

def extractTextFromPDF(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager,
                              fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
        page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        #Omit a strange symbol and break the string to a new line
        return text.replace(text[-1], '\n')

def highlightText(textArr, f, color):
    f.seek(0)
    doc = fitz.Document(stream=bytearray(f.read()), filename='cv.pdf')
    if (len(textArr) > 0):
        for p in doc.pages():
            for text in textArr:
                text_instances = p.searchFor(text)
                for inst in text_instances:
                    highlight = p.addHighlightAnnot(inst)
                    highlight.setColors({"stroke": color, "fill": (1, 1, 1)})
                    highlight.update()

    memoryStream = doc.write()
    doc.close()
    return base64.b64encode(memoryStream).decode('ascii')

# Get Invisible Text
def filterHiddenText(f):
    f.seek(0)
    doc = fitz.open(stream=bytearray(f.read()), filetype='pdf')
    textFilter = InvisibleTextFilter(deltaEThreshold= 25)
    result = []
    for page in doc:
        result.append(textFilter.getInvisibleText(page))

    return result