import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from utils import cleanfile

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.num = 0
        self.colorfish=cv2.COLOR_BGR2RGB

    def initUI(self):
        # Create a layout for the buttons on the left
        vbox1 = QVBoxLayout()
        button0 = QPushButton('Clean Picture file')
        button0.clicked.connect(self.clean_file)
        button1 = QPushButton('Take Picture')
        button1.clicked.connect(self.capture_images)
        button2 = QPushButton('Button 2')
        button2.clicked.connect(self.mono)
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')
        button5 = QPushButton('Button 5')
        vbox1.addWidget(button0)
        vbox1.addWidget(button1)
        vbox1.addWidget(button2)
        vbox1.addWidget(button3)
        vbox1.addWidget(button4)
        vbox1.addWidget(button5)

        # Create a layout for the video flux spaces
        hbox2 = QHBoxLayout()
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        hbox2.addWidget(self.label1)
        hbox2.addWidget(self.label2)
        hbox2.addWidget(self.label3)

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

        self.cap1 = cv2.VideoCapture(2) # FISH
        self.cap2 = cv2.VideoCapture(0)


    def update(self):
        ret1, frame1 = self.cap1.read()
        if ret1:
            # Display the video flux
            frame1 = cv2.cvtColor(frame1, self.colorfish)
            rgbImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            h1, w1, ch1 = rgbImage1.shape
            bytesPerLine1 = ch1 * w1
            qImg1 = QImage(rgbImage1.data, w1, h1, bytesPerLine1, QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(qImg1)
            self.label1.setPixmap(pixmap1.scaled(720, 540))

        ret2, frame2 = self.cap2.read()
        if ret2:

            rgbImage2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            h2, w2, ch2 = rgbImage2.shape
            bytesPerLine2 = ch2 * w2
            qImg2 = QImage(rgbImage2.data, w2, h2, bytesPerLine2, QImage.Format_RGB888)
            pixmap2 = QPixmap.fromImage(qImg2)
            self.label2.setPixmap(pixmap2.scaled(240, 180))


    def capture_images(self):
        ret1, img = self.cap1.read()
        ret2, img2 = self.cap2.read() 
        if ret1 and ret2:
            cv2.imwrite('calibration/img_calib/img_fisheye3/imageINF' + str(self.num) + '.png', img)
            cv2.imwrite('calibration/img_calib/img_infra3/imageFISH'+ str(self.num) + '.png', img2)
            print("images saved!")
            self.num +=1
            
    def clean_file(self):
        cleanfile('calibration/img_calib/img_fisheye3/')
        cleanfile('calibration/img_calib/img_infra3/')
        
    def mono(self):
        if self.colorfish == cv2.COLOR_BGR2GRAY:
                self.colorfish=cv2.COLOR_BGR2RGB
        else:
                self.colorfish=cv2.COLOR_BGR2GRAY



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
