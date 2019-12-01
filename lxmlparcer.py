#!/usr/bin/env python3

# link can be changed from dubai to uae
# Check price reduced
# redo output to table`

# import keyboard
# import sys
import requests
from bs4 import BeautifulSoup as bs
import json
import getpass
import platform
import os
import datetime
import re
import time
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
'''dictold = []
dictred = []
dictsold = []'''
dict_new = []

dict_nochanges = []
dict_red_nochanges = []

dict_disc = []
dict_disc_again = []

dicttosort = [dict_new, dict_nochanges, dict_disc, dict_disc_again, dict_red_nochanges]
sort = 'ad_posted'


# =============================== functions


def openbase(file, text):
    dict_var = []
    try:
        with open(file, "r") as old_file:  # encoding='utf-8'
            dict_var = json.load(old_file)
        print(text + " results are available: " + str(len(dict_var)) + " cars")
        return dict_var
    except FileNotFoundError:
        print("No " + text + " results")
        return dict_var


def scraping(base_url):  # main parse
    urls = [base_url]  # urls = []    urls.append(base_url)
    session = requests.Session()
    for link in urls:
        request = session.get(link)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')  # lxml
            try:
                pagination = soup.find_all('a', attrs={"class": "page-links"})
                last_page = int(pagination[-1].text)
                # print("last page number is: " + str(last_page))
                for page in range(1, last_page):
                    url = str(base_url) + "&page=" + str(page + 1)
                    if url not in urls:
                        urls.append(url)
            except IndexError:
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
                except AttributeError:
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
            continue


def osis():  # define path to Desktop folder
    if platform.system() == "Windows":
        return "C:\\Users\\" + getpass.getuser() + '\Desktop\\'  # try os.path.expanduser('~')
    elif platform.system() == "Linux":
        return os.path.expanduser('~') + "/Desktop/"
    else:
        return ''


def combine(main, dict0, dict1, dict2):
    for i in range(len(main), 0, -1):
        for z in range(len(dict0), 0, -1):
            if main[i - 1].get('href') == dict0[z - 1].get('href'):
                if main[i - 1].get('price') < dict0[z - 1].get('price'):
                    main[i - 1]['oldprice'] = dict0[z - 1].get('price')  # adding old price
                    dict1.append(main[i - 1])
                    main.pop(i - 1)
                    dict0.pop(z - 1)
                    break
                if main[i - 1].get('price') >= dict0[z - 1].get('price'):
                    dict2.append(main[i - 1])
                    main.pop(i - 1)
                    dict0.pop(z - 1)
                    break


def dump_data():
    out_new = dict_nochanges + dict_new
    out_disc = dict_disc + dict_disc_again + dict_red_nochanges
    out_sold = dictold + dictred + dictsold
    if dictold != out_new:
        with open("lxml_data.json", "w+") as write_file:
            json.dump(out_new, write_file)
    if dictred != out_disc:
        with open("lxml_data_disc.json", "w+") as write_disc_file:
            json.dump(out_disc, write_disc_file)
    # test of sold
    if dictsold != out_sold:
        with open("lxml_data_sold.json", "w+") as write_old_file:
            json.dump(out_sold, write_old_file)
    # test of sold


def sort_by_parametr(list_to_sort, parametr):
    for x in range(len(list_to_sort) - 1, 0, -1):
        for y in range(x):
            if list_to_sort[y].get(parametr) < list_to_sort[y + 1].get(parametr):
                list_to_sort[y], list_to_sort[y + 1] = list_to_sort[y + 1], list_to_sort[y]


