import numpy as np
import cv2
import glob
print("hello")

# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
print(stereoMapL_x.shape)
print(stereoMapL_y.shape)
print(stereoMapR_y.shape)
print(stereoMapR_x.shape)


# Open both cameras
#cap_right = cv2.VideoCapture(0) 
#cap_left =  cv2.VideoCapture(2)
#print(cap_right.isOpened(),cap_left.isOpened())

imagesFISH = sorted(glob.glob('img_calib/img_fisheye/*.png'))
imagesINFRA = sorted(glob.glob('img_calib/img_infra/*.png'))

i=0
for imgLeft, imgRight in zip(imagesFISH, imagesINFRA):
    img = cv2.imread(imgLeft)
    dst = cv2.remap(img,stereoMapL_x,stereoMapL_y,cv2.INTER_LINEAR)
    cv2.imwrite(f'test/fish/image_{i}.png',dst)
    img = cv2.imread(imgRight)
    dst = cv2.remap(img,stereoMapR_x,stereoMapR_y,cv2.INTER_LINEAR)
    cv2.imwrite(f'test/infra/image_{i}.png',dst)
    i+=1
    
    
# while(cap_right.isOpened() and cap_left.isOpened()):

    # succes_right, frame_right = cap_right.read()
   #  succes_left, frame_left = cap_left.read()
    # print(f"frame right shape:{frame_right.shape}\nframe left shape:{frame_left.shape}")

    # Undistort and rectify images
    # frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    # frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                     
    # Show the frames
    # cv2.imshow("frame right", frame_right) 
    # cv2.imshow("frame left", frame_left)


    # Hit "q" to close the window
    # if cv2.waitKey(1) & 0xFF == ord('q'):
     #    break


# Release and destroy all windows before termination
# cap_right.release()
# cap_left.release()

# cv2.destroyAllWindows()
