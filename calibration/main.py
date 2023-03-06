import subprocess
from calibration import calibrate_camera

subprocess.run(["bash","/home/jay_boo/projects/PFE/IHM-PFE/calibration/init_calibration.sh"])
calibrate_camera()
subprocess.run(["python3","/home/jay_boo/projects/PFE/IHM-PFE/calibration/calibration_bis.py"])
