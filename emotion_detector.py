list_of_movies_genre = ['Music', 'Animation', 'History', 'Thriller', 'Mystery', 'Action', 'Western', 'TVMovie', 'Horror', 'Documentary', 'Drama', 'ScienceFiction', 'Romance', 'Crime', 'Fantasy', 'Adventure', 'Comedy', 'Family', 'War']
list_of_animes_genre = ['Comedy', 'Mystery', 'Mecha', 'Vampire', 'Sports', 'Music', 'Dementia', 'Seinen', 'SuperPower', 'Thriller', 'Horror', 'Space', 'Supernatural', 'ShoujoAi', 'Game', 'MartialArts', 'Harem', 'Military', 'Cars', 'Psychological', 'Action', 'Demons', 'SliceofLife', 'School', 'Ecchi', 'ShounenAi', 'Historical', 'Shoujo', 'Parody', 'Hentai', 'Adventure', 'Fantasy', 'Shounen', 'Magic', 'Yuri', 'Romance', 'Drama', 'Police', 'Samurai', 'Josei', 'SciFi', 'Kids', 'Yaoi']

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
def twOutOfThree(set):
    if (choice1 in set and choice2 in set) or (choice1 in set and choice3 in set) or (choice3 in set and choice2 in set):
        return True
    return False

# function to detect composite emotions of the user
def compositeEmotion(set1,set2):
    composite = set1 + set2
    if (choice1 in composite and choice2 in composite) or (choice1 in composite and choice3 in composite) or (choice3 in composite and choice2 in composite):
        return True
    return False

#------------all the functions end-------------------




# list of colors
print('Choose any three colors among the given colors you want to color the given three objects:')
for i in range(0,9):
    print("{}. {}".format((i+1),colors[i]))

# taking user input of colors
choice1 = input("Color 1: ").upper()
choice2 = input("Color 2: ").upper()
choice3 = input("Color 3: ").upper()

# detecting emotions
if twOutOfThree(joy_colors):
    emotion = 'joy'
elif twOutOfThree(love_colors):
    emotion = 'love'
elif twOutOfThree(anger_colors):
    emotion = 'anger'
elif twOutOfThree(sadness_colors):
    emotion = 'sadness'
elif compositeEmotion(joy_colors,love_colors):
    emotion = 'joy-love'
elif compositeEmotion(anger_colors,sadness_colors):
    emotion = 'anger-sadness'

emotion = emotion.split('-')




