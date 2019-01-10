import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


import pandas as pd 
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from pattern import en
import pickle
import config
from nltk import pos_tag, word_tokenize
from pymongo import MongoClient


np.random.seed(0)

def preprocess_training_data(df, dir_model_name):
	"""
	    param df: dataframe
	    param dir_model_name: Name of the model

	"""
	all_text = ' '
	for i in df['text']:
		i = str(i)
		all_text+= i+" "

	all_text = all_text.lower()
	# print(all_text)

	vector = []

	tagged_text = pos_tag(word_tokenize(all_text))

	# for i in tagged_text:
	# 	if 'NN' in i[1] or 'JJ' in i[1] or 'VBG' in i[1]:
	# 		vector.append(i[0])

	vector = []
	for sentence in en.parsetree(all_text, tokenize=True, lemmata=True, tags=True):
		temp = []
		for chunk in sentence.chunks:
			for word in chunk.words:
				if word.tag == 'NN': # or word.tag == 'VB':
					temp.append(word.lemma)
		vector.append(temp)

	# print(vector)

	global model
	model = Word2Vec(vector, size=100, window=5, min_count=3, seed=42)
	model.save(config.output_path+dir_model_name)


if __name__ == '__main__':

	# client = MongoClient(config.mongo_host, 27017)
	# db = client.Resparse 
	# coll = db['ResumeText']
	# df = pd.DataFrame(list(coll.find()))

	df = pd.read_csv(config.output_path+"nontech.csv")
	df.dropna(inplace=True)

	preprocess_training_data(df, "model_nontech")


