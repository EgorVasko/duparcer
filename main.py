#!/usr/bin/env python
# ############################
# My first parser
# v0.01
# to do:    - json to def
#           - check price changes
#           - optimize remove weak
# ############################

from urllib import request
from parcerfunc import *
import os
import json
import re
import time
import datetime
t1 = time.time()
today = datetime.datetime.today()
time_of_parse = today.strftime("%Y-%m-%d %H:%M:%S")

# ------------------------------------ Variables --------------------------------------
looking_for_link = 'a href="https://dubai.dubizzle.com/motors/used-cars/'
carslinks = []
dict_new_raw = {}
dictnow = {}
infi = 'https://dubai.dubizzle.com/motors/used-cars/infiniti/gseries/?price__gte=&price__lte=25000&year__gte=2009&year__lte=&kilometers__gte=&kilometers__lte=230000'
x3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/x3/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/3-series/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw1 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/1-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a4 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a4/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a5 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a5/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a6 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a5/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is1 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-c/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is2 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-f/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is3 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
z350 = 'https://dubai.dubizzle.com/motors/used-cars/nissan/350z/?price__gte=&price__lte=29000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw5 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=25000&year__gte=2004&year__lte=&kilometers__gte=&kilometers__lte=230000'
clk = 'https://dubai.dubizzle.com/motors/used-cars/mercedes-benz/clk-class/?price__gte=&price__lte=29000&year__gte=2005&year__lte=&kilometers__gte=&kilometers__lte=190000'
cars = [infi, x3, bmw3, bmw1, a4, a5, a6, is1, is2, is3, z350, bmw5, clk]
#cars = [bmw3]#test cars for faster parcing

dictold = {}
dictred ={}
dict_new = {}
dict_nochanges = {}
dict_disc_again = {}
dict_disc = {}
dict_red_nochanges = {}

#----------------------------------------------Functions ---------------------------------------------


def parse():
    linkfound = []
    for i in range(0,len(carslinks)):
        otvet = request.urlopen(carslinks[i])
        mytext1 = otvet.readlines()
        for num, line in enumerate(mytext1, 1):
            if 'a href="https://dubai.dubizzle.com/motors/used-cars/' in line.decode('utf-8') and 'vin-report' not in line.decode('utf-8'):
                line_link = str(line)
                line_link = (line_link[line_link.find('"') + 1 : ])
                line_link = (line_link[0: + line_link.find('?back')])
                if line_link not in linkfound:
                    linkfound.append(line_link)
                    z = 0
                    for line in mytext1[num:]:
                        if "AED" in line.decode('utf-8') and z == 0:
                            line_price = str(line)
#                            line_price = (line_price[line_price.find('AED') : line_price.find('AED') + 10])
                            line_price = (line_price[line_price.find('AED') + 3 : line_price.find('AED') + 10])
                            line_price = re.sub(r'\D', '', line_price)
                            z = 1
                    if line_link.encode('utf-8') not in dict_new_raw.keys():
                        dict_new_raw[line_link] = line_price


def remove_weak_dict():
    for i in dict_new_raw:
        if "116" in str(i) or "118" in str(i) or "120" in str(i) or "316" in str(i) or "320" in str(i) or "323" in str(i) or "325" in str(i) or "250" in str(i):
            continue
        else:
            dictnow[i] = dict_new_raw[i]


#def open_json():
try:
    with open("data.json", "r",encoding='utf-8') as old_file:
        dictold = json.load(old_file)
    with open("data_disc.json", "r", encoding='utf-8') as disc_file:
        dictred = json.load(disc_file)
except:
    dictold = {}
    dictred = {}


def compare():
    for i in dictnow:
        if i in dictred:
            if dictnow[i] < dictred[i]:
                dict_disc_again[i] = dictnow[i]
                continue
            if dictnow[i] >= dictred[i]:
                dict_red_nochanges[i] = dictnow[i]
                continue
        if i in dictold:
            if dictnow[i] < dictold[i]:
                dict_disc[i] = dictnow[i]
                continue
            if dictnow[i] >= dictold[i]:
                dict_nochanges[i] = dictnow[i]
                continue
        else:
            dict_new[i] = dictnow[i]


def dump_data():
    out_new = {**dict_nochanges,**dict_new}
    out_disc = {**dict_disc, **dict_disc_again, **dict_red_nochanges}
    with open("data_disc.json", "w+") as write_disc_file:
        json.dump(out_disc, write_disc_file)
    with open("data.json", "w+") as write_file:
        json.dump(out_new, write_file)


def load_to_html():
    with open(path + 'output.html', 'w+') as out_file:
        if not dict_new:
            line = "<center><h2> No new cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
            for i in dict_new:
                line = 'Link is : <a href="' + str(i) + '">' + i + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + str(dict_new[i]) + "<br />"
                out_file.write(line)

        if not dict_disc_again:
            line = ""
        else:
            line = "<center><h2>  Price reduced AGAIN! </center></h2>"
            out_file.write(line)
            for i in dict_disc_again:
                line = 'Link is : <a href="' + i + '">' + i + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + str(dictnow[i]) + "&nbsp;&nbsp;&nbsp;&nbsp;Old price is: " + str(dictred[i]) + "<br />"
                out_file.write(line)

        if not dict_disc:
            line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = 'Link is : <a href="' + i + '">' + i + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + str(dict_disc[i]) + "<br />"
                out_file.write(line)

        if not dict_nochanges:
            line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            for i in dict_nochanges:
                line = 'Link is : <a href="' + i + '">' + i + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + dict_nochanges[i] + "<br />"
                out_file.write(line)

        if not dict_red_nochanges:
            line = ""
        else:
            for i in dict_red_nochanges:
                line = 'Link is : <a href="' + i + '">' + i + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + dict_red_nochanges[i] + "<br />"
                out_file.write(line)


def cli_output():
    for i in dict_new:
        print("NEW                  Key = " + str(i) + "    Price =     " + str(dictnow[i]))

    for i in dict_disc_again:
        print("PRICE REDUCED AGAIN! Key = " + str(i) + "    New price = " + str(dictnow[i]) + "    Old price is = " + str(dictred[i]))

    for i in dict_disc:
        print("PRICE REDUCED!       Key = " + str(i) + "    New price = " + str(dictnow[i]) + "    Old price is = " + str(dictold[i]))

    for i in dict_nochanges:
        print("OLD                  Key = " + str(i) + "    Value =     " + str(dictnow[i]))

    for i in dict_red_nochanges:
        print("OLD                  Key = " + str(i) + "    Value =     " + str(dictnow[i]))


# ---------------------------------------------main--------------------------------------------------

car_list(cars,carslinks)
print('Program is running, please wait ~30 seconds')
parse()                     # get all links
exit_text()
remove_weak_dict()          # remove 116, 118, 320, etc..
#open_json()                # load data from files
compare()                   # compare dictionaries
dump_data()                 # upload to files
#cli_output()               # output in command line
load_to_html()
exit_text()                 # Print completion, timing
