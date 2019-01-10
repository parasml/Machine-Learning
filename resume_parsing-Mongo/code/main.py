import pandas as pd 
import numpy as np 
import config 
import pymongo
from pymongo import MongoClient
from resume_jd_match import resume_matching, skilled_resumes
import sys
import base64
from pprint import pprint
import warnings


warnings.filterwarnings("ignore")
downlaod_path = "E:/ML/resume_parsing-master/data/processed/"
pd.set_option('display.max_columns', None)


def main(jd, skills, city_, edu_, exp_):
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

        detailed_df['score'] = np.round(detailed_df['score'] * 100, 4)

        detailed_df['resume'] = downlaod_path + detailed_df['filename']

        detailed_df = detailed_df[['name', 'score', 'location', 'mobile number', 'education',
                                                             'email id', 'experience', 'upload_date', 'resume']]

        if edu_ == 'Graduate':
                edu_ = ['Graduate', 'B.E', 'Post Graduate', None]
        if edu_ == 'Post Graduate':
                edu_ = ['Post Graduate', None]
        if edu_ == 'HSC':
                edu_ = ['HSC', 'Graduate', 'Post Graduate', None]
        if edu_ == 'SSC':
                edu_ = ['SSC', 'HSC', 'Graduate', None]
        if edu_ == 'Diploma':
                edu_ = ['Diploma', 'B.E', None]


        detailed_df = detailed_df[(detailed_df['location'] == city_) & (detailed_df['education'].isin(edu_))]


        detailed_df.sort_values(by='score', ascending=False, inplace=True)
        detailed_df.to_csv(config.output_path+"matched_candidates.csv", index = False)
        # print("Hello World")
        # print(config.output_path+"matched_candidates.csv")
        print(detailed_df.reset_index(drop=True))
        # return detailed_df
 

if __name__ == "__main__":

    skills = ['python', 'machine learning', 'statistics', 'sql', 'spark', 'c#']
    city = 'Mumbai'
    edu = 'Graduate'
    exp = 1
    jd = """Human Resource HR Manager some random words to check if result is relevant or not, creative thinker, data nerd and possess strong analytical skills. 
 
 Develop and plan required analytic projects in response to business needs.  Partner with Product and Engineering teams to solve problems and identify trends and opportunities.  Processing, cleansing, and verifying the integrity of data used for analysis  Apply expertise in quantitative analysis, data mining, and the presentation of data to see beyond the numbers and understand how our users interact with both our consumer and business products.  Design and evaluate experiments  Data mining using state-of-the-art methods  Selecting features, building and optimizing classifiers using machine learning techniques  Enhancing data collection procedures to include information that is relevant for building analytic systems  Extending company’s data with third party sources of information when needed  Doing ad-hoc analysis and presenting results in a clear manner  Building and fine tuning analytical answers  Visualise the data with charts and graphs  Assist in building and analysing dashboards and reports  Contribute to data mining architectures, modelling standards, reporting, and data analysis methodologies  Work with application developers to extract data relevant for analysis  Propose what to build in the next roadmap  Understand ecosystems, user behaviours, and long-term trends  Identify new levers to help move key metrics  An attitude that ensures safe and secure operations. A security & privacy first approach to dealing with everything.  Ability to lead initiatives and people toward common goals.  Should possess good analytical and interpersonal communication skills. Able to write and communicate effectively.  Motivated to work in start-up environment. 
 c#
Requirements: 
 
 Experience in Data Science  Excellent understanding of machine learning techniques and algorithms, such as k-NN, Naive Bayes, SVM, Decision Forests, Neural Networks etc.  Experience with common data science toolkits, such as Python, NumPy, Pandas etc.  Experience with data visualisation tools, such as D3.js, GGplot, etc
                """
        

    # skills = str(sys.argv[1])
    # skills = skills.replace("-"," ")
    # skills = skills.split(",")

    # city = str(sys.argv[2])
    # city = city.replace("-"," ")

    # edu = str(sys.argv[3])
    # edu = edu.replace("-"," ")

    # exp = int(sys.argv[4])

    # jd = sys.argv[5: ]
    # jd = " ".join(jd)
    # jd = str(jd)
    main(jd, skills, city, edu, exp)