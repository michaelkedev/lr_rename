import os
import sys
import math
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
    QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QScreen
from PyQt6 import uic

image_format = ("jpg", "jpeg", "png")

title_name = ["A", "B", "C", "D", "E", "F"]  # 5 --> 0


class MyQLabel(QLabel):
    def __init__(self, rating):
        super().__init__(str(rating))
        self.rating = rating

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            line_edit = QLineEdit(self.text(), self.parent())
            line_edit.setGeometry(self.geometry())
            line_edit.setStyleSheet(self.styleSheet())
            line_edit.setFocus()
            line_edit.editingFinished.connect(self.handleEditingFinished)
            self.hide()
            line_edit.show()

    def handleEditingFinished(self):
        line_edit = self.sender()
        new_text = line_edit.text()
        title_name[5 - self.rating] = new_text
        self.setText(new_text)
        self.show()
        line_edit.deleteLater()

        print(title_name)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setWindowTitle("Python QLabel")
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setMaximumWidth(1520)
        self.setMinimumWidth(1520)
        self.setMaximumHeight(monitorInfo.getWorkAreaHeight() - 32)
        self.setMinimumHeight(monitorInfo.getWorkAreaHeight() - 32)
        self.picture_list = []
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

        layout = QVBoxLayout()
        layout.setSpacing(10)

        for score in range(0, 6):
            layout.addLayout(
                self.galleryLayout(
                    self.ratingFilter(5 - score, self.getPictureList("./images"))
                )
            )

        scroll_area = self.scollArea(layout)

        main_layout.addWidget(scroll_area)

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

    def ratingFilter(self, score, picture_list):
        return list(filter(lambda x: (x.getRating() == score), picture_list))

    def getPictureList(self, path="./images/"):
        self.picture_list = []
        files = os.listdir(path)

        for file in files:
            picture_info = self.PictureInfo(f"{path}/{file}")
            self.picture_list.append(picture_info)

        return self.picture_list

    def galleryLayout(self, picture_list=[]):
        gallery_layout = QVBoxLayout()
        gallery_layout.setContentsMargins(0, 0, 0, 0)
        gallery_layout.setSpacing(0)

        rating = picture_list[0].getRating()

        file_count = QLabel(f"{len(picture_list)} 個項目")
        file_count.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        file_count.setStyleSheet(
            "font-weight:normal; font-size: 14px;  border: 0px; color: #696969"
        )

        title = MyQLabel(rating)

        title.setContentsMargins(20, 0, 0, 0)
        # title.setFixedSize(1486, 50)  # width, height
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("border: 0px")
        # title.setText

        title_bar_layout = QHBoxLayout()
        title_bar_layout.addWidget(title)
        title_bar_layout.addWidget(file_count)

        title_bar_widget = QWidget()
        title_bar_widget.setLayout(title_bar_layout)
        title_bar_widget.setFixedSize(1486, 50)
        title_bar_widget.setStyleSheet(
            "background-color: #292929; color : white; font-weight:black; font-size: 20px;border:1px solid #696969"
        )

        # title = self.starWidget(picture_list[0].getRating())
        # title.setFixedHeight(10)

        img_layout = QGridLayout()
        img_layout.setSpacing(0)
        img_layout.setContentsMargins(0, 0, 0, 0)

        row, column = 0, 0
        for i in range(0, math.ceil(len(picture_list) / 5) * 5):
            if i < len(picture_list):
                picture = picture_list[i]
                widget = self.imgWidget(picture.getFileName())
            else:
                widget = QWidget()
                widget.setFixedWidth(300)
                widget.setFixedHeight(400)
                # widget.setContentsMargins(2, 2, 2, 2)
                if i == len(picture_list):
                    widget.setStyleSheet("border-left: 1px solid #696969")

            img_layout.addWidget(widget, row, column)

            column += 1
            if column == 5:
                row += 1
                column = 0  # row, column = 0, 0

        gallery_layout.addWidget(title_bar_widget)
        gallery_layout.addLayout(img_layout)

        return gallery_layout

    def imgWidget(self, file_name):
        widget = QWidget()
        widget.setFixedWidth(296)
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
        rating.setFixedSize(296, 50)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(widget)
        outer_layout.addWidget(rating, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.setContentsMargins(2, 2, 2, 2)

        outer_box = QWidget()
        outer_box.setLayout(outer_layout)
        outer_box.setFixedWidth(300)
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

    my_app_id = "michael.lr_rename.v1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    myApp = MyApp()

    myApp.showMaximized()
    try:
        sys.exit(app.exec())

    except SystemExit:
        print("Closing Window")
