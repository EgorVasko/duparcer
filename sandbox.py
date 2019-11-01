#!/usr/bin/env python

'''

import pypyodbcconnection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-GGL05MB\SQLEXPRESS;'
                              'Database=master;'
                              'uid=Maria;'
                              'pwd=;')

cursor = connection.cursor()
'''

import getpass
import platform


def OSIS(): # define path to Desktop folder
    if platform.system() == "Windows":
        print("windows")
    elif platform.system() == "Linux":
        print("\home\\" + getpass.getuser() + "\Desktop")
    else:
        print('xz')

OSIS()

