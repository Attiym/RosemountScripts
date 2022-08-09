import arcpy, os, shutil
from arcgis.gis import GIS
from PyPDF2 import PdfFileMerger

######### USAGE ########

## This script will export all the PDF's available in the printed maps portion of our website located here: https://rosemountemployeehub-cirosemountmn.hub.arcgis.com/
## These PDF's will all be exported to this folder: T:\Project\Automation\Exported PDF\ and will be uploaded onto the website from there.
## The PDF's should also go into their appropraite folders on the T: drive using the 2nd part of this script. Make sure it is commented out when running part 1.

# Script Last Updated By MKA 7/19/2021

print("Initializing...\n")

def ExportPDFs():
    print("Exporting from MXD to PDF. All files located in the folder at T:\Project\Automation\Exported PDF\n")
    #Addressing
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\CommDev\Addressing\Addressing\Addressing.aprx")
    Layout = aprx.listLayouts("Layout")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Address_Base_Map_42x42.pdf")
    print("Address Base Map 42x42 PDF Exported")

    #Adopt-A-Street Volunteers
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Engineering\AdoptAStreet\AdoptAStreet.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Adopt_A_Street_Program.pdf")
    print("Adopt_A_Street_Program PDF Exported")

    #Bicycle Facilities
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Parks\Trails\BikeRoutes\BikeRoutes.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\City_of_Rosemount_Bicycle_Facilities_Bike_Racks_2.pdf")
    print("City_of_Rosemount_Bicycle_Facilities_Bike_Racks_2 PDF Exported")

##    #Construction Projects
##    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Engineering\ConstructionProjects\CurrentConstruction.aprx")
##    Layout = aprx.listLayouts("Layout1")[0]
##    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\CurrentConstructionProjects.pdf")
##    print("CurrentConstructionProjects PDF Exported")

##    #Election Precincts
##    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Admin\Voting\VotingPrecincts2.aprx")
##    Layout = aprx.listLayouts("Layout1")[0]
##    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Precincts1117.pdf")
##    print("Precincts1117 PDF Exported")

    #Electrical Service Providers
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Utilities\GasElectric\UtilityServiceProviders.aprx")
    Layout = aprx.listLayouts("Electric")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Electric_Service_Area.pdf")
    print("Electric_Service_Area PDF Exported")

    #Land Use
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\CommDev\LandUse_Zoning.aprx")
    Layout = aprx.listLayouts("Land Use 11x17")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Land_Use_Comp_Plan_11x17.pdf")
    print("Land_Use_Comp_Plan_11x17 PDF Exported")

    #Natural Gas Providers
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Utilities\GasElectric\UtilityServiceProviders.aprx")
    Layout = aprx.listLayouts("Gas")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Natural_Gas_Service_Areas.pdf")
    print("Natural_Gas_Service_Areas PDF Exported")

    #Railroad Quite Zone
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Engineering\QuietZone\RailroadQuietZone.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Quiet_Zone11_17.pdf")
    print("Quiet_Zone11_17 PDF Exported")

    #Road Weight Restrictions
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\WeightRestrictions\SeasonalWeightRestrictions.aprx")
    Layout = aprx.listLayouts("Layout 1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Street_Weight_Restrictions_Map.pdf")
    print("Street_Weight_Restrictions_Map PDF Exported")

    #Snowplowing - Priority Streets
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\plowing\Snowplowing.aprx")
    Layout = aprx.listLayouts("Priority Routes - Public")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Priority_Routes.pdf")
    print("Priority_Routes PDF Exported")

    #Snowplowing - Trails and Sidewalks
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\plowing\Snowplowing.aprx")
    Layout = aprx.listLayouts("Trail Plowing - Public")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Trail_and_Sidewalk.pdf")
    print("Trail_and_Sidewalk PDF Exported")

    #Streetlights
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\StreetLights\StreetLights2.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\2019_Street_Lights_Inventory_1117.pdf")
    print("2019_Street_Lights_Inventory_1117 PDF Exported")

    #Streets
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\StreetMap\StreetMap.aprx")
    Layout = aprx.listLayouts("Landscape")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\StreetMap_landscape.pdf")
    print("StreetMap PDF Exported (landscape)")

    #Streets
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Streets\StreetMap\StreetMap.aprx")
    Layout = aprx.listLayouts("Portrait 1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\StreetMap_portrait.pdf")
    print("StreetMap Exported PDF Exported (portrait)")

    #Subdivisions
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\CommDev\Subdivisions\Subdivisions22x34.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Subdivision_2234.pdf")
    print("Subdivision_2234 PDF Exported")

    #Park Amenities
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Parks\Park_Amenities\ParkAmenities.aprx")
    Layout = aprx.listLayouts("Layout1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\ParkAmenities11x17.pdf")
    print("ParkAmenities11x17 PDF Exported (for Trails and Parks)")

    #Trails and Sidewalks
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\Parks\Trails\Trails&Sidewalks.aprx")
    Layout = aprx.listLayouts("Portrait 1")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Trails&Sidewalks.pdf")
    print("Trails&Sidewalks PDF Exported (check pdf name)")

    #Zoning
    aprx = arcpy.mp.ArcGISProject(r"T:\Project\CommDev\LandUse_Zoning.aprx")
    Layout = aprx.listLayouts("Zoning11x17")[0]
    Layout.exportToPDF(r"T:\Project\Automation\Exported PDF\Zoning11x17.pdf")
    print("Zoning11x17 PDF Exported")


