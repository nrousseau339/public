#took data from .nfo file used by Folio Views and converted to JSON.


import re
#function to reverse file from Folio View database so the file could more easily be parsed. 
def rev_text():
    f = open("reverse1.txt", mode ="w")
    for line in reversed(list(open("fulldata.txt"))):
        f.writelines(line.rstrip() + '\n')

#function to generate a json file based on content
def gen_json():
    #regex
    edition = r"\d{2}_\w+_\d{4}"
    page = r"page_\w+\s"
    column = r"column_\w+$"
    content = r"^\t.+"
    name = r"^.+"
    #variables
    prevline = ""
    f = open("jsonprep.txt", mode="w")
    f.writelines('{\n\t"editions": [\n')
    for line in open("reverse.txt"):
        if re.match(edition, line):
            f.writelines('\t{\n\t\t"edition": "' + re.findall(edition, line)[0].strip() + '",\n')
            f.writelines('\t\t"page": "' + re.findall(page, line)[0].strip() + '",\n')
            f.writelines('\t\t"column": "' + re.findall(column, line)[0].strip() + '",\n\t\t"content": [')
        elif re.match(content, line):
            f.writelines('\n\t\t\t\t"' + re.sub('"', '\\\"', re.findall(content,line)[0].strip()) + '",')
        elif re.match(content, prevline) and re.match(name, line):
            f.writelines('\n\t\t ],\n\t\t"name": "' + re.sub('"', '\\\"', re.findall(name,line)[0].strip()) + '"\n\t},\n')
            
        prevline = line    
    f.writelines('\t]\n}')
    f.close



#remove commas before ]s, because the json function created an extra comma at the end.
def rm_comma():
    prevline = ''
    bad_comma = r"\t{4}.+\"\,$"
    bracket = r"\t{2}.+\]\,$"
    f = open("vernalexpress.json", mode="w")
    for line in open("jsonprep.txt"):
        if re.match(bad_comma, prevline) and re.match(bracket, line):
            f.writelines(re.sub(",$", "",prevline))
            f.writelines(line)
            #print(re.sub(",$", "",prevline))
            #print(line)
        else:
            f.writelines(line)
            # print(line)
        prevline = line






gen_json()
rm_comma()
