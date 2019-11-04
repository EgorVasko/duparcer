#!/usr/bin/env python
import time
import datetime
import os
import getpass
import platform

t1 = time.time()
today = datetime.datetime.today()
time_of_parse = today.strftime("%Y-%m-%d %H:%M:%S")


def car_list(x,y):
    for car in x:
        y.append(car)


def OSIS(): # define path to Desktop folder
    if platform.system() == "Windows":
        return("C:\\Users\\" + getpass.getuser() + "\Desktop\\") # try os.path.expanduser('~')
    elif platform.system() == "Linux":
        return(os.path.expanduser('~') + "/Desktop/")
    else:
        return('')


path = OSIS()


def rename():
    if os.path.exists(path + "output.txt"):
        old_file = os.path.join(path, "output.txt")
    else:
        x = open(path + "output.txt", "w", encoding=('utf-8'))
        x.close()
        old_file = os.path.join(path, "output.txt")
    new_file = os.path.join("", "output.old")
    os.rename(old_file, new_file)


def copy_new():

    with open('temp1.txt','r') as in_file, open(path + 'output.txt', 'w+') as out_file, open('output.old','r') as check_file:
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
    with open('output.old','r') as in_file, open(path + 'output.txt', 'r+') as out_file:
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


def timer():
    print(f'Execution time: {round(time.time()-t1,3)} seconds.')


def exit_text():
    print(f'Completed\nExecution time: {round(time.time()-t1,3)} seconds.')
