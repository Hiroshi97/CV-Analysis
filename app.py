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

#Regular Expressionn
import re

#PyMuPDFf
import fitz

#date finder sorter
from datetime import datetime


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

# itemgetter
from operator import itemgetter

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

        # Quantify bullet points
        bpQuantify = quantifyBulletPoints(text)

        #datefinder
        date = datefindersorter(text)

        #firstPersonSentiment
        fps = firstPersonSentiment(text)

        #Count word frequency
        word_list = word_filter(word_frequency(text))
        essential_section = word_matching(word_frequency(text))
        word_count = "Word Count: " + str(word_count_num)

        #Four factors
        impact = [0, filename, filesize, word_count, fps[0], fps[1]]
        brevity = [0, spellcheck[0], bpCounter[2], word_count_result, bpQuantify]
        style = [essential_section[0],essential_section[1],essential_section[2],essential_section[3],date]
        soft_skills = [0, "a", "b", "c", "d", "e"]
        length = [len(impact), len(brevity), len(style), len(soft_skills)]

        #Highlighted files
        pdfstrings = []
        pdfstrings.append(pdfstring) #Original file
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
    clonedList = re.sub('[\W+]',' ', text)
    clonedList = clonedList.split()
    misspelled = sc.unknown(clonedList)

    for m in misspelled:
        if(re.search(emailRegex,m)):
            continue
        cleanString = re.sub('\W+','', m)
        shortenedWords.append(reduce_lengthening(cleanString))

    cleanList = shortenedWords.copy()    

    if not cleanList:
        output = "Your resume is free of spelling errors! Congratulations!"
    else:
        output = "You may have misspelled the following words: " + '\n' + ', '.join(cleanList)   
    

    return [output, cleanList]

# Count bullet points
def bulletPointCounter(text):
    bulletPointRegex = '•\s(.+?)((?=(•))|(?=($)))'

    bulletPointList = re.findall(bulletPointRegex, text, re.IGNORECASE | re.MULTILINE)
    bulletPointCount = len(bulletPointList)

    processed = "Your CV has " + str(bulletPointCount) + " total bullet points."
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
        if(re.search(quantifyRegEx,i)):
            quantifiedCount += 1
    result = "Out of " + str(bulletPointCount) + " bullet points in your CV, " + str(quantifiedCount) + " has been quantified."


    return result


#firstPersonSentiment
def firstPersonSentiment(text):
    textClone = nltk.word_tokenize(text)
    textCloneTag= nltk.pos_tag(textClone)
    
    tagged_sent = textCloneTag
    tagged_sent_str = ' '.join([word + '/' + pos for word, pos in tagged_sent])

    countFirstPerson = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("PRP"), tagged_sent_str))

    countNoun = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("NN"), tagged_sent_str))
    countActionVerb = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("VB"), tagged_sent_str))

    processed="Your CV has " + str(countFirstPerson) + " instances of first-person usage. A good CV should have no instances, as it seems unproffesional."

    nounverb = "There were " + str(countNoun) + " nouns in your CV. It contains "+ str(countActionVerb) + " action verbs. Action verbs make you stand out as a candidate!"

    return [processed, nounverb]

