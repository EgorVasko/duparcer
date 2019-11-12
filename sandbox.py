import requests, lxml, re, time
from bs4 import BeautifulSoup as bs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Access
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('duparcer').sheet1
sheet.clear()
sheet.append_row(['Title','Link','Price','Year','Mileage'])

carslinks = []

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

jobs_lxml = []
jobs_html = []

def carlink():
    for i in cars:
        carslinks.append(i)

base_urll = "https://dubai.dubizzle.com/motors/used-cars/bmw/5-series/?price__gte=&price__lte=29000&year__gte=2005&year__lte=&kilometers__gte=&kilometers__lte=190000"


def dubizzle_parse(base_url):
    session = requests.Session()
    request = session.get(base_url)
    if request.status_code == 200:
        soup = bs(request.content, "html.parser" )
        divs = soup.find_all('div', attrs={"id" : "featured-listing-item"})
        divs += soup.find_all('div', attrs={"class" : "cf item paid-featured-item featured-motors"})
        divs += soup.find_all('div', attrs={"class" : "cf item"})
        for div in divs:
            title = div.find('a').text
            title = title.strip()
            href = div.find('a')['href']
            href = (href[0: + href.find('?back')])
            price = div.find('div', attrs={"class" : "price"}).text
            price = price.strip()
            price = re.sub(r'\D', '', price)
            try:
                features = div.find("ul", attrs={"class" : "features"}).text
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6 : 11]
                mileage = features[mileage_index + 25 : 32]
                mileage = re.sub(r'\D', '', mileage)
            except:
                features = div.find("ul", attrs={"class" : "featured_listing_features"}).text
                features = features.strip()
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6 : 10]
                mileage = features[mileage_index + 25 : 32]
                mileage = re.sub(r'\D', '', mileage)
            jobs_html.append({
                'title' : title,
                'href' : href,
                'price' : price,
                'year' : year,
                'mileage' : mileage
            })

    else:
        print("error")

#============

def dubizzle_parse_lxml(base_url):
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url)
    if request.status_code == 200:
        soup = bs(request.content, "lxml" )
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
        divs = soup.find_all('div', attrs={"id" : "featured-listing-item"})
        divs += soup.find_all('div', attrs={"class" : "cf item paid-featured-item featured-motors"})
        divs += soup.find_all('div', attrs={"class" : "cf item"})
        for div in divs:
            title = div.find('a').text
            title = title.strip()
            href = div.find('a')['href']
            href = (href[0: + href.find('?back')])
            price = div.find('div', attrs={"class" : "price"}).text
            price = price.strip()
            price = re.sub(r'\D', '', price)
            try:
                features = div.find("ul", attrs={"class" : "features"}).text
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6 : 11]
                mileage = features[mileage_index + 25 : 32]
                mileage = re.sub(r'\D', '', mileage)
            except:
                features = div.find("ul", attrs={"class" : "featured_listing_features"}).text
                features = features.strip()
                year_index = features.find('Year:')
                mileage_index = features.find('Mileage:')
                year = features[year_index + 6 : 10]
                mileage = features[mileage_index + 25 : 32]
                mileage = re.sub(r'\D', '', mileage)
            jobs_lxml.append({
                'title' : title,
                'href' : href,
                'price' : price,
                'year' : year,
                'mileage' : mileage
            })
    else:
        print("error")

#============================

carlin = carlink()
'''
start = time.time()
for i in cars:
    #print(i)
    dubizzle_parse(i)
finish = time.time()
result = finish - start
print('html.parser',result)
'''

start = time.time()
for i in cars:
    dubizzle_parse_lxml(i)
finish = time.time()
result = finish - start
print('lxml',result)
print(len(jobs_lxml))
print(jobs_lxml)

for i in jobs_lxml:
#    print(title,href,price,year,mileage)
    sheet.append_row([i['title'],i['href'],i['price'],i['year'],i['mileage']])
