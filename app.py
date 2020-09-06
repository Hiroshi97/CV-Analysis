#PDF Lib
from operator import itemgetter
from fuzzywuzzy import fuzz
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
from InvisibleTextFilter import InvisibleTextFilter

import io
from matplotlib.figure import Figure
import base64

#Grammar & Spelling Lib
import pylanguagetool
import nltk

#Regular Expressionn
import re

#PyMuPDFf
import fitz

#date finder sorter
from DateSorter import DateSorter


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

# base64 encode

# itemgetter

# itemgetter
from operator import itemgetter

app = Flask(__name__)
#sslify = SSLify(app)

#CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#global variable for scoring system
list1_score = ["2", "1", "3", "4", "4", "2", "3", "4"]
list2_score = [True, True, True, True, True, True, True, True]
scored_list = ["", ""]

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

        # Filter invisible text
        invisible_text = filterHiddenText(f)
        print(invisible_text)

        global list2_score
        #scoring system
        if int(len(f.read())/1024) > 20000:
            list2_score[2] = True
        else:
            list2_score[2] = False 

        #Word count metrics
        word_count_num = len(text.split())
        word_count_result = word_metric(word_count_num)

        #scoring system
        if word_count_num > 2000:
            list2_score[7] = True
        else:
            list2_score[7] = False 

        #Spellchecker
        spellcheck = spellchecker(text)

        # Bullet points counter
        bpCounter = bulletPointCounter(text)

        # Quantify bullet points
        bpQuantify = quantifyBulletPoints(text)

        #datefinder
        datesorter = DateSorter()

        #firstPersonSentiment
        fps = firstPersonSentiment(text)

        #Count word frequency
        word_list = word_filter(word_frequency(text))
        essential_section = word_matching(word_frequency(text))
        word_count = "Word Count: " + str(word_count_num)

        #Four factors
        impact = [0, filename, filesize, word_count, fps[0], fps[1]]

        brevity = [0, spellcheck[0], bpCounter[2],
                   word_count_result, bpQuantify]
        style = [essential_section[0], essential_section[1],
                 essential_section[2], essential_section[3], datesorter.datefindersorter(text)]

        soft_skills = [0, "a", "b", "c", "d", "e"]
        length = [len(impact), len(brevity), len(style), len(soft_skills)]

        #Highlighted files
        pdfstrings = []
        pdfstrings.append(pdfstring)  # Original file
        pdfstrings.append(highlightText(spellcheck[1], f, (1, 0, 0)))
        pdfstrings.append(highlightText(essential_section[6], f, (0, 1, 0)))

        return render_template("result.html", impact=impact, brevity=brevity, style=style, soft_skills=soft_skills, pdfstrings=pdfstrings, length=length)
    return redirect(url_for('index'))


#Spellchecker
def spellchecker(text):
    sc = SpellChecker()
    sc.word_frequency.load_dictionary('static/test_dict.json')
    shortenedWords = []

    #Spellchecking
    emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    clonedList = re.sub('[\W+]', ' ', text)
    clonedList = clonedList.split()
    misspelled = sc.unknown(clonedList)

    for m in misspelled:
        if(re.search(emailRegex, m)):
            continue
        cleanString = re.sub('\W+', '', m)
        shortenedWords.append(reduce_lengthening(cleanString))

    cleanList = shortenedWords.copy()

    if not cleanList:
        output = "Your resume is free of spelling errors! Congratulations!"
    else:
        output = "You may have misspelled the following words: " + \
            '\n' + ', '.join(cleanList)
        
    global list2_score
    #scoring system
    if cleanList:
        list2_score[6] = False
    else:
        list2_score[6] = True

    return [output, cleanList]

# Count bullet points


def bulletPointCounter(text):
    bulletPointRegex = '•\s(.+?)((?=(•))|(?=($)))'

    bulletPointList = re.findall(
        bulletPointRegex, text, re.IGNORECASE | re.MULTILINE)
    bulletPointCount = len(bulletPointList)

    processed = "Your CV has " + \
        str(bulletPointCount) + " total bullet points."

    processed = "Your CV has " + str(bulletPointCount) + " total bullet points."

    global list2_score
    #scoring system
    if bulletPointCount >= 0:
        list2_score[5] = False
    else:
        list2_score[5] = True

    return [bulletPointList, bulletPointCount, processed]

