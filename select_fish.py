import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from utils import cleanfile,delete_pic
import glob
from calibration.undistort import undistort


from main import MainWindow
class StereoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.num = 0
        self.imagesFish = sorted(glob.glob('calibration/img_calib/img_fisheye_stereo/*.png'))
        self.deleteFish=[]
        self.overlayDelete = cv2.imread('deleted.png')

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



    def update(self):
        frame1 = cv2.imread(self.imagesFish[self.num])

        chessboardSize=(8,6)

        imgR = undistort(frame1)

        grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        retR, cornersR = cv2.findChessboardCorners(grayR, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        
        if retR == True :
            cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)

        if self.imagesFish[self.num] in self.deleteFish:
            opacity = 0.4
            imgR = cv2.addWeighted(self.overlayDelete, opacity, imgR, 1 - opacity, 0)

        rgbImage1 = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)
        h1, w1, ch1 = rgbImage1.shape
        bytesPerLine1 = ch1 * w1
        qImg1 = QImage(rgbImage1.data, w1, h1, bytesPerLine1, QImage.Format_RGB888)
        pixmap1 = QPixmap.fromImage(qImg1)
        self.label1.setPixmap(pixmap1.scaled(360, 270))

    def previous(self):
        if self.num != 0:
            self.num+=1
    def next(self):
        if self.num != len(self.imagesFish):
            self.num-=1
    def delete(self):
        if self.imagesFish[self.num] not in self.deleteFish:
            self.deleteRight.append(self.imagesFish[self.num])
    def remove(self):
        if self.imagesFish[self.num] in self.deleteFish:
            self.deleteRight.remove(self.imagesFish[self.num])
        
    def validate(self):
        for right in self.deleteFish:
            delete_pic(right)
        main = MainWindow()
        main.show()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
