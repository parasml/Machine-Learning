import os
import config
import pandas as pd
import numpy as np
import pickle
import re
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import Word2Vec, KeyedVectors
from pattern import en
from scipy import spatial
from nltk import word_tokenize
from nltk.corpus import stopwords
from pymongo import MongoClient
from collections import OrderedDict
from operator import itemgetter


np.random.seed(0)
# model1 = Word2Vec.load(config.output_path + "model1")


def resume_matching(jd, df):
    df = df.reset_index()
    data = jd.lower()
    
    w2v = []
    aux = " ".join(data.split(" ")[0:10]).lower()
    tech_skills = set(['java', 'sap', 'tester', 'testing', 'user interface', 'ui', 'analytics', 'developer', 'data analyst',
                       'big data', 'data scientist',])
    hr_skills = set(['hr', 'recurit', 'human resource'])
    sel = False
    sel2 = False
    for t in tech_skills:
        if t in aux:
            sel = True
    for t in hr_skills:
        if t in aux:
            sel2 = True


    # print(sel)
    if sel:
        model = Word2Vec.load(config.output_path + "model_tech")
        # print("Tech Model")
    elif sel2:
        model = Word2Vec.load(config.output_path + "model_hr")
        # print("HR Model")
    else:
        model = Word2Vec.load(config.output_path + "model_nontech")
        # print("Non-Tech Model")
    val = True

    for sentence in en.parsetree(data, tokenize=True, lemmata=True, tags=True):
        for chunk in sentence.chunks:
            for word in chunk.words:
                if val:
                    if word.lemma in model.wv.vocab:
                        w2v.append(model.wv[word.lemma])
                    else:
                        if word.lemma.lower() in model.wv.vocab:
                            w2v.append(model.wv[word.lemma.lower()])
                        # else:
                        #     if word.string in model.keys():
                        #     w2v.append(model[word.string])
                        #     else:
                        #     if word.string.lower() in model.keys():
                        #         w2v.append(model[word.string.lower()])

    Q_w2v = np.mean(w2v, axis=0)
    # print("Q_w2v: ", Q_w2v)
    D_w2v = []

    for i, yd in enumerate(df['text']):
        w2v = []
        for sentence in en.parsetree(str(yd).lower(), tokenize=True, lemmata=True, tags=True):
            for chunk in sentence.chunks:
                for word in chunk.words:
                    if val:
                        if word.lemma in model.wv.vocab:
                            w2v.append(model.wv[word.lemma])
                        else:
                            if word.lemma.lower() in model.wv.vocab:
                                w2v.append(model.wv[word.lemma.lower()])
                            # else:
                            # 	if word.string in model.keys():
                            # 		w2v.append(model[word.string])
                            # 	else:
                            # 		if word.string.lower() in model.keys():
                            #     w2v.append(model[word.string.lower()])
        D_w2v.append((np.mean(w2v, axis=0), df.iloc[i]['filename'], df.iloc[i]['date_inserted'], 
                      df.iloc[i]['have_skills'], df.iloc[i]['last_modified']))
    
    # retrieval = []
    retrieval = []
    for i in range(len(D_w2v)):
        retrieval.append((1 - spatial.distance.cosine(Q_w2v, D_w2v[i][0]), D_w2v[i][1], D_w2v[i][2], 
                          D_w2v[i][3], D_w2v[i][4]))

    retrieval = [i for i in retrieval if not np.isnan(i[0])]
    retrieval = [i for i in retrieval if i[0] > 0.4]
    retrieval.sort(reverse=True)
    
    # for i in range(len(retrieval)):
    #     print(f"CV : {retrieval[i][1]},  Score: {round(retrieval[i][0],2)}")

    return retrieval


def skilled_resumes(df, skills):
    len_skills = len(skills)
    resume_name = []
    number_of_skills = []
    for idx, row in df.iterrows():
        have_skills = []
        for s in skills:
            s = s.lower()
            pattern = r'\b'+s+r'\b'
            if re.search(pattern, str(row['text']).lower()):
                have_skills.append(s)
        
        if len(have_skills)/len_skills >= 0.5:
            resume_name.append(str(row['filename']))
            number_of_skills.append(len(have_skills))

    return resume_name, number_of_skills



if __name__ == '__main__':

    jd = """Role: User Interface Designer & Developer

Work Location: New Mumbai

Experience: 5-7 years

Desired Skills & Experience:
•   5-7 years of work experience with: Web application design, iOS design, Android design, front-end design, OSX design, interaction design, GUI design & Digital Marketing content
•   Proficiency in popular graphic designing tools - Photoshop, Dreamweaver & Illustrator, HTML, CSS 
•   Define interaction models, user task flows, and UX specifications 
•   Develop concepts through innovation and creativity
•   Create well-balanced and extremely innovative, original designs for digital marketing / websites / micro sites/ mobile and web applications.
•   Design banners, templates, emailers, flash animations, logos and landing pages
•   Result oriented and independent worker with out of the box and independent thinking capability
•   Must be able to justify the graphics / elements choices in the design     
•   Strong visualization skills
•   Must be detail oriented and have the ability to deliver on time and work under deadline pressure
"""

    skills = ['html', 'ui', 'user interface', 'design', 'css']

    client = MongoClient('localhost', 27017)
    db = client.Resparse 
    coll = db['ResumeText']

    df = pd.DataFrame(list(coll.find()))

    # df = pd.read_csv(config.output_path+"temp.csv")
    df.dropna(inplace=True)

    if skills:
        listOfResume, have_skills = skilled_resumes(df, skills)
        print(listOfResume)
        df = df[df['filename'].isin(listOfResume)]
        df['have_skills'] = have_skills
    
    resume_matching(jd, df)
