from pymongo import MongoClient

connection_string = "mongodb+srv://adishiro:gintoki@cluster0.wlmssnp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.get_database("ChatraMitra")
users = db.get_collection("users")


if __name__ == "__main__":
    anime_preferences = {
        'joy': [],
        'love': [],
        'anger': [],
        'sadness': [],
    }

    def userChoice(choices,anime_preferences_list):
        for gen_ind in choices:
            anime_preferences_list.append(list_of_animes_genre[(int(gen_ind)-1)])

    list_of_movies_genre = ['Music', 'Animation', 'History', 'Thriller', 'Mystery', 'Action', 'Western', 'TVMovie', 'Horror', 'Documentary', 'Drama', 'ScienceFiction', 'Romance', 'Crime', 'Fantasy', 'Adventure', 'Comedy', 'Family', 'War']
    list_of_animes_genre = ['Comedy', 'Mystery', 'Mecha', 'Vampire', 'Sports', 'Music', 'Dementia', 'Seinen', 'SuperPower', 'Thriller', 'Horror', 'Space', 'Supernatural', 'ShoujoAi', 'Game', 'MartialArts', 'Harem', 'Military', 'Cars', 'Psychological', 'Action', 'Demons', 'SliceofLife', 'School', 'Ecchi', 'ShounenAi', 'Historical', 'Shoujo', 'Parody', 'Hentai', 'Adventure', 'Fantasy', 'Shounen', 'Magic', 'Yuri', 'Romance', 'Drama', 'Police', 'Samurai', 'Josei', 'SciFi', 'Kids', 'Yaoi']

    print("What kind of anime would you like to watch when you are happy?")
    for i in range(0,len(list_of_animes_genre)):
        print("{}. {}".format((i+1),list_of_animes_genre[i]))
    h_gen = input().split(" ")
    userChoice(h_gen,anime_preferences['joy'])

    print("What kind of anime would you like to watch when you are in love?")
    for i in range(0,len(list_of_animes_genre)):
        print("{}. {}".format((i+1),list_of_animes_genre[i]))
    l_gen = input().split(" ")
    userChoice(l_gen,anime_preferences['love'])

    print("What kind of anime would you like to watch when you are angry?")
    for i in range(0,len(list_of_animes_genre)):
        print("{}. {}".format((i+1),list_of_animes_genre[i]))
    a_gen = input().split(" ")
    userChoice(a_gen,anime_preferences['anger'])

    print("What kind of anime would you like to watch when you are sad?")
    for i in range(0,len(list_of_animes_genre)):
        print("{}. {}".format((i+1),list_of_animes_genre[i]))
    s_gen = input().split(" ")
    userChoice(s_gen,anime_preferences['sadness'])

    doc = {
        "name": "Aditya Shirodkar",
        "username": "adishiroGOD",
        "birthdate": "18/9/2003",
        "password": "",
        "likes_more": "Anime",
        "anime_preferences": anime_preferences,
        "favourites": [],
        "anime_watched": [],
        "anime_considering": [],
        "anime_recommended": []
    }
    response = users.insert_one(doc)
    last_inserted_id = response.inserted_id
    print(db.list_collection_names())
    print(last_inserted_id)



    