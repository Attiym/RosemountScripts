# Import system modules
import os, arcpy
import pandas as pd
import smtplib
from email.mime.text import MIMEText

####Set up####
arcpy.env.overwriteOutput = True
FolderName = input("Type todays date to create a new folder here: T:\Data\Downloads\Parcels\....")
os.mkdir("T:\\Data\\Downloads\\Parcels\\" + FolderName)

#Variables
ParcelSDE = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.Cadastral\\RosemountEGDB.DBO.parcels"
NewParcels = "T:\\Project\\Automation\\ToolOutputs.gdb\\NewParcels"
ExistingParcels = "T:\\Project\\Automation\\ToolOutputs.gdb\\ExistingParcels"
NewParcelsList = "T:\\Project\\Automation\\ToolOutputs.gdb\\NewParcelsList"

#Calculate PADDRESS in parcel feature class
print("Calculating PADDRESS")
arcpy.management.CalculateField(ParcelSDE, "PADDRESS", 'Concatenate($feature.PHOUSE, " ",$feature.PSTREET)', "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

#create table of existing parcels
print("Creating Existing Parcels Table")
arcpy.conversion.TableToTable(ParcelSDE, "T:\\Project\\Automation\\ToolOutputs.gdb", "ExistingParcels", "OLDPIN LIKE '%0%' Or OLDPIN LIKE '%1%' Or OLDPIN LIKE '%2%' Or OLDPIN LIKE '%3%' Or OLDPIN LIKE '%4%' Or OLDPIN LIKE '%5%' Or OLDPIN LIKE '%6%' Or OLDPIN LIKE '%7%' Or OLDPIN LIKE '%8%' Or OLDPIN LIKE '%9%'", 'OLDPIN "OLDPIN" true true false 12 Text 0 0,First,#,Parcels,OLDPIN,0,12;PADDRESS "PADDRESS" true true false 200 Text 0 0,First,#,Parcels,PADDRESS,0,200;created_date "created_date" false true false 8 Date 0 0,First,#,Parcels,created_date,-1,-1', '')

#Pause so you can copy parcels from ftp site to new folder.
input("Press Enter once you have copied parcels to newly created folder")

#Location of new parcels copied from ftp site
NewParcels = "T:\\Data\\Downloads\\Parcels\\" +FolderName+ "\\parcels.shp"
ClippedParcels = "T:\\Data\\Downloads\\Parcels\\" +FolderName+ "\\parcels_clipped.shp"

#City Boundary Layer to clip parcel layer
CityBoundary = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.ReferenceData\\RosemountEGDB.DBO.City_Boundary"

#LFID Table and intermediate parcel FC to join to
LFID_Table = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.Parcels_LFID"
ParcelIntermediate = "T:\\Project\\Automation\\ToolOutputs.gdb\\ParcelsForTool"

####Run Tool######

# Clip parcels to city boundary
arcpy.Clip_analysis(NewParcels, CityBoundary, ClippedParcels)
print("Clip to city boundary done")
countFeatures = str(arcpy.GetCount_management("T:\\Data\\Downloads\\Parcels\\" + FolderName + "\\parcels_clipped.shp"))
print("There are "+ countFeatures + " Features in the clipped layer")        

#Remove existing features from  intermediate Parcel Layer
arcpy.management.TruncateTable(ParcelIntermediate)
print("Truncate table done for intermediate layer")

#Take the clipped parcels and load into the parcel feature class in Intermediate Layer
arcpy.management.Append(ClippedParcels, ParcelIntermediate, "NO_TEST")
print("Clipped features loaded into intermediate layer")

#Join Tables and calculate field in intermediate parcel layer
arcpy.management.JoinField(ParcelIntermediate, "OLDPIN", LFID_Table, "PIN_String")
print("LFID table joined to intermediate layer")
arcpy.management.CalculateField(ParcelIntermediate, "LFID", "!LFID_1!", "PYTHON3")
arcpy.management.CalculateField(ParcelIntermediate, "PADDRESS", "!ADDRESS!", "PYTHON3")
print("LFID and PADDRESS fields calculated on intermediate parcel layer")

#Delete fields from join
arcpy.management.DeleteField(ParcelIntermediate, ["PIN_1", "LFID_1", "ADDRESS", "PIN_STRING"])
print("Joined fields deleted from intermediate layer")

#Get Precinct ID's with spatial join
#arcpy.analysis.SpatialJoin(ParcelIntermediate, "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.VotingPrecinct_2022", r"T:\Project\Automation\ToolOutputs.gdb\ParcelsForToolwPrecincts", "JOIN_ONE_TO_ONE", "KEEP_ALL", 'TAXPIN "TAXPIN" true true false 12 Text 0 0,First,#,Parcels,TAXPIN,0,12;OLDPIN "OLDPIN" true true false 12 Text 0 0,First,#,Parcels,OLDPIN,0,12;PIN "PIN" true true false 13 Text 0 0,First,#,Parcels,PIN,0,13;PTYPE "PTYPE" true true false 1 Text 0 0,First,#,Parcels,PTYPE,0,1;OLNAME "OLNAME" true true false 18 Text 0 0,First,#,Parcels,OLNAME,0,18;OFNAME "OFNAME" true true false 20 Text 0 0,First,#,Parcels,OFNAME,0,20;FULLNAME "FULLNAME" true true false 40 Text 0 0,First,#,Parcels,FULLNAME,0,40;JOLNAME "JOLNAME" true true false 18 Text 0 0,First,#,Parcels,JOLNAME,0,18;JOFNAME "JOFNAME" true true false 20 Text 0 0,First,#,Parcels,JOFNAME,0,20;BUSINESS "BUSINESS" true true false 1 Text 0 0,First,#,Parcels,BUSINESS,0,1;CPORFEE "CPORFEE" true true false 1 Text 0 0,First,#,Parcels,CPORFEE,0,1;MULTIOWN "MULTIOWN" true true false 1 Text 0 0,First,#,Parcels,MULTIOWN,0,1;OADDR1 "OADDR1" true true false 36 Text 0 0,First,#,Parcels,OADDR1,0,36;OADDR2 "OADDR2" true true false 36 Text 0 0,First,#,Parcels,OADDR2,0,36;OCITYST "OCITYST" true true false 25 Text 0 0,First,#,Parcels,OCITYST,0,25;OZIP "OZIP" true true false 10 Text 0 0,First,#,Parcels,OZIP,0,10;PHOUSE "PHOUSE" true true false 8 Text 0 0,First,#,Parcels,PHOUSE,0,8;PSTREET "PSTREET" true true false 20 Text 0 0,First,#,Parcels,PSTREET,0,20;PAPARTMENT "PAPARTMENT" true true false 6 Text 0 0,First,#,Parcels,PAPARTMENT,0,6;PCITY "PCITY" true true false 27 Text 0 0,First,#,Parcels,PCITY,0,27;PSTATE "PSTATE" true true false 2 Text 0 0,First,#,Parcels,PSTATE,0,2;PZIP "PZIP" true true false 9 Text 0 0,First,#,Parcels,PZIP,0,9;CNAME "CNAME" true true false 38 Text 0 0,First,#,Parcels,CNAME,0,38;STATDATE "STATDATE" true true false 6 Text 0 0,First,#,Parcels,STATDATE,0,6;GREEN "GREEN" true true false 1 Text 0 0,First,#,Parcels,GREEN,0,1;AG "AG" true true false 1 Text 0 0,First,#,Parcels,AG,0,1;EXEMPT "EXEMPT" true true false 2 Text 0 0,First,#,Parcels,EXEMPT,0,2;TAXINCR "TAXINCR" true true false 3 Text 0 0,First,#,Parcels,TAXINCR,0,3;COOP "COOP" true true false 3 Text 0 0,First,#,Parcels,COOP,0,3;FORFEIT "FORFEIT" true true false 1 Text 0 0,First,#,Parcels,FORFEIT,0,1;CONTIG "CONTIG" true true false 1 Text 0 0,First,#,Parcels,CONTIG,0,1;DELINQ "DELINQ" true true false 1 Text 0 0,First,#,Parcels,DELINQ,0,1;LOAN "LOAN" true true false 6 Text 0 0,First,#,Parcels,LOAN,0,6;SCHLDIST "SCHLDIST" true true false 3 Text 0 0,First,#,Parcels,SCHLDIST,0,3;WTRSHED "WTRSHED" true true false 2 Text 0 0,First,#,Parcels,WTRSHED,0,2;SUBDIST "SUBDIST" true true false 2 Text 0 0,First,#,Parcels,SUBDIST,0,2;SCHLAREA "SCHLAREA" true true false 1 Text 0 0,First,#,Parcels,SCHLAREA,0,1;YRBUILT "YRBUILT" true true false 8 Double 8 38,First,#,Parcels,YRBUILT,-1,-1;UNITS "UNITS" true true false 8 Double 8 38,First,#,Parcels,UNITS,-1,-1;LANDVAL "LANDVAL" true true false 8 Double 8 38,First,#,Parcels,LANDVAL,-1,-1;BLDGVAL "BLDGVAL" true true false 8 Double 8 38,First,#,Parcels,BLDGVAL,-1,-1;TOTALVAL "TOTALVAL" true true false 8 Double 8 38,First,#,Parcels,TOTALVAL,-1,-1;LMVLAND "LMVLAND" true true false 8 Double 8 38,First,#,Parcels,LMVLAND,-1,-1;LMVBLDG "LMVBLDG" true true false 8 Double 8 38,First,#,Parcels,LMVBLDG,-1,-1;LMVTOTAL "LMVTOTAL" true true false 8 Double 8 38,First,#,Parcels,LMVTOTAL,-1,-1;HMSTD "HMSTD" true true false 1 Text 0 0,First,#,Parcels,HMSTD,0,1;MUSE "MUSE" true true false 1 Text 0 0,First,#,Parcels,MUSE,0,1;MCNT "MCNT" true true false 8 Double 8 38,First,#,Parcels,MCNT,-1,-1;USE1 "USE1" true true false 2 Text 0 0,First,#,Parcels,USE1,0,2;ZONE1 "ZONE1" true true false 1 Text 0 0,First,#,Parcels,ZONE1,0,1;HCOD1 "HCOD1" true true false 1 Text 0 0,First,#,Parcels,HCOD1,0,1;XUSE1 "XUSE1" true true false 4 Text 0 0,First,#,Parcels,XUSE1,0,4;USE2 "USE2" true true false 2 Text 0 0,First,#,Parcels,USE2,0,2;ZONE2 "ZONE2" true true false 1 Text 0 0,First,#,Parcels,ZONE2,0,1;HCOD2 "HCOD2" true true false 1 Text 0 0,First,#,Parcels,HCOD2,0,1;XUSE2 "XUSE2" true true false 4 Text 0 0,First,#,Parcels,XUSE2,0,4;USE3 "USE3" true true false 2 Text 0 0,First,#,Parcels,USE3,0,2;ZONE3 "ZONE3" true true false 1 Text 0 0,First,#,Parcels,ZONE3,0,1;HCOD3 "HCOD3" true true false 1 Text 0 0,First,#,Parcels,HCOD3,0,1;XUSE3 "XUSE3" true true false 4 Text 0 0,First,#,Parcels,XUSE3,0,4;USE4 "USE4" true true false 2 Text 0 0,First,#,Parcels,USE4,0,2;ZONE4 "ZONE4" true true false 1 Text 0 0,First,#,Parcels,ZONE4,0,1;HCOD4 "HCOD4" true true false 1 Text 0 0,First,#,Parcels,HCOD4,0,1;XUSE4 "XUSE4" true true false 4 Text 0 0,First,#,Parcels,XUSE4,0,4;SALE_YR "SALE_YR" true true false 8 Double 8 38,First,#,Parcels,SALE_YR,-1,-1;SALE_MO "SALE_MO" true true false 8 Double 8 38,First,#,Parcels,SALE_MO,-1,-1;SALE_VAL "SALE_VAL" true true false 8 Double 8 38,First,#,Parcels,SALE_VAL,-1,-1;SALE_QUAL "SALE_QUAL" true true false 1 Text 0 0,First,#,Parcels,SALE_QUAL,0,1;VSALE_YR "VSALE_YR" true true false 8 Double 8 38,First,#,Parcels,VSALE_YR,-1,-1;VSALE_MO "VSALE_MO" true true false 8 Double 8 38,First,#,Parcels,VSALE_MO,-1,-1;VSALE_VAL "VSALE_VAL" true true false 8 Double 8 38,First,#,Parcels,VSALE_VAL,-1,-1;VSALE_QUAL "VSALE_QUAL" true true false 1 Text 0 0,First,#,Parcels,VSALE_QUAL,0,1;LMVLAND2 "LMVLAND2" true true false 8 Double 8 38,First,#,Parcels,LMVLAND2,-1,-1;LMVBLDG2 "LMVBLDG2" true true false 8 Double 8 38,First,#,Parcels,LMVBLDG2,-1,-1;LMVTOTA2 "LMVTOTA2" true true false 8 Double 8 38,First,#,Parcels,LMVTOTA2,-1,-1;TTCAP "TTCAP" true true false 8 Double 8 38,First,#,Parcels,TTCAP,-1,-1;NETTAX "NETTAX" true true false 8 Double 8 38,First,#,Parcels,NETTAX,-1,-1;SATAX "SATAX" true true false 8 Double 8 38,First,#,Parcels,SATAX,-1,-1;TOTTAX "TOTTAX" true true false 8 Double 8 38,First,#,Parcels,TOTTAX,-1,-1;TOTTAX2 "TOTTAX2" true true false 8 Double 8 38,First,#,Parcels,TOTTAX2,-1,-1;FEATURE "FEATURE" true true false 8 Double 8 38,First,#,Parcels,FEATURE,-1,-1;OPEN_ "OPEN_" true true false 1 Text 0 0,First,#,Parcels,OPEN_,0,1;LFID "LFID" true true false 4 Long 0 10,First,#,Parcels,LFID,-1,-1;PADDRESS "PADDRESS" true true false 200 Text 0 0,First,#,Parcels,PADDRESS,0,200;created_user "created_user" false true false 255 Text 0 0,First,#,Parcels,created_user,0,255;created_date "created_date" false true false 8 Date 0 0,First,#,Parcels,created_date,-1,-1;last_edited_user "last_edited_user" false true false 255 Text 0 0,First,#,Parcels,last_edited_user,0,255;last_edited_date "last_edited_date" false true false 8 Date 0 0,First,#,Parcels,last_edited_date,-1,-1;NAME "Precinct Name" true true false 50 Text 0 0,First,#,RosemountEGDB.DBO.VotingPrecinct_2022,NAME,0,50', "HAVE_THEIR_CENTER_IN", None, '')
arcpy.analysis.SpatialJoin(ParcelIntermediate, "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.VotingPrecinct_2022", r"T:\Project\Automation\ToolOutputs.gdb\ParcelsForToolwPrecincts", "JOIN_ONE_TO_ONE", "KEEP_ALL", 'TAXPIN "TAXPIN" true true false 12 Text 0 0,First,#,ParcelsForTool,TAXPIN,0,12;OLDPIN "OLDPIN" true true false 12 Text 0 0,First,#,ParcelsForTool,OLDPIN,0,12;PIN "PIN" true true false 13 Text 0 0,First,#,ParcelsForTool,PIN,0,13;PTYPE "PTYPE" true true false 1 Text 0 0,First,#,ParcelsForTool,PTYPE,0,1;OLNAME "OLNAME" true true false 18 Text 0 0,First,#,ParcelsForTool,OLNAME,0,18;OFNAME "OFNAME" true true false 20 Text 0 0,First,#,ParcelsForTool,OFNAME,0,20;FULLNAME "FULLNAME" true true false 40 Text 0 0,First,#,ParcelsForTool,FULLNAME,0,40;JOLNAME "JOLNAME" true true false 18 Text 0 0,First,#,ParcelsForTool,JOLNAME,0,18;JOFNAME "JOFNAME" true true false 20 Text 0 0,First,#,ParcelsForTool,JOFNAME,0,20;BUSINESS "BUSINESS" true true false 1 Text 0 0,First,#,ParcelsForTool,BUSINESS,0,1;CPORFEE "CPORFEE" true true false 1 Text 0 0,First,#,ParcelsForTool,CPORFEE,0,1;MULTIOWN "MULTIOWN" true true false 1 Text 0 0,First,#,ParcelsForTool,MULTIOWN,0,1;OADDR1 "OADDR1" true true false 36 Text 0 0,First,#,ParcelsForTool,OADDR1,0,36;OADDR2 "OADDR2" true true false 36 Text 0 0,First,#,ParcelsForTool,OADDR2,0,36;OCITYST "OCITYST" true true false 25 Text 0 0,First,#,ParcelsForTool,OCITYST,0,25;OZIP "OZIP" true true false 10 Text 0 0,First,#,ParcelsForTool,OZIP,0,10;PHOUSE "PHOUSE" true true false 8 Text 0 0,First,#,ParcelsForTool,PHOUSE,0,8;PSTREET "PSTREET" true true false 20 Text 0 0,First,#,ParcelsForTool,PSTREET,0,20;PAPARTMENT "PAPARTMENT" true true false 6 Text 0 0,First,#,ParcelsForTool,PAPARTMENT,0,6;PCITY "PCITY" true true false 27 Text 0 0,First,#,ParcelsForTool,PCITY,0,27;PSTATE "PSTATE" true true false 2 Text 0 0,First,#,ParcelsForTool,PSTATE,0,2;PZIP "PZIP" true true false 9 Text 0 0,First,#,ParcelsForTool,PZIP,0,9;CNAME "CNAME" true true false 38 Text 0 0,First,#,ParcelsForTool,CNAME,0,38;STATDATE "STATDATE" true true false 6 Text 0 0,First,#,ParcelsForTool,STATDATE,0,6;GREEN "GREEN" true true false 1 Text 0 0,First,#,ParcelsForTool,GREEN,0,1;AG "AG" true true false 1 Text 0 0,First,#,ParcelsForTool,AG,0,1;EXEMPT "EXEMPT" true true false 2 Text 0 0,First,#,ParcelsForTool,EXEMPT,0,2;TAXINCR "TAXINCR" true true false 3 Text 0 0,First,#,ParcelsForTool,TAXINCR,0,3;COOP "COOP" true true false 3 Text 0 0,First,#,ParcelsForTool,COOP,0,3;FORFEIT "FORFEIT" true true false 1 Text 0 0,First,#,ParcelsForTool,FORFEIT,0,1;CONTIG "CONTIG" true true false 1 Text 0 0,First,#,ParcelsForTool,CONTIG,0,1;DELINQ "DELINQ" true true false 1 Text 0 0,First,#,ParcelsForTool,DELINQ,0,1;LOAN "LOAN" true true false 6 Text 0 0,First,#,ParcelsForTool,LOAN,0,6;SCHLDIST "SCHLDIST" true true false 3 Text 0 0,First,#,ParcelsForTool,SCHLDIST,0,3;WTRSHED "WTRSHED" true true false 2 Text 0 0,First,#,ParcelsForTool,WTRSHED,0,2;SUBDIST "SUBDIST" true true false 2 Text 0 0,First,#,ParcelsForTool,SUBDIST,0,2;SCHLAREA "SCHLAREA" true true false 1 Text 0 0,First,#,ParcelsForTool,SCHLAREA,0,1;YRBUILT "YRBUILT" true true false 8 Double 0 0,First,#,ParcelsForTool,YRBUILT,-1,-1;UNITS "UNITS" true true false 8 Double 0 0,First,#,ParcelsForTool,UNITS,-1,-1;LANDVAL "LANDVAL" true true false 8 Double 0 0,First,#,ParcelsForTool,LANDVAL,-1,-1;BLDGVAL "BLDGVAL" true true false 8 Double 0 0,First,#,ParcelsForTool,BLDGVAL,-1,-1;TOTALVAL "TOTALVAL" true true false 8 Double 0 0,First,#,ParcelsForTool,TOTALVAL,-1,-1;LMVLAND "LMVLAND" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVLAND,-1,-1;LMVBLDG "LMVBLDG" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVBLDG,-1,-1;LMVTOTAL "LMVTOTAL" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVTOTAL,-1,-1;HMSTD "HMSTD" true true false 1 Text 0 0,First,#,ParcelsForTool,HMSTD,0,1;MUSE "MUSE" true true false 1 Text 0 0,First,#,ParcelsForTool,MUSE,0,1;MCNT "MCNT" true true false 8 Double 0 0,First,#,ParcelsForTool,MCNT,-1,-1;USE1 "USE1" true true false 2 Text 0 0,First,#,ParcelsForTool,USE1,0,2;ZONE1 "ZONE1" true true false 1 Text 0 0,First,#,ParcelsForTool,ZONE1,0,1;HCOD1 "HCOD1" true true false 1 Text 0 0,First,#,ParcelsForTool,HCOD1,0,1;XUSE1 "XUSE1" true true false 4 Text 0 0,First,#,ParcelsForTool,XUSE1,0,4;USE2 "USE2" true true false 2 Text 0 0,First,#,ParcelsForTool,USE2,0,2;ZONE2 "ZONE2" true true false 1 Text 0 0,First,#,ParcelsForTool,ZONE2,0,1;HCOD2 "HCOD2" true true false 1 Text 0 0,First,#,ParcelsForTool,HCOD2,0,1;XUSE2 "XUSE2" true true false 4 Text 0 0,First,#,ParcelsForTool,XUSE2,0,4;USE3 "USE3" true true false 2 Text 0 0,First,#,ParcelsForTool,USE3,0,2;ZONE3 "ZONE3" true true false 1 Text 0 0,First,#,ParcelsForTool,ZONE3,0,1;HCOD3 "HCOD3" true true false 1 Text 0 0,First,#,ParcelsForTool,HCOD3,0,1;XUSE3 "XUSE3" true true false 4 Text 0 0,First,#,ParcelsForTool,XUSE3,0,4;USE4 "USE4" true true false 2 Text 0 0,First,#,ParcelsForTool,USE4,0,2;ZONE4 "ZONE4" true true false 1 Text 0 0,First,#,ParcelsForTool,ZONE4,0,1;HCOD4 "HCOD4" true true false 1 Text 0 0,First,#,ParcelsForTool,HCOD4,0,1;XUSE4 "XUSE4" true true false 4 Text 0 0,First,#,ParcelsForTool,XUSE4,0,4;SALE_YR "SALE_YR" true true false 8 Double 0 0,First,#,ParcelsForTool,SALE_YR,-1,-1;SALE_MO "SALE_MO" true true false 8 Double 0 0,First,#,ParcelsForTool,SALE_MO,-1,-1;SALE_VAL "SALE_VAL" true true false 8 Double 0 0,First,#,ParcelsForTool,SALE_VAL,-1,-1;SALE_QUAL "SALE_QUAL" true true false 1 Text 0 0,First,#,ParcelsForTool,SALE_QUAL,0,1;VSALE_YR "VSALE_YR" true true false 8 Double 0 0,First,#,ParcelsForTool,VSALE_YR,-1,-1;VSALE_MO "VSALE_MO" true true false 8 Double 0 0,First,#,ParcelsForTool,VSALE_MO,-1,-1;VSALE_VAL "VSALE_VAL" true true false 8 Double 0 0,First,#,ParcelsForTool,VSALE_VAL,-1,-1;VSALE_QUAL "VSALE_QUAL" true true false 1 Text 0 0,First,#,ParcelsForTool,VSALE_QUAL,0,1;LMVLAND2 "LMVLAND2" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVLAND2,-1,-1;LMVBLDG2 "LMVBLDG2" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVBLDG2,-1,-1;LMVTOTA2 "LMVTOTA2" true true false 8 Double 0 0,First,#,ParcelsForTool,LMVTOTA2,-1,-1;TTCAP "TTCAP" true true false 8 Double 0 0,First,#,ParcelsForTool,TTCAP,-1,-1;NETTAX "NETTAX" true true false 8 Double 0 0,First,#,ParcelsForTool,NETTAX,-1,-1;SATAX "SATAX" true true false 8 Double 0 0,First,#,ParcelsForTool,SATAX,-1,-1;TOTTAX "TOTTAX" true true false 8 Double 0 0,First,#,ParcelsForTool,TOTTAX,-1,-1;TOTTAX2 "TOTTAX2" true true false 8 Double 0 0,First,#,ParcelsForTool,TOTTAX2,-1,-1;FEATURE "FEATURE" true true false 8 Double 0 0,First,#,ParcelsForTool,FEATURE,-1,-1;OPEN_ "OPEN_" true true false 1 Text 0 0,First,#,ParcelsForTool,OPEN_,0,1;LFID "LFID" true true false 4 Long 0 0,First,#,ParcelsForTool,LFID,-1,-1;PADDRESS "PADDRESS" true true false 200 Text 0 0,First,#,ParcelsForTool,PADDRESS,0,200;created_user "created_user" true true false 255 Text 0 0,First,#,ParcelsForTool,created_user,0,255,RosemountEGDB.DBO.VotingPrecinct_2022,created_user,0,255;created_date "created_date" true true false 8 Date 0 0,First,#,ParcelsForTool,created_date,-1,-1,RosemountEGDB.DBO.VotingPrecinct_2022,created_date,-1,-1;last_edited_user "last_edited_user" true true false 255 Text 0 0,First,#,ParcelsForTool,last_edited_user,0,255,RosemountEGDB.DBO.VotingPrecinct_2022,last_edited_user,0,255;last_edited_date "last_edited_date" true true false 8 Date 0 0,First,#,ParcelsForTool,last_edited_date,-1,-1,RosemountEGDB.DBO.VotingPrecinct_2022,last_edited_date,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,ParcelsForTool,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,ParcelsForTool,Shape_Area,-1,-1;NAME "Precinct Name" true true false 50 Text 0 0,First,#,RosemountEGDB.DBO.VotingPrecinct_2022,NAME,0,50', "HAVE_THEIR_CENTER_IN", None, '')
ParcelsForToolswPrecincts = r"T:\Project\Automation\ToolOutputs.gdb\ParcelsForToolwPrecincts"

#Remove existing features from parcel feature class in SDE
arcpy.management.TruncateTable(ParcelSDE)
print("Truncate table done for SDE parcel Layer")

#Take the intermediate parcel layer and load into the parcel feature class into the sde parcel layer
arcpy.management.Append(ParcelsForToolswPrecincts, ParcelSDE, "NO_TEST")
print("Clipped features loaded into SDE layer")

#count final features
countFeaturesFinal = str(arcpy.GetCount_management("T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.Cadastral\\RosemountEGDB.DBO.parcels"))
print("There are " + countFeaturesFinal + " Features in the final layer")

####Find the new parcels####

#Variables
NewParcels = "T:\\Project\\Automation\\ToolOutputs.gdb\\NewParcels"
ExistingParcels = "T:\\Project\\Automation\\ToolOutputs.gdb\\ExistingParcels"
NewParcelsList = "T:\\Project\\Automation\\ToolOutputs.gdb\\NewParcelsList"

#Calculate PADDRESS in parcel feature class
print("Calculating PADDRESS")
arcpy.management.CalculateField(ParcelSDE, "PADDRESS", 'Concatenate($feature.PHOUSE, " ",$feature.PSTREET)', "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

#create table of new parcels
print("Creating New Parcels Table")
arcpy.conversion.TableToTable(ParcelSDE, "T:\\Project\\Automation\\ToolOutputs.gdb", "NewParcels", "OLDPIN LIKE '%0%' Or OLDPIN LIKE '%1%' Or OLDPIN LIKE '%2%' Or OLDPIN LIKE '%3%' Or OLDPIN LIKE '%4%' Or OLDPIN LIKE '%5%' Or OLDPIN LIKE '%6%' Or OLDPIN LIKE '%7%' Or OLDPIN LIKE '%8%' Or OLDPIN LIKE '%9%'", 'OLDPIN "OLDPIN" true true false 12 Text 0 0,First,#,Parcels,OLDPIN,0,12;PADDRESS "PADDRESS" true true false 200 Text 0 0,First,#,Parcels,PADDRESS,0,200;created_date "created_date" false true false 8 Date 0 0,First,#,Parcels,created_date,-1,-1', '')

#Join tables
print("Joining Tables")
arcpy.management.JoinField(NewParcels, "OLDPIN", ExistingParcels, "OLDPIN", "OLDPIN;PADDRESS;created_date")

#Add "compare" field to NewParcels
print("Adding and calculating Compare field")
arcpy.management.AddField(NewParcels, "Compare", "TEXT", None, None, 100, '', "NULLABLE", "NON_REQUIRED", '')

#calculate "compare" field to show new addresses
arcpy.management.CalculateField(NewParcels, "Compare", """if ($feature.OLDPIN != $feature.OLDPIN_1) {
return $feature.PADDRESS};
""", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

#create table of new addresses only
print("Creating NewParcelsList table and deleting extra columns")
arcpy.conversion.TableToTable(NewParcels, r"T:\\Project\\Automation\\ToolOutputs.gdb", "NewParcelsList", "Compare IS NOT NULL And PADDRESS IS NOT NULL and PADDRESS NOT LIKE '   %'", 'OLDPIN "OLDPIN" true true false 12 Text 0 0,First,#,NewParcels,OLDPIN,0,12;PADDRESS "PADDRESS" true true false 200 Text 0 0,First,#,NewParcels,PADDRESS,0,200;created_date "created_date" true true false 8 Date 0 0,First,#,NewParcels,created_date,-1,-1;OLDPIN_1 "OLDPIN" true true false 12 Text 0 0,First,#,NewParcels,OLDPIN_1,0,12;PADDRESS_1 "PADDRESS" true true false 200 Text 0 0,First,#,NewParcels,PADDRESS_1,0,200;created_date_1 "created_date" true true false 8 Date 0 0,First,#,NewParcels,created_date_1,-1,-1;Compare "Compare" true true false 25 Text 0 0,First,#,NewParcels,Compare,0,25', '')

#Delete extra columns
arcpy.management.DeleteField(NewParcelsList, "OLDPIN_1;PADDRESS_1;created_date_1;Compare", "DELETE_FIELDS")

#Table to Excel
print("Exporting NewParcelsList to excel")
arcpy.conversion.TableToExcel(NewParcelsList, r"T:\Project\Automation\ParcelCompare\NewParcelsList.xls", "NAME", "CODE")

#Table to Pandas
print("Importing to Pandas and generating email")
df = pd.read_excel(r"T:\Project\Automation\ParcelCompare\NewParcelsList.xls")

#Convert the dataframe into HTML so it can be added to body of email.
table = df.to_html(index=False, justify = "left", border = None)

def sendEmail(ToEmail):
    fromEmail = 'GISHelpdesk@ci.rosemount.mn.us'
    ToEmail = ToEmail
    SUBJECT = "New addresses have recently been created"
    TEXT = table
    smtpObj = smtplib.SMTP('cirosemountmnus.mail.protection.outlook.com', 25)
    msg = MIMEText(TEXT, 'html')
    msg['Subject'] = SUBJECT
    msg['From'] = fromEmail
    msg['To'] = ToEmail
    smtpObj.sendmail(fromEmail, ToEmail, msg.as_string())
    smtpObj.quit()

#send email if there are new parcels
NumNewAddresses = len(df)
print("There are " + str(NumNewAddresses) + " new addresses.")
if NumNewAddresses > 0:
    print("Sending Email with new parcel list")
    sendEmail('matthew.attiyeh@rosemountmn.gov')
    sendEmail('jessie.paque@rosemountmn.gov')
    sendEmail('erin.fasbender@rosemountmn.gov')

