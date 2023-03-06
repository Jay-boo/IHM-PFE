import cv2 as cv 
import numpy as np
import glob




def calibrate_camera(chessboardSize=(8,6),img_calib_dir="img_calib/"):
    chessboardSize = (8,6)
    frameSize = (640,480)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((1,chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    size_of_chessboard_squares_mm = 22
    objp = objp * size_of_chessboard_squares_mm

    objpoints = [] # 3d point in real world space
    imgpointsL = [] # 2d points in image plane.
    imgpointsR = [] # 2d points in image plane.
    _img_shape=None

    imagesFISH_ind = sorted(glob.glob(img_calib_dir+'img_fisheye5/*.jpg'))
    imagesINFRA = sorted(glob.glob( img_calib_dir+'img_infra_stereo/*.png'))
    print(imagesINFRA,imagesFISH_ind)

    for imgLeft, imgRight in zip(imagesFISH_ind, imagesINFRA):

        imgL = cv.imread(imgLeft)
        imgR = cv.imread(imgRight)
        grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
        grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
        if _img_shape==None:
            _img_shape=imgL.shape[:2]


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

    calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv.fisheye.CALIB_FIX_SKEW
    rms, cameraMatrixL, distL, rvecsL, tvecsL =cv.fisheye.calibrate(
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

    final_K= cv.fisheye.estimateNewCameraMatrixForUndistortRectify(cameraMatrixL,
                                                                     distL,
                                                                     frameSize,
                                                                     np.eye(3),
                                                                     balance=0.0)
 

    retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
    heightR, widthR, channelsR = imgR.shape
    heightL, widthL, channelsL = imgL.shape
    newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))



    print("--------------Indidual camera parameter calibration------------------------")
    print("FISHEYE MATRIX")
    print(f"rmse:{rms}")
    print(K)
    print(D,D.shape)
    print("INFRA MATRIX")
    print(f"rmse:{retR}")
    print(cameraMatrixR)
    print("--------------------------------------")

    map_1L,map_2L=cv.fisheye.initUndistortRectifyMap(K,D,np.eye(3),final_K,frameSize,cv.CV_16SC2)
    map_1R,map_2R=cv.initUndistortRectifyMap(cameraMatrixR,distR,None,newCameraMatrixR,frameSize,cv.CV_32FC1)

    counter=0


    #--------------------Applying undistort
    # imagesFISH_stereo = sorted(glob.glob(img_calib_dir+'others/img_fisheye/*.png'))
    # print(imagesFISH_stereo)
    # 
    # for imgLeft in imagesFISH_stereo :
    #     img = cv.imread(imgLeft)
    #     cv.imshow("frame fisheye",img)
    #     undistorted_img=cv.remap(img,map_1L,map_2L,interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    #     cv.imshow("frame undistorted",undistorted_img)
    #     cv.imwrite(f'undistort/fish/imgFISH{counter}.png',undistorted_img)
    #     cv.waitKey(1000)
    #     counter+=1
    # cv.destroyAllWindows()




    print("Saving Individual Calibration params !")
    cv_file = cv.FileStorage('res/fishEyeCalib.xml', cv.FILE_STORAGE_WRITE)
    cv_file.write('frameSize',_img_shape[::-1])
    cv_file.write('K_L',cameraMatrixL)
    cv_file.write('distL',distL)
    cv_file.write('map_1L',map_1L)
    cv_file.write('map_2L',map_2L)
    cv_file.release()

    cv_file = cv.FileStorage('res/infraCalib.xml', cv.FILE_STORAGE_WRITE)
    cv_file.write('K_R',cameraMatrixR)
    cv_file.write('new_K_R',newCameraMatrixR)
    cv_file.write('distR',distR)

    cv_file.write('map_1R',map_1R)
    cv_file.write('map_2R',map_2R)
    cv_file.release()


if __name__ == "__main__":
    
    print(cv.__version__)
    calibrate_camera()
