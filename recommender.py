import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import database as app
import emotion_detector as ed

user = app.users.find_one({})

#after analysing emotion, setting the required genre from user database
emotional_genre = []
print(ed.emotion)
for emo in ed.emotion:
    emotional_genre = list(set(emotional_genre + user['anime_preferences'][emo]))
    print(emotional_genre)


# Create another row and append row (as df) to existing CSV
row = [{'uid': -1, 'title':'TempAnime', 'synopsis':'Anything', 'genre': emotional_genre, 'aired': 'date', 'episodes':1, 'popularity': -1, 'score':-1, 'img_url':'nolink', 'link': 'nolink'}]
df = pd.DataFrame(row)
df.to_csv('../finalAnimeCSV.csv', mode='a', header=False, index=False)

df = pd.read_csv('../finalAnimeCSV.csv')

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title].index.values[0]

def get_genre_from_index(index):
    return df[df.index == index]["genre"].values[0]

#Step : Select Features
animeFeatures = ['genre','title']

#Step : Create a column in df which combines all the selected features
def combine_features(row):  
    return row["genre"]

df["combined_features"] = df.apply(combine_features, axis=1)
#print(df["combined_features"].head())

# Step : Create a new count matrix from this new combined column 
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

#Step : Compute the cosine similarity based on the count matrix
cosine_sim = cosine_similarity(count_matrix)

#Step : Get the index of the anime from its title
# anime_user_likes = input("Enter your favourite anime: ")
# anime_index = get_index_from_title(anime_user_likes)
similar_anime = list(enumerate(cosine_sim[15809]))

#Step : Get a list of sorted similar anime based on their similarity score
sorted_similar_anime = sorted(similar_anime,key=lambda x:x[1],reverse=True)

i = 0
for anime in sorted_similar_anime:
    recommended_anime = get_title_from_index(anime[0])
    if(recommended_anime == 'TempAnime'):
        continue
    print(recommended_anime," - ",get_genre_from_index(anime[0]))
    i += 1
    if i>45:
        break

df.drop([15809], axis=0, inplace=True)
df.to_csv('../finalAnimeCSV.csv', index = False)



