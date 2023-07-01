# import os
# from pyexiv2 import Image

# image_format = ("jpg", "jpeg", "png")


# def get_rating(jpg_file):
#     if jpg_file.lower().endswith(image_format):
#         # print(jpg_file)
#         img = Image(jpg_file)
#         xmp_data = img.read_xmp()
#         img.close()

#         return xmp_data["Xmp.xmp.Rating"]


# files = os.listdir("./")
# for file in files:
#     print(get_rating(file))

from exif import Image
import piexif
import struct

# with open("./images/01.jpg", "rb") as f:
#     my_image = Image(f)

#     qp = QPixmap()
#     qp.loadFromData(my_image.get_thumbnail())


piexif_dict = piexif.load("./images/01.jpg")
piexif_dict_byte = piexif.dump(piexif_dict)
print(piexif_dict_byte)

# b = piexif_dict["Exif"][18246]
# count = len(b) / 2
# rating = struct.unpack("H" * int(count), b)
# print(rating)
