import arcpy, os, shutil
import pandas as pd 
from arcgis.gis import GIS
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText

#Set Environment
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"T:\Project\Automation\CodeEnforcementAutomate\CodeEnforcementAutomate.gdb"
out_path = r"T:\Project\Automation\CodeEnforcementAutomate\CodeEnforcementAutomate.gdb"
recentInspections = "https://rs-gis.ci.rosemount.mn.us/server/rest/services/Hosted/Recent_Inspections/FeatureServer/0"

def CleanData():
    #Table to Table (convert recent inspections feature class into a table in a GDB)
    arcpy.conversion.TableToTable(recentInspections, out_path, "RecentInspectionsTable")

    #Create variable to store filepath of the recent inspections table
    RecentInspectionsTable = r"T:\Project\Automation\CodeEnforcementAutomate\CodeEnforcementAutomate.gdb\RecentInspectionsTable" #Var

    #Add field to newly created table to calculate todays date and the difference between todays date and the upcoming inspection date
    arcpy.AddField_management(RecentInspectionsTable, "TodaysDate","Date")
    arcpy.AddField_management(RecentInspectionsTable, "DateDifference","Short")

    #Calculate newly created fields to calculate todays date and the difference between todays date and the upcoming inspection date
    arcpy.management.CalculateField(RecentInspectionsTable, "TodaysDate", "Date()", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(RecentInspectionsTable, "DateDifference", 'DateDiff($feature.flwupdate,$feature.TodaysDate,"days")', "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

    #Select rows that have a date difference of 1 (or whatever you change it to) to isolate the ones with upcoming dates
    arcpy.analysis.TableSelect(RecentInspectionsTable, r"T:\Project\Automation\CodeEnforcementAutomate\CodeEnforcementAutomate.gdb\UpcomingDueDatesTable", "DateDifference = 1 And inspstatus <> 'Complete'")

    #Create variable to store filepath of the table created from previous step (upcoming dates)
    UpcomingDueDatesTable = r"T:\Project\Automation\CodeEnforcementAutomate\CodeEnforcementAutomate.gdb\UpcomingDueDatesTable" #Var

    #Delete extra fields from UpcomingDueDates table so the email is not too crowded
    arcpy.management.DeleteField(UpcomingDueDatesTable, "inspyear;addressno;street;guid;globalid_1648740846623;TodaysDate;DateDifference", "DELETE_FIELDS")

    #Export UpcomingDueDatesTable to excel so it can be loaded into pandas
    arcpy.conversion.TableToExcel(UpcomingDueDatesTable, r"T:\Project\Automation\CodeEnforcementAutomate\UpcomingDueDates.xlsx", "NAME", "CODE")


def sendEmailCodeEnforcement(ToEmail):
    fromEmail = 'GISHelpdesk@ci.rosemount.mn.us'
    ToEmail = ToEmail
    SUBJECT = "You have " + str(NumInspections) + ' follow up inspections scheduled for tomorrow'
    TEXT = table
    smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
    msg = MIMEText(TEXT, 'html')
    msg['Subject'] = SUBJECT
    msg['From'] = fromEmail
    msg['To'] = ToEmail
    smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
    smtpObj.quit()

def sendEmailMatt(ToEmail):
    fromEmail = 'GISHelpdesk@ci.rosemount.mn.us'
    ToEmail = ToEmail
    SUBJECT = "You have " + str(NumInspections) + ' follow up inspections scheduled for tomorrow'
    TEXT = table
    smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
    msg = MIMEText(TEXT, 'html')
    msg['Subject'] = SUBJECT
    msg['From'] = fromEmail
    msg['To'] = ToEmail
    smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
    smtpObj.quit()
    
######Run functions######

CleanData() #Clean Data Function

#Load UpcomingDueDates excel file into pandas and drop the ObjectID column(column[0]).
df = pd.read_excel(r"T:\Project\Automation\CodeEnforcementAutomate\UpcomingDueDates.xlsx", index_col=None)
df.drop(df.columns[0], axis=1, inplace=True)

#Rename columns to add ' and ' to the end. This will make concantenating look better and read better
df.rename(columns = {"parking":"parking and ", "composting":"composting and ", "firewood":"firewood and ", "lawn":"lawn and ", "homeoccupations":"homeoccupations and ", "housenum":"housenum and ", "vehicles":"vehicles and ", "irrigation":"irrigation and ", "recvehicles":"recvehicles and ", "snowremoval":"snowremoval and ", "other":"other and ","vehiclesales":"vehiclesales and ", "wastecontainers":"wastecontainers and ", }, inplace = True)

#Replace Yes values with the name of the column
for col in df:
    df[col]=df[col].replace("Yes", df[col].name)

#replace No values with empty space    
nan_value = float("NaN")
df.replace("No",nan_value, inplace=True)

#create a new field called "concat" that concantenates the fields to make a readable output for the email
df["concat"] = df["address"].str.cat(df["composting and "], sep = " - Issues:", na_rep = "")
df["concat"] = df["concat"].str.cat(df["firewood and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["lawn and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["homeoccupations and "], sep = " ", na_rep = "")
df["concat"] = df["concat"].str.cat(df["housenum and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["vehicles and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["irrigation and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["parking and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["recvehicles and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["snowremoval and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["vehiclesales and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["wastecontainers and "], sep = "", na_rep = "")
df["concat"] = df["concat"].str.cat(df["other and "], sep = "" , na_rep = "")
df["concat"] = df["concat"].str.cat(df["notes"], sep = "Notes: ", na_rep = "")
df["concat"] = df["concat"].str.cat(df["flwupdate"].astype(str), sep = " )- Due on ", na_rep = " ")

#replace "and notes" with just "notes" so it will look nicer
df["concat"] = df["concat"].str.replace("and Notes"," (Notes")
#df["concat"] = df["concat"].str.replace("(Notes: )","", regex=None) ##### attempt to clean up more but can't make it work right ####

#drop extra columns so only the concat column is left
df.drop(df.columns[0:19], axis=1, inplace=True)

#df.to_excel(r"T:\Project\Automation\CodeEnforcementAutomate\UpcomingDueDatestest.xlsx")

#Convert the dataframe into HTML so it can be added to body of email.
table = df.to_html(index=False, header = False, justify = "left", border = None)

#Calculate how many follow up inspections there are by checking rows in table
NumInspections = len(df)

#Send email if there are inspections due tomorrow
if NumInspections > 0:
    sendEmailCodeEnforcement('Aju.Kurakkaran@ci.rosemount.mn.us') # Send email function
    sendEmailMatt('matthew.attiyeh@ci.rosemount.mn.us') # Send email function
    print("sent to matt")
else:
    print("no inspections due")
