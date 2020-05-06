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
import PyPDF2
import string
import mapplotlib.pyplot as plt, mpld3

import matplotlib.pyplot as plt, mpld3
import io
from matplotlib.figure import Figure
import base64

#Grammar & Spelling Lib
import pylanguagetool
import nltk
import re

# Flask initialization
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from nltk.tokenize import PunktSentenceTokenizer
nltk.download('averaged_perceptron_tagger')
<<<<<<< Updated upstream
nltk.download('punkt')
=======
nltk.downlload('punkt')
>>>>>>> Stashed changes

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
        text = extract_text_from_pdf(f)
        word_count = len(text.split())
        text_array = text.strip().split('\n')
        for i in range (len(text_array)):
            text_array[i] = "<p>" + text_array[i] + "</p>"
        
        text = Markup(''.join(text_array))
        
<<<<<<< Updated upstream
        if  450 <= word_count <= 650:
            word_count_warning = "Top resumes are generally between 450 and 650 words long. Congrats! your resume has " + str(word_count) + " words."
        else:
            word_count_warning = "Top resumes are generally between 450 and 650 words long. Unfortunately, your resume has " + str(word_count) + " words."
=======
>>>>>>> Stashed changes



    #firstPersonSentiment
    textClone = nltk.word_tokenize(text)
    textCloneTag= nltk.pos_tag(textClone)
    
    tagged_sent =textCloneTag
    tagged_sent_str = ' '.join([word + '/' + pos for word, pos in tagged_sent])

    countFirstPerson = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("PRP"), tagged_sent_str))

    countNoun = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("NN"), tagged_sent_str))
    countActionVerb = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("VB"), tagged_sent_str))

<<<<<<< Updated upstream
    
        
    processed="Your CV has " + str(countFirstPerson) + " instances of first-person usage."

    nounverb = "There were " + str(countNoun) + " nouns in your CV. It contains "+ str(countActionVerb) + " action verbs."
=======
    processed="Your CV has " + str(countFirstPerson) + " instances of first-person usage. Please fix!"
>>>>>>> Stashed changes



    #piechart
    plt.figure(figsize=(5,5))
<<<<<<< Updated upstream
    fig = Figure(figsize =(4,4))
=======
>>>>>>> Stashed changes

    labels = ["Nouns","Action Verbs"]
    values = [countNoun, countActionVerb]
    

<<<<<<< Updated upstream
    plt.pie(values,labels=labels, autopct="%.1f%%")
    #plt.show()
    #mpld3.show()
    fig = plt.figure()
    figureImage = mpld3.fig_to_html(fig)
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    base = base64.b64encode(img.getvalue())
    plt.close(fig)

    
    basesend ='<img src="data:image/png;base64, {}">'.format(base.decode('utf-8'))
                 
                
    
    
    return render_template("result.html", text=text, word_count = word_count, processed = processed, nounverb = nounverb,my_html =base)
=======
    plt.pie(values,labels=labels, autopct="%.1f%%",figure = fig)
    plt.show()
    mpld3.show()
    fig = plt.figure()
    figureImage = mpld3.fig_to_html(fig)
    
    return render_template("result.html", text=text, word_count = word_count, processed = processed, piechart = figureImage)
>>>>>>> Stashed changes


    
    

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
