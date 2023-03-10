import cv2 as cv
import numpy as np
import os
import glob
from calibration.undistort import undistort

def calib_fish(chessboardSize = (8,6),img_calib_dir="calibration/img_calib/"):
    frameSize = (640,480)


    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((1,chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    size_of_chessboard_squares_mm = 22
    objp = objp * size_of_chessboard_squares_mm

    _img_shape=None
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    #imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye3/*.png'))
    #imagesFISH += sorted(glob.glob(img_calib_dir+'img_fisheye4/*.png'))
    imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye_indi/*.jpg'))
    #imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye4/*.png'))
    for img in imagesFISH:


        img = cv.imread(img)
        if _img_shape == None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "All images must share the same size."
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret:

            objpoints.append(objp)

            corners = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, chessboardSize, corners, ret)
            #cv.imshow('img left', img)

            #cv.waitKey(200)


    #cv.destroyAllWindows()

    #print(rms)
    calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv.fisheye.CALIB_FIX_SKEW #+ cv.fisheye.CALIB_CHECK_COND

    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    rms, _, _, _, _ = \
        cv.fisheye.calibrate(
            objpoints,
            imgpoints,
            gray.shape[::-1],
            K,
            D,
            rvecs,
            tvecs,
            calibration_flags,
            (cv.TERM_CRITERIA_EPS+cv.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
        )
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")
    DIM=_img_shape[::-1]


    cv_file = cv.FileStorage('calibration/res/fishEyeCalib.xml', cv.FILE_STORAGE_WRITE)
    cv_file.write('frameSize',DIM)
    cv_file.write('K_fish',K)
    cv_file.write('dist_fish',D)
    cv_file.release()

    # imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye4/*.png'))
    # i=0
    # for fname in imagesFISH:
    #     undistort(fname)
    #     i+=1

if __name__ == "__main__":
    
    print(cv.__version__)
    calib_fish()
