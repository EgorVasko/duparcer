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
import os


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
cardict = {}
looking_for_link = 'a href="https://dubai.dubizzle.com/motors/used-cars/'


#----------------------------------------------Functions ---------------------------------------------

#parce old
def parse():
    temp = open(tempfile, mode = 'w+', encoding ='utf-8')
    temp.truncate(0)
    for i in range(0,len(carslinks)):
        otvet = request.urlopen(carslinks[i])
        mytext1 = otvet.readlines()
        for num, line in enumerate(mytext1, 1):
            if 'a href="https://dubai.dubizzle.com/motors/used-cars/' in line.decode('utf-8') and 'vin-report' not in line.decode('utf-8'):
                line_link = str(line)
                line_link = (line_link[line_link.find('"') + 1 : ])
                line_link = (line_link[0: + line_link.find('?back')])
                temp.write(str(line_link) + "\n")
                z = 0
                for line in mytext1[num:]:
                    if "AED" in line.decode('utf-8') and z == 0:
                        line_price = str(line)
                        line_price = (line_price[line_price.find('AED') : line_price.find('AED') + 10])
                        z = 1
                if line_link.encode('utf-8') not in cardict.keys():
                    cardict[line_link] = line_price
    temp.close()


# ---------------------------------------------main--------------------------------------------------

car_list(cars,carslinks)
print('Program is running, please wait ~30 seconds')
parse()              # get all links
remove_weak()        # remove 116, 118, 320, etc..
rename()             # rename source
copy_new()           # write from temp1
copy_old()           # write from source
exit_procedures()    # closing files
exit_text()          # Print completion, timing
