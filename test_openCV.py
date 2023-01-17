import cv2 as cv
import numpy as np

cap=cv.VideoCapture(0) 
if not cap.isOpened():
    print("Cannot open camera")