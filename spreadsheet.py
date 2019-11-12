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
sheet.clear()

sheet.append_row(['title','link','price','year','mileage'])

print('completed')
