import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from utils import cleanfile,delete_pic
import glob
from main import MainWindow
class StereoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.num = 0
        self.imagesRight = sorted(glob.glob('calibration/img_calib/img_fisheye_stereo/*.png'))
        self.imagesLeft = sorted(glob.glob('calibration/img_calib/img_infra_stereo/*.png'))

        self.deleteRight=[]
        self.deleteLeft=[]


    def initUI(self):
        # Create a layout for the buttons on the left
        vbox1 = QVBoxLayout()
        button0 = QPushButton('Previous')
        button0.clicked.connect(self.previous)
        button1 = QPushButton('Next')
        button1.clicked.connect(self.next)
        button2 = QPushButton('Delete')
        button2.clicked.connect(self.delete)
        button3 = QPushButton('Undelete')
        button3.clicked.connect(self.undo)
        button4 = QPushButton('Validate selection')
        button4.clicked.connect(self.validate)

        vbox1.addWidget(button0)
        vbox1.addWidget(button1)
        vbox1.addWidget(button2)
        vbox1.addWidget(button3)
        vbox1.addWidget(button4)




        # Create a layout for the video flux spaces
        hbox2 = QHBoxLayout()
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        hbox2.addWidget(self.label1)
        hbox2.addWidget(self.label2)

        # Create a layout to combine the buttons and video flux spaces
        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(hbox2)

        self.setLayout(hbox1)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('PyQt with OpenCV video flux spaces')

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        self.cap1 = cv2.VideoCapture(0) # FISH
        self.cap2 = cv2.VideoCapture(1)


    def update(self):
        frame1 = cv2.imread(self.imagesRight[self.num])
        frame2 = cv2.imread(self.imagesLeft[self.num])

        rgbImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        h1, w1, ch1 = rgbImage1.shape
        bytesPerLine1 = ch1 * w1
        qImg1 = QImage(rgbImage1.data, w1, h1, bytesPerLine1, QImage.Format_RGB888)
        pixmap1 = QPixmap.fromImage(qImg1)
        self.label1.setPixmap(pixmap1.scaled(360, 270))



        rgbImage2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        h2, w2, ch2 = rgbImage2.shape
        bytesPerLine2 = ch2 * w2
        qImg2 = QImage(rgbImage2.data, w2, h2, bytesPerLine2, QImage.Format_RGB888)
        pixmap2 = QPixmap.fromImage(qImg2)
        self.label2.setPixmap(pixmap2.scaled(360, 270))

    def previous(self):
        if self.num != 0:
            self.num+=1
    def next(self):
        if self.num != len(self.imagesRight):
            self.num-=1
    def delete(self):
        if self.imagesRight[self.num] not in self.deleteRight:
            self.deleteRight.append(self.imagesRight[self.num])
            self.deleteLeft.append(self.imagesLeft[self.num])
    def remove(self):
        if self.imagesRight[self.num] in self.deleteRight:
            self.deleteRight.remove(self.imagesRight[self.num])
            self.deleteLeft.remove(self.imagesLeft[self.num])
        
    def validate(self):
        for right,left in zip(self.deleteRight,self.deleteLeft):
            delete_pic(right)
            delete_pic(left)
        main = MainWindow()
        main.show()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
