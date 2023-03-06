import cv2
import numpy as np


cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)
K_webcam = cv_file.getNode('K2').mat()
D_webcam  = cv_file.getNode('D2').mat()
K_fisheye = cv_file.getNode('K1').mat()
D_fisheye = cv_file.getNode('D1').mat()
T = cv_file.getNode('T').mat()
R = cv_file.getNode('R').mat()

print(K_webcam)
cv_file = cv2.FileStorage()
cv_file.open('undiFish.xml', cv2.FileStorage_READ)
K_fish = cv_file.getNode('K').mat()

extrinsic = np.hstack((R, T.reshape(-1,1)))
print(extrinsic)

points = [[0, 0] ,[0, 640] ,[480, 0],[640, 480]]
listpoint=[]
for point in points:
    point2D = np.array([point], dtype=np.float32)
    

    print(point2D)
    # Undistort point (if necessary)
    #point2D_undistorted = cv2.undistortPoints(point2D, K_webcam, D_webcam)
    print('=====')
    # Convert 2D point to normalized camera coordinates


    point2D_normalized = np.hstack((point2D, np.array([[1.0]])))
    print(np.linalg.inv(K_webcam))
    point3D_normalized = np.linalg.inv(K_webcam) @ point2D_normalized.T
    print(point3D_normalized)

    point3D_normalized2 = np.vstack((point3D_normalized, np.array([[1.0]])))

    #print(extrinsic)
    # Project point into camera coordinates
    point3D_camera = extrinsic @ point3D_normalized2


    print('=====')

    point_2d_transformed = K_fisheye @ point3D_camera

    point_2d_transformed = point_2d_transformed / point_2d_transformed[2]
    listpoint.append(point_2d_transformed[:2])

    # point_2d_transformed_undistorted = cv2.undistortPoints(np.array([point_2d_transformed[:2]]), K_fisheye, D_fisheye)
    #print(point_2d_transformed_undistorted)


img_fisheye = cv2.imread('img_calib/img_fisheye4/imageFISH0.png')
tt=np.array([point_2d_transformed[:2][0],point_2d_transformed[:2][1]])

for elem in listpoint:
    print(elem)
    cv2.circle(img_fisheye, (int(elem[0]),int(elem[1])), 5, (0, 255, 0), -1)

img_infra = cv2.imread('img_calib/img_infra4/imageINF0.png')

cv2.imshow('Fisheye Camera', img_fisheye)
cv2.imshow('Infra Camera',img_infra)
cv2.waitKey(0)
cv2.destroyAllWindows()
