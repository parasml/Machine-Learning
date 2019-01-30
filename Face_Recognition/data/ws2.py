from flask import Flask, flash, request, redirect, url_for, session, jsonify

app = Flask(__name__)

import face_recognition
import pickle
import cv2
import pymongo
import pandas as pd
import numpy as np
import json
from imutils import paths
import os
import sys
import time
import requests
from skimage import io
import shutil
import time
from sync_ws import ImgProcessingThread
import threading
from queue import Queue
import datetime
import logging
# from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')

file_handler = logging.FileHandler('logs/mainlogs/main.log')
file_handler.setFormatter(formatter)
# file_handler.suffix = "%Y%m%d"

logger.addHandler(file_handler)


hostname = "172.16.1.70"   # MongoDB hostname
data = pickle.loads(open("output/encodings2.pickle", "rb").read())


@app.route("/", methods=['GET'])
def hello():
	return "Welcome to Calibehr-Face-Detection Feature!!!"


@app.route("/register", methods=['POST'])
def register():
	imagefile1 = request.files['file1']
	imagefile2 = request.files['file2']
	imagefile3 = request.files['file3']
	imagefile4 = request.files['file4']

	id_ = request.form['id']
	auth_token = request.form['authtoken']
	type_ = request.form['type']    # Android=1, iOS=2, webapp=3
	timestamp = str(datetime.datetime.utcnow())

	client = pymongo.MongoClient(hostname)
	db = client.FaceRecognition             # replace `database` by name of the database
	coll = db["Registration"]            # replace `collection` by name of the collection

	logger.debug("[Register]: Registeration request received for userid {}.".format(id_))

	coll.insert_one({'userid:': id_, 'authtoken': auth_token, 'type': type_, 'timestamp': timestamp})

	img_list = [imagefile1, imagefile2, imagefile3, imagefile4]
	new_dir = "data/train_images/"+str(id_)

	try:
		# If directory exists then delete it and create new one with same name
		if os.path.exists(new_dir):
			shutil.rmtree(new_dir)
			time.sleep(0.05)
		os.makedirs(new_dir)
		for i,img in enumerate(img_list):
			offset = int(time.time())
			save_dir = new_dir+"/imagefile"+str(i)+str(offset)+".jpg"
			img.save(save_dir)
	except Exception as e :
		logger.exception("[Register Error]: Error occured while creating a new direcotry and storing the images")
		return json.dumps({"ReconStatus":False , 'Msg': str(e)})

	imagePaths = list(paths.list_images("data/train_images/"+str(id_)))

	for i in imagePaths:
		temp = cv2.imread(i)
		rgb = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
		boxes = face_recognition.face_locations(rgb, model="hog")
		# print("Faces in image {}: {}".format(i, boxes))
		if not boxes:
			records = {'ReconStatus': False, 'Msg': 'Can not find face in the image'}
			logger.debug("[Face Detection]: Not able to find a face in the image.")
			return json.dumps(records)
		elif len(boxes) > 1:
			records = {'ReconStatus': False, 'Msg': 'Multiple Faces detected in the image'}
			logger.debug("[Face Detection]: Multiple faces detected in the image.")
			return json.dumps(records)
	try:
		response = requests.post("http://wsautomatebanking.calibehr.com/MService.svc/UpdateFaceReconStatus", json={"ReconStatus": True, "authToken": auth_token})
		response1 = json.loads(response.text)
		logger.debug("[Status Update]: UpdateFaceReconStatus API has been called successfully.")
	except:
		logger.exception("[Status Update]: Not able to call UpdateFaceReconStatus API.")
		return json.dumps({'ReconStatus': False, 'Msg': "UpdateFaceReconStatus API is not reachable"})

	if response1['Response']['Type'] == 'SUCCESS':
		records = {'ReconStatus': True, 'Msg': 'Record Entered in Database'}
	else:
		records = {'ReconStatus': False, 'Msg': 'Failed to enter a record into Database'}
	# print(auth_token)
	# print(response)
	logger.debug("[Status Update]: {}".format(records['Msg']))
	return json.dumps(records)


@app.before_first_request
def activate_job_monitor():
    thread = ImgProcessingThread()
    app.imgprocess = thread
    thread.start()


@app.route("/faceparams", methods=['GET','POST'])
def check():
	try:
		data = request.json
		# print(data)
		path = data['path']
		id_ = data['id']
		date = data['date']

		# offset = str(int(time.time()))

		# df = pd.DataFrame({'path':[path], 'id':[id_], 'date':[date]})
		# df.to_csv("logs/logfile"+offset+".csv", index=False)
		logger.debug("[Check-in]: Check-in request recieved for userid {} with imagepath {}"
			          .format(id_,path))

		app.imgprocess.send((path, id_, date))
		res = {'Status': True}
		logger.debug("[Check-in]: Face Recognition script has been called.")
		return json.dumps(res)
	except:
		logger.exception("[Check-in]: Unable to process Check-in request.")
		return json.dumps({'Status': False})


# app.run(host='0.0.0.0', port=8080, debug=True)

# if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=5001, debug=True)
