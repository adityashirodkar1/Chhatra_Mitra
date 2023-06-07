from flask import Flask , render_template , request , redirect, url_for , session
from flask_bcrypt import Bcrypt
from emotion_detector import *
import database as dbs
from recommender import *
from assignment import *
import rec
from bson import ObjectId
import smtp

anime_already_recommended = []
anime_user_likes = ""

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.pop('username')
    anime_to_show = []
    return redirect(url_for('index'))

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    print(session)

    user = dbs.users.find_one({'username' : session['username']})
    no_of_ass = user['assignments']
    if len(no_of_ass) > 0:
        for i in range(0,len(no_of_ass)):
            due = str_to_date(no_of_ass[i]['due'])
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = str_to_datetime(dt_string)
            time_left = subtract_date(due,now)
            days_left = time_left.days
            hrs_left = sec_to_hrs(time_left.seconds)
            print(time_left)
            print(time_left.days)
            print("time left")
            print(time_left.seconds)
            # if days_left == 1 and time_left.seconds == 43200:
            #     body = "1 day left to complete!!\nAssignment: " + no_of_ass[0]['assgn'] + "\nSubject: " + no_of_ass[0]['sub']
            #     smtp.send_mail(user['email'],body)
            # if days_left == 0 and time_left.seconds == 43200:
            #     body = "Only 12 hours left to complete!!\nAssignment: " + no_of_ass[0]['assgn'] + "\nSubject: " + no_of_ass[0]['sub']
            #     smtp.send_mail(user['email'],body)
            if days_left == 0 and time_left.seconds <= 14400 and time_left.seconds >= 13100:
                body = "Only 12 hours left to complete!!\nAssignment: " + no_of_ass[0]['assgn'] + "\nSubject: " + no_of_ass[0]['sub']
                smtp.send_mail(user['email'],body)
    return render_template('home.html', n = len(no_of_ass))

@app.route('/firstTime', methods = ['POST' , 'GET'])
def firstTime():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        imd = request.form
        anime_preferences = imd.to_dict(flat=False)
        subjects = imd['subjects'].split('-')
        attendance = []
        for sub in subjects:
            obj = {
                'sub_name': sub,
                'attended': 0,
                'not_attended': 0
            }  
            attendance.append(obj)
        myquery = {'username': session['username']} 
        newvalues = { "$set" : { "anime_preferences": anime_preferences } }
        dbs.users.update_one(myquery, newvalues)
        newvalues = { "$set" : { "attendance": attendance } }
        dbs.users.update_one(myquery, newvalues)
        print(session['username'])
        return redirect(url_for('home'))
    
    return render_template('firstTime.html', user = session['username'] ,genres = list_of_animes_genre)

