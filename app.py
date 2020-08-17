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

import io
from matplotlib.figure import Figure
import base64

#Grammar & Spelling Lib
import pylanguagetool
import nltk

#Regular Expression
import re

from spellchecker import SpellChecker

# Flask initialization
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from nltk.tokenize import PunktSentenceTokenizer
nltk.download('averaged_perceptron_tagger')

nltk.download('punkt')

# fuzzywuzzy lib
from fuzzywuzzy import fuzz

# base64 encode
import base64

app = Flask(__name__)
#sslify = SSLify(app)

#CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/api/result', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        f = request.files['cvfile']
        
        #PDF Preview
        pdfstring = base64.b64encode(f.read())
        pdfstring = pdfstring.decode('ascii')

        f.seek(0)
        filename = "File name: " + f.filename
        filesize = "File size: " + str(int(len(f.read())/1024)) + "kb"
        text = extract_text_from_pdf(f)

        #Word count metrics
        word_count_num = len(text.split())
        word_count_result = word_metric(word_count_num)

        #Spellchecker
        spellcheck = spellchecker(text)

        # Bullet points counter
        bpCounter = bulletPointCounter(text)

        #firstPersonSentiment
        fps = firstPersonSentiment(text)

        #Count word frequency
        word_list = word_filter(word_frequency(text))
        essential_section = word_matching(word_frequency(text))
        word_count = "Word Count: " + str(word_count_num)

        #Four factors
        impact = [filename, filesize, word_count, fps[0], fps[1]]
        brevity = [spellcheck, bpCounter, word_count_result, word_count_num]
        style = essential_section
        soft_skills = ["a", "b", "c", "d", "e"]

        return render_template("result.html", impact=impact, brevity=brevity, style=style, soft_skills=soft_skills, pdfstring=pdfstring)
    return redirect(url_for('index'))


#Spellchecker
def spellchecker(text):
    sc = SpellChecker()
    sc.word_frequency.load_dictionary('static/test_dict.json')
    shortenedWords = []

    #Spellchecking
    emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    clonedList = re.sub('[\W+]',' ', text)
    clonedList = clonedList.split()
    misspelled = sc.unknown(clonedList)


    for m in misspelled:
        if(re.search(emailRegex,m)):
            continue
        cleanString = re.sub('\W+','', m)
        shortenedWords.append(reduce_lengthening(cleanString))

    cleanList = shortenedWords.copy()    

    output = "You may have misspelled the following words: " + '\n' + ', '.join(cleanList)

    return output

# Count bullet points
def bulletPointCounter(text):
    bulletPointRegex = '•\s(.+?)((?=(•))|(?=($)))'

    bulletPointList = re.findall(bpRegex, text, re.IGNORECASE | re.MULTILINE)
    bulletPointCount = len(bulletPointList)

    processed = "Your CV has " + str(bulletPointCount) + " total bullet points."
    return processed



#firstPersonSentiment
def firstPersonSentiment(text):
    textClone = nltk.word_tokenize(text)
    textCloneTag= nltk.pos_tag(textClone)
    
    tagged_sent = textCloneTag
    tagged_sent_str = ' '.join([word + '/' + pos for word, pos in tagged_sent])

    countFirstPerson = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("PRP"), tagged_sent_str))

    countNoun = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("NN"), tagged_sent_str))
    countActionVerb = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("VB"), tagged_sent_str))

    processed="Your CV has " + str(countFirstPerson) + " instances of first-person usage."

    nounverb = "There were " + str(countNoun) + " nouns in your CV. It contains "+ str(countActionVerb) + " action verbs."

    return [processed, nounverb]

def word_metric(word_count):
    if  450 <= word_count <= 650:
        metric_result = "Appropriate word count"
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Congrats! your resume has " + str(word_count) + " words."
    else:
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Unfortunately, your resume has " + str(word_count) + " words."
        if word_count <= 449:
            metric_result = "Add more words!"
        if word_count >= 650:
            metric_result = "Reduce amount of words!"

    return metric_result + word_count_warning

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
    score = 0
    result = ["", "", "", "", "", ""]

    for(key, value) in dictObject.items():
        #print(key)
        if li1:
            for x in list1:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li1 = False
                    print("career objective achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    result[1] = "Career objective: included"
                    break
                else:
                    result[1] = "Career objective: not included"

        if li2:
            for x in list2:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li2 = False
                    print("education achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    result[2] = "Education & Qualification: included"
                    break
                else:
                    result[2] = "Education & Qualification: not included"

        if li3:
            for x in list3:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li3 = False
                    print("employment achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    result[3] = "Employment History: included"
                    break
                else:
                    result[3] = "Employment History: not included"

        if li4:
            for x in list4:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li4 = False
                    print("skill achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    result[4] = "Skills summary: included"
                    break
                else:
                    result[4] = "Skills summary: not included"

        if li5:
            for x in list5:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li5 = False
                    print("reference achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    result[5] = "References: included"
                    break
                else:
                    result[5] = "References: not included"

        #result[0] = "Total score: " + str(score)
        result[0] = score
    return result

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')

if __name__ == '__main__':
    app.run()