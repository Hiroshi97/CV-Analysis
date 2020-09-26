from datetime import datetime
import re

class DateSorter():
    
    def datefindersorter(self, text):
        result = "Your dates are in the correct order on your CV."  # score up?
        badresult = "Your dates are not in the correct yearly order. Employers like to see the most recent work and study experience first."  # score down?
        monthresult = "Your dates are not in the correct monthly order. Employers like to see the most recent work and study experience first."  # score down?

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
        regex11 = r'[\d]{1,2}/[\d]{1,2}/[\d]{4}'  # dd/mm/yyyy or d/m/yyyy
        regex12 = r'[\d]{1,2}-[\d]{1,2}-[\d]{2}'  # dd-mm-yyyy or d-m-yyyy
        #regex13 = r'\s[\d]{2}\s'
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
                return [dates1[i:i+x] for i in range(0, len(dates1), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%B %Y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates2:

            def split_list(x):
                return [dates2[i:i+x] for i in range(0, len(dates2), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%b %y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates3:

            def split_list(x):
                return [dates3[i:i+x] for i in range(0, len(dates3), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%b %Y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            num_list = list(map(lambda sub: int(
                ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
            second_num_list = list(map(lambda sub: int(
                ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%b %y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates5:
            def split_list(x):
                return [dates5[i:i+x] for i in range(0, len(dates5), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%B %Y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates6:

            def split_list(x):
                return [dates6[i:i+x] for i in range(0, len(dates6), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%B %y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates7:

            def split_list(x):
                return [dates7[i:i+x] for i in range(0, len(dates7), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%B %y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates8:
            def split_list(x):
                return [dates8[i:i+x] for i in range(0, len(dates8), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()
            both_months3 = both_months.copy()
            try:

                both_months_sorted = both_months2.sort(
                    key=lambda date: datetime.strptime(date, '%B %Y'))  # this format changes

            except:
                both_months_sorted2 = both_months3.sort(
                    key=lambda date: datetime.strptime(date, '%b %Y'))

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            elif (both_months == both_months3):
                flag = 0
            elif (both_months != both_months3):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates9:

            def split_list(x):
                return [dates9[i:i+x] for i in range(0, len(dates9), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%b %Y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates10:

            def split_list(x):
                return [dates10[i:i+x] for i in range(0, len(dates10), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%b %y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates11:

            def split_list(x):
                return [dates11[i:i+x] for i in range(0, len(dates11), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%x'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates12:

            def split_list(x):
                return [dates12[i:i+x] for i in range(0, len(dates12), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%d-%m-%Y '))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult

        if dates14:

            def split_list(x):
                return [dates14[i:i+x] for i in range(0, len(dates14), x)]

            try:
                
                splitted_list = split_list(2)
                num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[0]))
                second_num_list = list(map(lambda sub: int(
                    ''.join([ele for ele in sub if ele.isnumeric()])), splitted_list[1]))
            except IndexError as e:
                return "Your dates could not be found."

            month_list = splitted_list[0][1]
            second_month_list = splitted_list[1][0]
            both_months = []
            both_months.append(month_list)
            both_months.append(second_month_list)
            flag = 0

            both_months2 = both_months.copy()

            both_months_sorted = both_months2.sort(
                key=lambda date: datetime.strptime(date, '%Y'))  # this format changes

            if (both_months == both_months2):
                flag = 0
            elif (both_months != both_months2):
                flag = 1

            if (num_list[1] > second_num_list[0]):
                return result
            elif (num_list[1] == second_num_list[0]) & (flag == 0):
                return monthresult
            elif (num_list[1] == second_num_list[0]) & (flag == 1):
                return result
            else:
                return badresult
