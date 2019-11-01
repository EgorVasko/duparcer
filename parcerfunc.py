#!/usr/bin/env python
import time
import datetime
import os

tempfile = "temp.txt"
temp1file = "temp1.txt"
t1 = time.time()
today = datetime.datetime.today()
time_of_parse = today.strftime("%Y-%m-%d %H:%M:%S")

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


def rename():
    if os.path.exists("../../Desktop/output.txt"):
        old_file = os.path.join("../../Desktop/", "output.txt")
    else:
        x = open("../../Desktop/output.txt", "w", encoding=('utf-8'))
        x.close()
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


def exit_procedures():
    os.remove(tempfile)
    os.remove(temp1file)
    old_old = os.path.join("", "output.old")
    os.remove(old_old)


def exit_text():
    print(f'Completed\nExecution time: {round(time.time()-t1,3)} seconds.')
