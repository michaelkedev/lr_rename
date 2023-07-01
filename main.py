import os
from pyexiv2 import Image
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt6 import uic

image_format = ("jpg", "jpeg", "png")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setWindowTitle("Python QLabel")
        self.setWindowIcon(QIcon("icons/icon.png"))

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

        scroll_area_plan = QWidget()
        scroll_area_plan.setLayout(gallery_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidget(scroll_area_plan)
        scroll_area.setStyleSheet("background-color:white;")

        main_layout.addWidget(scroll_area)
        # main_layout.addLayout(gallery_layout)

        self.setLayout(main_layout)

    def isImage(self, file):
        return file.lower().endswith(image_format)

    def galleryLayout(self):
        gallery_layout = QVBoxLayout()
        gallery_layout.setContentsMargins(0, 0, 0, 0)
        gallery_layout.setSpacing(0)

        title = QLabel("Images")
        title.setContentsMargins(20, 0, 0, 0)
        title.setFixedSize(1500, 50)  # width, height
        # title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title.setText
        title.setStyleSheet(
            "background-color: #1A1A1A; color : white; font-weight:black; font-size: 20px"
        )
        # title.setFixedHeight(10)

        img_layout = QGridLayout()
        img_layout.setSpacing(0)
        img_layout.setContentsMargins(0, 0, 0, 0)

        files = os.listdir("./images")

        row, column = 0, 0
        for file in files:
            img_layout.addWidget(self.imgWidget(f"./images/{file}"), row, column)
            column += 1
            print()
            if column == 3:
                row += 1
                column = 0
            # img_layout.addWidget(img_label, row, column)

        gallery_layout.addWidget(title)
        gallery_layout.addLayout(img_layout)

        return gallery_layout

    #
    def imgWidget(self, img):
        widget = QWidget()
        widget.setFixedWidth(300)
        widget.setFixedHeight(350)
        widget.setStyleSheet("border: 0px")

        _img = self.loadImg(img)
        _img.setStyleSheet("border: 0px")

        img_layout = QHBoxLayout()
        img_layout.setContentsMargins(10, 10, 10, 10)  #  left, top, right, bottom
        img_layout.addWidget(_img, alignment=Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(img_layout)

        rating = self.starWidget(self.readRating(img))
        rating.setStyleSheet("color:black; border: 0px")
        rating.setFixedSize(300, 50)

        outerLayout = QVBoxLayout()
        outerLayout.addWidget(widget)
        outerLayout.addWidget(rating, alignment=Qt.AlignmentFlag.AlignCenter)
        outerLayout.setContentsMargins(2, 2, 2, 2)

        outerBox = QWidget()
        outerBox.setLayout(outerLayout)
        outerBox.setFixedWidth(303)
        outerBox.setFixedHeight(400)
        outerBox.setStyleSheet("background-color: #1A1A1A; border: 1px solid #696969;")

        return outerBox

    def starWidget(self, rating):
        starLayout = QHBoxLayout()
        starBox = QWidget()
        starBox.setLayout(starLayout)

        starLayout.addStretch(1)

        for i in range(1, 6):
            imgSrc = 1 if i <= rating else 0

            self.starResourceList = [
                self.loadImg("./icons/star_empty.png", w=16, h=16),
                self.loadImg("./icons/star.png", w=16, h=16),
            ]

            starLayout.addWidget(
                self.starResourceList[imgSrc], alignment=Qt.AlignmentFlag.AlignCenter
            )
            starLayout.addStretch(0)

        starLayout.addStretch(1)

        return starBox

    def loadImg(self, file, w=300, h=350):
        # print(f"Loading image {file}")
        label = QLabel(self)

        origin_image = QPixmap(f"{file}")
        scale_image = origin_image.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )  # width, height
        label.setPixmap(scale_image)

        return label

    def readRating(self, file):
        if self.isImage(file):
            # print(jpg_file)
            img = Image(file)
            xmp_data = img.read_xmp()
            img.close()
        print(int(xmp_data["Xmp.xmp.Rating"]))
        return int(xmp_data["Xmp.xmp.Rating"])


class TestAPP(QWidget):
    def __init__(self):
        super().__init__()

        # Create a main widget and set it as the central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a QVBoxLayout for the main layout
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Create a QTextEdit widget
        text_edit = QTextEdit()
        main_layout.addWidget(text_edit)

        # Append some text to the QTextEdit
        text_edit.append("Line 1")
        text_edit.append("Line 2")
        text_edit.append("Line 3")
        text_edit.append("Line 4")

        # Scroll down programmatically
        scroll_bar = text_edit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myApp = MyApp()

    myApp.showMaximized()
    try:
        sys.exit(app.exec())

    except SystemExit:
        print("Closing Window")
