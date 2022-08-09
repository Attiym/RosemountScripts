#### This script will copy from the as-built drive to a new folder based on what shows up in the locate.
#### Run script and enter the name of the folder you want to create.
#### Make sure to update the xlf, original, os.mkdir, and target file paths depending on whose computer it is running on.
#### There is a limit of 500mb worth of PDF's that can be run at one time.

import os, shutil, arcpy

###Variables for getting map selection into a list
fc = "Plan Areas"
field = "Comments"
cursor = arcpy.SearchCursor(fc)
PdfList = []

###Takes the current selection of plan areas and puts them into a list
for row in cursor:
    Output = (row.getValue(field))
    PdfList.append(Output)
    #print(Output)

###Varibales for use later. Show the number of plan areas selected.    
NumPDFSelected=len(PdfList)
NumPDFSelectedstr = str(NumPDFSelected)

###This will ask you what you want to name the new folder. Recommended name is ticket #.
NewFolder = input("Type the name of your new folder. Recommended name is the ticket number from the locate request. ")

###This sets the folder to copy the as-builts from. Replace everything inside the quotes
original = "C:\\Users\\mka\\Desktop\\asbuilts\\"

###This creates the new folder from above and sets the script to place the as-builts in that folder.
os.mkdir('C:\\Users\mka\\Desktop\\' + NewFolder)
target = 'C:\\Users\mka\\Desktop\\' + NewFolder + '\\'

###This runs the code to copy and paste the files from above into their correct location.
###Set up to ignore the error of not finding certain pdf's

try:
    for pdf_name in PdfList:
        shutil.copyfile(original + pdf_name, target + pdf_name)
    print('\n' + "New folder with requested pdf's created at this location: " + target + "\n\nThere should be " + NumPDFSelectedstr + " PDF's in the folder." + '\n')

except:
    ###Looks is export folder and counts the actual number of PDF's that got exported.
    PdfsExported=os.listdir(target)
    NumExportedPdfs = len(PdfsExported)
    NumExportedPdfsstr = str(NumExportedPdfs)
    
    ###creates a variable that subtracts the actual number of PDF's in the new folder from the amount of plan areas selected.
    NotCopied = str(NumPDFSelected - NumExportedPdfs)
    
    ###Display an output that says some were not able to get copied and display how many could not copy.
    print('\n' + "New folder with requested pdf's created at this location: " + target + '\n')
    print("!!!!I noticed I wasn't able to copy over all the files!!!!")
    print("\nThere are some as-builts that you selected that I cannot find in the as-builts folder!")
    print("\nThere should be " + NumPDFSelectedstr + " PDF's in your new folder but a total of " + NotCopied + " PDF's were not found in the as-built folder.\n\nSee list of PDF's not copied below:\n")
    
    ###Show a list of the PDF's that could not get copied.
    for PDFs in PdfList:
        if PDFs not in PdfsExported:
            print(PDFs)
