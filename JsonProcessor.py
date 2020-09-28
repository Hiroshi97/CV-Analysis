import json
import os

#this function will extract all the data from the json file and put all the keys (dictionary) into an array.
#Return an array
def jsonfile_reader(jsonFile):
    emptyList = []
    script_dir = os.path.dirname(__file__)
    fileName = 'static\keywords\\' + jsonFile
    file_path = os.path.join(script_dir, fileName)
    print(file_path)
    with open(file_path) as f:
        data = json.load(f)

    for key in data.keys():
        emptyList.append(key)
    print(emptyList)
    return emptyList

#this function will also extract all the data from the json file
#It will return each of the value of the dict 
#Return a bunch of arrays
def jsonfile_reader_Advance(jsonFile):
    emptyList = []
    script_dir = os.path.dirname(__file__)
    fileName = 'static\keywords\\' + jsonFile
    file_path = os.path.join(script_dir, fileName)
    with open(file_path) as f:
        data = json.load(f)
        
    for key in data.keys():
        emptyList.append(key)
    
    print(emptyList)
    print(len(emptyList))
    if len(emptyList) == 6: 
        return data[emptyList[0]],data[emptyList[1]],data[emptyList[2]],data[emptyList[3]],data[emptyList[4]],data[emptyList[5]]
    else :
        return data[emptyList[0]],data[emptyList[1]],data[emptyList[2]],data[emptyList[3]],data[emptyList[4]]








