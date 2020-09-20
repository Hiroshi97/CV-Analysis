# fuzzywuzzy lib
from fuzzywuzzy import fuzz

#Scoring system
from ScoringSystem import section_Scored, final_overall_scored

import ListScore

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
            li4, score, result[4] = word_match(
                key, list4, li4, score, "Skill")
            if li4 is False:
                highlight.append(key)

        if li5:
            li5, score, result[5] = word_match(
                key, list5, li5, score, "References")
            if li5 is False:
                highlight.append(key)

    ListScore.scored_list[0] = float("{:.2f}".format(section_Scored([4, 4, 4, 4, 4], [li1, li2, li3, li4, li5])*100))
    result[0] = (ListScore.scored_list[0])
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

    ListScore.scored_list[1] = float("{:.2f}".format(section_Scored([4, 4, 4], [li1, li2, li3])*100))

    result[0] = (ListScore.scored_list[1])
    print("list score1:",ListScore.list1_score)
    print("list score2:",ListScore.list2_score)
    print("scored_list:",ListScore.scored_list)
    return result