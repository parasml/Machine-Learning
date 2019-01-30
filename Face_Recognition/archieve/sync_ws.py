import threading
from queue import Queue
from skimage import io
import pandas as pd
import cv2
import face_recognition
import pickle
import numpy as np
import json
import time
import pyodbc
from datetime import datetime as dt


data = pickle.loads(open("output/encodings2.pickle", "rb").read())


class ImgProcessingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        self.input_queue.put(item)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        while True:
            try:
                path, id_, date = self.input_queue.get()
                if id_ is None:
                    break
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
                cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.1.70;DATABASE=AutomateBanking;UID=sa_admin;PWD=St33p@54321')
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
                        cursor.execute("Update UserFaceReconStatus set isRecognized=(?), CreatedDate=(?) where UserId = (?)", True, date, id_)
                        cnxn.commit()
                    else:
                        cursor.execute("Update UserFaceReconStatus set isRecognized=(?), CreatedDate=(?) where UserId = (?)", False, date, id_)
                        cnxn.commit()

                self.input_queue.task_done()
                time.sleep(1)
            except:
                print("Error!!!!")
        # Done
        self.input_queue.task_done()
        return
