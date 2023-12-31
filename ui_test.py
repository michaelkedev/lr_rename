import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
from PyQt6.QtGui import QIcon

print("test branch")
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setWindowIcon(QIcon("./icons/icon.png"))
        self.resize(300, 200)  # width and height

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputField = QLineEdit()
        button = QPushButton("&Say Hello", clicked=self.say_hello)
        # button.clicked.connect(self.sayHello)
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)

    def say_hello(self):
        inputText = self.inputField.text()
        self.output.setText(f"Hello {inputText}")


app = QApplication(sys.argv)
app.setStyleSheet(
    """
        QWidget{
            font-size : 25px;
        }

        QPushButton{
            font-size : 20px;
        }
    """
)

window = MyApp()
window.show()

app.exec()
