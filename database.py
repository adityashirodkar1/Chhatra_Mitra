from pymongo import MongoClient


client = MongoClient(connection_string)
db = client.get_database("ChatraMitra")
users = db.get_collection("users")


if __name__ == "__main__":
    anime_preferences = { 'joy': [],'love': [],'anger': [],'sadness': [] } 

    def userChoice(choices,anime_preferences_list):
        for gen_ind in choices:
            anime_preferences_list.append(list_of_animes_genre[(int(gen_ind)-1)])

    list_of_movies_genre = ['Music', 'Animation', 'History', 'Thriller', 'Mystery', 'Action', 'Western', 'TVMovie', 'Horror', 'Documentary', 'Drama', 'ScienceFiction', 'Romance', 'Crime', 'Fantasy', 'Adventure', 'Comedy', 'Family', 'War']
    list_of_animes_genre = ['Comedy', 'Mystery', 'Mecha', 'Vampire', 'Sports', 'Music', 'Dementia', 'Seinen', 'SuperPower', 'Thriller', 'Horror', 'Space', 'Supernatural', 'ShoujoAi', 'Game', 'MartialArts', 'Harem', 'Military', 'Cars', 'Psychological', 'Action', 'Demons', 'SliceofLife', 'School', 'Ecchi', 'ShounenAi', 'Historical', 'Shoujo', 'Parody', 'Hentai', 'Adventure', 'Fantasy', 'Shounen', 'Magic', 'Yuri', 'Romance', 'Drama', 'Police', 'Samurai', 'Josei', 'SciFi', 'Kids', 'Yaoi']

    doc = {
            "name": "Haridas Singh",
            "username": "harisinghKING",
            "birthdate": "20/4/2003",
            "password": "",
            "likes_more": "Anime",
            "anime_preferences": anime_preferences,
            "favourites": ['One Piece', 'Black Clover', 'Naruto', 'Kimetsu no Yaiba'],
            "anime_watched": ['One Piece', 'Death Note', 'Naruto', 'Kimetsu no Yaiba', 'Fullmetal Alchemist: Brotherhood'],
            "anime_considering": [],
            "anime_recommended": ['One Piece', 'Black Clover', 'Naruto']
            
        }
        # {
        #     "name": "Onam Sarode",
        #     "username": "sarodeonam",
        #     "birthdate": "31/8/2002",
        #     "password": "",
        #     "likes_more": "Anime",
        #     "anime_preferences": anime_preferences,
        #     "favourites": ['Jujutsu Kaisen', 'Dragon Ball', 'Naruto'],
        #     "anime_watched": ['Jujutsu Kaisen', 'Dragon Ball', 'Naruto'],
        #     "anime_considering": ['Fullmetal Alchemist: Brotherhood', 'Shingeki no Kyojin'],
        #     "anime_recommended": ['Death Note', 'Dragon Ball', 'Kimetsu no Yaiba']
        # }
    # ]
    response = users.insert_one(doc)
    last_inserted_id = response.inserted_id
    print(db.list_collection_names())
    print(last_inserted_id)



    
