from flask import Flask, flash, request, redirect, url_for, session

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


hostname = "172.16.1.70"   # 172.16.1.70
data = pickle.loads(open("output/encodings.pickle", "rb").read())


def find_faces(rgb, boxes):
	encodings = face_recognition.face_encodings(rgb, boxes)

	# initialize the list of names for each face detected
	names = []
	for encoding in encodings:
		# attempt to match each face in the input image to our known encodings
		matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.48)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a dictionary to count 
			# the total number of times each face was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
	 
			# loop over the matched indexes and maintain a count for each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
	 
			# determine the recognized face with the largest number of votes 
			# Note: in the event of an unlikely tie Python will select first entry in the dictionary
			name = max(counts, key=counts.get)
	
		# update the list of names
		names.append(name)
	return names



@app.route("/faceDeviation2", methods=['POST'])
def main():
	path = request.form['path']
	id_ = request.form['id']

	image = cv2.imread(path)
	image = cv2.resize(image, (512, 512))

	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	boxes = face_recognition.face_locations(rgb, model='cnn')  # Model parameter can either be `cnn` or `hog`

	# Get some info from original image for rotation
	(h, w) = rgb.shape[:2]
	# calculate the center of the image
	center = (w / 2, h / 2)
	 
	angle90 = 90
	angle180 = 180
	angle270 = 270
	 
	scale = 1.0
	names = None
	if boxes:
		names = find_faces(rgb, boxes)
	else:
		# Rotate image by 90 degrees
		M = cv2.getRotationMatrix2D(center, angle90, scale)
		rotated90 = cv2.warpAffine(rgb, M, (h, w))
		boxes2 = face_recognition.face_locations(rotated90, model='cnn')
		if boxes2:
			names = find_faces(rotated90, boxes2)
		else:
			M = cv2.getRotationMatrix2D(center, angle270, scale)
			rotated270 = cv2.warpAffine(rgb, M, (h, w))
			boxes3 = face_recognition.face_locations(rotated270, model='cnn')
			if boxes2:
				names = find_faces(rotated270, boxes3)
			else:
				records = {'ReconStatus': False, 'Msg': "Face not detected."}
				return json.dumps(records)


	if len(names) > 1:
		records = {'ReconStatus': False, 'Msg': "Multiple Faces Detected in Image. Please try again."}

	elif len(names) == 1:
		if id_ in names: 
			records = {'ReconStatus': True, 'Msg': "Employee identification is successful for userid {} as {}".format(id_, names[0])}
		else:
			records = {'ReconStatus': False, 'Msg': "Employee identification failed for userid {}".format(id_)}

		
	return json.dumps(records)



@app.route("/register2", methods=['POST'])
def register():
	imagefile1 = request.files['file1']
	imagefile2 = request.files['file2']
	imagefile3 = request.files['file3']
	imagefile4 = request.files['file4']

	id_ = request.form['id']
	auth_token = request.form['authtoken']

	img_list = [imagefile1, imagefile2, imagefile3, imagefile4]

	try:
		os.makedirs("data/train_images/"+str(id_), exist_ok=True)
		for i,img in enumerate(img_list):
			offset = int(time.time())
			save_dir = "data/train_images/"+str(id_)+"/imagefile"+str(i)+str(offset)+".jpg"
			img.save(save_dir)
	except :
		return json.dumps({"ReconStatus":False , 'Msg': 'Error in the code'})

	imagePaths = list(paths.list_images("data/train_images/"+str(id_)))

	for i in imagePaths:
		temp = cv2.imread(i)
		rgb = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
		boxes = face_recognition.face_locations(rgb, model="hog")
		print("Faces in image {}: {}".format(i, boxes))
		if not boxes:
			records = {'ReconStatus': False, 'Msg': 'Can not find face in the image'}
			return json.dumps(records)
		elif len(boxes) > 1:
			records = {'ReconStatus': False, 'Msg': 'Multiple Faces detected in the image'}
			return json.dumps(records)

	response = requests.post("http://wsautomatebanking.calibehr.com/MService.svc/UpdateFaceReconStatus", json={"ReconStatus": True, "authToken": auth_token})
	response1 = json.loads(response.text)

	if response1['Response']['Type'] == 'SUCCESS':
		records = {'ReconStatus': True, 'Msg': 'Record Entered in Database'}
	else:
		records = {'ReconStatus': False, 'Msg': 'Failed to enter a record into Database'}
	# print(auth_token)
	# print(response)
	return json.dumps(records)


if __name__ == '__main__':
	
	app.run(host='0.0.0.0', port=5002, debug=True)
