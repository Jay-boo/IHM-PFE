import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot,Qt
import cv2 as cv 
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout,QWidget
import sys
import numpy as np
from picamera2 import Picamera2


class VideoThread(QThread):
    change_pixmap_signal=pyqtSignal(np.ndarray)# We will emit numpy.ndarray
    def __init__(self,camera_index=0):
        super().__init__()
        self._run_flag=True
        self.camera_index=camera_index


    def calibrate_camera(self):
        pass

    def run(self):

        cap=cv.VideoCapture(self.camera_index)

        counter=0
        print("-----------------------")
        while self._run_flag:
            ret,frame=cap.read()
            if ret:
                # ret est un bool indiquant si la frame a ete bien recu
                self.change_pixmap_signal.emit(frame)
                if counter % 150==0:
                    print("Worth the wait")
                if counter % 200==0:
                    print("taking pic")
                    cv.imwrite(f'img_calib/image_{self.camera_index}_{counter}.jpg',frame)
            if not ret :
                print("Can't receive frame")
                pass
            counter+=1
        cap.release()


    def stop(self):
        """
        Wait for thread to finish
        """
        self._run_flag=False
        self.wait()




# TEMPORARY THREAD . NOT USED --------------

class VideoThreadPiCamera(QThread):
    change_pixmap_signal=pyqtSignal(np.ndarray)# We will emit numpy.ndarray
    def __init__(self,camera_index=0):
        super().__init__()
        print("IN VideoThread Constructor picamera")
        self._run_flag=True
        self.camera_index=camera_index


    def calibrate_camera(self):
        pass

    def run(self):

        cap=cv.VideoCapture(self.camera_index)
        picam2=Picamera2()
        picam2.start()
        counter=0
        print("-----------------counter")
        print(counter)
        

        while self._run_flag:
            print(counter)
            im=picam2.capture_array("main")
            picam2.capture_file(f"img/test_{self.camera_index}{counter}.jpg")
            print("picamera capture flow")
            self.change_pixmap_signal.emit(im)
            time.sleep(5)
            counter+=1

    def stop(self):
        """
        Wait for thread to finish
        """
        self._run_flag=False
        self.wait()
# -----------------------------------------------------------

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 300
        self.display_height = 300

        #--------------------------------------------
        # Element for Infrarouge camera Thread
        # create the label that holds the image

        self.image_label_camera_infra = QLabel(self)
        self.image_label_camera_infra.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel_infra = QLabel('Camera Infrarouge')


        #--------------------------------------------
        # Elements for Fisheye camera Thread
        # create the video capture thread

        self.image_label_camera_fisheye = QLabel(self)
        self.image_label_camera_fisheye.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel_fisheye = QLabel('Camera fisheye')


        #-------------------------------------
        #Merge camera
        # 
        self.image_label_all = QLabel(self)
        self.image_label_all.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel_all = QLabel('view')
        





        #--------------------------------------------
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        hbox=QHBoxLayout()

        vbox_infra=QVBoxLayout()
        vbox_infra.addWidget(self.image_label_camera_infra)
        vbox_infra.addWidget(self.textLabel_infra)

        vbox_fisheye=QVBoxLayout()
        vbox_fisheye.addWidget(self.image_label_camera_fisheye)
        vbox_fisheye.addWidget(self.textLabel_fisheye)

        hbox.addLayout(vbox_infra)
        hbox.addLayout(vbox_fisheye)

        
        vbox.addLayout(hbox)
        vbox.addWidget(self.image_label_all)
        vbox.addWidget(self.textLabel_all)
        

        #--------------------------------------------
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        



        #--------------------------------------------
        self.thread_infra = VideoThread(1)
        print("-----------vieoThreadPicamera creation")
        self.thread_fisheye= VideoThread(0)
        print("-----------")

        #--------------------------------------------
        # connect its signal to the update_image slot

        self.thread_infra.change_pixmap_signal.connect(self.update_infra_image)
        self.thread_infra.start()
        print("----------------------------thread launching")
        self.thread_fisheye.change_pixmap_signal.connect(self.update_fisheye_image)
        self.thread_fisheye.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()





    @pyqtSlot(np.ndarray)
    def update_infra_image(self,frame):
        """
        When new frame emit from VideoThread.change_pixmap_signal in run() then we update self.image_label
        """
        qt_img=self.convert_cv_qt(frame)

        self.image_label_camera_infra.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_fisheye_image(self,frame):
        """
        When new frame emit from VideoThread.change_pixmap_signal in run() then we update self.image_label
        """
        qt_img=self.convert_cv_qt(frame)
        self.image_label_camera_fisheye.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_fisheye_image_bis(self,frame):
        """
        When new frame emit from VideoThread.change_pixmap_signal in run() then we update self.image_label
        """
        qt_img=self.convert_cv_qt(frame)

        self.image_label_camera_fisheye.setPixmap(qt_img)
        self.image_label_camera_infra.setPixmap(qt_img)
        self.image_label_all.setPixmap(qt_img)




    def convert_cv_qt(self,cv_img):
        """
        Convert openCV captured frame into QT Pixmap
        """
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)




if __name__ == "__main__":
    app=QApplication(sys.argv) 
    window=App()
    window.show()
    app.exec()

    
