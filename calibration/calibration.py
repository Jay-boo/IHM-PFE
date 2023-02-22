import cv2 as cv 
import numpy as np
import os
import glob




def calibrate_camera(chessboardSize=(8,6),img_calib_dir="img_calib/"):
    chessboardSize = (8,6)
    frameSize = (640,480)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((1,chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    objpoints = [] # 3d point in real world space
    imgpointsL = [] # 2d points in image plane.
    imgpointsR = [] # 2d points in image plane.

    imagesFISH = sorted(glob.glob(img_calib_dir+'img_fisheye2/*.png'))
    imagesINFRA = sorted(glob.glob( img_calib_dir+'img_infra2/*.png'))
    print(imagesINFRA,imagesFISH)

    for imgLeft, imgRight in zip(imagesFISH, imagesINFRA):

        imgL = cv.imread(imgLeft)
        imgR = cv.imread(imgRight)
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
    print(grayL)




    #---------------------------------------------------
    # 1. Individual calibration



    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

    calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv.fisheye.CALIB_CHECK_COND+cv.fisheye.CALIB_FIX_SKEW
    rms, _, _, _, _ = \
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

    final_K= cv.fisheye.estimateNewCameraMatrixForUndistortRectify(K,
                                                                     D,
                                                                     frameSize,
                                                                     np.eye(3),
                                                                     balance=1.0)
 

    retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
    heightR, widthR, channelsR = imgR.shape
    newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))



    print("--------------Indidual camera parameter calibration------------------------")
    print("FISHEYE MATRIX")
    print(f"rmse:{rms}")
    print(K)
    print(D)
    print("INFRA MATRIX")
    print(f"rmse:{retR}")
    print(cameraMatrixR)
    print(newCameraMatrixR.shape)
    print("--------------------------------------")


    #---------------------------------------------------
    # 2. Undistort Point
    # undistorted_imgpointsL=[]
    # for img_point in imgpointsL:
    #     undistorted_imgpointsL.append(cv.fisheye.undistortPoints(img_point,K,D))
    #     
    # undistorted_imgpointsR=[]
    # for img_point in imgpointsR:
    #     undistorted_imgpointsR.append(cv.undistortPoints(img_point,newCameraMatrixR,distR))
    #
    # counter=0
    # for imgLeft, imgRight in zip(imagesFISH, imagesINFRA):
    #     img = cv.imread(imgLeft)
    #     cv.imshow("frame fisheye",img)
    #     map_1,map_2=cv.fisheye.initUndistortRectifyMap(K,D,np.eye(3),K,frameSize,cv.CV_16SC2)
    #     undistorted_img=cv.remap(img,map_1,map_2,interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    #     cv.imshow("frame undistorted",undistorted_img)
    #     cv.imwrite(f'../undistort/fish/image_{counter}.png',undistorted_img)
    #
        # img = cv.imread(imgRight)
        # cv.imshow("frame Infra",img)
        # map_1,map_2=cv.initUndistortRectifyMap(cameraMatrixR,distR,None,newCameraMatrixR,frameSize,cv.CV_32FC1)
        # undistorted_img=cv.remap(img,map_1,map_2,interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
        # cv.imshow("frame undistorted",undistorted_img)
        # cv.imwrite(f'../undistort/infra/image_{counter}.png',undistorted_img)
    #     cv.waitKey(1000)
    #     counter+=1
    # cv.destroyAllWindows()

    #-------------------------------------------------------
    # 3. Estimate extrinsic parameters
    #
    # flags=0
    # flags |=cv.CALIB_FIX_INTRINSIC
    #
    # criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    #
    # retStereo, cameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(
    # objpoints, 
    # undistorted_imgpointsL,
    #     undistorted_imgpointsR,
    # final_K,
    # D,
    # newCameraMatrixR,
    # distR,
    # grayL.shape[::-1], 
    # criteria_stereo,
    # flags)
    #
    # print("---------Stereo Camera Calibration-----------")
    # print(f"rmse :{retStereo}")
    # print(cameraMatrixL)
    # print(cameraMatrixR)
    # print("---------------")
    # rectifyScale=1
    # rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R= cv.stereoRectify(cameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))
    #
    # stereoMapL = cv.initUndistortRectifyMap(cameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
    # stereoMapR = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)
    #
    # print("Saving parameters!")
    # cv_file = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)
    #
    # cv_file.write('stereoMapL_x',stereoMapL[0])
    # cv_file.write('stereoMapL_y',stereoMapL[1])
    # cv_file.write('stereoMapR_x',stereoMapR[0])
    # cv_file.write('stereoMapR_y',stereoMapR[1])
    #
    # cv_file.release()

if __name__ == "__main__":
    
    print(cv.__version__)
    calibrate_camera()
