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
import os

def OSIS(): # define path to Desktop folder
    if platform.system() == "Windows":
        print("C:\\" + getpass.getuser() + "\Desktop\\")
    elif platform.system() == "Linux":
        print("\home\\" + getpass.getuser() + "\Desktop")
    else:
        print('xz')

OSIS()

