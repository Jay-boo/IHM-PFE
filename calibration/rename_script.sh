counter=0
for file in img_calib/img_fisheye3/imageINF*.png;
  
  do
     mv $file  "img_calib/img_fisheye3/imageFISH${counter}.png";
     ((counter=counter+1))
  done
  
