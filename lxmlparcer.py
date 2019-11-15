#!/usr/bin/env python3
import requests, lxml, re, time
from bs4 import BeautifulSoup as bs
import json
import getpass
import platform
import os
import datetime

today = datetime.datetime.today()
time_of_parse = today.strftime("%Y-%m-%d %H:%M:%S")

infi = 'https://dubai.dubizzle.com/motors/used-cars/infiniti/gseries/?price__gte=&price__lte=25000&year__gte=2009&year__lte=&kilometers__gte=&kilometers__lte=230000'
x3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/x3/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/3-series/?price__gte=&price__lte=25000&year__gte=2007&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw1 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/1-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a4 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a4/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a5 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a5/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
a6 = 'https://dubai.dubizzle.com/motors/used-cars/audi/a6/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is1 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-c/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is2 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-f/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
is3 = 'https://dubai.dubizzle.com/motors/used-cars/lexus/is-series/?price__gte=&price__lte=25000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
z350 = 'https://dubai.dubizzle.com/motors/used-cars/nissan/350z/?price__gte=&price__lte=29000&year__gte=2006&year__lte=&kilometers__gte=&kilometers__lte=230000'
bmw5 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=25000&year__gte=2004&year__lte=&kilometers__gte=&kilometers__lte=230000'
clk = 'https://dubai.dubizzle.com/motors/used-cars/mercedes-benz/clk-class/?price__gte=&price__lte=29000&year__gte=2005&year__lte=&kilometers__gte=&kilometers__lte=190000'
cars = [infi, x3, bmw3, bmw1, a4, a5, a6, is1, is2, is3, z350, bmw5, clk]
#test = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=9999000&year__gte=1990&year__lte=&kilometers__gte=&kilometers__lte=930000'
#cars = [test]

parsed = []
parsed1 = []
carslinks = []
dictold = []
dictred =[]
dict_new = []
dict_nochanges = []
dict_disc_again = []
dict_disc = []
dict_red_nochanges = []

# =============================== functions


def carlink(list_of_cars):  # links to list
    for i in cars:
        list_of_cars.append(i)


def dubizzle_parse_lxml(base_url):  # main parse
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url)
    if request.status_code == 200:
        soup = bs(request.content, "lxml")
        '''
        try: # not working
            pagination = soup.find_all('a', attrs={"class" : "page-links"} )
            last_page = int(pagination[-1].text)
            print("last page number is: " + last_page)
            for i in range(last_page):
                url = str(base_url) + "&page=" + str(i)
                if url not in urls:
                    urls.append(url)
                print(url)
        except:
            pass'''
        divs = soup.find_all('div', attrs={"id": "featured-listing-item"})
        divs += soup.find_all('div', attrs={"class": "cf item paid-featured-item featured-motors"})
        divs += soup.find_all('div', attrs={"class": "cf item"})
        for div in divs:
            title = div.find('a').text
            title = title.strip()
            href = div.find('a')['href']
            href = (href[0: + href.find('?back')])
            price = div.find('div', attrs={"class": "price"}).text
            price = price.strip()
            price = re.sub(r'\D', '', price)
            try:
                features = div.find("ul", attrs={"class": "features"}).text
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6: 11]
                mileage = features[mileage_index + 25: 32]
                mileage = re.sub(r'\D', '', mileage)
            except:
                features = div.find("ul", attrs={"class": "featured_listing_features"}).text
                features = features.strip()
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6: 10]
                mileage = features[mileage_index + 25: 32]
                mileage = re.sub(r'\D', '', mileage)
            parsed.append({
                'title': title,
                'href': href,
                'price': price,
                'year': year,
                'mileage': mileage
            })
    else:
        print("error")






def dump_data():
    out_new = dict_nochanges + dict_new
    out_disc = dict_disc + dict_disc_again + dict_red_nochanges
    with open("lxml_data_disc.json", "w+") as write_disc_file:
        json.dump(out_disc, write_disc_file)
    with open("lxml_data.json", "w+") as write_file:
        json.dump(out_new, write_file)


def OSIS(): # define path to Desktop folder
    if platform.system() == "Windows":
        return("C:\\Users\\" + getpass.getuser() + "\Desktop\\") # try os.path.expanduser('~')
    elif platform.system() == "Linux":
        return(os.path.expanduser('~') + "/Desktop/")
    else:
        return('')


