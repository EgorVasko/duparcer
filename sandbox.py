#!/usr/bin/env python
import pypyodbc
'''
connection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-GGL05MB\SQLEXPRESS;'
                              'Database=master;'
                              'uid=Maria;'
                              'pwd=;')

cursor = connection.cursor()
'''

import platform

if platform.system() == "Windows":
    print("Your system is Windows")
elif platform.system() == "Linux":
    print("Your system is Linux")
else:
    print('xz')
