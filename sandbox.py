#!/usr/bin/env python3.6

'''
import urllib.request
import requests
import time

user_agent = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
pa = ["https://dubai.dubizzle.com", "https://fujairah.dubizzle.com","https://www.tut.by","http://vidno.by","https://hh.ru","https://www.google.com"]

# ================================= 2
start = time.time()
for i in pa:
    if urllib.request.urlopen(i).getcode() == 200:
        print(i,"Checked & avaliable")
        continue
    else:
        print(i,"Not avaliable")
finish = time.time()
result = round(finish - start, 2)
print("done in: ", result)

# ================================= 1
start = time.time()
for i in pa:
    session = requests.Session()
    response = requests.get(i, headers=user_agent, timeout=5)
    if response.status_code == 200:
        print(i,"Checked & avaliable")
        continue
    else:
        print(i,"Not avaliable",response.status_code)
finish = time.time()
result = round(finish - start, 2)
print("done in: ", result)

# ================================= 3
start = time.time()
for i in pa:
    session = requests.head(i, headers=user_agent)
    #response = requests.session(i, headers=user_agent, timeout=5)
    if session.status_code == 200:
        print(i,"Checked & avaliable")
        continue
    else:
        print(i,"Not avaliable",session.status_code)
finish = time.time()
result = round(finish - start, 2)
print("done in: ", result)
'''

import requests
import time
import asyncio
from aiohttp import ClientSession

pa = ["https://dubai.dubizzle.com", "https://fujairah.dubizzle.com","https://www.tut.by","http://vidno.by","https://hh.ru","https://www.google.com"]

def hello(href):
    return requests.get(href)

start = time.time()

#for i in pa:
#    print(i,hello(i))

finish = time.time()
result = round(finish - start, 2)
print("done in: ", result)


start = time.time()


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)

loop = asyncio.get_event_loop()

for i in pa:
    loop.run_until_complete(hello(i))

finish = time.time()
result = round(finish - start, 2)
print("done in: ", result)
