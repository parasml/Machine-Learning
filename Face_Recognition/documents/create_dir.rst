
*****************************
   create_dir.py
*****************************



		**Created By**:         Akshay Nevrekar
		
		**Created On**:      	10th December, 2018
		
		**Last Modified On**: 	26th December, 2018

=======================================================================================================================================


**Objective**

	*	To create directories(folders) to store images based as per CSV file
	

**Code Block** ::

		import os, errno
		import pandas as pd
		import argparse


		def making_directories(csv_file, wdir, column):
			data = pd.read_csv(csv_file, encoding='windows-1252')
			dir_names = list(data[column])

			os.chdir(wdir)  

			print("[INFO] Creating new directories")
			for path in dir_names:
				try:
					os.makedirs(str(path))
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise

			print("[INFO] Created {} directories".format(len(dir_names)))

			return
			


		
**Modules Required**

* os :
* errno
* pandas 
* argparse


**Code Explanation** 

**Functions**

1. *making_directories()* 

Params:

*	csv_file: Path to csv file
*	wdir: directory in which folders to be created
*	column: column name from csv file to be used as foldername


		data = pd.read_csv(csv_file, encoding='windows-1252')
		dir_names = list(data[column])
		