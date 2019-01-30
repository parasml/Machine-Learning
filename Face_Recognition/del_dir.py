import os
import argparse
import shutil
import requests
import json
import logging
from logging.handlers import TimedRotatingFileHandler


# Setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')

file_handler = TimedRotatingFileHandler("logs/deletelogs/delete.log", when="midnight", interval=1)
file_handler.setFormatter(formatter)
file_handler.suffix = "%Y%m%d"

logger.addHandler(file_handler)


# Setting up Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--userid", required=True,
	            help='userid to be deteled from the directory.')
args = vars(ap.parse_args())


path = 'data/train_images/' + args['userid']

try:
	shutil.rmtree(path)
	logger.debug("[Message]: Userid {} deleted from record successfully.".format(args['userid']))
except:
	logger.exception("[Exception]: Userid doen't exists.")


try:
	response = requests.post("http://wsbanking.go4automate.com/MService.svc/ResetUserFaceReconStatus", 
		                      json={"UserId": int(args['userid']), "authToken": "QXV0b21hdGVAMTIz"})
	response = json.loads(response.text)
	print(response)

	if response['Response']['Type'] == 'SUCCESS':
		logger.debug("[Message]: FaceReconStatus updated Successfully for userid {}.".format(args['userid']))
	else:
		logger.debug("[Message]: FaceReconStatus updation Failed for userid {}.".format(args['userid']))

except:
	logger.exception("[Exception]: UpdateFaceReconStatus API is not reachable.")


