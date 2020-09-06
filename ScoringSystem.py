import ListScore

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
    return (section_Scored(ListScore.list1_score, ListScore.list2_score) + ListScore.scored_list[0] + ListScore.scored_list[1])/4*100