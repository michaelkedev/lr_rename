import json
from pyexiv2 import Image

files = os.listdir("./")
for file in files:
    if ".jpg" in file:
        print(f"------------------{file}----------------")
        img = Image(file)
        xmpdata = img.read_xmp()

        img.close()

        print(xmpdata["Xmp.xmp.Rating"])
