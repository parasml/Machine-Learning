import config
import numpy as np 
import pandas as pd 
import os


path = config.output_path
os.chdir(path)
filename = 'output_List_of_districts_in_India_t'
cities = []

"""
for i in range(36):
    f = filename+str(i+1)+".csv"
    
    df = pd.read_csv(f, usecols=[1], encoding='ISO-8859-1', names=['city'], skiprows=1)
    print(f, df.columns)
    loc = list(df.city)

    cities.extend(loc)


# print(cities)
with open('location.txt','w') as f:
    for c in cities:
        f.write(c+"\n")
"""

df = pd.read_csv("location.csv", names=['Location'])

loc = list(df['Location'])
print(len(loc))
loc = list(set(loc))
print(len(loc))

df_new = pd.DataFrame(loc, columns=['Location'])
df_new.to_csv("location.csv", index=False)