# Quantify bullet points


def quantifyBulletPoints(text):

    # 1. Extract content of bullet points
    bp = bulletPointCounter(text)
    contentList = []
    quantifiedCount = 0

    bulletPointCount = bp[1]
    bulletPointList = bp[0]

    contentList.append(list(map(itemgetter(0), bulletPointList)))

    # 2. Count how many of those strings contain a number

    quantifyRegEx = r'\b[^.,/a-zA-Z\-+\]](\d+)(?!\.|,)\b'
    clonedList = contentList[0].copy()

    for i in clonedList:
        if(re.search(quantifyRegEx, i)):
            quantifiedCount += 1
    result = "Out of " + str(bulletPointCount) + " bullet points in your CV, " + \
        str(quantifiedCount) + " has been quantified."

    return result


#firstPersonSentiment
def firstPersonSentiment(text):
    textClone = nltk.word_tokenize(text)
    textCloneTag = nltk.pos_tag(textClone)

    tagged_sent = textCloneTag
    tagged_sent_str = ' '.join([word + '/' + pos for word, pos in tagged_sent])

    countFirstPerson = sum(1 for _ in re.finditer(
        r'\b%s\b' % re.escape("PRP"), tagged_sent_str))

    countNoun = sum(1 for _ in re.finditer(r'\b%s\b' %
                                           re.escape("NN"), tagged_sent_str))
    countActionVerb = sum(1 for _ in re.finditer(
        r'\b%s\b' % re.escape("VB"), tagged_sent_str))

    processed = "Your CV has " + \
        str(countFirstPerson) + \
        " instances of first-person usage. A good CV should have no instances, as it seems unproffesional."

    nounverb = "There were " + str(countNoun) + " nouns in your CV. It contains " + str(
        countActionVerb) + " action verbs. Action verbs make you stand out as a candidate!"

    global list2_score
    #scoring system
    if countFirstPerson > 5:
        list2_score[0] = True
    else:

        list2_score[0] = False

    if countActionVerb > 5 and countNoun > 5:
        list2_score[1] = True
    else:
        list2_score[1] = False

    return [processed, nounverb]




def word_metric(word_count):
    if 450 <= word_count <= 650:
        metric_result = "Appropriate word count"
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Congrats! your resume has " + \
            str(word_count) + " words."
    else:
        word_count_warning = " Top resumes are generally between 450 and 650 words long. Unfortunately, your resume has " + \
            str(word_count) + " words."
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
    return pattern.sub(r"\1\1", text)


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
        if value >= 5:
            new_counts[key] = value

    return new_counts

def word_match(key,list,li,score,output):
    for x in list:
        if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
            li = False          
            print(output + " achieved!!!")
            print(fuzz.token_sort_ratio(key.lower(),x.lower()))
            print(key)
            score += 20
            print("score: ", score)
            result = output + ": included"
            break
        else:
            result = output + ": not included"
    return li,score,result    

def word_match(key, list, li, score, output):
    for x in list:
        if fuzz.token_sort_ratio(key.lower(), x.lower()) > 80:
            li = False
            print(output + " achieved!!!")
            print(fuzz.token_sort_ratio(key.lower(), x.lower()))
            print(key)
            score += 20
            print("score: ", score)
            result = output + ": included"
            break
        else:
            result = output + ": not included"
    return li, score, result

# word_matching is used for essential part
# it will find the word that match the lists and return related result


