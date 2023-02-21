import cv2 as cv
import numpy as np
import os
import glob

chessboardSize = (8,6)
frameSize = (640,480)
img_calib_dir="../img_calib/"

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((1,chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

_img_shape=None
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.

imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye/*.png'))
imagesINFRA = sorted(glob.glob( img_calib_dir+'img_infra/*.png'))

for imgLeft, imgRight in zip(imagesFISH, imagesINFRA):

    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    if _img_shape ==None:
        _img_shape=imgL.shape[:2]
        print(_img_shape)
    else:
        assert _img_shape==imgL.shape[:2]


    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    

    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, None)
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if retL and retR == True:

        objpoints.append(objp)

        cornersL = cv.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)

        # Draw and display the corners
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv.imshow('img left', imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow('img right', imgR)
        cv.waitKey(1000)


cv.destroyAllWindows()


N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv.fisheye.CALIB_CHECK_COND+cv.fisheye.CALIB_FIX_SKEW

print(np.asarray(objpoints).shape,np.asarray(objpoints).size)
print(np.asarray(imgpointsL).shape,np.asarray(imgpointsL).size)
# print(np.asarray(objpoints)[0].size(),np.asarray(imgpointsL)[0].size())
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
cv.fisheye.calibrate(
        objpoints,
        imgpointsL,
        grayL.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv.TERM_CRITERIA_EPS+cv.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )
