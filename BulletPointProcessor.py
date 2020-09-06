import re
import ListScore

# itemgetter
from operator import itemgetter

# Count bullet points
def bulletPointCounter(text):
    bulletPointRegex = '•\s(.+?)((?=(•))|(?=($)))'

    bulletPointList = re.findall(
        bulletPointRegex, text, re.IGNORECASE | re.MULTILINE)
    bulletPointCount = len(bulletPointList)

    processed = "Your CV has " + \
        str(bulletPointCount) + " total bullet points."

    processed = "Your CV has " + str(bulletPointCount) + " total bullet points."

    #scoring system
    if bulletPointCount >= 0:
        ListScore.list2_score[5] = False
    else:
        ListScore.list2_score[5] = True

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