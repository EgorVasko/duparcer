#!/usr/bin/env python
import time
import datetime
import os


t1 = time.time()
today = datetime.datetime.today()
time_of_parse = today.strftime("%Y-%m-%d %H:%M:%S")

tempfile = "temp.txt"
temp1file = "temp1.txt"
temp = open(tempfile, mode = 'w+', encoding ='utf-8')
temp.truncate(0)


def car_list(x,y):
    for car in x:
        y.append(car)


def remove_weak():
    outputf = "temp1.txt"
    out_f = open(outputf, mode = 'w+', encoding='utf-8')
    with open('temp.txt','r+') as in_file, out_f:
        for line in in_file:
            if 'g35' in line: continue
            if '116' in line: continue
            if '118' in line: continue
            if '120' in line: continue
            if '316' in line: continue
            if '318' in line: continue
            if '320' in line: continue
            if '323' in line: continue
            if '325' in line: continue
            if '250' in line: continue
            if '520' in line: continue
            if '523' in line: continue
            if '525' in line: continue
            if '430' in line: continue
            out_f.write(line)
    out_f.close()


def exit_procedures():
    temp.close()
    os.remove(tempfile)
    os.remove(temp1file)
    old_old = os.path.join("", "output.old")
    os.remove(old_old)


def exit_text():
    print(f'Completed\nExecution time: {round(time.time()-t1,3)} seconds.')
