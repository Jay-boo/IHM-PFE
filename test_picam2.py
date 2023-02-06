import time
import cv2
from picamera2 import Picamera2


picam2=Picamera2()
picam2.start()

counter=0
while True:
    im = picam2.capture_array("main")
    print(im)
    print(f"img type :{type(im)} \n {im.shape}")
    cv2.imwrite(f"test_{counter}.jpg",im)
    time.sleep(3)
    # cv2.imshow('img',im)
    picam2.capture_file(f"img/test_{counter}.jpg")
    counter+=1

