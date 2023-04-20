#turned out JSON files are handy, but when they are over 1,000,000 lines can be slow to load
#this is to convert the Vernal Express data to a TAB delimited  file to import into a sql database.
#also found there was a repeated line from the previous conversion. This handled that.

import json

file = open("vernalexpress.json")
data = json.load(file)
f = open("content.csv", mode ="w")
count = 0

for i in data['editions']:
    c = ''
    d = 0
    for j in i['content']:
        if d < len(i['content'])-2:
            c += j +' | '
        elif d == len(i['content'])-2: 
            c += j
        d += 1
    f.writelines(i['edition'] + '\t' + i['name'] + '\t' + i['page'] + '\t' + i['column'] + '\t' + c + '\n')
    count += 1
    print(count)
