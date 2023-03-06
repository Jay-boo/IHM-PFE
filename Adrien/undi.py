import cv2 as cv2
import numpy as np
import os
import glob






def undistort(img_path,DIM=None,K=None,D=None, balance=0.0, dim2=None, dim3=None,see_result=False):   
    if DIM==None:
        try:
            cv_file = cv2.FileStorage()
            cv_file.open('undiFish.xml', cv2.FileStorage_READ)
            DIM = cv_file.getNode('DIM').mat()
            print(DIM)
            K = cv_file.getNode('K').mat()
            D = cv_file.getNode('D').mat()
        except:
            pass
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"    
    if not dim2:
        dim2 = dim1    
    if not dim3:
        dim3 = dim1   

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) 
    if see_result : 
        cv2.imshow("undistorted", undistorted_img)
        cv2.imshow("normal", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return undistorted_img