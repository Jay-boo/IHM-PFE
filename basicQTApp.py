import sys
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qt app")
        self.setFixedSize(QSize(400,300))
        button=QPushButton("push button")
        self.setCentralWidget(button)

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()
