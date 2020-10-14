import nltk
from nltk.tokenize import PunktSentenceTokenizer
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

import re

import ListScore

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
        " instances of first-person usages such as 'I', 'Me' and much more."

    nounverb = "There were " + str(countNoun) + " nouns in your CV. It contains " + str(
        countActionVerb) + " action verbs."

    #scoring system
    if countFirstPerson > 5:
        ListScore.list2_score[0] = True
    else:

        ListScore.list2_score[0] = False

    if countActionVerb > 5 and countNoun > 5:
        ListScore.list2_score[1] = True
    else:
        ListScore.list2_score[1] = False

    return [processed, nounverb]
