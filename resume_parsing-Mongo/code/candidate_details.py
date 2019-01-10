import config
import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
import os
import more_itertools as mit
from collections import OrderedDict
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime as dt
from datetime import date


pd.set_option('display.max_columns', 500)
host = config.mongo_host
startTime = time.time()

os.environ['JAVAHOME'] = config.java_path
st = StanfordNERTagger('G:/Projects/resume_parsing/pkgs/stanford-ner/english.all.3class.distsim.crf.ser.gz',
                       'G:/Projects/resume_parsing/pkgs/stanford-ner/stanford-ner-2017-06-09/stanford-ner.jar')


def get_city(text, city):
    while text:
        text = text.partition('address')[-1].strip()
        if text != '':
            temp = next((w for w in nltk.word_tokenize(text) if w in city), None)
        else:
            text = text.partition('place')[-1].strip()
            temp = next((w for w in nltk.word_tokenize(text) if w in city), None)

        if temp:
            return temp.capitalize()


def get_eduction(text):
    ssc = config.ssc
    hsc = config.hsc
    diploma = config.diploma
    engineering = config.engineering
    degree = config.degree
    post_grad = config.post_grad

    if any(pg in text for pg in post_grad):  
        return 'Post Graduate'
    elif any(engg in text for engg in engineering):
        return 'B.E'
    elif any(deg in text for deg in degree):
        return 'Graduate'
    elif any(dip in text for dip in diploma):
        return 'Diploma'
    elif any(hs in text for hs in hsc):
        return 'HSC'
    elif any(ss in text for ss in ssc):
        return 'SSC'