def load_to_html():
    with open(path + 'output_lxml.html', 'w+') as out_file:
        if not dict_new:
            line = "<center><h2> No new cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
            for i in dict_new:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " +\
                       i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Year is: " + i['year'] + " Mileage is: " + i['mileage'] + "<br />"
                out_file.write(line)

        if not dict_disc_again:
            line = ""
        else:
            line = "<center><h2>  Price reduced AGAIN! </center></h2>"
            out_file.write(line)
            for i in dict_disc_again:
                for x in dictred:
                    if i['href'] == x['href']:
                        oldprice = x['price']
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + \
                       i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Year is: " + i['year'] + " Mileage is: " + i['mileage'] + \
                       "&nbsp;&nbsp;&nbsp;&nbsp;Old price is: " + dict_disc_again[i].get('price') + "<br />"
                out_file.write(line)

        if not dict_disc:
            line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + \
                       i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Year is: " + i['year'] + " Mileage is: " + i['mileage'] + "<br />"
                out_file.write(line)

        if not dict_nochanges:
            line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            for i in dict_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + \
                       i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Year is: " + i['year'] + " Mileage is: " + i['mileage'] + "<br />"
                out_file.write(line)

        if not dict_red_nochanges:
            line = ""
        else:
            for i in dict_red_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + \
                       i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Year is: " + i['year'] + " Mileage is: " + i['mileage'] + "<br />"
                out_file.write(line)


def cli_output():
    for i in dict_new:
        print("NEW                  Key = " + i['href'] + "    Price =     " + i['price'])

    for i in dict_disc_again:
        print("PRICE REDUCED AGAIN! Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i['price'])

    for i in dict_disc:
        print("PRICE REDUCED!       Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i['price'])

    for i in dict_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])

    for i in dict_red_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])

# ================================== Execution


carlink(carslinks)  # compiling list of links


print("Program is running. Estimated completion time is ~30 seconds.\nPlease wait...")

# =========================== open database
try:
    with open("lxml_data.json", "r") as old_file:   #encoding='utf-8'
        dictold = json.load(old_file)
    with open("lxml_data_disc.json", "r") as disc_file:   #encoding='utf-8'
        dictred = json.load(disc_file)
    print("Old results are avaliable...")
except:
    dictold = []
    dictred = []
# ==============================================================    parsing started
start = time.time()
for i in cars:
    dubizzle_parse_lxml(i)
finish = time.time()
result = round(finish - start,2)

print('Parcing completed with lxml method:', result, "seconds\nTotal:" ,len(parsed),"cars parsed")

path = OSIS()
# =========================================== comparison with old data

indextoremove = []
parsed1 = parsed.copy()

for i in range(0, len(parsed)):
    for z in range (len(dictred)):
        if parsed[i].get('href') == dictred[z].get('href'):
            if parsed[i].get('price') < dictred[z].get('price'):
                indextoremove.append(i)
                dict_disc_again.append(parsed[i])
                continue
            if parsed[i].get('price') >= dictred[z].get('price'):
                dict_red_nochanges.append(parsed[i])
                indextoremove.append(i)
                continue

"""
print(dict_disc_again, dict_red_nochanges)
print('=============from reduced')
print(parsed1, indextoremove)
"""

indextoremove.reverse()
for i in indextoremove:
    parsed1.pop(i)
indextoremove.clear()
"""
print(parsed1)
print(indextoremove,"remove")
"""
#===============================================================
for i in range(0,len(parsed1)):
    for z in range(len(dictold)):
        if parsed1[i].get('href') == dictold[z].get('href'):
            if parsed1[i].get('price') < dictold[z].get('price'):
                indextoremove.append(i)
                dict_disc.append(parsed[i])
                continue
            if parsed1[i].get('price') >= dictold[z].get('price'):
                dict_nochanges.append(parsed[i])
                indextoremove.append(i)
                continue
"""
print(dict_disc, dict_nochanges)
print('============= now from old')
print(parsed1, indextoremove)
"""
indextoremove.reverse()

for i in indextoremove:
    parsed1.pop(i)

indextoremove.clear()
dict_new = parsed1


#=========================

if (len(dict_new)) > 0:
    print(len(dict_new),"New cars found")
else:
    print("No new cars")

dump_data()     # dumping to base
load_to_html()  # html

#cli_output()
