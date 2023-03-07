import numpy as np
import cv2 as cv
from undi import undistort

# Camera parameters to undistort and rectify images
cv_file = cv.FileStorage()
cv_file.open('stereoMap.xml', cv.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()


# Open both cameras
cap_right = cv.imread('img_calib/img_fisheye4/imageFISH0.png')                  
cap_left =  cv.imread('img_calib/img_infra4/imageINF0.png')


imgR = undistort(cap_right)
imgL = cv.rotate(cap_left, cv.ROTATE_180)



frame_right = cv.remap(imgR, stereoMapR_x, stereoMapR_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
frame_left = cv.remap(imgL, stereoMapL_x, stereoMapL_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
print(frame_left)
    # Show the frames
cv.imshow("frame right", frame_right) 
cv.imshow("frame left", frame_left)
cv.waitKey(0)
cv.destroyAllWindows()