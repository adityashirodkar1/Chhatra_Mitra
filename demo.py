# this file is not important and not related to other files so no need to undertand this.
# ofc if you are curious then ask me i will tell u :)

import pandas as pd

def findGenre(a):
    gen = ""
    for ch in a:
        if ord(ch) in range(97,123) or ord(ch) in range(65,91):
            gen += ch
        if ord(ch) == 44:
            gen += ','
    return gen.split(",")

# arr = []
#df = pd.ExcelFile('../movieDatasetCopy.xlsx').parse()
df = pd.read_csv('../animes.csv')
#arr.append(df['Genre'])
arr = df['genre'].tolist()

start = findGenre(arr[0])
for i in range(1,len(arr)):
    start = list(set(start + findGenre(arr[i])))

#https://youtu.be/S7TbHDN8EXA