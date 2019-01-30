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
import datetime
import logging
import pyodbc
from datetime import datetime as dt
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')

# handler = logging.FileHandler('logs/mainlogs/main.log')
handler = TimedRotatingFileHandler('logs/mainlogs/main.log', when="midnight", interval=1)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"

logger.addHandler(handler)


hostname = "172.16.1.70"   # MongoDB hostname
data = pickle.loads(open("output/encodings2.pickle", "rb").read())


@app.route("/", methods=['GET'])
def hello():
	return "Welcome to Calibehr-Face-Detection Feature!!!"


@app.route("/register", methods=['POST'])
def register():
	# accept the data 
	imagefile1 = request.files['file1']
	imagefile2 = request.files['file2']
	imagefile3 = request.files['file3']
	imagefile4 = request.files['file4']

	id_ = request.form['id']
	auth_token = request.form['authtoken']
	type_ = request.form['type']    # Android=1, iOS=2, webapp=3

	# get the timestamp to insert into database
	timestamp = str(datetime.datetime.utcnow())

	# MongoDB config
	client = pymongo.MongoClient(hostname)
	db = client.FaceRecognition             # replace `database` by name of the database
	coll = db["Registration"]            # replace `collection` by name of the collection

	logger.debug("[Register]: Registeration request received for userid {}.".format(id_))

	# insert the input data recieved into MongoDB database
	coll.insert_one({'userid:': id_, 'authtoken': auth_token, 'type': type_, 'timestamp': timestamp})

	img_list = [imagefile1, imagefile2, imagefile3, imagefile4]

	# name for new directory to be created
	new_dir = "data/train_images/"+str(id_)

	try:
		# If directory exists then delete it and create new one with same name
		if os.path.exists(new_dir):
			shutil.rmtree(new_dir)
			time.sleep(0.05)
		os.makedirs(new_dir)

		# save the images into a newly created directory 
		for i,img in enumerate(img_list):
			offset = int(time.time())
			save_dir = new_dir+"/imagefile"+str(i)+str(offset)+".jpg"
			img.save(save_dir)
	except Exception as e :
		logger.exception("[Register Error]: Error occured while creating a new direcotry and storing the images")
		return json.dumps({"ReconStatus":False , 'Msg': str(e)})

	imagePaths = list(paths.list_images("data/train_images/"+str(id_)))

	# this block fetches faces from the image and genereates errors if no or multiple faces found
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
		# change flag value to True in FaceReconStatus table for given id
		response = requests.post("http://wsbanking.go4automate.com/MService.svc/UpdateFaceReconStatus", json={"ReconStatus": True, "authToken": auth_token})
		response1 = json.loads(response.text)
		logger.debug("[Status Update]: UpdateFaceReconStatus API has been called successfully.")
	except:
		logger.exception("[Status Update]: Not able to call UpdateFaceReconStatus API.")
		return json.dumps({'ReconStatus': False, 'Msg': "UpdateFaceReconStatus API is not reachable"})

	# Check if update is successful or not
	if response1['Response']['Type'] == 'SUCCESS':
		records = {'ReconStatus': True, 'Msg': response1['Response']['Message']}
	else:
		records = {'ReconStatus': False, 'Msg': response1['Response']['Message']}
	# print(auth_token)
	# print(response)
	logger.debug("[Status Update]: {}".format(records['Msg']))
	return json.dumps(records)


@app.route("/faceparams", methods=['GET','POST'])
def check():
	try:
		# accepts the data
		data1 = request.json
		path = data1['path']
		id_ = data1['id']
		date = data1['date']

		logger.debug("[Check-in]: Check-in request recieved for userid {} with imagepath {}"
			          .format(id_,path))
		image = io.imread(path)
		image = cv2.resize(image, (512, 512))
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		boxes = face_recognition.face_locations(rgb, model='cnn')  # Model parameter can either be `cnn` or `hog`
		encodings = face_recognition.face_encodings(rgb, boxes)
		# initialize the list of names for each face detected
		names = []
		for encoding in encodings:
			matches = face_recognition.compare_faces(data['encodings'], encoding, tolerance=0.5)
			name = "Unknown"

			if True in matches:
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1
					
				name = max(counts, key=counts.get)
				
			# update the list of names
			names.append(name)
		# print(names)
		logger.debug("[Check-in]: The Person identified in the image is {} for userid {}.".format(names, id_))
		cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.1.72;DATABASE=Automate_Fulfilment;UID=steeplap_sa;PWD=St33p@12345')
		cursor = cnxn.cursor()
		cursor.execute("Select UserId, AttendanceDate from UserFaceReconStatus where UserId = (?) AND AttendanceDate= (?)", id_, date)
		if len(cursor.fetchall()) == 0:
			if str(id_) in names:
				cursor.execute("Insert into UserFaceReconStatus(UserId, AttendanceDate, isRecognized, CreatedDate) values (?,?,?,?)",
	                            id_, date, True, dt.now())
				cnxn.commit()
			else:
				# print(names)
				cursor.execute("Insert into UserFaceReconStatus(UserId, AttendanceDate, isRecognized, CreatedDate) values (?,?,?,?)",
	                            id_, date, False, dt.now())
				cnxn.commit()
				
		else:
			if str(id_) in names:
				cursor.execute("Update UserFaceReconStatus set isRecognized=(?), CreatedDate=(?) where UserId=(?) and AttendanceDate=(?)", True, date, id_, date)
				cnxn.commit()
			else:
				cursor.execute("Update UserFaceReconStatus set isRecognized=(?), CreatedDate=(?) where UserId=(?) and AttendanceDate=(?)", False, date, id_, date)
				cnxn.commit()
		logger.debug("[Check-in]: Updated Status in Database.")
		logger.debug("[Check-in]: Check-in request successfully processed.")
		return json.dumps({'Status': True})
	except:
		logger.exception("[Check-in]: Unable to process Check-in request.")
		return json.dumps({'Status': False})


app.run(host='0.0.0.0', port=8080, debug=False)   # Keeping `Debug=False` would allow to create log files

