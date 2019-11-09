#!/usr/bin/env python
# https://www.youtube.com/watch?v=vISRn5qFrkM
# Storing data in google sheets its easy

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Access
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('duparcer').sheet1
sheet2 = client.open('duparcer').sheet2

pp = pprint.PrettyPrinter()
result = sheet.row_values(2)  #get_all_records()

pp.pprint(result)

sheet.update_cell(6,11, 'python access')
result1 = sheet.cell(6,11)

pp.pprint(result1)

sheet2.update_cell(1,1, 'new')