######## After uploading all the PDF's from the folder above run the script below to move them to their proper folder. ####

def MovePDFs():
    print("\nMoving PDF's to their individual folders\n")
    #Addressing
    shutil.copy(r"I:\GIS\Map_Library\CommDev\Addressing\Address_Base_Map_42x42.pdf", r"I:\GIS\Map_Library\CommDev\Addressing\Backup\Address_Base_Map_42x42_backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Address_Base_Map_42x42.pdf", r"I:\GIS\Map_Library\CommDev\Addressing\Address_Base_Map_42x42.pdf")

    #AdoptAStreet
    shutil.copy(r"I:\GIS\Map_Library\Engineering\AdoptAStreet\Adopt_A_Street_Program.pdf", r"I:\GIS\Map_Library\Engineering\AdoptAStreet\Backup\Adopt_A_Street_Program_backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Adopt_A_Street_Program.pdf", r"I:\GIS\Map_Library\Engineering\AdoptAStreet\Adopt_A_Street_Program.pdf")
    
    #BikeRoutes
    shutil.copy(r"I:\GIS\Map_Library\Parks\Trails\BikePath\City of Rosemount Bicycle Facilities_Bike Racks_2.pdf", r"I:\GIS\Map_Library\Parks\Trails\BikePath\Backup\City_of_Rosemount_Bicycle_Facilities_Bike_Racks_2_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\City_of_Rosemount_Bicycle_Facilities_Bike_Racks_2.pdf", r"I:\GIS\Map_Library\Parks\Trails\BikePath\City_of_Rosemount_Bicycle_Facilities_Bike Racks_2.pdf")

    #CurrentConstructionProjects
    shutil.copy(r"I:\GIS\Map_Library\Engineering\ConstructionProjects\CurrentConstructionProjects.pdf", r"I:\GIS\Map_Library\Engineering\ConstructionProjects\Backup\CurrentConstructionProjects_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\CurrentConstructionProjects.pdf", r"I:\GIS\Map_Library\Engineering\ConstructionProjects\CurrentConstructionProjects.pdf")
    
    #ElectricServiceAreas
    shutil.copy(r"I:\GIS\Map_Library\Utilities\GasElectric\Electric_Service_Area.pdf", r"I:\GIS\Map_Library\Utilities\GasElectric\Backup\Electric_Service_Area_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Electric_Service_Area.pdf", r"I:\GIS\Map_Library\Utilities\GasElectric\Electric_Service_Area.pdf")
    
    #Land Use Comp Plan 11x17
    shutil.copy(r"I:\GIS\Map_Library\CommDev\LandUse\Land_Use_Comp_Plan_11x17.pdf", r"I:\GIS\Map_Library\CommDev\LandUse\Backup\Land_Use_Comp_Plan_11x17_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Land_Use_Comp_Plan_11x17.pdf", r"I:\GIS\Map_Library\CommDev\LandUse\Land_Use_Comp_Plan_11x17.pdf")

    #Natural_Gas_Service_Areas
    shutil.copy(r"I:\GIS\Map_Library\Utilities\GasElectric\Natural_Gas_Service_Areas.pdf", r"I:\GIS\Map_Library\Utilities\GasElectric\Backup\Natural_Gas_Service_Areas_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Natural_Gas_Service_Areas.pdf", r"I:\GIS\Map_Library\Utilities\GasElectric\Natural_Gas_Service_Areas.pdf")
    
    #ParkAmenities
    shutil.copy(r"I:\GIS\Map_Library\Parks\ParkAmenities11x17.pdf", r"I:\GIS\Map_Library\Parks\Backup\ParkAmenities11x17_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\ParkAmenities11x17.pdf", r"I:\GIS\Map_Library\Parks\ParkAmenities11x17.pdf")

    #Priority Plow Routes Land-Public
    shutil.copy(r"I:\GIS\Map_Library\Streets\Plowing\Priority_Routes.pdf", r"I:\GIS\Map_Library\Streets\Plowing\Backup\Priority_Routes_backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Priority_Routes.pdf", r"I:\GIS\Map_Library\Streets\Plowing\Priority_Routes.pdf")
    
    #Quiet Zone11_17
    shutil.copy(r"I:\GIS\Map_Library\Engineering\QuietZone\Quiet_Zone11_17.pdf", r"I:\GIS\Map_Library\Engineering\QuietZone\Backup\Quiet_Zone11_17_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Quiet_Zone11_17.pdf", r"I:\GIS\Map_Library\Engineering\QuietZone\Quiet_Zone11_17.pdf")

    #Street Lights Inventory_1117
    shutil.copy(r"I:\GIS\Map_Library\Streets\StreetLights\2019_Street_Lights_Inventory_1117.pdf", r"I:\GIS\Map_Library\Streets\StreetLights\Backup\2019_Street_Lights_Inventory_1117.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\2019_Street_Lights_Inventory_1117.pdf", r"I:\GIS\Map_Library\Streets\StreetLights\2019_Street_Lights_Inventory_1117.pdf")

    #Street Weight Restrictions Map
    shutil.copy(r"I:\GIS\Map_Library\Streets\WeightRestrictions\Street_Weight_Restrictions_Map.pdf", r"I:\GIS\Map_Library\Streets\WeightRestrictions\Backup\Street_Weight_Restrictions_Map.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Street_Weight_Restrictions_Map.pdf", r"I:\GIS\Map_Library\Streets\WeightRestrictions\Street_Weight_Restrictions_Map.pdf")

    #StreetMap_landscape
    shutil.copy(r"I:\GIS\Map_Library\Streets\StreetMap\StreetMap_landscape.pdf", r"I:\GIS\Map_Library\Streets\StreetMap\Backup\StreetMap_landscape_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\StreetMap_landscape.pdf", r"I:\GIS\Map_Library\Streets\StreetMap\StreetMap_landscape.pdf")

    #StreetMap_portrait
    shutil.copy(r"I:\GIS\Map_Library\Streets\StreetMap\StreetMap_portrait.pdf", r"I:\GIS\Map_Library\Streets\StreetMap\Backup\StreetMap_portrait_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\StreetMap_portrait.pdf", r"I:\GIS\Map_Library\Streets\StreetMap\StreetMap_portrait.pdf")

    #Merge StreetMap_landscape and StreetMap_portrait into StreetMap.pdf
    pdfs = ['I:\GIS\Map_Library\Streets\StreetMap\StreetMap_Landscape.pdf', 'I:\GIS\Map_Library\Streets\StreetMap\StreetMap_Portrait.pdf']
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("I:\GIS\Map_Library\Streets\StreetMap\StreetMap.pdf")
    merger.close()
    shutil.copy(r"I:\GIS\Map_Library\Streets\StreetMap\StreetMap.pdf", r"T:\Project\Automation\Exported PDF\StreetMap.pdf")

    #Subdivision_2234
    shutil.copy(r"I:\GIS\Map_Library\CommDev\Subdivisions\Subdivision_2234.pdf", r"I:\GIS\Map_Library\CommDev\Subdivisions\Backup\Subdivision_2234_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Subdivision_2234.pdf", r"I:\GIS\Map_Library\CommDev\Subdivisions\Subdivision_2234.pdf")

    #Trail_and_sidewalk
    shutil.copy(r"I:\GIS\Map_Library\Streets\Plowing\Trail_and_sidewalk.pdf", r"I:\GIS\Map_Library\Streets\Plowing\Backup\Trail_and_sidewalk_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Trail_and_sidewalk.pdf", r"I:\GIS\Map_Library\Streets\Plowing\Trail_and_sidewalk.pdf")

    #TrailsandSidewalks
    shutil.copy(r"I:\GIS\Map_Library\Parks\Trails\Trails&Sidewalks.pdf", r"I:\GIS\Map_Library\Parks\Trails\Backup\Trails&Sidewalks_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Trails&Sidewalks.pdf", r"I:\GIS\Map_Library\Parks\Trails\Trails&Sidewalks.pdf")

