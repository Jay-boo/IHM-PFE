import numpy as np
import cv2


# def project_point(point_2d, camera1_matrix, camera1_dist_coeffs, camera1_R, camera1_t, camera2_matrix, camera2_dist_coeffs, camera2_R, camera2_t):
#     # Undistort the point using camera1's distortion coefficients
#     point_2d_undistorted = cv2.undistortPoints(np.array([point_2d]), camera1_matrix, camera1_dist_coeffs)

#     # Convert the point to homogeneous coordinates
#     point_2d_homogeneous = np.hstack((point_2d_undistorted, np.array([1])))

#     # Calculate the 3D point in camera coordinates using camera1's extrinsic matrix
#     point_3d = np.linalg.inv(camera1_matrix) @ point_2d_homogeneous.T
#     point_3d = point_3d / point_3d[2]

#     # Transform the 3D point to camera2's coordinates using camera2's extrinsic matrix
#     point_3d_transformed = camera2_R @ point_3d + camera2_t

#     # Project the 3D point onto the image plane of camera2 using camera2's intrinsic matrix
#     point_2d_transformed_homogeneous = camera2_matrix @ point_3d_transformed
#     point_2d_transformed_homogeneous = point_2d_transformed_homogeneous / point_2d_transformed_homogeneous[2]

#     # Apply distortion correction using camera2's distortion coefficients
#     point_2d_transformed_undistorted = cv2.undistortPoints(np.array([point_2d_transformed_homogeneous[:2]]), camera2_matrix, camera2_dist_coeffs)

#     # Return the transformed 2D point
#     return point_2d_transformed_undistorted[0][0]



def project_point(point_2d, camera1_matrix, camera1_dist_coeffs, camera2_matrix, camera2_dist_coeffs, camera2_R, camera2_t):
    # Undistort the point using camera1's distortion coefficients
    point_2d_undistorted = cv2.undistortPoints(point_2d, camera1_matrix, camera1_dist_coeffs)


    # Convert the point to homogeneous coordinates
    point_2d_homogeneous = np.hstack((point_2d_undistorted[0], np.array([[1]])))

    # Calculate the 3D point in camera coordinates using camera1's extrinsic matrix
    point_3d = np.linalg.inv(camera1_matrix) @ point_2d_homogeneous.T
    point_3d = point_3d / point_3d[2]

    # Transform the 3D point to camera2's coordinates using camera2's extrinsic matrix
    point_3d_transformed = camera2_R @ point_3d + camera2_t

    # Project the 3D point onto the image plane of camera2 using camera2's intrinsic matrix
    point_2d_transformed_homogeneous = camera2_matrix @ point_3d_transformed
    point_2d_transformed_homogeneous = point_2d_transformed_homogeneous / point_2d_transformed_homogeneous[2]
    print(point_2d_transformed_homogeneous)
    # Apply distortion correction using camera2's distortion coefficients
    point_2d_transformed_undistorted = cv2.undistortPoints(np.array([point_2d_transformed_homogeneous[:2]]), camera2_matrix, camera2_dist_coeffs)

    # Return the transformed 2D point
    return point_2d_transformed_undistorted[0][0]

cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)
K_webcam = cv_file.getNode('K2').mat()
D_webcam  = cv_file.getNode('D2').mat()
K_fisheye = cv_file.getNode('K1').mat()
D_fisheye = cv_file.getNode('D1').mat()
T = cv_file.getNode('T').mat()
R = cv_file.getNode('R').mat()

print(project_point(np.array([[257,103]], dtype=np.float32)
                    ,K_webcam,D_webcam,K_fisheye,D_fisheye,R,T))