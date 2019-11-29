#!/usr/bin/env python3

# link can be changed from dubai to uae
# Check price reduced
# redo output to table`
# sort output by date

import keyboard
import sys
import requests
from bs4 import BeautifulSoup as bs
import json
import getpass
import platform
import os
import datetime
import re
import time
#import lxml
from urllib.parse import urlsplit

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
z3 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/z3/?price__gte=&price__lte=29000&year__gte=1998&year__lte=&kilometers__gte=&kilometers__lte=190000'
z4 = 'https://dubai.dubizzle.com/motors/used-cars/bmw/z4/?price__gte=&price__lte=26000&year__gte=1998&year__lte=&kilometers__gte=&kilometers__lte=190000'
e = 'https://dubai.dubizzle.com/motors/used-cars/mercedes-benz/e-class/?price__gte=&price__lte=25000&year__gte=2004&year__lte=&kilometers__gte=&kilometers__lte=170000'
cars = [infi, x3, bmw3, bmw1, a4, a5, a6, is1, is2, is3, z350, bmw5, clk, z3, z4, e]

# test = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=9999000&year__gte=1990&year__lte=&kilometers__gte=&kilometers__lte=930000'
# cars = [test]

parsed = []
parsed1 = []
carslinks = []
dictold = []
dictred = []

dict_new = []

dict_nochanges = []
dict_red_nochanges = []

dict_disc = []
dict_disc_again = []

dicttosort = [dict_new, dict_nochanges, dict_disc, dict_disc_again, dict_red_nochanges]



# =============================== functions


def carlink(list_of_cars):  # links to list
    for car in cars:
        list_of_cars.append(car)


def dubizzle_parse_lxml(base_url):  # main parse
    urls = [base_url]  # urls = []    urls.append(base_url)
    session = requests.Session()
    for i in urls:
        request = session.get(i)
        if request.status_code == 200:
            soup = bs(request.content, "lxml")
            try:
                pagination = soup.find_all('a', attrs={"class" : "page-links"} )
                last_page = int(pagination[-1].text)
                print("last page number is: " + str(last_page))
                for i in range(1,last_page):
                    url = str(base_url) + "&page=" + str(i+1)
                    if url not in urls:
                        urls.append(url)
            except:
                pass
            divs = soup.find_all('div', attrs={"id": "featured-listing-item"})
            divs += soup.find_all('div', attrs={"class": "cf item paid-featured-item featured-motors"})
            divs += soup.find_all('div', attrs={"class": "cf item"})
            for div in divs:
                title = div.find('a').text
                title = title.strip()
                # issues with title:    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
                #                       UnicodeEncodeError: 'charmap' codec can't encode characters in position 126-130: character maps to <undefined>
                # trying do encode
                # title = title.encode('utf-8')
                # end of try
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
                # add code from sandbox here
                parse_result = urlsplit(href)
                query_s = parse_result.path
                car_data = query_s.split("/")
                car_data = car_data[3:9]
                brand = str(car_data[0]).capitalize()
                model = str(car_data[1]).capitalize()
                # ad_posted = str(car_data[2]) + "-" + str(car_data[3]) + "-" + str(car_data[4])
                if len(str(car_data[3])) == 1:
                    month = "0" + str(car_data[3])
                else:
                    month = str(car_data[3])
                if len(str(car_data[4])) == 1:
                    date = "0" + str(car_data[4])
                else:
                    date = str(car_data[4])
                ad_posted = str(car_data[2]) + "-" + month + "-" + date
                title_test = str(car_data[5]).replace("-", " ")
                # end of sandbox
                '''if {
                        'title': title,
                        'href': href,
                        'price': price,
                        'year': year,
                        'mileage': mileage,
                        'brand': brand,
                        'model': model,
                        'ad_posted': ad_posted,
                        'title_test': title_test
                    } not in parsed:'''
                parsed.append({
                    'title': title,
                    'href': href,
                    'price': price,
                    'year': year,
                    'mileage': mileage,
                    'brand': brand,
                    'model': model,
                    'ad_posted': ad_posted,
                    'title_test': title_test
                })
        else:
            print("error")

def dump_data():
    out_new = dict_nochanges + dict_new
    out_disc = dict_disc + dict_disc_again + dict_red_nochanges
    if dictold != out_new:
        with open("lxml_data.json", "w+") as write_file:
            json.dump(out_new, write_file)
    if dictred != out_disc:
        with open("lxml_data_disc.json", "w+") as write_disc_file:
            json.dump(out_disc, write_disc_file)


def OSIS():  # define path to Desktop folder
    if platform.system() == "Windows":
        return ("C:\\Users\\" + getpass.getuser() + "\Desktop\\")  # try os.path.expanduser('~')
    elif platform.system() == "Linux":
        return (os.path.expanduser('~') + "/Desktop/")
    else:
        return ('')


