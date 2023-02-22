counter=10
for file in img_calib/img_infra2/imageFISH*.png;
  
  do
     mv $file  "img_calib/img_infra/imageINF${counter}.png";
     ((counter=counter+1))
  done
  
