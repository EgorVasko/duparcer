#!/usr/bin/env python3
import requests, lxml, re, time
from bs4 import BeautifulSoup as bs
import csv, json


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
# test = 'https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=9999000&year__gte=1990&year__lte=&kilometers__gte=&kilometers__lte=930000'
# cars = [test]

parsed = []
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


def open_json():
    try:
        with open("lxml_data.json", "r") as old_file:   #encoding='utf-8'
            dictold = json.load(old_file)
        with open("lxml_data_disc.json", "r") as disc_file:   #encoding='utf-8'
            dictred = json.load(disc_file)
    except:
        dictold = []
        dictred = []


def compare(list):
    for i in list:
        for x in dictred:
            if i['href'] == x['href']:
                if i['price'] < x['price']:
                    dict_disc_again.append(i)        # add to again discounted
                    continue
                if i['price'] >= x['price']:
                    dict_red_nochanges.append(i)
                    continue

    parsed1 = []
    for i in dict_disc_again:
        for x in parsed:
            if i != x:
                parsed1.append(x)
    list = []
    for i in dict_red_nochanges:
        for x in parsed1:
            if i != x:
                list.append(x)
    for i in list:
        for z in dictold:
            if i['href'] == z['href']:
                if i['price'] < z['price']:
                    dict_disc.append(i)
                    continue
                if i['price'] >= z['price']:
                    dict_nochanges.append(i)
                    continue
    parsed1 = []
    for i in dict_disc:
        for x in list:
            if i != x:
                parsed1.append(x)
    for i in dict_nochanges:
        for x in parsed1:
            if i != x:
                dict_new.append(x)


def dump_data():
    out_new = dict_nochanges + dict_new
    out_disc = dict_disc + dict_disc_again + dict_red_nochanges
    with open("lxml_data_disc.json", "w+") as write_disc_file:
        json.dump(out_disc, write_disc_file)
    with open("lxml_data.json", "w+") as write_file:
        json.dump(out_new, write_file)


def load_to_html():
    with open('output.html', 'w+') as out_file:
        if not dict_new:
            line = "<center><h2> No new cars " + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + "</center></h2>"
            out_file.write(line)
            for i in dict_new:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
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
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Old price is: " + oldprice + "<br />"
                out_file.write(line)

        if not dict_disc:
            line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

        if not dict_nochanges:
            line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            for i in dict_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

        if not dict_red_nochanges:
            line = ""
        else:
            for i in dict_red_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

# ================================== Execution

carlink(carslinks)

print("Program is running. Estimated completion time is ~30 seconds.\nPlease wait...")

start = time.time()
for i in cars:
    dubizzle_parse_lxml(i)
finish = time.time()
result = round(finish - start,2)

print('Parcing completed with lxml method:', result, "seconds\nTotal:" ,len(parsed),"cars parsed")

for i in parsed:
    print(i)
print(dictred)
print(dictold)

compare(parsed)       # comparing, sorting

print(dict_new)
print(dict_red_nochanges)
print(dict_disc_again)
print(dict_disc)
print(dict_nochanges)


dump_data()     # dumping to base
load_to_html()  # html


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

cli_output()
