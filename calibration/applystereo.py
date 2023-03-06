import cv2
import numpy as np


cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)
K_webcam = cv_file.getNode('K1').mat()
D_webcam  = cv_file.getNode('D1').mat()
K_fisheye = cv_file.getNode('K2').mat()
D_fisheye = cv_file.getNode('D2').mat()
T = cv_file.getNode('T').mat()
R = cv_file.getNode('R').mat()


# corner_3d = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0],[1,1,0]], dtype=np.float32)

# # Transform 3D coordinates of the corners of the webcam into the fisheye camera coordinate system
# corner_3d_transformed = cv2.transform(corner_3d.reshape(-1, 1, 3), R, T)


# tt  = np.array([corner_3d_transformed[0][0], corner_3d_transformed[1][0], corner_3d_transformed[2][0] ,corner_3d_transformed[3][0]], dtype=np.float32)
# # Project 3D coordinates of the corners of the webcam onto the 2D image plane of the fisheye camera
# print(tt)

# corner_2d_fisheye, _ = cv2.projectPoints(tt, np.zeros((4, 1)), np.zeros((3, 1)), K_fisheye, D_fisheye)



# # Project 3D coordinates of the corners of the webcam onto the 2D image plane of the webcam

# print(corner_2d_fisheye.reshape(-1, 2))

# # Draw corner po

point2D = np.array([[u, v]], dtype=np.float32)

# Undistort point (if necessary)
point2D_undistorted = cv2.undistortPoints(point2D, K, distortionCoefficients)

# Convert 2D point to normalized camera coordinates
point2D_normalized = np.hstack((point2D_undistorted, np.array([[1.0]])))
point3D_normalized = np.linalg.inv(K) @ point2D_normalized.T

# Project point into camera coordinates
point3D_camera = extrinsic @ point3D_normalize

# ints on fisheye camera image
img_fisheye = cv2.imread('img_calib/img_fisheye4/imageFISH0.png')

for pt in corner_2d_fisheye.reshape(-1, 2):
     cv2.circle(img_fisheye, tuple(pt.astype(int)), 5, (0, 255, 0), -1)


img_infra = cv2.imread('img_calib/img_infra4/imageINF0.png')

# Display images with corner points
cv2.imshow('Fisheye Camera', img_fisheye)
cv2.imshow('Infra Camera',img_infra)
cv2.waitKey(0)
cv2.destroyAllWindows()
