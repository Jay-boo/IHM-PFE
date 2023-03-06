import numpy as np
import cv2 as cv
import glob
from undi import undistort

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################


chessboardSize = (8,6)
frameSize = (640,480)


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 22
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.


imagesRight = sorted(glob.glob('img_calib/img_fisheye/*.png'))
imagesLeft = sorted(glob.glob('img_calib/img_infra/*.png'))


imagesRight += sorted(glob.glob('img_calib/img_fisheye2/*.png'))
imagesLeft += sorted(glob.glob('img_calib/img_infra2/*.png'))

print(imagesLeft)
print(imagesRight)
print(f" Number of base images :{len(imagesLeft)}")

counter=0
for imgLeft, imgRight in zip(imagesLeft, imagesRight):

   
    imgLe= cv.imread(imgRight)
    imgL = undistort(imgLe)
    
    img = cv.imread(imgLeft)
    imgR = cv.rotate(img, cv.ROTATE_180)

    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)

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
        cv.imshow('fisheye', imgL)
        cv.imwrite(f'draw/fish/imgFISH{counter}.png',imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow('img right', imgR)
        cv.imwrite(f'draw/infra/imgINF{counter}.png',imgR)
        cv.waitKey(200)
        counter+=1
    # else:
    #     print("NOt ok retL and retR")
    #     print(imgLeft,imgRight)

cv.destroyAllWindows()



print(f" Number of used images :{len(objpoints)}")

############## CALIBRATION #######################################################

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))
print('-------------------individual cam calib')
print("FISHEYE")
print(retL)
print("INFRA")
print(retR)


print("--------------------Stereo Calibration")

########## Stereo Vision Calibration #############################################

flags = 0
flags |= cv.CALIB_FIX_INTRINSIC

criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

def calc_rms_stereo(objectpoints, imgpoints_l, imgpoints_r, A1, D1, A2, D2, R, T):
    tot_error = 0
    total_points = 0

    for i, objpoints in enumerate(objectpoints):
        print(f"-------------------- {i} ----------")
        # calculate world <-> cam1 transformation
        _, rvec_l, tvec_l,_ = cv.solvePnPRansac(objpoints, imgpoints_l[i], A1, D1)

        # compute reprojection error for cam1
        rp_l, _ = cv.projectPoints(objpoints, rvec_l, tvec_l, A1, D1)
        print("fisheye reprojection error")
        print(np.sum(np.square(np.float64(imgpoints_l[i] - rp_l))))
        tot_error += np.sum(np.square(np.float64(imgpoints_l[i] - rp_l)))
        total_points += len(objpoints)

        # calculate world <-> cam2 transformation
        # rvec_r, tvec_r  = cv.composeRT(rvec_l,tvec_l,cv.Rodrigues(R)[0],T)[:2]
        _, rvec_r, tvec_r,_ = cv.solvePnPRansac(objpoints, imgpoints_r[i], A2, D2)

        # compute reprojection error for cam2
        rp_r,_ = cv.projectPoints(objpoints, rvec_r, tvec_r, A2, D2)
        tot_error += np.square(imgpoints_r[i] - rp_r).sum()
        print("infra reprojection error square")
        print(np.square(imgpoints_r[i] - rp_r).sum())
        total_points += len(objpoints)

    mean_error = np.sqrt(tot_error/total_points)

    return mean_error

res_1=calc_rms_stereo(
    objpoints,
    imgpointsL,
    imgpointsR,
    newCameraMatrixL,
    distL,
    newCameraMatrixR,
    distR,
    rot,
    trans
)


print(f"custom stereo calibration rmse :{res_1}")
print(f"built in sterroCalibration rmse : {retStereo}")


#--------------------------Stereo Calibration

rectifyScale= 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R= cv.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))

stereoMapL = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
stereoMapR = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)


#--------------------- Export Calibration Matrices

print("Saving parameters!")
cv_file = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)
cv_file.write('stereoMapL_x',stereoMapL[0])
cv_file.write('stereoMapL_y',stereoMapL[1])
cv_file.write('stereoMapR_x',stereoMapR[0])
cv_file.write('stereoMapR_y',stereoMapR[1])

cv_file.write('K1',newCameraMatrixL)
cv_file.write('D1',distL)
cv_file.write('K2',newCameraMatrixR)
cv_file.write('D2',distR)
cv_file.write('R',rot)
cv_file.write('T',trans)
cv_file.release()

