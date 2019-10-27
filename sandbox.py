#!/usr/bin/env python
import pypyodbc

#try:
connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=local;'
                              'Database=TestDB;'
                              'uid=SA;'
                              'pwd=1qaz@WSX;')
#except:

