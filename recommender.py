import pandas as pd
import numpy as np
import hyperlink
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer()

def findGenre(a):
    gen = ""
    for ch in a:
        if ord(ch) in range(97,123) or ord(ch) in range(65,91):
            gen += ch
        if ord(ch) == 44:
            gen += ','
    return gen.split(",")

def get_title_from_index(index,df):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title,df):
    return df[df.title == title].index.values[0]

def get_genre_from_index(index,df):
    return df[df.index == index]["genre"].values[0]

def get_link_from_index(index,df):
    return df[df.index == index]["link"].values[0]

def get_poster_from_index(index,df):
    return df[df.index == index]["img_url"].values[0]

def get_synopsis_from_index(index,df):
    return df[df.index == index]["synopsis"].values[0]

def get_genre_from_index(index,df):
    return df[df.index == index]["genre"].values[0]

def get_score_from_index(index,df):
    return df[df.index == index]["score"].values[0]

def recommending(flag,anime_user_likes = 'Emote',emotional_genre = []):
    if flag == 1:
        df = pd.read_csv('finalAnimeCSV.csv')
        df["combined_features"] = df.apply(combine_features, axis=1)
        count_matrix = cv.fit_transform(df["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)
        anime_index = get_index_from_title(anime_user_likes,df=df)
        similar_anime = list(enumerate(cosine_sim[anime_index]))
    else:
        row = [{'uid': -1, 'title':'TempAnime', 'synopsis':'Anything', 'genre': emotional_genre, 'aired': 'date', 'episodes':1, 'popularity': -1, 'score':-1, 'img_url':'nolink', 'link': 'nolink'}]
        df = pd.DataFrame(row)
        df.to_csv('finalAnimeCSV.csv', mode='a', header=False, index=False)
        df = pd.read_csv('finalAnimeCSV.csv')
        df["combined_features"] = df.apply(combine_features, axis=1)
        count_matrix = cv.fit_transform(df["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)
        similar_anime = list(enumerate(cosine_sim[15809]))    

    sorted_similar_anime = sorted(similar_anime,key=lambda x:x[1],reverse=True)

    if flag==1:
        return sorted_similar_anime
    else:
        return sorted_similar_anime, df

def displaying_recommended_anime(anime_already_recommended,sorted_similar_anime):
    anime_to_show = [] ; i=0 ; recommended_anime_title = []
    df = pd.read_csv('finalAnimeCSV.csv')
    for anime in sorted_similar_anime:
        recommended_anime = get_title_from_index(anime[0],df=df)
        if(recommended_anime == 'TempAnime' or (recommended_anime.split(" ")[0] in recommended_anime_title)):
            continue
        recommended_anime_title.append(recommended_anime.split(" ")[0])
        temp_anime_dict = {
            "index": anime[0],
            "title": get_title_from_index(anime[0],df=df),
            "poster": get_poster_from_index(anime[0],df=df),
        }
        anime_to_show.append(temp_anime_dict)
        i += 1
        if i>5:
            break
    return anime_to_show

# how = int(input('How to search\n1 - By Name\n2 - Emotion\n'))
# if(how==2):
#     import emotion_detector as ed

#user = app.users.find_one({})

#after analysing emotion, setting the required genre from user database

# if how == 2:
#     for emo in ed.emotion:
#         emotional_genre = list(set(emotional_genre + user['anime_preferences'][emo]))
#         print(emotional_genre)

def detecting_genre(emotion,user):
    emotional_genre = []
    for emo in emotion:
        emotional_genre = list(set(emotional_genre + user['anime_preferences'][emo]))
        return emotional_genre


# Create another row and append row (as df) to existing CSV
# if how == 2:
#     row = [{'uid': -1, 'title':'TempAnime', 'synopsis':'Anything', 'genre': emotional_genre, 'aired': 'date', 'episodes':1, 'popularity': -1, 'score':-1, 'img_url':'nolink', 'link': 'nolink'}]
#     df = pd.DataFrame(row)
#     df.to_csv('finalAnimeCSV.csv', mode='a', header=False, index=False)



#Step : Select Features
animeFeatures = ['genre','title']

#Step : Create a column in df which combines all the selected features
def combine_features(row):
    # if how == 2:  
    #     return row["title"] + " " + row["genre"]
    return row["genre"]


# df["combined_features"] = df.apply(combine_features, axis=1)
#print(df["combined_features"].head())

# Step : Create a new count matrix from this new combined column 
# cv = CountVectorizer()
# count_matrix = cv.fit_transform(df["combined_features"])

#Step : Compute the cosine similarity based on the count matrix
# cosine_sim = cosine_similarity(count_matrix)

#Step : Get the index of the anime from its title
# if how==2:
#     similar_anime = list(enumerate(cosine_sim[15809]))
# else:
#     anime_user_likes = input("Enter your favourite anime: ")
#     anime_index = get_index_from_title(anime_user_likes)
#     similar_anime = list(enumerate(cosine_sim[get_index_from_title(anime_user_likes)]))

# #Step : Get a list of sorted similar anime based on their similarity score
# sorted_similar_anime = sorted(similar_anime,key=lambda x:x[1],reverse=True)

# recommended_anime_title = []

# j = 0
# while(True):
#     i = 0
#     print("\n")
#     for anime in sorted_similar_anime:
#         recommended_anime = get_title_from_index(anime[0])
        
#         if(recommended_anime == 'TempAnime' or (recommended_anime.split(" ")[0] in recommended_anime_title)):
#             continue
#         recommended_anime_title.append(recommended_anime.split(" ")[0])

#         url = hyperlink.parse(url = get_title_from_index(anime[0]))
#         better_url = url.replace(scheme=u'https', port=443)
#         org_url = better_url.click(u'.')

#         print(recommended_anime," - ",get_genre_from_index(anime[0])," - ",org_url.to_text())
#         i += 1
#         if i>10:
#             break   
    
#     flag = input("\nShuffle?: ")
#     if flag=='n':
#         break
#     j+=1
#     if j == 6:
#         j = 0
#         recommended_anime_title = []


def deleteLast(df):
    df.drop([15809], axis=0, inplace=True)
    df.to_csv('finalAnimeCSV.csv', index = False)

# df = pd.read_csv('finalAnimeCSV.csv')
# deleteLast(df=df)


