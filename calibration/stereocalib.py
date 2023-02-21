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



imagesFISH = sorted(glob.glob('../undistort/fish/*.png'))
imagesINFRA = sorted(glob.glob('../img_calib/img_infra/*.png'))

i=0
for imgLeft, imgRight in zip(imagesFISH, imagesINFRA):
    img = cv2.imread(imgLeft)
    dst = cv2.remap(img,stereoMapL_x,stereoMapL_y,cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT,0)
    cv2.imwrite(f'../test/fish/image_{i}.png',dst)
    cv2.imshow("frame fisheye",dst)
    img = cv2.imread(imgRight)
    dst = cv2.remap(img,stereoMapR_x,stereoMapR_y,cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT,0)
    cv2.imwrite(f'../test/infra/image_{i}.png',dst)
    cv2.imshow("frame infra",dst)
    cv2.waitKey(1000)
    i+=1
cv2.destroyAllWindows()
    
    
