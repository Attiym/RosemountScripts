#https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil

import os, pdfkit, pathlib
from PIL import Image


for subdir, dirs, files in os.walk("T:\\Project\\Automation\\images"):
    for filename in files:
        filepath = subdir + os.sep + filename
        #print(filename)
        #print(filepath)


        #Open Jpeg
        PavementImg = Image.open(filepath)
        # I downsize the image with an ANTIALIAS filter (gives the highest quality)
        PavementImg = PavementImg.resize((2000,1500),Image.ANTIALIAS)
        PavementImg.save(filepath,quality=55)
        # The saved downsized image size is 24.8kb
        #foo.save("T:\\Project\\Automation\\images\\test2.jpg",optimize=True,quality=75)
        # The saved downsized image size is 22.9kb

