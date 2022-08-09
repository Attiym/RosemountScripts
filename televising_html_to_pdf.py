#### This script will go through a specified folder in the televising drive
#### and search for html documents that are called plot.html and convert them to
#### a pdf document that can be uploaded into cartegrapgh.

import os, pdfkit, pathlib

#Variables
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#Input for the televising folder
folder = input("What is the name of the project folder in the Televising Drive? ")

#Search the folder in the televising drive from above and create variables.
#If it finds anyhting called plot.html it will convert to a pdf and give it
#the name of the folder it is in.

for subdir, dirs, files in os.walk('z:\\' + folder):
    for filename in files:
        filepath = subdir + os.sep + filename
        foldername = pathlib.PurePath(filepath)
        pdfname = foldername.parent.parent.name
        filepath_out = subdir + os.sep + pdfname + ".pdf"
        
        
        if filepath.endswith("Plot.html"):
            pdfkit.from_file(filepath, filepath_out, configuration=config)
            print ("\nConverted HTML document to PDF in this file location: " + filepath_out + "\n")
            
        elif filepath.endswith("plot.html"):
            pdfkit.from_file(filepath, filepath_out, configuration=config)
            print ("\nConverted HTML document to PDF in this file location: " + filepath_out + "\n")
input()


