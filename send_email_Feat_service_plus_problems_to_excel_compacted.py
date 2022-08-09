import requests, json, datetime, time, smtplib, arcpy
import pandas as pd
import openpyxl, os
from datetime import timedelta
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select



# Disable warnings
requests.packages.urllib3.disable_warnings()

#Global Variables
hoursValue = 1
URL = 'https://services2.arcgis.com/g9tzqCz1E9uQq6Yy/arcgis/rest/services/CitizenProblems_5d28d4bd046a44919399e732970690ac/FeatureServer/0'
arcpy.env.workspace = "https://services2.arcgis.com/g9tzqCz1E9uQq6Yy/arcgis/rest/services/CitizenProblems_5d28d4bd046a44919399e732970690ac/FeatureServer"
username = 'matthew.attiyeh@ci.rosemount.mn.us'                                                                                   # AGOL Username
password = 'Workin2day12345' 
dateField = 'CreationDate'
arcpy.env.overwriteOutput = True

# Generate AGOL token
try:
        print('Generating Token')
        tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
        params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'http://www.arcgis.com'}
        r = requests.post(tokenURL, data=params, verify=False)
        response = json.loads(r.content)
        token = response['token']
        print(r)
except:
        token = ''

# Return largest ObjectID
whereClause = '1=1'
params = {'where': whereClause, 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
r = requests.post(URL + '/query', data = params, verify = False)
response = json.loads(r.content)
try:
    response['objectIds'].sort()
except Exception as e:
    print("Error: {0}".format(e))

count = len(response['objectIds'])

#######Process Data#######

def send_email_feat_service():
    fromEmail = 'GISHelpdesk@ci.rosemount.mn.us'        # Email sender

    # Function to send email
    def sendEmailCodeEnforcement(ToEmail):
        SUBJECT = 'Problem Reported'
        TEXT = "A new problem was reported. \n\nSubmitter name: {6} \n\nCategory:{5} \n\nType of Problem: {0} \n\nThis problem has a status of: {1} \n\nProblem details: {2} \n\nLocation: {3} \n\nPlese go to the link below to view in the app: \n\nhttps://cirosemountmn.maps.arcgis.com/apps/webappviewer/index.html?id=c875b18f4aaa424789576484dc18b4cd".format(typeProb, status, details, location, numvotes, category, pocfullname, phone)
        smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
        msg = MIMEText(TEXT)
        msg['Subject'] = SUBJECT
        msg['From'] = fromEmail
        msg['To'] = ToEmail
        smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
        #print("Successfully sent email to pwadmn")
        smtpObj.quit()
    def sendEmailOther(ToEmail):
        SUBJECT = 'Problem Reported'
        TEXT = "A new problem was reported. \n\nSubmitter name: {6} \n\nSubmitter Phone: {7} \n\nCategory: {5} \n\nType of Problem: {0} \n\nThis problem has a status of: {1} \n\nProblem details: {2} \n\nLocation: {3}  \n\nPlese go to the link below to view in the app: \n\nhttps://cirosemountmn.maps.arcgis.com/apps/webappviewer/index.html?id=1aceaef1910046ebbf8d50692505d2f1".format(typeProb, status, details, location, numvotes, category, pocfullname, phone)
        smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
        msg = MIMEText(TEXT)
        msg['Subject'] = SUBJECT
        msg['From'] = fromEmail
        msg['To'] = ToEmail
        smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
        #print("Successfully sent email Rick")
        smtpObj.quit()
    def sendEmailSubmitter(ToEmail):
        SUBJECT = 'Problem Report Received'
        TEXT = "Thank you for you submission to the City of Rosemount's Report an Issue tool. We are currently reviewing your issue ({0}) and we will take the appropriate steps to remedy it. If we have any further questions we will contact you at this email address or the phone number you provided. \n\nPlease do not respond to this email as it is not monitored. If you have any further questions please contact the city directly. \n\nThank you for your patience and have a great day!".format(typeProb, status, details, location, numvotes, category)
        smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
        msg = MIMEText(TEXT)
        msg['Subject'] = SUBJECT
        msg['From'] = fromEmail
        msg['To'] = ToEmail
        smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
        #print("Successfully sent email to submitter")
        smtpObj.quit()
        
    # Query service and check if CreationDate time is within the last hour
    if count < 1000:
        params = {'f': 'pjson', 'where': "1=1", 'outFields' : '*', 'returnGeometry' : 'false', 'token' : token}
        r = requests.post(URL + '/query', data=params, verify=False)
        response = json.loads(r.content)
        for feat in response['features']:
            typeProb = feat['attributes']['probtype']
            status = feat['attributes']['status']
            details = feat['attributes']['details']
            location = feat['attributes']['locdesc']
            numvotes = feat['attributes']['numvotes']
            category = feat['attributes']['category']
            pocfullname = feat['attributes']['pocfullname']
            submitterEmail = feat['attributes']['pocemail']
            phone = feat['attributes']['pocphone']
            createDate = feat['attributes'][dateField]
            createDate = int(str(createDate)[0:-3])
            t = datetime.datetime.now() - timedelta(hours=hoursValue) #to change it to a different time change the hoursValue variable to something else above(eg .5 for half hour)
            t = time.mktime(t.timetuple())
            #print(feat)
            #print(submitteremail)
            #print(createDate)
            #print(t)
            #print(createDate - t)
            if createDate > t:
                if category == "Code Enforcement":
                    sendEmailCodeEnforcement('matthew.attiyeh@ci.rosemount.mn.us') #change to ricks email
                    print("Successfully sent email to Rick")
                    #sendEmailSubmitter(submitterEmail) #add back in
                    print("Successfully sent email to Submitter")
                    #print(category)
                else:
                    sendEmailOther('matthew.attiyeh@ci.rosemount.mn.us') #change to pwadmin email
                    print("Successfully sent email to Pwadmn")
                    #sendEmailSubmitter(submitterEmail) #add back in
                    #print(category)
    else:
        y = minOID
        x = minOID + 1000

        ids = response['objectIds']
        newIteration = (math.ceil(iteration/1000.0) * 1000)
        while y < newIteration:
            if x > int(newIteration):
                x = newIteration
            where = OID + '>' + str(y) + ' AND ' + OID + '<=' + str(x)
            print('Querying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
            params = {'f': 'pjson', 'where': where, 'outFields' : '*', 'returnGeometry' : 'false', 'token' : token}
            r = requests.post(URL + '/query', data=params, verify=False)
            response = json.loads(r.content)
            for feat in response['features']:
                typeProb = feat['attributes']['probtype']
                status = feat['attributes']['status']
                details = feat['attributes']['details']
                location =feat['attributes']['locdesc']
                numvotes = feat['attributes']['numvotes']
                category = feat['attributes']['category']
                pocfullname = feat['attributes']['pocfullname']
                phone = feat['attributes']['pocphone']
                createDate = feat['attributes'][dateField]
                createDate = int(str(createDate)[0:-3])
                t = datetime.datetime.now() - timedelta(hours=hoursValue)
                t = time.mktime(t.timetuple())
                if createDate > t:
                    if category == "Code Enforcement":
                        sendEmail('matthew.attiyeh@ci.rosemount.mn.us')#change to ricks email
                        print("Successfully sent email to Rick")
                        #sendEmailSubmitter(submitterEmail) #add back in
                        print("Successfully sent email to Submitter")
                        #print(category)
                    else:
                        sendEmail('matthew.attiyeh@ci.rosemount.mn.us')#change to pwadmin email
                        #print(category)
            x += 1000
            y += 1000

            
def problems_to_excel():
    # Variables
    dictionary = {'Graffiti/Vandalism':'Vandalism','Other':'Miscellaneous','Playgrounds':'Playgrounds','Port-a-potties':'Park Maintenance','Trash Cans (in parks)':'Park Maintenance','Wasp Nests':'Park Maintenance','Icy Street':'Icy Streets','Other':'Snowplowing Issue','Road Not Cleared':'Snowplowing Issue','Snowplow Damage - Mailbox':'Snowplowing Damage - Mailbox','Snowplow Damage - Sod':'Snowplowing Damage - Sod','Trail/Sidewalk Not Cleared':'Snowplowing Issue','Curbstop Issues/Lower Pipe in yard':'Water Issue','Hydrant Issues':'Hydrant Issue','Other':'Miscellaneous','Sewer Back Up or Overflow':'Sanitary Sewer Issue','Storm Drain Blocked':'Storm Sewer Issue','Storm Water Drainage Issue':'Storm Sewer Issue','Water Leak':'Water Issue','Water Meter Issue':'Water Meter Service','Water Pressure':'Water Issue','Water Quality':'Water Issue','Crosswalks':'Crosswalks','Damaged Trail/Sidewalk':'Trail/Sidewalk Issue','Dead Animal':'Road Kill','Excessive Dust':'Excessive Dust','Other':'Miscellaneous','Pothole':'Pothole','Street Sign Down or Damaged':'Street Sigh/Other','Traffic/Pedestrian Safety Concern':'Traffic Concern','Block Party':'Block Party','Compliment':'Compliment','Illegal Dumping':'Illicit Discharge','Other ':'Miscellaneous','Report a Spill':'Illicit Discharge'}
    cats = []                       #category
    prob = []                       #probtype
    dets = []                       #details
    OBID = []                       #OBJECTID
    X = []                          #X
    Y = []                          #Y
    SubmitterName = []              #pocfullname
    SubmitterEmail = []             #pocemail
    SubmitterAddress = []           #locdesc
    SubmitterPhone = []             #pocphone



    # Query service and check if CreationDate time is within the last hour
    if count < 1000:
        #calculate the X and Y coordinates in the feature class
        arcpy.management.CalculateGeometryAttributes("L0Citizen_Problems", "X POINT_X;Y POINT_Y", '', '', 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]', "DD")
        #get date from feature class and store it locally
        params = {'f': 'pjson', 'where': "1=1", 'outFields' : '*', 'returnGeometry' : 'false', 'token' : token}
        r = requests.post(URL + '/query', data=params, verify=False)
        response = json.loads(r.content)
        for feat in response['features']:
            typeProb = feat['attributes']['probtype']
            status = feat['attributes']['status']
            details = feat['attributes']['details']
            locdesc = feat['attributes']['locdesc']
            numvotes = feat['attributes']['numvotes']
            XLoc = feat['attributes']['X']
            YLoc = feat['attributes']['Y']
            category = feat['attributes']['category']
            pocemail = feat['attributes']['pocemail']
            pocphone = feat['attributes']['pocphone']
            pocfullname = feat['attributes']['pocfullname']
            ObjectID = feat['attributes']['OBJECTID']
            createDate = feat['attributes'][dateField]
            createDate = int(str(createDate)[0:-3])
            t = datetime.datetime.now() - timedelta(hours=hoursValue) #to change it to a different time change the hoursValue variable to something else above(eg .5 for half hour)
            t = time.mktime(t.timetuple())
            #print(feat)
            #put the data into lists which will be used to create data frames
            if createDate > t:
                cats.append(category)
                dets.append(details)
                OBID.append(ObjectID)
                prob.append(typeProb)
                X.append(XLoc)
                Y.append(YLoc)
                SubmitterEmail.append(pocemail)
                SubmitterName.append(pocfullname)
                SubmitterAddress.append(locdesc)
                SubmitterPhone.append(pocphone)
                
        if createDate > t:
                #Create the dataframe to export export from the fields above
                RequestCSV = pd.DataFrame({"RequestID":"", "Issue":prob, "Department":"","priority":"low","Description":dets, "SpatialX":X, "SpatialY":Y, "SubmitterEmail":SubmitterEmail, "SubmitterAddress":SubmitterAddress})
                RequestorLogCSV = pd.DataFrame({"ID":"","Primary Phone": SubmitterPhone, "Email Address":SubmitterEmail, "FullName":SubmitterName, "SubmitterAddress":SubmitterAddress, "City":"Rosemount", "Zip Code":"55068"})    

                #Replace the probtype from the problem reporter with the issue types from cartegraph
                RequestCSV['RequestID']=RequestCSV['RequestID'].replace(dictionary)
                #RequestorLogCSV['probtype']=RequestCSV['probtype'].replace(dictionary)
                
                #Split the name and address fields into new columns
                #RequestCSV[['First','Last']] = RequestCSV.SubmitterName.str.split(n=1,expand=True)
                RequestCSV[['Address number','Street']] = RequestCSV.SubmitterAddress.str.split(n=1,expand=True)
                RequestCSV[['StreetName','Street3']] = RequestCSV.Street.str.split(pat=",",n=1,expand=True)
                RequestorLogCSV[['First Name','Last Name']] = RequestorLogCSV.FullName.str.split(n=1,expand=True)
                RequestorLogCSV[['Address number','StreetName']] = RequestorLogCSV.SubmitterAddress.str.split(n=1,expand=True)
                RequestorLogCSV[['Street','Street3']] = RequestorLogCSV.StreetName.str.split(pat=",",n=1,expand=True)
                
                #Make sure the street number is actually a number
                for addresses in RequestCSV['Address number']:
                    if type(addresses)==str:
                        if addresses[0]=="0" or addresses[0]=="1" or addresses[0]=="2" or addresses[0]=="3" or addresses[0]=="4" or addresses[0]=="5" or addresses[0]=="6" or addresses[0]=="7" or addresses[0]=="8" or addresses[0]=="9":
                            junkvar="1"
                        else:
                            RequestCSV['Address number']=RequestCSV['Address number'].replace({addresses:"9999"})
                    else:
                        RequestCSV['Address number']=RequestCSV['Address number'].replace({addresses:"9999"})
                        
                for addresses in RequestorLogCSV['Address number']:
                    if type(addresses)==str:
                        if addresses[0]=="0" or addresses[0]=="1" or addresses[0]=="2" or addresses[0]=="3" or addresses[0]=="4" or addresses[0]=="5" or addresses[0]=="6" or addresses[0]=="7" or addresses[0]=="8" or addresses[0]=="9":
                            junkvar="1"
                        else:
                            RequestorLogCSV['Address number']=RequestCSV['Address number'].replace({addresses:"9999"})
                    else:
                        RequestorLogCSV['Address number']=RequestCSV['Address number'].replace({addresses:"9999"})
                
                #Remove extra columns
                RequestCSV=RequestCSV.drop(["Street3","Street"], 1)
                RequestorLogCSV=RequestorLogCSV.drop(["Street3","StreetName", "SubmitterAddress"], 1)
                
                #export the dataframe to csv so it can be imported to Cartegraph.
                RequestCSV.to_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv", index=False)
                RequestorLogCSV.to_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestorLogCSV.csv", index=False)
        else:
                RequestCSV = pd.read_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv", index_col=None)[0:0]
                RequestorLogCSV = pd.read_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestorLogCSV.csv", index_col=None)[0:0] 
                RequestCSV.to_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv", index=False)
                RequestorLogCSV.to_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestorLogCSV.csv", index=False)


def cart_auto():
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
        LinkToRequestCSV = "T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv"
        FormatCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]'
        FormatRequestorCart = '/html/body/div[10]/div/div[3]/div[2]/div[3]/div[2]/div[2]/div[1]'
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
        driver.find_element_by_xpath(CategoryRequestsCart).click()
        time.sleep(.5)
        driver.find_element_by_xpath(FormatCart).click()
        time.sleep(.5)
        driver.find_element_by_xpath(FormatRequestorCart).click()
        time.sleep(.5)
        s = driver.find_element_by_xpath("//input[@type='file']") # this is how you upload a file
        time.sleep(.5)
        s.send_keys(LinkToRequestCSV) #link to requestcsv
        time.sleep(.5)
        driver.find_element_by_xpath(ImportButtonCart).click()
def cart_auto2():
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
        

#run functions
send_email_feat_service()
problems_to_excel()

#run cart_auto() if there are new rows in the RequestCSV spreadsheet
RequestCSV = pd.read_csv("T:\\Project\\CitizenProblemReporter\\spreadsheets\\RequestCSV.csv", index_col=None)
rows = (len(RequestCSV.index))
if rows > 0:
    cart_auto2()