##    #VotingPrecincts
##    shutil.copy(r"I:\GIS\Map_Library\Admin\Voting\Precincts1117.pdf", r"I:\GIS\Map_Library\Admin\Voting\Backup\Precincts1117_Backup.pdf")
##    shutil.copy(r"T:\Project\Automation\Exported PDF\Precincts1117.pdf", r"I:\GIS\Map_Library\Admin\Voting\Precincts1117.pdf")

    #Zoning 11x17
    shutil.copy(r"I:\GIS\Map_Library\CommDev\Zoning\Zoning11x17.pdf", r"I:\GIS\Map_Library\CommDev\Zoning\Backup\Zoning11x17_Backup.pdf")
    shutil.copy(r"T:\Project\Automation\Exported PDF\Zoning11x17.pdf", r"I:\GIS\Map_Library\CommDev\Zoning\Zoning11x17.pdf")

    print("All PDF's succesfully moved to new folders\n")

###Run the first two functions###
ExportPDFs()
MovePDFs()

###Prompt for login and password for AGOL. Used in UpdateItems Function###
#print("Enter your AGOL login and password below to update the PDF's on the website. Please QC exported maps before uploading to ensure there are no issues.\n")
#login = input("Type your login for AGOL: ")
#password = input("Type password for AGOL: ")