@app.route('/login', methods=['POST'])
def login():
    users = dbs.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if bcrypt.check_password_hash(login_user['password'], request.form['pass']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = dbs.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(request.form['pass'], 10)
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username' : request.form['username'], 'password' : hashpass, 'email': request.form['email'] , 'dob' : request.form['dob'], 'attendance': [], 'assignments' : [], 'anime_dropped':[]})
            session['username'] = request.form['username']
            return redirect(url_for('firstTime'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/check')
def check():
    if 'username' not in session:
        return redirect(url_for('index'))
    current_user = dbs.users.find_one({'username': session['username']})
    if len(current_user['assignments']) > 0:
        nearest_ass = current_user['assignments'][0]
        if subdate(str_to_date(nearest_ass['due'])):
            return render_template('warning.html', ass = nearest_ass)
    return redirect(url_for('anime'))

@app.route('/anime')
def anime():
    if 'username' not in session:
        return redirect(url_for('index'))
    current_user = dbs.users.find_one({'username': session['username']})
    anime = []
    df = pd.read_csv('finalAnimeCSV.csv')
    franime = []
    if 'friends' in current_user:
        current_user_freind = current_user['friends']
        id = current_user_freind[0]
        objInstance = ObjectId(id)
        friend = dbs.users.find_one({"_id": objInstance})['anime_recommended']
        for i in friend:
            index = int(i)
            obj = {
                'index': index,
                'poster': get_poster_from_index(index,df),
                'title': get_title_from_index(index,df)
            }
            franime.append(obj)
    return render_template('anime.html', animes = anime, franime = franime)

@app.route('/byName')
def byName():
    if 'username' not in session:
        return redirect(url_for('index'))
    flag = 1 ; 
    df = pd.read_csv('finalAnimeCSV.csv')
    anime_user_likes = str(request.args.get('animeName'))
    sorted_similar_anime = recommending(flag = flag,anime_user_likes = anime_user_likes)
    anime_to_show = displaying_recommended_anime(anime_already_recommended,sorted_similar_anime)
    for anime in anime_to_show:
        anime_already_recommended.append(anime['index'])
    current_user = dbs.users.find_one({'username': session['username']})
    #anime_to_show = {k: v for k, v in anime_to_show.items() if v not in current_user['anime_dropped']}
    franime = []
    if 'friends' in current_user:
        current_user_friend = current_user['friends']
        id = current_user_friend[0]
        objInstance = ObjectId(id)
        friend = dbs.users.find_one({"_id": objInstance})['anime_recommended']
        for i in friend:
            index = int(i)
            obj = {
                'index': index,
                'poster': get_poster_from_index(index,df),
                'title': get_title_from_index(index,df)
            }
            franime.append(obj)
    return render_template('anime.html', animes = anime_to_show, franime = franime)

@app.route('/byEmotion', methods = ['POST', 'GET'])
def byEmotion():
    user_colors = []
    if request.method == 'GET':
        return render_template('color.html')
    else:
        df = pd.read_csv('finalAnimeCSV.csv')
        current_user = dbs.users.find_one({'username': session['username']})
        franime = []
        if 'friends' in current_user:
            current_user_friend = current_user['friends']
            id = current_user_friend[0]
            objInstance = ObjectId(id)
            friend = dbs.users.find_one({"_id": objInstance})['anime_recommended']
            for i in friend:
                index = int(i)
                obj = {
                    'index': index,
                    'poster': get_poster_from_index(index,df),
                    'title': get_title_from_index(index,df)
                }
                franime.append(obj)
        color = []
        for i in request.form:
            if request.form[i] == '1':
                color.append(i.upper())
        flag = 2
        user = dbs.users.find_one({'username': session['username']})
        emotion = analyse_emotion(color)
        emotional_genre = detecting_genre(emotion,user=user)
        sorted_similar_anime , df = recommending(flag = flag,emotional_genre=emotional_genre)
        anime_to_show = displaying_recommended_anime(anime_already_recommended,sorted_similar_anime)
        for anime in anime_to_show:
            anime_already_recommended.append(anime['index'])
        deleteLast(df=df)
        return render_template('anime.html', animes = anime_to_show, franime = franime)

@app.route('/spotify', methods = ['POST','GET'])
def spotify():
    if request.method == 'GET':
        return render_template('colorSongs.html')
    else:
        color = []
        for i in request.form:
            if request.form[i] == '1':
                color.append(i.upper())
        emotion = analyse_emotion(color)
        if 'happy' or 'sad' in emotion:
            songs = rec.hapSad
            if 'happy' in emotion:
                print('happy')
                songs = rec.sortHappyAngry(songs)
            else:
                print('sad')
                songs = rec.sortSadLove(songs)
        else:
            songs = rec.angryLov
            if 'angry' in emotion:
                print('angry')
                songs = rec.sortHappyAngry(songs)
            else:
                print('love')
                songs = rec.sortSadLove(songs)

        return render_template('spotify.html', songs = songs)

@app.route('/show/<i>')
def show(i):
    if 'username' not in session:
        return redirect(url_for('index'))
    df = pd.read_csv('finalAnimeCSV.csv')
    index = int(i)
    temp_anime_dict = {
        "index": index,
        "title": get_title_from_index(index,df),
        "score": get_score_from_index(index,df),
        "genre": findGenre(get_genre_from_index(index,df)),
        "poster": get_poster_from_index(index,df),
        "synopsis": get_synopsis_from_index(index,df),
        "link" : get_link_from_index(index,df)
    }
    return render_template('show.html', anime = temp_anime_dict)

@app.route('/assignment', methods=['POST','GET'])
def assignment():
    if 'username' not in session:
        return redirect(url_for('index'))
    myquery = {'username': session['username']}
    if request.method == 'POST':
        userAss = dbs.users.find_one(myquery)['assignments']
        userAss.append(request.form)
        sortedAss = sorted(userAss, key=lambda i: datetime.strptime(i['due'], "%Y-%m-%d"))
        newvalues = { "$set" : { "assignments": sortedAss } }
        dbs.users.update_one(myquery, newvalues)
        return redirect(url_for('assignment'))
    

    userAss = dbs.users.find_one(myquery)['assignments']
    if len(userAss) != 0:
        recent = userAss[0]['due']
        if toRemove(recent):
            userAss.pop(0)
            sortedAss = sorted(userAss, key=lambda i: datetime.strptime(i['due'], "%Y-%m-%d"))
            newvalues = { "$set" : { "assignments": sortedAss } }
            dbs.users.update_one(myquery, newvalues)
    return render_template('assignment.html', ass = userAss, n = len(userAss))

@app.route('/assignment/delete/<i>')
def assgnDelete(i):
    myquery = {'username': session['username']}
    userAss = dbs.users.find_one(myquery)['assignments']
    userAss.pop(int(i))
    sortedAss = sorted(userAss, key=lambda i: datetime.strptime(i['due'], "%Y-%m-%d"))
    newvalues = { "$set" : { "assignments": sortedAss } }
    dbs.users.update_one(myquery, newvalues)
    return redirect(url_for('assignment'))

@app.route('/attendance', methods = ['POST', 'GET'])
def attendance():
    if 'username' not in session:
        return redirect(url_for('index'))
    myquery = {'username': session['username']}
    attendance = dbs.users.find_one(myquery)['attendance']
    if request.method == 'POST':
        for sub in request.form:
            lst = sub.split("_")
            for i in range(0,len(attendance)):
                if attendance[i]['sub_name'] in lst and 'attended' in lst:
                    attendance[i]['attended'] += int(request.form[sub])
                elif attendance[i]['sub_name'] in lst and 'bunked' in lst:
                    attendance[i]['not_attended'] += int(request.form[sub])

        newvalues = { "$set" : { "attendance": attendance } }
        dbs.users.update_one(myquery, newvalues)
        return redirect(url_for('attendance'))

        
        
    return render_template('attendance.html', attendance = attendance)

@app.route('/attendance/subjects', methods = ['POST'])
def edit_subjects():
    subjects = request.form['subjects'].split('-')
    attendance = []
    for sub in subjects:
        obj = {
            'sub_name': sub,
            'attended': 0,
            'not_attended': 0
        }  
        attendance.append(obj)
    myquery = {'username': session['username']}
    newvalues = { "$set" : { "attendance": attendance } }
    dbs.users.update_one(myquery, newvalues)
    return redirect(url_for('attendance'))
    

@app.route('/status/<i>', methods = ['POST'])
def set_status(i):
    index = int(i)
    myquery = {'username': session['username']} 
    status = request.form
    if status["favourite"] == 'yes':
        newvalues = { "$addToSet" : { "favourites": index } }
        dbs.users.update_one(myquery, newvalues)
    if status["recommend"] == 'yes':
        newvalues = { "$addToSet" : { "anime_recommended": index } }
        dbs.users.update_one(myquery, newvalues)
    if status["status"] == 'watched':
        newvalues = { "$addToSet" : { "anime_watched": index } }
        dbs.users.update_one(myquery, newvalues)
    elif status["status"] == 'considering':
        newvalues = { "$addToSet" : { "anime_considering": index } }
        dbs.users.update_one(myquery, newvalues)
    else:
        newvalues = { "$addToSet" : { "anime_dropped": index } }
        dbs.users.update_one(myquery, newvalues)
    return redirect(url_for('anime'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)