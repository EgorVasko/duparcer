#!/usr/bin/env python

'''

import pypyodbcconnection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-GGL05MB\SQLEXPRESS;'
                              'Database=master;'
                              'uid=Maria;'
                              'pwd=;')

cursor = connection.cursor()
'''

import os
import platform
import getpass

def OSIS(): # define path to Desktop folder
    if platform.system() == "Windows":
        return("C:\\Users\\" + getpass.getuser() + "\Desktop\\")
    elif platform.system() == "Linux":
        return(os.path.expanduser('~') + "/Desktop/")
    else:
        return('')

z = os.path.expanduser('~')
print(OSIS())
