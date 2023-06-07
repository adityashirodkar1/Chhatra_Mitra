import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm
from operator import itemgetter

df = pd.read_csv("valence_arousal_dataset.csv")
print(df.shape)
df.head()

df["mood_vec"] = df[["valence", "energy"]].values.tolist()
df["mood_vec"].head()

# uri = df["uri"][0]
# valence = df["valence"][0]
# liveness = df["liveness"][0]

hapSad = []
for i in range(0,194):
    avg = (df["valence"][i] + df["liveness"][i])/2
    dic = {
        'uri' : df["uri"][i],
        'avg': avg
    }
    hapSad.append(dic)

angryLov = []
for i in range(0,194):
    avg = (df["energy"][i] + df["danceability"][i])/2
    dic = {
        'uri' : df["uri"][i],
        'avg': avg
    }
    angryLov.append(dic)

def sortHappyAngry(hapSad):
    lst = sorted(hapSad, key=itemgetter('avg'), reverse=True)
    return lst

def sortSadLove(hapSad):
    lst = sorted(hapSad, key=itemgetter('avg'))
    return lst

sp = authorization.authorize()

def recommend(track_id, ref_df, sp, n_recs = 5):
    
    # Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    #print(f"mood_vec for {track_id}: {track_moodvec}")
    
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

# track1 = random.choice(df["id"])
# print ('Input song')
# turi = 'spotify:track:'+track1
# print (turi)
# r = recommend(track_id = track1, ref_df = df, sp = sp, n_recs = 5)
# songs = list(r.uri)
# print (list(r.uri)[0])
#mad_world = "3JOVTQ5h8HGFnDdp4VT3MP"
#recommend(track_id = mad_world, ref_df = df, sp = sp, n_recs = 5)
