import datetime
import os
import pandas as pd
import arcpy
import shutil

# To get today's date in 'day-month-year' format(01-12-2017).
dateToday=datetime.datetime.today()
#FormatedDate=('{:02d}'.format(dateToday.day)+'-'+'{:02d}'.format(dateToday.month)+'-'+'{:04d}'.format(dateToday.year))
FormattedDate=('{:02d}'.format(dateToday.month)+'{:02d}'.format(dateToday.day)+'{:04d}'.format(dateToday.year))
#print(dateToday)
#print(FormattedDate)

#Variables
ToDoFolder = "T:\\Project\\Police\\Violations\\CAD_Data\\ToDo"
CompleteFolder = "T:\\Project\\Police\\Violations\\CAD_Data\\Complete\\2022"
CsvName = FormattedDate

#Arc Variables
arcpy.env.workspace = "T:\\Project\\Police\\Violations\\CAD_Data\\"
arcpy.env.overwriteOutput = True
fc = "T:\\Project\\Police\\Violations\\CAD_Data\\ViolationsContainer.gdb\\IncidentsCopy"
newShape = "T:\\Project\\Police\\Violations\\CAD_Data\\ViolationsContainer.gdb\\" + "t" + FormattedDate
IncidentsLayer = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\RosemountEGDB.DBO.LawEnforcementOperations\RosemountEGDB.DBO.Incidents"
field = "rsosdt_WD"
cursor = arcpy.SearchCursor(fc)

#Take downloaded file and move to correct foler then rename dowloaded file so it has todays name as a date
shutil.move("C:\\Users\\mka\\OneDrive - ci.rosemount.mn.us\\Email attachments from Flow\\RS - CAD - Incident Report - Google Earth - Last Week.csv","T:\\Project\\Police\\Violations\\CAD_Data\\todo\\RS - CAD - Incident Report - Google Earth - Last Week.csv")
os.rename("T:\\Project\\Police\\Violations\\CAD_Data\\todo\\RS - CAD - Incident Report - Google Earth - Last Week.csv","T:\\Project\\Police\\Violations\\CAD_Data\\todo\\" + CsvName + ".csv")

#Convert CSV to XLS
df = pd.read_csv("T:\\Project\\Police\\Violations\\CAD_Data\\ToDo\\" + CsvName + ".csv", index_col=False)
df.to_excel("T:\\Project\\Police\\Violations\\CAD_Data\\ToDo\\" + CsvName + ".xlsx", index=False)
df.to_csv("T:\\Project\\Police\\Violations\\CAD_Data\\Complete\\2022\\" + CsvName + ".csv", index=False)

#print(df)
Violations = "T:\\Project\\Police\\Violations\\CAD_Data\\ToDo\\" + CsvName + ".xlsx"

#Excel to Table - Create a table in the GDB out of the spreadsheet
arcpy.conversion.ExcelToTable(Violations, "T:\\Project\\Police\\Violations\\CAD_Data\\ViolationsContainer.gdb\\today", '', 1, '')
print("Todays spreadsheet exported to " + "T:\Project\Police\Violations\CAD_Data\ViolationsContainer.gdb" + " today")

#XY Table To Point - Create a shapefile from the table of the new incidents
arcpy.management.XYTableToPoint("T:\\Project\\Police\\Violations\\CAD_Data\\ViolationsContainer.gdb\\today", newShape, "Longitude", "Latitude", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')
arcpy.conversion.FeatureClassToShapefile(newShape, r"T:\Project\Police\Violations\CAD_Data\Complete\2022")

print("shapefile created in same GDB with a filename of t plus todays date")

#add new field called masterincnum and calculate field - add a new field in the shapefile so it can be joined to the incidents layer via masterincnum field
arcpy.management.AddField(newShape, "masterincnum", "TEXT", None, None, 20, "masterincnum", "NULLABLE", "NON_REQUIRED", '')
print("add field done line 44")
arcpy.management.CalculateField(newShape, "masterincnum", "!Master_Incident_Number!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
print("calc field done line 46")

#delete all from IncidentsCopy
arcpy.management.DeleteRows(fc)
      
#Append newShape to IncidentsCopy FC so masterincnum can be filled out in IncidentsCopy
arcpy.management.Append(newShape, fc, "NO_TEST", None, '', '')
#arcpy.management.DeleteField("T:\\Project\\Police\\Violations\\CAD_Data\\ViolationsContainer.gdb\\" + "t" + FormattedDate, "masterincnum", "DELETE_FIELDS")
print("append done line 49")

#Join tdate to incidents copy and Calculate Field to fill out the rest of the fields
arcpy.management.JoinField(fc, "masterincnum", newShape, "masterincnum", "ID;Response_Date;Address;Officer1Name;Call_Disposition;Call_Back_Phone;Caller_Name")
print("join field done line 53")

arcpy.management.CalculateField(fc, "incidentid", "!ID!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "responsedate", "!Response_Date!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "fulladdress", "!Address!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "officer", "!Officer1Name!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "actiontaken", "!Call_Disposition!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "callerphone", "!Call_Back_Phone!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField(fc, "callername", "!Caller_Name!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
print("Calculate Field ran")

#delete the joined fields
arcpy.management.DeleteField(fc, "ID;Response_Date;Address;Officer1Name;Call_Disposition;Call_Back_Phone;Caller_Name", "DELETE_FIELDS")
print("deleted extra fields")

#Append to incidents layer
arcpy.management.Append(fc, IncidentsLayer, "NO_TEST", None, '', '')
print("Appended to Incidents layer")

#Delete csv and xlsx from todo folder
os.remove("T:\\Project\\Police\\Violations\\CAD_Data\\ToDo\\" + FormattedDate + ".csv")
os.remove("T:\\Project\\Police\\Violations\\CAD_Data\\ToDo\\" + FormattedDate + ".xlsx")
print("Files removed from ToDo folder")

#extract date parts to field (doesnt work)
#arcpy.crime.ExtractDateParts(IncidentsLayer, "responsedate", True, True, None, None, None)
#arcpy.ca.AddDateAttributes("Incidents", "responsedate", "DAY_FULL_NAME responsedate_DW;HOUR responsedate_HR")

