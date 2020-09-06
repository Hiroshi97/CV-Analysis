from spellchecker import SpellChecker
# Regular Expressionn
import re

import ListScore

# Spellchecker
def spellchecker(text):
    sc = SpellChecker()
    sc.word_frequency.load_dictionary('static/test_dict.json')
    shortenedWords = []

    # Spellchecking
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

    # scoring system
    if cleanList:
        ListScore.list2_score[6] = False
    else:
        ListScore.list2_score[6] = True

    return [output, cleanList]


def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)