def load_to_html():
    counter = 1
    with open(path + 'output_lxml.html', 'w+') as out_file:
        if not dict_new:
            line = "<center><h2> No new cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
            for i in dict_new:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        if not dict_disc_again:
            line = ""
        else:
            line = "<center><h2>  Price reduced AGAIN! </center></h2>"
            out_file.write(line)
            for i in dict_disc_again:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " Old price is: " + i['oldprice'] + " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + \
                       ' <b>Link is :</b> <a href="' + i['href'] + '">' + i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        if not dict_disc:
            line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " Old price is: " + i['oldprice'] + " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + \
                       ' <b>Link is :</b> <a href="' + i['href'] + '">' + i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        if not dict_nochanges:
            line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            for i in dict_nochanges:
                """
                line = 'Link is : <a href="' + i['href'] + '">' + i['title_test'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + \
                       i['price'] + " Year is: " + i['year'] + " Mileage is: " + i['mileage'] + \
                       " Model is: " + i['brand'] + " " + i['model'] + " Ad posted: " + i['ad_posted'] +"<br />"
                """
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        if not dict_red_nochanges:
            line = ""
        else:
            for i in dict_red_nochanges:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1

def cli_output():
    for i in dict_new:
        print("NEW                  Key = " + i['href'] + "    Price =     " + i['price'])

    for i in dict_disc_again:
        print("PRICE REDUCED AGAIN! Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i[
            'price'])

    for i in dict_disc:
        print("PRICE REDUCED!       Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i[
            'price'])

    for i in dict_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])

    for i in dict_red_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])


def exitmessage():
    if (len(dict_new)) > 0:
        print(len(dict_new), "New cars found")
    else:
        print("No new cars")


# ================================== Execution


carlink(carslinks)  # compiling list of links

print("Program is running. Estimated completion time is ~30 seconds.\nPlease wait...")

# =========================== open database
try:
    with open("lxml_data.json", "r") as old_file:  # encoding='utf-8'
        dictold = json.load(old_file)
    print("Old results are avaliable: " + str(len(dictold)) + " cars")
except:
    print("No old results")
    dictold = []

try:
    with open("lxml_data_disc.json", "r") as disc_file:  # encoding='utf-8'
        dictred = json.load(disc_file)
    print("Old discounted results are avaliable..." + str(len(dictred)) + " cars")
except:
    dictred = []
    print("No old discounted results")

# ==============================================================    parsing started
start = time.time()
for i in cars:
    dubizzle_parse_lxml(i)
finish = time.time()
result = round(finish - start, 2)

print('Parcing completed with lxml method:', result, "seconds\nTotal:", len(parsed), "cars parsed")

path = OSIS()
# =========================================== comparison with old data


for i in range(len(parsed),0,-1):
    for z in range(len(dictred),0,-1):
        if parsed[i-1].get('href') == dictred[z-1].get('href'):
            if parsed[i-1].get('price') < dictred[z-1].get('price'):
                parsed[i-1]['oldprice'] = dictred[z-1].get('price')  # adding old price
                dict_disc_again.append(parsed[i-1])
                parsed.pop(i-1)
                dictred.pop(z-1)
                break
            if parsed[i-1].get('price') >= dictred[z-1].get('price'):
                dict_red_nochanges.append(parsed[i-1])
                parsed.pop(i-1)
                dictred.pop(z-1)
                break

# ===============================================================
for i in range(len(parsed),0,-1):
    for z in range(len(dictold),0,-1):
        if parsed[i-1].get('href') == dictold[z-1].get('href'):
            if parsed[i-1].get('price') < dictold[z-1].get('price'):
                parsed[i-1]['oldprice'] = dictold[z-1].get('price')
                dict_disc.append(parsed[i-1])
                parsed.pop(i-1)
                dictold.pop(z-1)
                break
            if parsed[i-1].get('price') >= dictold[z-1].get('price'):
                dict_nochanges.append(parsed[i-1])
                parsed.pop(i-1)
                dictold.pop(z-1)
                break

dict_new = parsed

# =========================


exitmessage()


# ============================== sorting by date


def sort_by_parametr(list_to_sort, parametr):
    for x in range(len(list_to_sort) - 1, 0, -1):
        for i in range(x):
            if list_to_sort[i].get(parametr) < list_to_sort[i + 1].get(parametr):
                list_to_sort[i], list_to_sort[i + 1] = list_to_sort[i + 1], list_to_sort[i]


sort = 'ad_posted'


# ============================== sorting by date

dump_data()  # dumping to base

for i in dicttosort:
    sort_by_parametr(i,sort)

load_to_html()  # html

# cli_output()
#print("Press ESC key to exit")
#keyboard.wait('esc','space')
