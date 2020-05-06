#PDF Lib
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
import string

#Grammar & Spelling Lib
import nltk

# Flask initialization
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# base64 encode
import base64

app = Flask(__name__)

#CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/api/result', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        f = request.files['cvfile']
        
        pdfstring = base64.b64encode(f.read())
        pdfstring = pdfstring.decode('ascii')

        filename = f.filename
        filesize = str(int(len(f.read())/1024)) + "kb"
        text = extract_text_from_pdf(f)
        word_count = len(text.split())
        word_result = word_metric(word_count)
        text_array = text.strip().split('\n')
        for i in range (len(text_array)):
            text_array[i] = "<p>" + text_array[i] + "</p>"
        text = Markup(''.join(text_array))
        
        return render_template("result.html", filename=filename, filesize=filesize, word_count=word_count, pdfstring=pdfstring, word_result=word_result)

def word_metric(word_count):
    if word_count <= 449:
        metric_result = "Add more words!"
    if word_count >= 650:
        metric_result = "Reduce amount of words!"
    if word_count >= 450 & word_count <= 649:
        metric_result = "Appropriate word count"
    
    return metric_result

def extract_text_from_pdf(file):
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


if __name__ == '__main__':
    app.run()
