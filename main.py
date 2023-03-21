import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer,Qt
from utils import cleanfile,delete_pic
from calibration.undistort import undistort
from calibration.project_image import project_image
from calibration.calibration_stereo import calibrate_camera
from calibration.calib_fish import calib_fish
from select_stereo import StereoWindow
from select_fish import FishWindow
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.num_stereo = 0
        self.num_fish = 0
        self.undist=False
        self.seeresult=False
        #self.opacity = 0.4
        self.overlay = []
        self.overlayall =[]
        self.overlaycorners = []
        self.overlayborders = []
        self.numoverlay = 0


    def initUI(self):
        # Create a layout for the buttons on the left
        vbox1 = QVBoxLayout()
        button0 = QPushButton('Fish - Clean Pictures file')
        button0.clicked.connect(self.clean_file_fish)
        button1 = QPushButton('Fish - Take Picture')
        button1.clicked.connect(self.capture_image_fish)
        button2 = QPushButton('Fish - Select images')
        button2.clicked.connect(self.select_fish)
        button3 = QPushButton('Fish - Execute calibration')
        button3.clicked.connect(self.exec_fishcalib)
        button4 = QPushButton('Fish - Undistort video')
        button4.clicked.connect(self.see_unidst)


        button5 = QPushButton('Stereo - Clean Pictures files')
        button5.clicked.connect(self.clean_file_stereo)
        button6 = QPushButton('Stereo - Take Pictures')
        button6.clicked.connect(self.capture_images)
        button7 = QPushButton('Stereo - Select images')
        button7.clicked.connect(self.select_stereo)
        button8 = QPushButton('Stereo - Execute stereo calibration')
        button8.clicked.connect(self.exec_stereocalib)
        button9 = QPushButton('Stereo - See result')
        button9.clicked.connect(self.see_result)

        self.bal = QSlider(Qt.Horizontal)
        self.bal.setMinimum(0)
        self.bal.setMaximum(100)
        self.bal.setValue(0)
        self.bal_text = QLabel("Balance")

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(40)
        self.opa = QLabel("Opacity")
        
        vbox1.addWidget(button0)
        vbox1.addWidget(button1)
        vbox1.addWidget(button2)
        vbox1.addWidget(button3)
        vbox1.addWidget(button4)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.bal_text)
        hbox4.addWidget(self.bal)
        vbox1.addLayout(hbox4)

        vbox1.addWidget(button5)
        vbox1.addWidget(button6)
        vbox1.addWidget(button7)
        vbox1.addWidget(button8)
        vbox1.addWidget(button9)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.opa)
        hbox3.addWidget(self.sl)
        vbox1.addLayout(hbox3)

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
        self.setWindowTitle('App')

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        self.cap1 = cv2.VideoCapture(0) # FISH
        self.cap2 = cv2.VideoCapture(1)


    def update(self):
        self.opacity = self.sl.value()/100
        self.balance = self.bal.value()/100
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()
        if ret1:
            # Display the video flux
            # frame1 = cv2.cvtColor(frame1, self.colorfish)
            if self.numoverlay != 0 and ret2:
                frame1=undistort(frame1)
                frame1 = cv2.addWeighted(self.overlay, self.opacity, frame1, 1 - self.opacity, 0)
            if self.undist and self.numoverlay == 0:
                frame1=undistort(frame1, balance=self.balance)
            rgbImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            h1, w1, ch1 = rgbImage1.shape
            bytesPerLine1 = ch1 * w1
            qImg1 = QImage(rgbImage1.data, w1, h1, bytesPerLine1, QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(qImg1)
            self.label1.setPixmap(pixmap1.scaled(720, 540))


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
            cv2.imwrite('calibration/img_calib/img_fisheye_stereo/imageFISH' + str(self.num) + '.png', img)
            cv2.imwrite('calibration/img_calib/img_infra_stereo/imageINF'+ str(self.num) + '.png', img2)
            print("images saved!")
            self.num_stereo +=1
            
    def capture_image_fish(self):
        ret1, img = self.cap1.read()
        if ret1 :
            cv2.imwrite('calibration/img_calib/img_fisheye_indi/imageFISH' + str(self.num) + '.jpg', img)
            print("images saved!")
            self.num_fish +=1

    def clean_file_stereo(self):
        cleanfile('calibration/img_calib/img_fisheye_stereo/')
        cleanfile('calibration/img_calib/img_infra_stereo/')


    def clean_file_fish(self):
        cleanfile('calibration/img_calib/img_fisheye_indi/')
    
    def select_fish(self):
        self.fishW = FishWindow()
        self.fishW.show()

    def select_stereo(self):
        self.stereoW = StereoWindow()
        self.stereoW.show()
        

    def see_unidst(self):
        if self.undist:
            self.undist=False
        else:
            self.undist=True
    
    def exec_fishcalib(self):
        rms = calib_fish(chessboardSize = (8,6))
        msg = QMessageBox(win)
        msg.setWindowTitle("Fish calibration")
        msg.setText(f"Fish calibration ended with a RMSE = {rms}")
         
        msg.exec_()


    def exec_stereocalib(self):
        res_1,retStereo,rms_infra,rms_fish = calibrate_camera(chessboardSize = (8,6))
        msg = QMessageBox(win)
        msg.setWindowTitle("Stereo calibration")
        msg.setText(f"Stereo calibration ended with a RMSE = {retStereo} (custom rmse = {res_1}) \n RMSE Infrared camera = {rms_infra} ")
         
        msg.exec_()

        
    def see_result(self):
        if self.numoverlay == 0:
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            self.overlayall ,self.overlaycorners,self.overlayborders, coord_corner= project_image(frame1,frame2)
            self.overlay = self.overlayall
            self.numoverlay = 1
            
        elif self.numoverlay == 1:
            self.overlay = self.overlayborders
            self.numoverlay = 2
            
        elif self.numoverlay == 2:
            self.overlay = self.overlaycorners
            self.numoverlay = 3
            
        elif self.numoverlay == 3:
            self.numoverlay = 0
            




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
