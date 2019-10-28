import os
from urllib import request

tempfile = "temp.txt"
temp1file = "temp1.txt"
temp = open(tempfile, mode = 'w+', encoding ='utf-8')
temp.truncate(0)
cardict = {}
'''
if 'c' not in d.keys():
    d['c'] = 300
json.dump(di, open("text.txt",'w'))
# load from file to new variable with dict type
dy = json.load(open("text.txt"))
'''

toparce = open("toparce", mode='r', encoding='utf-8')
mytext1 = toparce.readlines()
text_to_find = 'a href="https://dubai.dubizzle.com/motors/used-cars/'
price = "AED"
for num, line in enumerate(mytext1, 1):
    if text_to_find in line and 'vin-report' not in line:
        line_link = str(line)
        line_link = (line_link[line_link.find('"') + 1 : ])
        line_link = (line_link[0: + line_link.find('?back')])
        z = 0
        for line in mytext1[num:]:
            if price in line and z == 0:
                line_price = str(line)
                line_price = (line_price[line_price.find('AED') : line_price.find('AED') + 10])
                z = 1

        temp.write(str(line_link) + ' price is: ' + str(line_price))
        if line_link not in cardict.keys():
            cardict[line_link] = line_price

temp.truncate(0)

for i in cardict:
    temp.write("Link is: " + str(i) + " Price is: " + str(cardict[i]))

for i in cardict:
    print("Link is: " + str(i) + " Price is: " + str(cardict[i]))

temp.close()
os.remove(tempfile)
