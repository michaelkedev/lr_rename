import os
from pyexiv2 import Image

image_format = ("jpg", "jpeg", "png")


def get_rating(jpg_file):
    if jpg_file.lower().endswith(image_format):
        # print(jpg_file)
        img = Image(jpg_file)
        xmp_data = img.read_xmp()
        img.close()

        return xmp_data["Xmp.xmp.Rating"]


files = os.listdir("./")
for file in files:
    print(get_rating(file))
