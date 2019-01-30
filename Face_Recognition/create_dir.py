import os, errno
import pandas as pd
import argparse


def making_directories(csv_file, wdir, column):
	"""
		@param csv_file: path to csv file
		@param wdir: directory in which sub-directories to be created
		@param column: columnname in csv file to be used as directory names
	"""
	data = pd.read_csv(csv_file, encoding='windows-1252')
	dir_names = list(data[column])

	os.chdir(wdir)  

	print("[INFO] Creating new directories")
	for path in dir_names:
		try:
			# create a directory
			os.makedirs(str(path))
		except OSError as e:
		    if e.errno != errno.EEXIST:
		        raise

	print("[INFO] Created {} directories".format(len(dir_names)))

	return


if __name__ == '__main__':

	# path_to_csv = "data/sample_data.csv"
	# working_dir = 'data/train_images/'
	# column = 'ID'

	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--path", required=True,
	                 help="path to csv file")
	ap.add_argument("-d", "--directory", required=True,
	                 help="directory in which folders to be created")
	ap.add_argument("-c", "--column", type=str, required=True,
	                 help="column which contains name of the directories")
	args = vars(ap.parse_args())

	path_to_csv = args['path']
	directory = args['directory']
	column = args['column']

	making_directories(path_to_csv, directory, column)