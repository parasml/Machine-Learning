import os
import config
import textract
import pandas as pd
import PyPDF2
import warnings
import re
from pymongo import MongoClient
import json
from datetime import datetime


host = config.mongo_host
warnings.filterwarnings("ignore")
path_ = "G:/Projects/resume_parsing/data/new/"  # config.data_new
files = os.listdir(path_)
# print(files)

dates = []
f_name = []
txt = []
last_modified = []
bad_files = []

# Remember to remove idx while writing into Database
for idx, f in enumerate(files):

    text = None
    if f.endswith('.docx'):
        try:
            text = textract.process(path_ + f)
            text = text.decode('utf-8')
            # text = ''.join(t for t in text).strip()
            text = ' '.join(text.split())
            dates.append(datetime.now())
            f_name.append(f)
            txt.append(text)
            t = os.path.getmtime(path_ + f)
            last_modified.append(datetime.fromtimestamp(t).strftime('%Y-%m-%d'))

        except:
            bad_files.append(f)
            pass

    elif f.endswith('.pdf'):

        try:
            pdfFileObj = open(path_ + f, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            page_num = pdfReader.getNumPages()
            text = []
            for pg in range(page_num):
                text_ = PyPDF2.PdfFileReader(pdfFileObj).getPage(pg).extractText()
                text_ = ' '.join(text_.split())
                # To remove blank spaces in email id
                text_n = re.sub(r'[\w.-]+ ?@(?: [\w.-]+com|[\w. -]+com)', lambda e: e[0].replace(' ', ''), text_)
                text.append(text_n)

            dates.append(datetime.now())
            f_name.append(f)
            txt.append(text)
            t = os.path.getmtime(path_ + f)
            last_modified.append(datetime.fromtimestamp(t).strftime('%Y-%m-%d'))
        except :
            bad_files.append(f)
            pass

temp = pd.DataFrame({'date_inserted': dates, 'filename': f_name, 'text': txt, 'last_modified': last_modified})
# temp.to_csv(config.output_path + "temp.csv", index=False)

client = MongoClient(host, 27017)
db = client.Resparse
coll = db['ResumeText']

records = json.loads(temp.T.to_json()).values()
db.ResumeText.insert(records)
# print(len(records))


# Files that can not be decrypted 
print("Unprocessed Files")
for i in bad_files:
    print(i)