def calculate_experience(resume_text):
    def get_month_index(month):
        month_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
        return month_dict[month.lower()]
    
    not_alpha_numeric = r'[^a-zA-Z\d]'
    number = r'\d+'
    months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
    months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
    month = r'('+months_short+r'|'+months_long+r')'
    year = r'((20|19)(\d{2})|(\d{2}))'
    start_date = month+not_alpha_numeric+r"?"+year
    end_date = r'(('+month+not_alpha_numeric+r"?"+year+r')|(present))'+not_alpha_numeric
    longer_year = r"((20|19)(\d{2}))"
    year_range = longer_year+not_alpha_numeric+r"{1,3}"+longer_year
    date_range =  r"("+start_date+not_alpha_numeric+r"{1,3}"+end_date+r")|("+year_range+r")"
    
    experience = 0
    start_month = -1
    start_year = -1
    end_month = -1
    end_year = -1
    regular_expression = re.compile(date_range, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
        date_range = regex_result.group()
        year_regex = re.compile(year)
        year_result = re.search(year_regex, date_range)
        if (start_year == -1) or (int(year_result.group()) <= start_year):
            start_year = int(year_result.group())
            month_regex = re.compile(months_short, re.IGNORECASE)
            month_result = re.search(month_regex, date_range)
            if month_result:
                current_month = get_month_index(month_result.group())
                if (start_month == -1) or (current_month < start_month):
                    start_month = current_month
        if date_range.lower().find('present') != -1:
            end_month = date.today().month # current month
            end_year = date.today().year # current year
        else:
            year_result = re.search(year_regex, date_range[year_result.end():])
            if (end_year == -1) or (int(year_result.group()) >= end_year):
                end_year = int(year_result.group())
                month_regex = re.compile(months_short, re.IGNORECASE)
                month_result = re.search(month_regex, date_range)
                if month_result:
                    current_month = get_month_index(month_result.group())
                    if (end_month == -1) or (current_month > end_month):
                        end_month = current_month
        resume_text = resume_text[regex_result.end():]
        regex_result = re.search(regular_expression, resume_text)
    return end_year - start_year



def get_details(cvs):
    locs = pd.read_csv(config.output_path+"location.csv")
    locs = list(locs['Location'])
    locs = [l.lower() for l in locs]

    client = MongoClient(host, 27017)
    db = client.Resparse 
    coll = db['CandidateDetails']

    for idx, cv in cvs.iterrows():
        name = None
        email = None
        mobile = None
        exact_loc = None
        alternate_loc = None
        latest_working_detail = None
        edu = None
        text = str(cv['text'])   
        text = text.strip("-:,'[]()/{/} ")

        if len(text) < 50:
            continue

    
        # get name
        name_list = {}
        count = 0
        text_part = text[:100]
        for sent in nltk.sent_tokenize(text_part):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = st.tag(tokens)
            for tag in tags:
                count += 1
                not_names = config.not_names
                build_names = config.building_names
                if tag[1] == 'PERSON' and tag[0].lower() not in not_names:
                    name_list[count] = tag[0]
                if tag[0].lower() in build_names:
                    val = name_list.get(count-1, None)
                    if val:
                        del name_list[count-1]

        cons = [list(group) for group in mit.consecutive_groups(sorted(name_list.keys()))]
        res = [[name_list[y] for y in x] for x in cons if len(x) > 1]
        if res:
            if len(res[0]) < 3:
                name = " ".join(res[0][:2])
            else: 
                name = " ".join(res[0][:3])

        if not name:
            pattern = re.compile(r"(?<![Ff]ather's )(?<![Mm]other's )(?<![Cc]ompany )(?<![Ff]ather’s )(?<![Mm]other’s )[Nn]ame\s*[:-]+\s*(\w+.?\s?\w+)")
            names = re.findall(pattern, text.lower())
            if names:
                name = names[0].upper()
            else:
                words = nltk.word_tokenize(text)
                words = [w for w in words if w.lower() not in not_names]
                words = [w for w in words if w.isalpha()]
                if len(words) > 1:
                    name = str(words[0])+" "+str(words[1])

        
        # get city
        text = text.lower()
        city = []
        for c in locs:
            a = re.search(r'\b'+c+r'\b', text)
            if a:
                city.append(c)

        if ('new delhi' in city) and ('delhi' in city):
            city.remove('delhi')

        if ('navi mumbai' in city) and ('mumbai' in city):
            city.remove('mumbai')

        exact_loc = get_city(text, city)

        if not exact_loc:
            city_count = {}
            for c in city:
                city_count[c] = text.count(c)

            if city_count:
                exact_loc = max(city_count, key=city_count.get)
                del city_count[exact_loc]
                exact_loc = exact_loc.capitalize()
                if city_count:
                    alternate_loc = max(city_count, key=city_count.get).capitalize()
        
        # get mobile number
        match_mob = re.search(r'((?:\(?\+?91\)?)?0?\d{10})', text)
        if match_mob:
            mobile = match_mob.group(0)

        
        # get email
        match_mail = re.search(r'[-\w-]*[:]*[[\w\.-]+@[\w\.-]+\.\w+', text)
        if match_mail:
            email = match_mail.group(0)
            if "-" in email:
                email = email.split("-")
                email = email[-1]
            elif ":" in email:
                email = email.split(":")
                email = email[-1]

            email = email.lstrip('0123456789-.:')


        # Last Working Details
        pattern= r"\D(\d{%d})\D" % 4
        all_years = re.findall(pattern, text)
        current_year = dt.now().year
        if all_years:
            all_years = [int(i) for i in all_years if int(i)<=current_year]
            if all_years:
                latest_working_detail = max(all_years)
        

        # Work Experience
        text = re.sub(pattern, "", text)
        exp = []
        total_experience = None
        for sent in nltk.sent_tokenize(text):
            if ("experience" in sent) and any(char.isdigit() for char in sent) and ("year" in sent):
                digits = re.findall(r'-?\d+\.?\d*', sent)
                if digits:
                    digits = [float(d) for d in digits if len(str(d))<5]
                    if digits:
                        if digits[0] < 30:
                            total_experience = digits[0]
                    
                break

        if not total_experience or total_experience == 0:
            total_experience = calculate_experience(text)

        # Get Education
        edu = get_eduction(text)


        records = {
                   'resume_name': cv['filename'], 
                   'name': name, 
                   'mobile number': mobile, 
                   'location': exact_loc,
                   'alternate location': alternate_loc,
                   'education': edu ,
                   'email id': email, 
                   'experience': total_experience, 
                   'latest working details': latest_working_detail,
                   'date_inserted': cv['date_inserted'],
                   'upload_date': cv['last_modified'],
                  }

        db.CandidateDetails.insert_one(records)
        # db.CandidateDetails.update({"date_inserted": records['date_inserted']}, 
        #                            {"$set": {"alternate_location": records['alternate location']}})
        print(records)



if __name__ == '__main__':
    client = MongoClient(host, 27017)
    db = client.Resparse 
    coll1 = db['ResumeText']
    coll2 = db['CandidateDetails']


    df1 = pd.DataFrame(list(coll1.find()))
    df2 = pd.DataFrame(list(coll2.find()))

    latest_upload_date = max(df2['date_inserted'])

    df1 = df1[df1['date_inserted'] > latest_upload_date]
    # print(df1)

    # df = pd.read_csv(config.output_path+"temp.csv")

    # Remove Null Values
    df1.dropna(inplace=True)

    get_details(df1)
    print('The script took {} second !'.format(time.time() - startTime))