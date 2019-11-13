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

dictold = {}
dictred ={}
dict_new = {}
dict_nochanges = {}
dict_disc_again = {}
dict_disc = {}
dict_red_nochanges = {}

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
        with open("data.json", "r",encoding='utf-8') as old_file:
            dictold = json.load(old_file)
        with open("data_disc.json", "r", encoding='utf-8') as disc_file:
            dictred = json.load(disc_file)
    except:
        dictold = {}
        dictred = {}

# dictold - parsed before
# dictred - price was reduced before
# dictnow = parsed = new parsed cars

for i in parsed:
    for x in dictred:
        if i['href'] == x['href']:
            if i['price'] < x['price']:
                dict_disc_again.append(i)        # add to again discounted
                continue
            if i['price'] >= x['price']:
                dict_red_nochanges.append(i)
                continue
    for z in dictold:
        if i['price'] < z['price']:
            dict_disc.append(i)
            continue
        if i['price'] >= z['price']:
            dict_nochanges.append(i)


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

# ================================== Execution

carlink(carslinks)

print("Program is running. Estimated completion time is ~30 seconds.\nPlease wait...")

start = time.time()
for i in cars:
    dubizzle_parse_lxml(i)
finish = time.time()
result = round(finish - start,2)

print('Parcing completed with lxml method:', result, "seconds\nTotal:" ,len(parsed),"cars parsed")

#for i in parsed:
#    print(i['title'], i['href'], i['price'], i['year'], i['mileage'])
#    sheet.append_row([i['title'], i['href'], i['price'], i['year'], i['mileage']])
