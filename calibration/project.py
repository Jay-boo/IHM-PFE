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

# print(f'K_webcam ={K_webcam}')
# print(f'D_webcam ={D_webcam}')
# print(f'K_fisheye ={K_fisheye}')
# print(f'D_fisheye ={D_fisheye}')
# print(f'R={R}')
# print(f'T={T}')
#


# cv_file = cv2.FileStorage()
# cv_file.open('res/fishEyeCalib.xml', cv2.FileStorage_READ)
# K_fish = cv_file.getNode('K').mat()

extrinsic = np.hstack((R, T.reshape(-1,1)))
print("----------extrinsic:")
print(extrinsic)

points = [[0, 0] ,[0, 640] ,[480, 0],[640, 480]]
listpoint=[]

for point in points:
    print(f'------{point}-------')
    point2D = np.array([point], dtype=np.float32)
    

    # Undistort point (if necessary)
    #point2D_undistorted = cv2.undistortPoints(point2D, K_webcam, D_webcam)
    # Convert 2D point to normalized camera coordinates


    point2D_normalized = np.hstack((point2D, np.array([[1.0]])))
    print("point 2D homogene")
    print(point2D_normalized)

    point3D_normalized = np.linalg.inv(K_webcam) @ point2D_normalized.T
    print("point 2D  pixel coords -> infra camera systeme cords")
    print(point3D_normalized)

    point3D_normalized2 = np.vstack((point3D_normalized, np.array([[1.0]])))
    print(point3D_normalized2)


    #print(extrinsic)
    # Project point into camera coordinates
    point3D_camera = extrinsic @ point3D_normalized2
    print("cam1 -> cam2")
    print(point3D_camera)


    point_2d_transformed = K_fisheye @ point3D_camera
    print("3D fisheye camera system cords -> point 2D pixel coords")
    print(point_2d_transformed)

    point_2d_transformed = point_2d_transformed / point_2d_transformed[2]
    print(point_2d_transformed)
    listpoint.append(point_2d_transformed[:2])

    # point_2d_transformed_undistorted = cv2.undistortPoints(np.array([point_2d_transformed[:2]]), K_fisheye, D_fisheye)
    #print(point_2d_transformed_undistorted)
print(listpoint)

# img_fisheye = cv2.imread('img_calib/others/img_fisheye/imageFISH0.png')
#
# tt=np.array([point_2d_transformed[:2][0],point_2d_transformed[:2][1]])
#
# for elem in listpoint:
#     print(elem)
#     cv2.circle(img_fisheye, (int(elem[0]),int(elem[1])), 5, (0, 255, 0), -1)
#
# img_infra = cv2.imread('img_calib/others/img_infra/imageINF0.png')
#
# cv2.imshow('Fisheye Camera', img_fisheye)
# cv2.imshow('Infra Camera',img_infra)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
