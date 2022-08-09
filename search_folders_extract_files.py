#https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil

import os, pdfkit, pathlib, glob, shutil
from PIL import Image

#Change the search folder and target folder variables to the folders you want to search through and send the files to.
#Change the substring to the word or phrase you are looking for. Use all caps!!!!
#Change the fileType variable to the filetype extension you are looking for


#variables
search = "C:\\Users\\mka\\Desktop\\GradingPermits\\"
target = "C:\\Users\\mka\\Desktop\\Gradingpermitsnarrow\\"
substring = "APPLICATION" #Use all caps!!!!
substring2 = "COPY"
fileType = ".pdf"

for subdir, dirs, files in os.walk(search):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filename.endswith(fileType):
            if substring not in filename.upper() and substring2 not in filename.upper():
                print(filename)
                print(filepath)
                shutil.copyfile(filepath, target + filename)


