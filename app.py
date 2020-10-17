import string

###External functions
#TextProcessor
from TextProcessor import filterHiddenText, extractTextFromPDF, highlightText
#Date finder sorter
from DateSorter import DateSorter
#Spellchecker
from Spellchecker import spellchecker
#Word processing
from WordProcessor import word_filter, word_frequency, word_metric
#Bullet point processing
from BulletPointProcessor import quantifyBulletPoints, bulletPointCounter
#First Personal Sentiment
from FirstPersonalSentiment import firstPersonSentiment
#Word matching
from WordMatching import word_matching, word_matching_Softskill
#Scoring system
from ScoringSystem import section_Scored_split, final_overall_scored

# from matplotlib.figure import Figure

# Flask initialization
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

#base64
import base64

app = Flask(__name__)
#sslify = SSLify(app)

#CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#global variable for scoring system
import ListScore

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/api/result', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        f = request.files['cvfile']

        # TODO: testing getting input
        user = request.form['user_type']
        print(user)

        #Dropdown menu selection
        t = request.form['job_type']
        print(t)

        #PDF Preview
        pdfstring = base64.b64encode(f.read())
        pdfstring = pdfstring.decode('ascii')

        f.seek(0)
        filename = "File name: " + f.filename
        filesize = "File size: " + str(int(len(f.read())/1024)) + "kb"
        text = extractTextFromPDF(f)
        
        # Filter invisible text
        if user == "admin":
            invisible_text = filterHiddenText(f)
            invisible_textlist = []

            for txt in range(len(invisible_text[0])):
                invisible_textlist.append(invisible_text[0][txt]['text'])
            
            invisible_output = "There are " + str(len(invisible_textlist)) + " invisible sentences."
            print(invisible_textlist)
        elif user == "applicant":
            invisible_textlist = False

        #scoring system
        if int(len(f.read())/1024) > 20000:
            ListScore.list2_score[2] = True
        else:
            ListScore.list2_score[2] = False 

        #Word count metrics
        word_count_num = len(text.split())
        word_count_result = word_metric(word_count_num)

        #scoring system
        if word_count_num > 2000:
            ListScore.list2_score[7] = True
        else:
            ListScore.list2_score[7] = False 

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
        essential_section = word_matching(word_frequency(text),t)
        word_count = "Word Count: " + str(word_count_num)

        #Four factors
        if invisible_textlist:
            impact = [0, invisible_output, filename, filesize, word_count, fps[0], fps[1]]
        else:
            impact = [0, filename, filesize, word_count, fps[0], fps[1]]

        brevity = [0, spellcheck[0], bpCounter[2],
                   word_count_result, bpQuantify]
        style = [essential_section[0], essential_section[1],
                 essential_section[2], essential_section[3], essential_section[4], essential_section[5], datesorter.datefindersorter(text)]

        soft_skills = word_matching_Softskill(word_frequency(text))
        length = [len(impact), len(brevity), len(style), len(soft_skills)]
        section_Scored_split(ListScore.list1_score,ListScore.list2_score)
        impact[0] = ListScore.scored_list[2]
        brevity[0] = ListScore.scored_list[3]
        final_overall_scored()
        #Highlighted files
        pdfstrings = []
        if invisible_textlist:
            pdfstrings.append(highlightText(invisible_textlist, f, (0, 1, 0)))
        else:
            pdfstrings.append(pdfstring)
        pdfstrings.append(highlightText(spellcheck[1], f, (1, 0, 0)))
        pdfstrings.append(highlightText(essential_section[6], f, (0, 1, 0)))
        pdfstrings.append(pdfstring)

        return render_template("result.html", impact=impact, brevity=brevity, style=style, soft_skills=soft_skills, pdfstrings=pdfstrings, length=length)
    return redirect(url_for('index'))

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')


if __name__ == '__main__':
    app.run()
