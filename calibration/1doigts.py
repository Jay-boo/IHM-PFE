
import cv2 as cv
import numpy as np
from undi import undistort

def getcorners(img):
    x_coords = img[:,:,0]
    c1_index = np.argmin(x_coords)
    c1_coords = img[c1_index]
    c2_index = np.argmax(x_coords)
    c2_coords = img[c2_index]
    y_coords = img[:,:,1]
    c3_index = np.argmin(y_coords)
    c3_coords = img[c3_index]
    c4_index = np.argmax(y_coords)
    c4_coords = img[c4_index]
    return [c1_coords,c2_coords,c3_coords,c4_coords]



cv_file = cv.FileStorage()
cv_file.open('stereoMap.xml', cv.FileStorage_READ)
Q = cv_file.getNode('Q').mat()
cameraMatrixR = cv_file.getNode('cameraMatrixR').mat()
distR = cv_file.getNode('distR').mat()


imgLeft = cv.imread('img_calib/img_infra4/imageINF0.png')

imgL = cv.rotate(imgLeft, cv.ROTATE_180)
grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)

# obtain the 3D coordinates of the corners in the left image
cornersL_3D = cv.reprojectImageTo3D(grayL, Q)

# project the 3D points onto the right image
cornersL_3D = cornersL_3D.reshape(-1, 3)
cornersR_2D, _ = cv.projectPoints(cornersL_3D, np.zeros((3, 1)), np.zeros((3, 1)), cameraMatrixR, distR)


corners= getcorners(cornersR_2D)

# draw the corners in the right image
imgRight = cv.imread('img_calib/img_fisheye4/imageFISH0.png')
imgR = undistort(imgRight)
overlay=imgR.copy()
for corner in cornersR_2D:
    x, y = corner.ravel()
    cv.circle(overlay, (int(x), int(y)), 5, (0, 0, 255), -1)

alpha = 0.4  # Transparency factor.
image_new = cv.addWeighted(overlay, alpha, imgR, 1 - alpha, 0)
cv.imshow('Right', image_new)
cv.imshow('Left', imgL)
cv.waitKey(0)