def datefindersorter(text):
    result= "Your dates are in the correct order on your CV." #score up?
    badresult="Your dates are not in the correct yearly order. Employers like to see the most recent work and study experience first." #score down?
    monthresult ="Your dates are not in the correct monthly order. Employers like to see the most recent work and study experience first." #score down?
    
    regex1 = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}'
    regex2 = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}'
    regex3 = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{4}'
    regex4 = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{2}'
    regex5 = r'(?:january|february|march|april|may|june|july|august|september|october|november|december)\s\d{4}'
    regex6 = r'(?:january|february|march|april|may|june|july|august|september|october|november|december)\s\d{2}'
    regex7 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2}'
    regex8 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}'
    regex9 = r'(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s\d{4}'
    regex10 = r'(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s\d{2}'
    regex11 = r'[\d]{1,2}/[\d]{1,2}/[\d]{4}' #dd/mm/yyyy or d/m/yyyy
    regex12 = r'[\d]{1,2}-[\d]{1,2}-[\d]{2}' #dd-mm-yyyy or d-m-yyyy
    #regex13 = r'[\d]{1,2}'
    regex14 = r'[\d]{4}'
    
   
    
    dates1 = re.findall(regex1, text)
    dates2 = re.findall(regex2, text)
    dates3 = re.findall(regex3, text)
    dates4 = re.findall(regex4, text)
    dates5 = re.findall(regex5, text)
    dates6 = re.findall(regex6, text)
    dates7 = re.findall(regex7, text)
    dates8 = re.findall(regex9, text)
    dates9 = re.findall(regex9, text)
    dates10 = re.findall(regex10, text)
    dates11 = re.findall(regex11, text)
    dates12 = re.findall(regex12, text)
    #dates13 = re.findall(regex13, text)
    dates14 = re.findall(regex14, text)


    if dates1:

        def split_list(x):
            return [dates5[i:i+x] for i in range(0, len(dates5), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %Y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates2:

        def split_list(x):
            return [dates2[i:i+x] for i in range(0, len(dates2), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates3:

        def split_list(x):
            return [dates3[i:i+x] for i in range(0, len(dates3), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%b %Y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates4:

        def split_list(x):
            return [dates4[i:i+x] for i in range(0, len(dates4), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%b %y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates5:
        
        def split_list(x):
            return [dates5[i:i+x] for i in range(0, len(dates5), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        
            
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %Y')) #this format changes
       
        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult
    
    if dates6:

        def split_list(x):
            return [dates6[i:i+x] for i in range(0, len(dates6), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

            
    if dates7:

        def split_list(x):
            return [dates7[i:i+x] for i in range(0, len(dates7), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

        
    if dates8:
        
        def split_list(x):
            return [dates8[i:i+x] for i in range(0, len(dates8), x)]

        splitted_list = split_list(2)
        
        
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        both_months3=both_months.copy()
        try:
            
        
            both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%B %Y')) #this format changes

        except:
            both_months_sorted2 = both_months3.sort(key = lambda date:datetime.strptime(date, '%b %Y'))
            
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1

        elif (both_months == both_months3):
            flag=0
        elif (both_months != both_months3):
            flag=1    
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates9:

        def split_list(x):
            return [dates9[i:i+x] for i in range(0, len(dates9), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%b %Y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates10:

        def split_list(x):
            return [dates10[i:i+x] for i in range(0, len(dates10), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%b %y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult

    if dates11:

        def split_list(x):
            return [dates11[i:i+x] for i in range(0, len(dates11), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%x')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult
        
    if dates12:

        def split_list(x):
            return [dates12[i:i+x] for i in range(0, len(dates12), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%d-%m-%Y ')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return result 
        else:
            return badresult
        
    

    if dates14:

        def split_list(x):
            return [dates14[i:i+x] for i in range(0, len(dates14), x)]

        splitted_list = split_list(2)
        num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[0]))
        second_num_list = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])),splitted_list[1]))

        
        month_list= splitted_list[0][1] 
        second_month_list= splitted_list[1][0]
        both_months=[] 
        both_months.append(month_list)
        both_months.append(second_month_list)
        flag=0

        
        
        both_months2=both_months.copy()
        
        both_months_sorted = both_months2.sort(key = lambda date:datetime.strptime(date, '%Y')) #this format changes

        
            
        if (both_months == both_months2):
            flag=0
        elif (both_months != both_months2):
            flag=1
        
        
    
        if (num_list[1] > second_num_list[0]): 
            return result 
        elif (num_list[1] == second_num_list[0]) &  (flag == 0):
            return  splitted_list#monthresult
        elif (num_list[1] == second_num_list[0]) &  (flag == 1):
            return splitted_list#result 
        else:
            return splitted_list#badresult

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
    list3 = ["part-time","employment", "Experience", "work", "placement", "internship", "professional", "volunteer", "practicums", "job"]
    list4 = ["skill", "attribute", "strength", "key skills", "know", "knew", "programming", "java", "language", "c#", "flask", "python", "AWS", "d3"]
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
            for x in list1:
                if fuzz.token_sort_ratio(key.lower(),x.lower()) > 80:
                    li1 = False
                    print("career objective achieved!!!")
                    print(fuzz.token_sort_ratio(key.lower(),x.lower()))
                    print(key)
                    score += 20
                    print("score: ", score)
                    highlight.append(key)
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
                    highlight.append(key)
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
                    highlight.append(key)
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
                    highlight.append(key)
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
                    highlight.append(key)
                    result[5] = "References: included"
                    break
                else:
                    result[5] = "References: not included"

        #result[0] = "Total score: " + str(score)
        result[0] = score
        result.append(highlight)
    return result

def highlightText(textArr, f, color):
    f.seek(0)
    doc = fitz.Document(stream=bytearray(f.read()), filename = 'cv.pdf')
    if (len(textArr) > 0):
        for p in doc.pages():
            for text in textArr:
                text_instances = p.searchFor(text)
                for inst in text_instances:
                    highlight = p.addHighlightAnnot(inst)
                    highlight.setColors({"stroke":color, "fill":(1, 1, 1)})
                    highlight.update()

    memoryStream = doc.write()
    doc.close()
    return base64.b64encode(memoryStream).decode('ascii')

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')

if __name__ == '__main__':
    app.run()
