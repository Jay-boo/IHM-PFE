import cv2
import numpy as np



def undistort(DIM,K,D,img_path):  
    K=np.array(K)
    D=np.array(D)
    img = cv2.imread(img_path)
    h,w = img.shape[:2]  
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)