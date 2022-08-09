import requests, json, datetime, time, smtplib, arcpy
import pandas as pd
import openpyxl, os

# Disable warnings
requests.packages.urllib3.disable_warnings()

# Generate AGOL token
print('Generating Token')
tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
params = {'f': 'pjson', 'username': 'MatthewAttiyeh', 'password': 'Workin2day12345', 'referer': 'http://www.arcgis.com'}
r = requests.post(tokenURL, data=params, verify=False)
response = json.loads(r.content)
token = response['token']
print("Token:\n")
print(token)