def word_matching(dictObject):
    # dictObject variable must come from word_frequency result
    list1 = ["career", "objective", "summary", "profile"]
    list2 = ["elementary", "education", "qualification", "training", "academic", "GPA", "Bachelor", "degree",
             "master", "PhD", "high school", "diploma", "accociate degree", "TAFE", "certificates", "archiement"]
    list3 = ["part-time", "employment", "Experience", "work", "placement",
             "internship", "professional", "volunteer", "practicums", "job"]
    list4 = ["skill", "attribute", "strength", "key skills", "know", "knew",
             "programming", "java", "language", "c#", "flask", "python", "AWS", "d3"]
    list5 = ["referee", "reference"]
    li1 = True
    li2 = True
    li3 = True
    li4 = True
    li5 = True
    score = 0
    result = ["", "", "", "", "", ""]
    highlight = []

    for(key, value) in dictObject.items():
        #print(key)
        if li1:
            li1, score, result[1] = word_match(
                key, list1, li1, score, "Career objective")
            if li1 is False:
                highlight.append(key)

        if li2:
            li2, score, result[2] = word_match(
                key, list2, li2, score, "education")
            if li2 is False:
                highlight.append(key)

        if li3:
            li3, score, result[3] = word_match(
                key, list3, li3, score, "Employment History")
            if li3 is False:
                highlight.append(key)

        if li4:
            li4, score, result[4] = word_match(key, list4, li4, score, "Skill")
            if li4 is False:
                highlight.append(key)

        if li5:
            li5, score, result[5] = word_match(
                key, list5, li5, score, "References")
            if li5 is False:
                highlight.append(key)

    global scored_list
    scored_list[0] = section_Scored(
        [4, 4, 4, 4, 4], [li1, li2, li3, li4, li5])*100
    result[0] = (scored_list[0])
    result.append(highlight)
    return result

# word_match_Softskill is used for softskill part
# the function will only approved the resume have the specific skill when more than half of word from the list is found in the resume


def word_match_Softskill(key, list, li, score, output, counter):
    final_output = ""
    for x in list:
        if fuzz.token_sort_ratio(key.lower(), x.lower()) > 80:
            counter = counter + 1
            print(fuzz.token_sort_ratio(key.lower(), x.lower()))
            print(key)
            break

        if counter >= (len(list)/3):
            li = False
            score += 1
            print("score: ", score)
            final_output = output[0]
            break
        else:
            final_output = output[1]

    return li, score, final_output, counter


def word_matching_Softskill(dictObject):
    # dictObject variable must come from word_frequency result
    listCommunication = ["communicated", "described", "explained", "conveyed",
                         "reported", "presented", "expressed", "briefing", "briefed", "discussion"]
    listLeadership = ["lead", "leadership", "guided", "guide", "direct", "directed", "managed", "management", "orchestrated",
                      "initiative", "supervised", "supervisor", "authority", "controlled", "administrative", "administration", "capacity"]
    listTeamwork = ["collaborated", "collaboration", "together", "team", "joint",
                    "effort", "synergy", "cooperation", "cooperated", "assisted", "partnership", "team"]
    output_Communication = ["Your CV displays an adequate level of communication skills.",
                            "Your CV could display more evidence of communication skills. Words such as 'conveyed', 'briefed' and 'discussed' are useful."]
    output_Leadership = ["Your CV proves good leadership skills.",
                         "Your CV may appear more attractive to employers if you describe evidence of leadership. Some useful words to consider are 'directed', 'managed', 'supervised' and 'initiative'."]
    output_Teamwork = ["Your CV shows you are a team player.",
                       "Your CV could stand to display more team-oriented language. Words such as 'collaborated, 'synergy' and 'cooperation' are good."]
    li1 = True
    li2 = True
    li3 = True
    counter1 = 0
    counter2 = 0
    counter3 = 0
    score = 0
    result = ["", "", "", ""]

    for(key, value) in dictObject.items():
        #print(key)
        if li1:
            li1, score, result[1], counter1 = word_match_Softskill(
                key, listCommunication, li1, score, output_Communication, counter1)

        if li2:
            li2, score, result[2], counter2 = word_match_Softskill(
                key, listLeadership, li2, score, output_Leadership, counter2)

        if li3:
            li3, score, result[3], counter3 = word_match_Softskill(
                key, listTeamwork, li3, score, output_Teamwork, counter3)

    global scored_list
    scored_list[1] = section_Scored([4, 4, 4], [li1, li2, li3])*100

    result[0] = "Total score: " + str(scored_list[1])
    return result

#calculate the total score of each section, it can calculate more than 1 section if needed

def section_Scored(list1, list2):
    total = scored = 0
    for index, score in enumerate(list1):
        total += score
        if not list2[index]:
            scored += score
    return (scored/total)

#calculate the final overall scored in percentage (+ 4 sections and devided by 4)

def final_overall_scored():
    return (section_Scored(list1_score, list2_score) + scored_list[0] + scored_list[1])/4*100

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
    textFilter = InvisibleTextFilter()
    result = []
    for page in doc:
        result.append(textFilter.getInvisibleText(page))

    return result

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')


if __name__ == '__main__':
    app.run()
