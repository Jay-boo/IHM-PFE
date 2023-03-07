
import cv2 as cv
import numpy as np
from calibration.project_image import project_image

from calibration.calibration_stereo import calibrate_camera
calibrate_camera()
imgRight = cv.imread('calibration/img_calib/img_fisheye_stereo/imageFISH2.png')
imgLeft = cv.imread('calibration/img_calib/img_infra_stereo/imageINF2.png')
opacity = 0.4  # Transparency factor.

overlay , imgR= project_image(imgRight,imgLeft)
image_new = cv.addWeighted(overlay, opacity, imgR, 1 - opacity, 0)
cv.imshow('Right', image_new)
cv.imshow('Left', imgLeft)
cv.waitKey(0)