from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import openpyxl, pandas, csv, shutil, time, smtplib, os, numpy, datetime

# Variables
chromedriver_location = "T://Project//Automation//chromedriver//chromedriver"
email = 'matthew.attiyeh@ci.rosemount.mn.us'
password = 'Workin4day12345'

# Call chromedriver and navigate to a page
driver = webdriver.Chrome(chromedriver_location)
#driver.get('https://cgweb07.cartegraphoms.com/RosemountMN/#ImportExport/?bid=92f7a263-7c75-4221-a3ad-a9673b9e4438&area=Administration')
driver.get('https://login.microsoftonline.com/ec21f265-968a-4738-b94c-72918b7a9664/saml2?SAMLRequest=fVLLTsMwEPyVyPfETeBArSRSH0JUKiVqC1K5IDfZpJaSdfDaUPh63BakcmiPuzs7OzN2SrJrezFydodLeHdANth3LZI4DjLmDAotSZFA2QEJW4rV6HEukmggeqOtLnXLzlaub0giMFZpZMFsmrE3hKb4rqbjxbauN5P9hgUvYMjPM%2BbhHkTkYIZkJVrfGiRJOLgJ43gd34l4KG6HrywoflWMFVYKm%2BsCticQiYf1ugiLp9WaBaM%2FURON5DowKzAfqoTn5TxjO2t7EpwbChtFUakiowk67dBGHUaOeK%2BNlS2nnTSemRsfIdfSB5rwQyCcVIMKWZ4eKnF0ZPKLdNGJLuXn6PT0SgtvZzYtdKvKr%2BBem07ay27jKD52VBXWR6hwSD2UqlZQedNtqz8nBqSFjFnjgPH8dPT%2Fb8h%2FAA%3D%3D&RelayState=WwzxxYn3zLhMbZsWYQR3WNbUmc5eRn_LTbvmxpDEdNJ3dNIJLTkL144IFR6B2hFOYjs4MobF_S4MzVFLiNxY2kzO0TIYkWhYS1PSXDFi4X9GNJDQ7gLGlBVBnOdtSChN9rSplxheyj49KSDpm-V-eUTHRiq3-P7mEfzlfYebk_iIzE_vJTvC7DOkFbQGIsDwokh_yTzKbU2PVA5pnlgPO3MVt_ZO2Mx4O-mbtQPt1LpvAjuqHjy4tusQrm3b9VmZrNb8GNlhbObco3t9WvHL5i_-ee0YkpHjL6zpLa65f6_vmUI2qeexd9b6nGHeAbydvAdzIupGOCVyMO8HufrMYq3PIdka7dT3DiH_U9UtKmTHzew9dlDk85NnkAFYUu1AMrLjvMRcWC9vBbjnBV-Na4QTwPq4GBdoijUS0m98MCHGn-jtio2NJu8k66WOmdc4AwBOpoC3qO4S_r2onj96V490cITfWH9RdkLuIBcjh106Zg79nZPnbe6RI8BPl64Y-ZwGz8vpdy5PntXbRe1He9mkn8IBoTpj0rzRu_e_Me7UEjVj4x8LsyL0828_w9ICkGk6ME1e7D6QLwxWqOxykCwzNUO-1XfILkH0wenvQLk2z6Hg2WSlA-3oYhvS3q12&sso_reload=true')
# Define the x paths from using inspect element in chrome and copy x path

typeEmailBox = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'
clickNext = 'idSIButton9'
emailPassword = 'i0118'
staySignedInButton = '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input'
importButtonCart = '/html/body/div[3]/div[3]/div/div[2]/div/div[1]'
CategoryCart = '/html/body/div[10]/div/div[3]/div[2]/div[1]/div[2]'
CategoryRequestsCart = '/html/body/div[10]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]'
CategoryLibrariesCart = '/html/body/div[10]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[5]'
LinkToRequestCSV = "T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv"
LinkToRequestorLogCSV = "T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestorLogCSV.csv"
FormatCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]'
#FormatRequestorCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]/div[2]/div[1]'
FormatRequestorCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]/div[2]/div[5]'
FormatSpatialCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]'
ImportButtonCart = '/html/body/div[10]/div/div[2]/div[2]'

#Use selenmium webdriver to automate cartegraph
driver.find_element_by_xpath(typeEmailBox).send_keys(email)
driver.find_element_by_id(clickNext).click()
driver.find_element_by_id(emailPassword).send_keys(password)
time.sleep(1)
driver.find_element_by_id(emailPassword).submit()
time.sleep(1)
driver.find_element_by_xpath(staySignedInButton).click()
time.sleep(1)
driver.find_element_by_xpath(importButtonCart).click()
time.sleep(.5)
driver.find_element_by_xpath(CategoryCart).click()
time.sleep(.5)
#driver.find_element_by_xpath(CategoryRequestsCart).click()
driver.find_element_by_xpath(CategoryLibrariesCart).click()
time.sleep(.5)
driver.find_element_by_xpath(FormatCart).click()
time.sleep(.5)
driver.find_element_by_xpath(FormatRequestorCart).click()
time.sleep(.5)
s = driver.find_element_by_xpath("//input[@type='file']") # this is how you upload a file
time.sleep(.5)
s.send_keys(LinkToRequestorLogCSV) #link to requestorcsv
time.sleep(.5)
driver.find_element_by_xpath(ImportButtonCart).click()
time.sleep(.5)
driver.find_element_by_xpath(importButtonCart).click()
time.sleep(.5)
driver.find_element_by_xpath(CategoryCart).click()
time.sleep(.5)
driver.find_element_by_xpath(CategoryRequestsCart).click()
time.sleep(.5)
driver.find_element_by_xpath(FormatCart).click()
time.sleep(.5)
driver.find_element_by_xpath(FormatSpatialCart).click()
time.sleep(.5)
s = driver.find_element_by_xpath("//input[@type='file']") # this is how you upload a file
time.sleep(.5)
s.send_keys(LinkToRequestCSV) #link to requestcsv
time.sleep(.5)
driver.find_element_by_xpath(ImportButtonCart).click()
time.sleep(.5)
