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
from spellchecker import SpellChecker

# Flask initialization
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# fuzzywuzzy lib
from fuzzywuzzy import fuzz

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

        sc = SpellChecker()
        sc.word_frequency.load_dictionary('static/test_dict.json')
        shortenedWords = []

        
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


        #Spellchecking
        emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        clonedList = text
        misspelled = sc.unknown(clonedList.split())

        for m in misspelled:
            if(re.search(emailRegex,m)):
                continue
            cleanString = re.sub('\W+','', m)
            shortenedWords.append(reduce_lengthening(cleanString))

        cleanList = shortenedWords.copy()

        for s in range(len(shortenedWords)):
            shortenedWords[s] = sc.correction(shortenedWords[s])
        
        #Count word frequency
        word_list = word_filter(word_frequency(clonedList))
        word_matching(word_frequency(clonedList))
        text = Markup(''.join(text_array))

        text = Markup(''.join(text_array))
        
        return render_template("result.html", filename=filename, filesize=filesize, word_count=word_count, misspelled=cleanList, corrected=shortenedWords,
        word_list = word_list, pdfstring=pdfstring, word_result=word_result)

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

def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1",text)

def word_frequency(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def word_filter(dictObject):
    new_counts = dict()
    for(key, value) in dictObject.items():
        if value >= 5: new_counts[key] = value
 
    return new_counts

# word_matching is used for essential part
# it will find the word that match the lists and return related result
def word_matching(dictObject):
    # dictObject variable must come from word_frequency result
    list1 = ["career", "objective", "summary", "profile"]
    list2 = ["elementary","education", "qualification", "training", "academic", "GPA", "Bachelor", "degree", "master", "PhD", "high school", "diploma", "accociate degree", "TAFE", "certificates", "archiement"]
    list3 = ["part-time","employment", "Experience", "work", "placement", "internship", "profesional", "volunteer", "practicums", "job"]
    list4 = ["skill", "attribute", "strength", "key skills", "know", "knew", "programming", "java", "language", "c#", "flask", "python", "AWS", "d3"]
    list5 = ["referee", "reference"]
    li1 = True
    li2 = True
    li3 = True
    li4 = True
    li5 = True

    for(key, value) in dictObject.items():
        #print(key)
        if li1:
            for x in list1:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li1 = False
                    print("career objective achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                # else:
                #     print(fuzz.token_sort_ratio(key.lower(),x.lower()))

        if li2:
            for x in list2:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li2 = False
                    print("education achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                # else:
                #     print(fuzz.token_sort_ratio(key.lower(),x.lower()))

        if li3:
            for x in list3:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li3 = False
                    print("employment achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                # else:
                #     print(fuzz.token_sort_ratio(key.lower(),x.lower()))

        if li4:
            for x in list4:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li4 = False
                    print("skill achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                # else:
                #     print(fuzz.token_sort_ratio(key.lower(),x.lower()))

        if li5:
            for x in list5:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li5 = False
                    print("reference achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                # else:
                #     print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                            
if __name__ == '__main__':
    app.run()

