####Check the As built folder for PDF's and if there are new ones in there copy them to the as built folder in the Locate Request Folder

import os, pdfkit, pathlib, glob, shutil

#Main As built folder
AsBuiltFolder = "A:\\"

#As built folder in Locate request folder. Copy new as builts to here
LocateAsBuilts = "T:\\Project\\LocateRequestsNew\\asbuilts\\"

#list of the as built files in locate request folder to compare AsBuiltFolder to
LocateABList = []

#Search through the LocateAsBuilts folder on the T: drive and make a list of all the PDFs in there
for subdir, dirs, files in os.walk(LocateAsBuilts):
    for filename in files:
        LocateABList.append(filename)
        
#Search through the main As Built folder and compare the files in there to the list created above. If there are files in the
#main folder that are not in the T: drive folder then copy them over.
for subdir, dirs, files in os.walk(AsBuiltFolder):
    if subdir == AsBuiltFolder:
        for filename in files:
            if filename not in LocateABList:
                shutil.copyfile(AsBuiltFolder + filename, LocateAsBuilts + filename)
                print(filename)
