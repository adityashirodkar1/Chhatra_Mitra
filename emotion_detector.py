list_of_movies_genre = ['Music', 'Animation', 'History', 'Thriller', 'Mystery', 'Action', 'Western', 'TVMovie', 'Horror', 'Documentary', 'Drama', 'ScienceFiction', 'Romance', 'Crime', 'Fantasy', 'Adventure', 'Comedy', 'Family', 'War']
list_of_animes_genre = ['Comedy', 'Mystery', 'Mecha', 'Sports', 'Music', 'Seinen', 'SuperPower', 'Thriller', 'Horror', 'Supernatural', 'MartialArts', 'Harem', 'Military', 'Psychological', 'Action', 'Demons', 'SliceofLife', 'School', 'Ecchi', 'Historical', 'Shoujo', 'Parody', 'Adventure', 'Fantasy', 'Shounen', 'Magic', 'Romance', 'Drama', 'Police', 'Samurai', 'SciFi', 'Kids']

# hentai, cars, dementia, yuri, yaoi, shonen/shojo- ai, game, josei

colors = ["Light Orange - lo","Grey - gr","Dark Red - dr","Yellow - y","Black - bk","Brown - br","Blue - b","Light Red - lr","Green - g"]
joy_colors = ['Y','LO','G','B']
love_colors = ['LR']
anger_colors = ['DR']
sadness_colors = ['BR','GR','BK']

#------------all the functions-------------------

# function to put all their preferred in their user list according to their emotions
def userChoice(choices,user_choice_list):
    for gen_ind in choices:
        user_choice_list.append(list_of_movies_genre[(int(gen_ind)-1)])

# function to detect singular emotion of the user
def twOutOfThree(set,choices):
    if (choices[0].upper() in set and choices[1].upper() in set) or (choices[0].upper() in set and choices[2].upper() in set) or (choices[2].upper() in set and choices[1].upper() in set):
        return True
    return False

# function to detect composite emotions of the user
def compositeEmotion(set1,set2,choices):
    composite = set1 + set2
    if (choices[0].upper() in composite and choices[1].upper() in composite) or (choices[0].upper() in composite and choices[2].upper() in composite) or (choices[2].upper() in composite and choices[1].upper() in composite):
        return True
    return False

#------------all the functions end-------------------




# list of colors
# print('Choose any three colors among the given colors you want to color the given three objects:')
# for i in range(0,9):
#     print("{}. {}".format((i+1),colors[i]))

# # taking user input of colors
# choice1 = input("Color 1: ").upper()
# choice2 = input("Color 2: ").upper()
# choice3 = input("Color 3: ").upper()
# detecting emotions

def analyse_emotion(choices):
    if twOutOfThree(['Y','LO','G','B'], choices):
        emotion = 'joy'
    elif twOutOfThree(['LR'], choices):
        emotion = 'love'
    elif twOutOfThree(['DR'], choices):
        emotion = 'anger'
    elif twOutOfThree(['BR','GR','BK'], choices):
        emotion = 'sadness'
    elif compositeEmotion(['Y','LO','G','B'],['LR'], choices):
        emotion = 'joy-love'
    elif compositeEmotion(['DR'],['BR','GR','BK'], choices):
        emotion = 'anger-sadness'
    return emotion.split('-')

# emotion = emotion.split('-')




