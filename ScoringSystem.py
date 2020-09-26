import ListScore

#calculate the total score of each section, it can calculate more than 1 section if needed
def section_Scored(list1, list2):
    total = scored = 0
    for index, score in enumerate(list1):
        total += int(score)
        if not list2[index]:
            scored += int(score)
    return (scored/total)

#calculate the total score of brevity and impact (by spliting the lists)
def section_Scored_split(list1, list2):
    half = len(list1)//2
    impact_list1 = list1[:half]
    impact_list2 = list2[:half]
    brevity_list1 = list1[half:]
    brevity_list2 = list2[half:]
    ListScore.scored_list[2] = float("{:.2f}".format(section_Scored(impact_list1,impact_list2)*100))
    ListScore.scored_list[3] = float("{:.2f}".format(section_Scored(brevity_list1,brevity_list2)*100)) 

#calculate the final overall scored in percentage (+ 4 sections and devided by 4)
def final_overall_scored():
    print(section_Scored(ListScore.list1_score,ListScore.list2_score)*100, "%")
    print(ListScore.scored_list)
    return (ListScore.scored_list[0] + ListScore.scored_list[1] + ListScore.scored_list[2] + ListScore.scored_list[3])/4