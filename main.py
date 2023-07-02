import os
import sys
import monitorInfo
import ctypes
from pyexiv2 import Image
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QScreen
from PyQt6 import uic

image_format = ("jpg", "jpeg", "png")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setWindowTitle("Python QLabel")
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setMaximumWidth(1500)
        self.setMinimumWidth(1500)
        self.setMaximumHeight(monitorInfo.getWorkAreaHeight() - 32)
        self.setMinimumHeight(monitorInfo.getWorkAreaHeight() - 32)

        # self.starResourceList = [
        #     self.loadImg("./icons/star_empty.png", w=16, h=16),
        #     self.loadImg("./icons/star.png", w=16, h=16),
        # ]
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  #  left, top, right, bottom
        main_layout.setSpacing(0)
        main_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        gallery_layout = self.galleryLayout()
        scroll_area = self.scollArea(gallery_layout)

        main_layout.addWidget(scroll_area)
        # main_layout.addLayout(gallery_layout)

        self.setLayout(main_layout)

    def scollArea(self, layout):
        scroll_area_plan = QWidget()
        scroll_area_plan.setLayout(layout)
        scroll_area_plan.setFixedWidth(1500)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_area_plan)
        # scroll_area.setStyleSheet("background-color:white;")

        return scroll_area

    def ratingFilter(self, score):
        return filter(lambda x: (x.getRating() == score), self.picture_list)

    def galleryLayout(self):
        gallery_layout = QVBoxLayout()
        gallery_layout.setContentsMargins(0, 0, 0, 0)
        gallery_layout.setSpacing(0)

        title = QLabel("Score")
        title.setContentsMargins(20, 0, 0, 0)
        title.setFixedSize(1500, 50)  # width, height
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title.setText
        title.setStyleSheet(
            "background-color: #1A1A1A; color : white; font-weight:black; font-size: 20px"
        )
        # title.setFixedHeight(10)

        img_layout = QGridLayout()
        img_layout.setSpacing(0)
        img_layout.setContentsMargins(0, 0, 0, 0)

        files = os.listdir("./images")
        self.picture_list = []

        # even_numbers_iterator = filter(lambda x: (x%2 == 0), numbers)
        for file in files:
            picture_info = self.PictureInfo(f"./images/{file}")
            self.picture_list.append(picture_info)

        row, column = 0, 0
        for file_name in files:
            img_layout.addWidget(self.imgWidget(f"./images/{file_name}"), row, column)
            column += 1
            print()
            if column == 5:
                row += 1
                column = 0
            # img_layout.addWidget(img_label, row, column)

        gallery_layout.addWidget(title)
        gallery_layout.addLayout(img_layout)

        return gallery_layout

    def imgWidget(self, file_name):
        widget = QWidget()
        widget.setFixedWidth(300)
        widget.setFixedHeight(350)
        widget.setStyleSheet("border: 0px")

        _img, _rating = self.loadImg(file_name)
        _img.setStyleSheet("border: 0px")

        img_layout = QHBoxLayout()
        img_layout.setContentsMargins(10, 10, 10, 10)  #  left, top, right, bottom
        img_layout.addWidget(_img, alignment=Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(img_layout)

        rating = self.starWidget(_rating)
        rating.setStyleSheet("color:black; border: 0px")
        rating.setFixedSize(300, 50)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(widget)
        outer_layout.addWidget(rating, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.setContentsMargins(2, 2, 2, 2)

        outer_box = QWidget()
        outer_box.setLayout(outer_layout)
        outer_box.setFixedWidth(303)
        outer_box.setFixedHeight(400)
        outer_box.setStyleSheet("background-color: #1A1A1A; border: 1px solid #696969;")

        return outer_box

    def starWidget(self, rating):
        star_layout = QHBoxLayout()
        star_box = QWidget()
        star_box.setLayout(star_layout)

        star_layout.addStretch(1)

        for i in range(1, 6):
            imgSrc = 1 if i <= rating else 0

            self.star_resourceList = [
                self.loadImg("./icons/star_empty.png", w=16, h=16, is_picture=False),
                self.loadImg("./icons/star.png", w=16, h=16, is_picture=False),
            ]

            star_layout.addWidget(
                self.star_resourceList[imgSrc], alignment=Qt.AlignmentFlag.AlignCenter
            )
            star_layout.addStretch(0)

        star_layout.addStretch(1)

        return star_box

    def loadImg(self, file_name, w=300, h=350, is_picture=True):
        # print(f"Loading image {file_name}")

        img_data = file_name
        rating = 0

        qpixmap = QPixmap()

        if is_picture:
            picture = self.PictureInfo(file_name)
            img_data = picture.getThumbnail()
            rating = picture.getRating()
            qpixmap.loadFromData(img_data)

        else:
            qpixmap.load(img_data)

        label = QLabel(self)

        qpixmap.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )  # width, height
        label.setPixmap(qpixmap)

        if is_picture:
            return label, rating
        else:
            return label

    class PictureInfo:
        def __init__(self, file_name):
            self.file_name = file_name
            if self.isImage(file_name):
                self.imgData = Image(file_name)

        def getFileName(self):
            return self.file_name

        def getThumbnail(self):
            # my_image = exifImage(self.imgData)
            return self.imgData.read_thumbnail()

        def getRating(self):
            xmp_data = self.imgData.read_xmp()
            # print(f"xmpdata {xmp_data['Xmp.xmp.Rating']}")
            print(
                int(xmp_data["Xmp.xmp.Rating"]) if "Xmp.xmp.Rating" in xmp_data else 0
            )
            return (
                int(xmp_data["Xmp.xmp.Rating"]) if "Xmp.xmp.Rating" in xmp_data else 0
            )

        def isImage(self, file_name):
            return file_name.lower().endswith(image_format)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(sys.argv)

    my_app_id = "michael.lr_rename.v1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    myApp = MyApp()

    myApp.showMaximized()
    try:
        sys.exit(app.exec())

    except SystemExit:
        print("Closing Window")