def load_to_html():
    counter = 1
    with open('output_lxml.html', 'w+') as out_file:  # (path + 'output_lxml.html', 'w+')
        line = """  <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="data/styles.css">
                <title>Dubizzle scraper by 2rbo</title>
                </head>
                <body>
                    """
        out_file.write(line)

        if not dict_new:
            line = "<center><h2> No new cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + time_of_parse + "</center></h2>"
            out_file.write(line)
            # ==========================table test
            line = """
            <center><table style="width:80%">
      <tr>
    <th>#</th>
    <th>Posted</th>
    <th>Model</th>
    <th>Price</th>
    <th>Year</th>
    <th>Mileage</th>
    <th>Link</th>
      </tr>
      </table></center>
            """
            out_file.write(line)
            # =============== table test
            for i in dict_new:
                line = """
                <tr>
                  <td width="5%"><center>""" + str(counter) + """</center></td>
                  <center><td width="10%">""" + i['ad_posted'] + """</td></center>
                  <center><td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td></center>
                  <center><td width="10%">""" + i['price'] + """</td></center>
                  <center><td width="7%">""" + i['year'] + """</td></center>
                  <center><td width="10%">""" + i['mileage'] + """</td></center>
                  </center><td class="textfield" width="38%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td></center>
                  </tr>

                """
                out_file.write(line)
                """
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                """
                counter += 1
            line = """
                      </table></center>
                        """
            out_file.write(line)
        if not dict_disc_again:
            pass  # line = ""
        else:
            line = "<center><h2>  Price reduced AGAIN! </center></h2>"
            out_file.write(line)
            for i in dict_disc_again:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + \
                       i[
                           'model'] + " <b>Price is:</b> " + i['price'] + \
                       " Old price is: " + i['oldprice'] + " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + \
                       ' <b>Link is :</b> <a href="' + i['href'] + '">' + i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        if not dict_disc:
            pass  # line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + \
                       i[
                           'model'] + " <b>Price is:</b> " + i['price'] + \
                       " Old price is: " + i['oldprice'] + " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + \
                       ' <b>Link is :</b> <a href="' + i['href'] + '">' + i['title_test'] + '</a>' + "<br />"
                out_file.write(line)
                counter += 1
        # ======================================================== dict_nochanges
        if not dict_nochanges:
            pass  # line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            # ==========================table test
            line = """
            <center><table style="width:80%">
      <tr>
    <th>#</th>
    <th>Posted</th>
    <th>Model</th>
    <th>Price</th>
    <th>Year</th>
    <th>Mileage</th>
    <th>Link</th>
      </tr>
            """
            out_file.write(line)
            # =============== table test
            for i in dict_nochanges:
                '''line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                    " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                    i['title_test'] + '</a>' + "<br />"'''
                line = """
                <tr>
                  <td width="5%">""" + str(counter) + """</td>
                  <td width="10%">""" + i['ad_posted'] + """</td>
                  <td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td>
                  <td width="10%">""" + i['price'] + """</td>
                  <td width="7%">""" + i['year'] + """</td>
                  <td width="10%">""" + i['mileage'] + """</td>
                  <td class="textfield" width="38%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                  </tr>

                """
                out_file.write(line)
                counter += 1
        line = """
              </table></center>
                """
        out_file.write(line)
        # ========================================================= dict_red_nochanges
        if not dict_red_nochanges:
            pass  # line = ""
        else:
            line = """
            <center><table style="width:80%">
      <tr>
    <th>#</th>
    <th>Posted</th>
    <th>Model</th>
    <th>Price</th>
    <th>Year</th>
    <th>Mileage</th>
    <th>Link</th>
      </tr>
            """
            out_file.write(line)
            for i in dict_red_nochanges:
                '''line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"'''

                line = """
                <tr>
                  <td width="5%">""" + str(counter) + """</td>
                  <td width="10%">""" + i['ad_posted'] + """</td>
                  <td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td>
                  <td width="10%">""" + i['price'] + """</td>
                  <td width="7%">""" + i['year'] + """</td>
                  <td width="10%">""" + i['mileage'] + """</td>
                  <td class="textfield" width="38%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                  </tr>

                """

                out_file.write(line)
                counter += 1
                line = """
                    </table></center>
                    """
        out_file.write(line)
        # ============================================================ dict sold
        out_sold = dictold + dictred + dictsold
        if not out_sold:
            # line = ""
            pass  # instead of line = ""
        else:
            line = "<center><h2>  Sold Cars </center></h2>"
            out_file.write(line)

            line = """
            <center><table style="width:80%">
      <tr>
    <th>#</th>
    <th>Posted</th>
    <th>Model</th>
    <th>Price</th>
    <th>Year</th>
    <th>Mileage</th>
    <th>Link</th>
      </tr>
            """
            out_file.write(line)

            for i in out_sold:
                '''
                line = str(counter) + " <b>Ad posted:</b> " + i['ad_posted'] + " <b>Model is:</b> " + i['brand'] + " " + i[
                    'model'] + " <b>Price is:</b> " + i['price'] + \
                       " <b>Year is:</b> " + i['year'] + " <b>Mileage is:</b> " + i[
                           'mileage'] + ' <b>Link is :</b> <a href="' + i['href'] + '">' + \
                       i['title_test'] + '</a>' + "<br />"'''
                line = """
                <tr>
                  <td width="5%">""" + str(counter) + """</td>
                  <td width="10%">""" + i['ad_posted'] + """</td>
                  <td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td>
                  <td width="10%">""" + i['price'] + """</td>
                  <td width="7%">""" + i['year'] + """</td>
                  <td width="10%">""" + i['mileage'] + """</td>
                  <td class="textfield" width="38%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                  </tr>

                """
                out_file.write(line)
                counter += 1
        # test of sold
        line = """ </body>
                    </html>"""
        out_file.write(line)


def exitmessage():
    if (len(dict_new)) > 0:
        print(len(dict_new), "New cars found")
    else:
        print("No new cars")


# ================================== Execution
print("Program is running. Estimated completion time is ~30 seconds.\nPlease wait...")

dictold = openbase("lxml_data.json", "Old")
dictred = openbase("lxml_data_disc.json", "Old discounted")
dictsold = openbase("lxml_data_sold.json", "Sold")

# ==============================================================    parsing started
start = time.time()
for car in cars:
    scraping(car)
finish = time.time()
result = round(finish - start, 2)

print('Scraping completed with lxml method:', result, "seconds\nTotal:", len(parsed), "cars parsed")

path = osis()
# =========================================== comparison with old data


'''for i in range(len(parsed), 0, -1):
    for z in range(len(dictred), 0, -1):
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

for i in range(len(parsed), 0, -1):
    for z in range(len(dictold), 0, -1):
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
                break'''
# new def combine


combine(parsed, dictred, dict_disc_again, dict_red_nochanges)
combine(parsed, dictold, dict_disc, dict_nochanges)
# new def combine

dict_new = parsed

exitmessage()

dump_data()

for dict_ in dicttosort:
    sort_by_parametr(dict_, sort)

load_to_html()

# print("Press ESC key to exit")
# keyboard.wait('esc','space')
