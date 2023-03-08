
import cv2 as cv
import numpy as np
from calibration.undistort import undistort


def project_image(imgFISH,imgINFRA):
    cv_file = cv.FileStorage()
    cv_file.open('calibration/stereoMap.xml', cv.FileStorage_READ)
    Q = cv_file.getNode('Q').mat()
    cameraMatrixR = cv_file.getNode('cameraMatrixR').mat()
    distR = cv_file.getNode('distR').mat()


    imgL = cv.rotate(imgINFRA, cv.ROTATE_180)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)

    # obtain the 3D coordinates of the corners in the left image
    cornersL_3D = cv.reprojectImageTo3D(grayL, Q)

    # project the 3D points onto the right image
    cornersL_3D = cornersL_3D.reshape(-1, 3)
    cornersR_2D, ok = cv.projectPoints(cornersL_3D, np.zeros((3, 1)), np.zeros((3, 1)), cameraMatrixR, distR)


    # draw the corners in the right image
  
    imgR = undistort(imgFISH)
    overlay=imgR.copy()
    orvercorners = imgR.copy()
    overlayborder= imgR.copy()
    i=0
    coord_corner = []
    for corner in cornersR_2D:
        x, y = corner.ravel()
        cv.circle(overlay, (int(x), int(y)), 1, (0, 0, 255), -1)
        if i in [0,639,len(cornersR_2D)-1,len(cornersR_2D)-640]:
            cv.circle(orvercorners, (int(x), int(y)), 5, (0, 0, 255), -1)
            
        if i in range(0,640) or i in range(len(cornersR_2D)-641 ,len(cornersR_2D)) or i%640 ==0 or (i+1)%640 ==0 :
            cv.circle(overlayborder, (int(x), int(y)), 2, (0, 0, 255), -1)
            
            coord_corner.append((int(x), int(y)))
        #cv.circle(overlay, (int(x), int(y)), 5, (0, 0, 255), -1)
        i+=1
    return overlay,orvercorners,overlayborder,coord_corner
