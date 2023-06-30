import os
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt6 import uic

image_format = ("jpg", "jpeg", "png")


class MyApp(QWidget):
    def __init__(self):
        self.img_path = "./images/"

        super().__init__()

        self.setWindowTitle("Python QLabel")
        self.setWindowIcon(QIcon("icons/icon.png"))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  #  left, top, right, bottom
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        files = os.listdir(self.img_path)
        photos_per_row, photo_count = 3, 0
        photo_layout = self.imgLayout()
        for file in files:
            # to-do feature : set the number of photos per row
            print(file)
            if file.lower().endswith(image_format):
                img_label = self.loadImg(file)

                photo_layout.addWidget(img_label)
                photo_count += 1

                if photo_count % photos_per_row == 0:
                    main_layout.addLayout(self.blockName())
                    main_layout.addLayout(photo_layout)
                    photo_layout = self.imgLayout()

        self.setLayout(main_layout)

    def blockName(self):
        block_layout = QVBoxLayout()
        block_layout.setSpacing(0)

        block_name = QLabel("Block Name")
        block_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        block_name.setFont(QFont("Arial", 13, QFont.Weight.Bold))

        block_layout.addWidget(block_name)
        block_layout.setContentsMargins(5, 0, 5, 0)

        return block_layout

    def imgLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return layout

    def loadImg(self, file_name):
        label = QLabel(self)

        origin_image = QPixmap(f"{self.img_path}{file_name}")
        scale_image = origin_image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        label.setPixmap(scale_image)

        return label


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget{
            font-size: 12px;
        }
    """
    )

    myApp = MyApp()

    myApp.showMaximized()

    try:
        sys.exit(app.exec())

    except SystemExit:
        print("Closing Window")