#This will clear the screen so it is harder to see the password that was just typed in.
printlist = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
for n in printlist:
    print(n)
    
###Update Items Function
def UpdateItems(ID,PDFNAME):
    #Check to see if login and password works.    
    try:
        gis = GIS('http://arcgis.com', "MatthewAttiyeh" , "Workin2day12345")
        logintest = gis.content.get('129b25dbd61745a5bfcff03989a89f71')
    except:
        input("The login or password you entered is incorrect. Please verify your credentials. Press enter to close window.")

    #Search for the item and replace it with a pdf
        
    props = {
        "type":"PDF",
        "overwrite":True
        }

    GetContent = gis.content.get(ID)
    GCdata = os.path.join('T:\\Project\\Automation\\Exported PDF\\' + PDFNAME)
    print("\nReplacing Item: " + str(GetContent))
    GetContent.update(item_properties=props, data=GCdata)
    print("Uploaded pdf from this file: " + str(GCdata))
    
###Run Update Items Function###
print("Uploading PDF's to website\n")
UpdateItems('129b25dbd61745a5bfcff03989a89f71','Subdivision_2234.pdf')
UpdateItems('beb6c64dd6e148b7aa125ef5a3dc7cf2','Precincts1117.pdf')
UpdateItems('76ad333eef594873905a188115803c19','2019_Street_Lights_Inventory_1117.pdf')
UpdateItems('5541baad03b748909da95a377b59f7f1','Address_Base_Map_42x42.pdf')
UpdateItems('7d64fa8c3dbd43ad8e6117278529852a','Trails&Sidewalks.pdf')
UpdateItems('23e6b3dce36140609c22a8067ad3c8e6','StreetMap.pdf')
UpdateItems('c70a970271714c83a2beb8ff032f8258','Trail_and_Sidewalk.pdf')
UpdateItems('209a6424b67b4871b854c53c4edad68d','Priority_Routes.pdf')
UpdateItems('690524b1cb244f7f97aacb6847f184e3','Quiet_Zone11_17.pdf')
UpdateItems('26554a6f4de24a37a53fb9c2765430c5','Electric_Service_Area.pdf')
UpdateItems('1593c9997e7f4d3f82df5090d11bc1e6','Natural_Gas_Service_Areas.pdf')
UpdateItems('e786e57401024e6699dc9b35517f25fb','CurrentConstructionProjects.pdf')
UpdateItems('04f50dd6f1b141b8b27046bbb527fdec','Adopt_A_Street_Program.pdf')
UpdateItems('8f601035cf564c4d840e5b2b6e66fd60','Land_Use_Comp_Plan_11x17.pdf')
UpdateItems('86370be195154bc3a39a69072b7de92d','Zoning11x17.pdf')
UpdateItems('92df70e86f4048629319177e20679e2d','Street_Weight_Restrictions_Map.pdf')
UpdateItems('23efd966c0764b92882455d06a7207f3','ParkAmenities11x17.pdf')
UpdateItems('7a8edd29d415402480ba437a0e9745a2','City_of_Rosemount_Bicycle_Facilities_Bike_Racks_2.pdf')

