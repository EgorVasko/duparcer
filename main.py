#!/usr/bin/env python
# ############################
# My first parser
# v0.01
# to do:
#           - check price changes
#
# ##########################

from urllib import request
from parcerfunc import *

# ------------------------------------ Variables --------------------------------------

infi = 'https://dubai.dubizzle.com/motors/used-cars/infiniti/gseries/?price__gte=&price__lte=25000&year__gte=2009&year__lte=&kilometers__gte=&kilometers__lte=230000'
x3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/x3/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/3-series/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw1 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/1-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a4 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a4/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a5 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a5/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is1 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-c/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is2 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-f/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is3 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
z350 = 'https://dubai.dubizzle.com/motors/used-cars/nissan/350z/?price__gte=&price__lte=29000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw5 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=25000&year__gte=2004&year__lte=&kilometers__gte=&kilometers__lte=230000'
cars = [infi, x3, bmw3, bmw1, a4, a5, is1, is2, is3, z350, bmw5]
carslinks = []



#----------------------------------------------Functions ---------------------------------------------


def parse():
    for car in cars:
        carslinks.append(car)
    print('Program is running, please wait ~30 seconds')
    for i in range(0,len(carslinks)):
        otvet = request.urlopen(carslinks[i])
        mytext1 = otvet.readlines()
        for num, line in enumerate(mytext1, 1):
            if 'a href="https://dubai.dubizzle.com/motors/used-cars/'.encode('utf-8') in line and ('vin-report'.encode('utf-8')) not in line:
                line = str(line)
                line = (line[line.find('"') + 1 : ])
                line = (line[0: + line.find('?back')])
                temp.write(str(line) + "\n")
    temp.close()


def rename():
    old_file = os.path.join("../../Desktop/", "output.txt")
    new_file = os.path.join("", "output.old")
    os.rename(old_file, new_file)


def copy_new():

    with open('temp1.txt','r') as in_file, open('../../Desktop/output.txt', 'w+') as out_file, open('output.old','r') as check_file:
        seen = set()
        out_file.write('================================== new cars ' + time_of_parse + ' ==================================\n')
        for line in check_file:
            seen.add(line)
        for line in in_file:
            if line in seen: continue # skip duplicate
            if '====' in line: continue
            seen.add(line)
            out_file.write(line)


def copy_old():
    with open('output.old','r') as in_file, open('../../Desktop/output.txt', 'r+') as out_file:
        seen = set()
        out_file.write('============================================ old cars ============================================\n')
        for line in out_file:
            seen.add(line)
        for line in in_file:
            if line in seen: continue # skip duplicate
            if '====' in line: continue
            seen.add(line)
            out_file.write(line)


# ---------------------------------------------main--------------------------------------------------


parse() # get all links
remove_weak() # remove 116, 118, 320, etc..
rename() #rename source
copy_new() # write from temp1
copy_old() # write from source
exit_procedures() # closing files
exit_text() # Print completion, timing
