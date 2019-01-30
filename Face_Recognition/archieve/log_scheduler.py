import os
import shutil
from datetime import datetime as dt


dir_path = "logs/"

# print(datetime.now())
curr_date = dt.strftime(dt.now().date(),"%Y%m%d")
new_file = "main"+curr_date+".log"
print(new_file)

if os.path.exists(dir_path+ "main.log"):
	# shutil.rmtree(dir_path)
	os.rename(dir_path+"main.log", dir_path+new_file)