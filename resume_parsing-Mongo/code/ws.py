from flask import Flask
from flask import request

app = Flask(__name__)

import pandas as pd 
import numpy as np 
import config 
import pymongo
from pymongo import MongoClient
from resume_jd_match import resume_matching, skilled_resumes
import sys
import json


downlaod_path = "E:/ML/resume_parsing-master/data/processed/"
pd.set_option('display.max_columns', None)


@app.route("/", methods=['GET','POST'])
def main():

    jd = request.json['jd']
    skills = request.json['skills']
    city_ =request.json['city_']
    edu_ = request.json['edu_']
    exp_ = int(request.json['exp_'])

    skills = skills.split(",")
    skills = [i.strip() for i in skills]

    client = MongoClient(config.mongo_host, 27017)
    db = client.Resparse
    coll = db['ResumeText']
    df = pd.DataFrame(list(coll.find()))
    df.dropna(inplace=True)

    if skills:
        listOfResume, have_skills = skilled_resumes(df, skills)
        df = df[df['filename'].isin(listOfResume)]
        df['have_skills'] = have_skills
    else:
        df['have_skills'] = None

    matched_data = resume_matching(jd, df)

    matched_data = pd.DataFrame(matched_data, columns=['score', 'filename', 'date_inserted', 'have_skills', 'last_modified'])

    candidate_details = pd.DataFrame(list(db.CandidateDetails.find()))

    detailed_df = matched_data.merge(candidate_details, how='left', on ='date_inserted')

    del candidate_details, matched_data

    detailed_df['score'] = np.round(detailed_df['score'] * 100, 4)

    detailed_df['resume'] = downlaod_path + detailed_df['filename']

    # detailed_df['skill_score'] = detailed_df['have_skills'] / len(skills)

    detailed_df = detailed_df[['name', 'score', 'location', 'mobile number', 'education',
                               'email id', 'experience', 'upload_date', 'resume', 'alternate_location']]                                                    

    if edu_ == 'Graduate':
        edu_list = ['Graduate', 'B.E', 'Post Graduate', None]
    if edu_ == 'Post Graduate':
        edu_list = ['Post Graduate', None]
    if edu_ == 'HSC':
        edu_list = ['HSC', 'Graduate', 'Post Graduate', None]
    if edu_ == 'SSC':
        edu_list = ['SSC', 'HSC', 'Graduate', None]
    if edu_ == 'Diploma':
        edu_list = ['Diploma', 'B.E', None]
    if edu_ == 'B.E':
        edu_list = ['B.E']
    if not edu_:
        edu_list = ['Graduate', 'SSC', 'HSC', 'Post Graduate', 'Diploma', 'B.E']

    detailed_df['location'] = detailed_df['location'].str.lower()
    detailed_df['alternate_location'] = detailed_df['alternate_location'].str.lower()
    city_ = city_.lower()

    if city_ :
        detailed_df = detailed_df[((detailed_df['location'] == city_) | (detailed_df['alternate_location'] == city_))
                                                                 & (detailed_df['education'].isin(edu_list))]

    if exp_ :
        detailed_df = detailed_df[(detailed_df['experience'].between(exp_-2, exp_+2)) | (detailed_df['experience'].isnull())]

    # detailed_df['edu_score'] = np.where(detailed_df['education']==edu_, 100, 50)
    # detailed_df['city_score'] = np.where(detailed_df['location']==city_, 100, 50)
    # detailed_df['exp_score'] = np.select([detailed_df['experience']==exp_, detailed_df['experience']==exp_+1,
    #                                     detailed_df['experience']==exp_+2, detailed_df['experience']==exp_-1,
    #                                     detailed_df['experience']==exp_-2, detailed_df['experience']==0,
    #                                     detailed_df['experience']==None], [100, 75,50,75,50,20,20])

    # detailed_df['score2'] = (detailed_df['skill_score'] + detailed_df['edu_score'] + detailed_df['city_score']
    #                       + detailed_df['exp_score'])/4
    # detailed_df.drop(['edu_score','skill_score','city_score','exp_score'], axis=1, inplace=True)
    # detailed_df['combined_score'] = (detailed_df['score'] + detailed_df['score2'])/2


    detailed_df.drop(['alternate_location'], axis=1, inplace=True)
    detailed_df.columns = ['name','score','location','mobile','education',
                           'email','experience','upload_date','resume']   # add score2 column

    detailed_df.sort_values(by='score', ascending=False, inplace=True)
    detailed_df.to_csv(config.output_path+"matched_candidates.csv", index = False)
    # print(detailed_df.reset_index(drop=True))

    detailed_df = detailed_df.to_json(orient='records')
    
    return detailed_df


if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)