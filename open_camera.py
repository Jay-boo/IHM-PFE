from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image=frame.array
    cv2.imshow("Frame",image)
    key=cv2.waitKey(1)& 0xFF 
    raw_capture.truncate(0)
    if key ==ord("q"):
        break
