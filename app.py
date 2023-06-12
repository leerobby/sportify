from flask import Flask, request, render_template, redirect, flash, jsonify, make_response, url_for
import mysql.connector
from login import Login
from date import date
import os

app = Flask(__name__, template_folder = "templates")
secret_key = os.urandom(24)
app.secret_key = secret_key

app.config['TEMPLATES_AUTO_RELOAD'] = True

db_url = 'mysql+pymysql://'

db = mysql.connector.connect(
    host = "34.22.79.75",
    user = "root",
    password = "alex050601",
    database = "mydb"
)

cur_user = Login()

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    #input
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    #fetch user id, password from db
    sqlform = "SELECT ID, password FROM User"
    cursor = db.cursor()
    cursor.execute(sqlform)
    result = cursor.fetchall()

    #check user id, pass from db
    #result index = (user id, password)
    for row in result:
        if user_id == row[0]:
            if password == row[1]:
                cur_user.login(user_id, password)
                return redirect("/dashboard")
            else:
                flash('Incorrect password. Please try again.', 'error')
                return render_template('login.html')

    cursor.close()

    #if user id doesn't exist or password is incorrect
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/register', methods = ['GET', 'POST'])
def register():
    #input
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    gender = request.form.get('gender')
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    #fetch user id from db
    sqlform = "SELECT ID FROM User"
    cursor = db.cursor()
    cursor.execute(sqlform)
    result = cursor.fetchall()

    #check user id from db
    #result index = (id,)
    #if user id is taken
    for row in result:
        if user_id == row[0]:
                return redirect("/signup")

    #else add data to db
    sqlform = "Insert into User(ID, first_name, last_name, gender, password) values (%s, %s, %s, %s, %s)"
    user_data = [(user_id, first_name, last_name, gender, password)]
    cursor.executemany(sqlform, user_data)
    db.commit()
    cursor.close()

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    #generate html file
    dashboard_file = open('templates/textFiles/dashboard1.txt', 'r')
    dashboard_html_content = dashboard_file.read()

    dashboard_html_content += f'<a href="/joined_match" id="profile"><span>{cur_user.user_id}</span></a>'

    dashboard_file = open('templates/textFiles/dashboard2.txt', 'r')
    dashboard_html_content += dashboard_file.read()

    #output html file
    with open('templates/dashboard.html', 'w') as file:
        file.write(dashboard_html_content)

    return render_template("dashboard.html")


@app.route('/match', methods = ['GET', 'POST'])
def match():
    #fetch matches from db
    sqlform = "SELECT date, time, event_name, sport_type, gender, location_id, price, joined_player, player_slot, host_name, ID FROM Matches"
    cursor = db.cursor()
    cursor.execute(sqlform)
    matches = cursor.fetchall()

    #fetch location name from db
    sqlform = "SELECT ID, venue_name, province, city, address FROM Location"
    cursor.execute(sqlform)
    locations = cursor.fetchall()
    cursor.close()

    #generate html file
    match_file = open('templates/textFiles/match1.txt', 'r')
    match_html_content = match_file.read()

    match_html_content += f'<a href="/joined_match" id="profile"><span>{cur_user.user_id}</span></a>'

    match_file = open('templates/textFiles/match2.txt', 'r')
    match_html_content += match_file.read()

    count = 0

    for row in matches:
        for location in locations:
            if row[5] == location[0]:
                match_loc = {'name': location[1], 'province': location[2], 'city': location[3], 'address': location[4]}
        
        match_html_content += f'<div class="grid_content">'
        day_month_string, suffix, year = date(row[0])
        match_html_content += f'<span id = "date_time">{day_month_string}<sup>{suffix}</sup> {year} &bull; {row[1]}</span><hr>'
        match_html_content += f'<p id="event_name">{row[2]}</p>'
        match_html_content += f'<p id="sport_type"><img src="{{{{url_for("static", filename="img/sport.png") }}}}" alt="Sport Icon">{row[3]}</p>'
        match_html_content += f'<p id="gender"><img src="{{{{ url_for("static", filename = "img/gender-fluid.png")}}}}" alt="Sport Icon">{row[4]}</p>'
        match_html_content += f'<p id="location"><img src="{{{{ url_for("static", filename = "img/location.png")}}}}" alt="Location Icon">{match_loc["name"]}, {match_loc["province"]}, {match_loc["city"]}, {match_loc["address"]}</p>'
        match_html_content += f'<p id="price"><img src="{{{{ url_for("static", filename = "img/price-tag.png")}}}}" alt="Price Icon">&#8361;{row[6]}</p>'
        match_html_content += f'<p id="player_slot">Slots: {row[7]}/{row[8]}</p><hr class="dashed"><h3>Host</h3>'
        match_html_content += f'<p id="host_name">{row[9]}</p><form action="#"><input type="button" value="Join Match" class="custom-button" id="button{count}"></form></div>'
        match_html_content += f'<script>'
        match_html_content += f'$(document).ready(function() {{'
        match_html_content += f'$("#button{count}").click(function() {{'
        match_html_content += f'$.ajax({{'
        match_html_content += f'url: "/join",'
        match_html_content += f'type: "POST",'
        match_html_content += f'data: JSON.stringify({{"match_id": "{row[10]}", "joined_player": "{row[7]}"}}),'
        match_html_content += f'contentType: "application/json",'
        match_html_content += f'success: function(response) {{'
        match_html_content += f'alert(response);'
        match_html_content += f'}},'
        match_html_content += f'error: function(xhr, status, error) {{'
        match_html_content += f'alert("An error occurred: " + error);'
        match_html_content += f'}}'
        match_html_content += f'}});'
        match_html_content += f'}});'
        match_html_content += f'}});'
        match_html_content += f'</script>'
        count += 1

    match_file = open('templates/textFiles/match3.txt', 'r')
    match_html_content += match_file.read()

    #output html file
    with open('templates/match.html', 'w') as file:
        file.write(match_html_content)
    
    return render_template("match.html")

@app.route('/join', methods = ['POST'])
def join():
    #fetch matches from db INT
    cursor = db.cursor()
    sqlform = "SELECT ID, player_slot, joined_player, player_0, player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, player_9 FROM Matches"
    cursor.execute(sqlform)
    matches = cursor.fetchall()

    #get match id from join button STR
    data = request.get_json()
    match_id = data['match_id']
    joined_player = data['joined_player']
    
    for row in matches:
        if int(match_id) == row[0]:
            #if match is not full
            #if joined player < player slot
            if row[2] < row[1]:

                players = row[3:]
                if cur_user.user_id in players:
                    return "You have joined this match!"

                #add data to db
                sqlform = "UPDATE Matches SET player_%s = %s WHERE ID = %s"
                cursor.execute(sqlform, (row[2], cur_user.user_id, row[0]))
                db.commit()
                sqlform = "UPDATE Matches SET joined_player = %s WHERE ID = %s"
                cursor.execute(sqlform, (row[2]+1, row[0]))
                db.commit()
                cursor.close()

                return "Match joined successfully"

            else:
                return "Slot is full"
    

@app.route('/create_match')
def create_match():
    #generate html file
    create_match_file = open('templates/textFiles/create_match1.txt', 'r')
    create_match_html_content = create_match_file.read()

    create_match_html_content += f'<a href="/joined_match" id="profile"><span>{cur_user.user_id}</span></a>'

    dashboard_file = open('templates/textFiles/create_match2.txt', 'r')
    create_match_html_content += dashboard_file.read()

    #output html file
    with open('templates/create_match.html', 'w') as file:
        file.write(create_match_html_content)
    return render_template("create_match.html")


@app.route('/make_match', methods = ['GET', 'POST'])
def make_match():
    #fetch matches from db
    sqlform = "SELECT ID FROM Matches"
    cursor = db.cursor()
    cursor.execute(sqlform)
    matches = cursor.fetchall()
    cur_match_id = len(matches) + 1

    #input
    event_name = request.form.get("event_name")
    sport_type = request.form.get("sport")
    player_num = request.form.get("p_num")
    location_id = request.form.get("location")
    gender = request.form.get("gender")
    date_time = request.form.get("date_time")
    date = date_time[:10]
    time = date_time[-5:]
    description = request.form.get("description")
    price = request.form.get("price")
    kakaopay = request.form.get("k_pay")
    naverpay = request.form.get("n_pay")
    payco = request.form.get("payco")
    tosspay = request.form.get("t_pay")
    smilepay = request.form.get("s_pay")
    card = request.form.get("card")
    cash = request.form.get("cos")

    #add data to db
    sqlform = "Insert into Matches(ID, event_name, sport_type, player_slot, Location_ID, gender, date, time, description, price, host_name, joined_player, player_0) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    match_data = [(cur_match_id, event_name, sport_type, player_num, location_id, gender, date, time, description, price, cur_user.user_id, 1, cur_user.user_id)]
    cursor.executemany(sqlform, match_data)
    db.commit()
    cursor.close()

    return redirect("/match")

@app.route('/find', methods = ['GET', 'POST'])
def find():
    return render_template("home.html")
    #input
    search_event_name = request.form.get('search')
    search_city = request.form.get('city')
    search_sport_type = request.form.get('sport')

    #fetch matches from db INT
    cursor = db.cursor()
    sqlform = "SELECT date, time, event_name, sport_type, gender, location_id, price, joined_player, player_slot, host_name, ID FROM Matches"
    cursor.execute(sqlform)
    matches = cursor.fetchall()

    #fetch location name from db
    sqlform = "SELECT ID, venue_name, province, city, address FROM Location"
    cursor.execute(sqlform)
    locations = cursor.fetchall()
    cursor.close()

    #generate html file
    match_file = open('templates/textFiles/match1.txt', 'r')
    match_html_content = match_file.read()

    match_html_content += f'<a href="/joined_match" id="profile"><span>{cur_user.user_id}</span></a>'

    match_file = open('templates/textFiles/match2.txt', 'r')
    match_html_content += match_file.read()

    count = 0
    selected_matches = []



    for row in matches:
        for location in locations:
            if row[5] == location[0]:
                loc_city = location[1]

        if search_event_name and search_city and search_sport_type:
            if row[2] == search_event_name and loc_city == search_city and row[3] == search_sport_type:
                matches.remove(row)
                selected_matches.append(row)
        elif search_event_name and search_city:
            if row[2] == search_event_name and loc_city == search_city:
                matches.remove(row)
                selected_matches.append(row)
        elif search_event_name and search_sport_type:
            if row[2] == search_event_name and row[3] == search_sport_type:
                matches.remove(row)
                selected_matches.append(row)
        elif search_city and search_sport_type:
            if loc_city == search_city and row[3] == search_sport_type:
                matches.remove(row)
                selected_matches.append(row)
        elif search_event_name:
            if row[2] == search_event_name:
                matches.remove(row)
                selected_matches.append(row)
        elif search_city:
            if loc_city == search_city:
                matches.remove(row)
                selected_matches.append(row)
        elif search_sport_type:
            if row[3] == search_sport_type:
                matches.remove(row)
                selected_matches.append(row)

        if selected_matches:
            for row in selected_matches:
                for location in locations:
                    if row[0] == location[0]:
                        match_loc = {'name': location[1], 'province': location[2], 'city': location[3], 'address': location[4]}

                match_html_content += f'<div class="grid_content">'
                day_month_string, suffix, year = date(row[0])
                match_html_content += f'<span id = "date_time">{day_month_string}<sup>{suffix}</sup> {year} &bull; {row[1]}</span><hr>'
                match_html_content += f'<p id="event_name">{row[2]}</p>'
                match_html_content += f'<p id="sport_type"><img src="{{{{url_for("static", filename="img/sport.png") }}}}" alt="Sport Icon">{row[3]}</p>'
                match_html_content += f'<p id="gender"><img src="{{{{ url_for("static", filename = "img/gender-fluid.png")}}}}" alt="Sport Icon">{row[4]}</p>'
                match_html_content += f'<p id="location"><img src="{{{{ url_for("static", filename = "img/location.png")}}}}" alt="Location Icon">{match_loc["name"]}, {match_loc["province"]}, {match_loc["city"]}, {match_loc["address"]}</p>'
                match_html_content += f'<p id="price"><img src="{{{{ url_for("static", filename = "img/price-tag.png")}}}}" alt="Price Icon">&#8361;{row[6]}</p>'
                match_html_content += f'<p id="player_slot">Slots: {row[7]}/{row[8]}</p><hr class="dashed"><h3>Host</h3>'
                match_html_content += f'<p id="host_name">{row[9]}</p><form action="#"><input type="button" value="Join Match" class="custom-button" id="button{count}"></form></div>'
                match_html_content += f'<script>'
                match_html_content += f'$(document).ready(function() {{'
                match_html_content += f'$("#button{count}").click(function() {{'
                match_html_content += f'$.ajax({{'
                match_html_content += f'url: "/join",'
                match_html_content += f'type: "POST",'
                match_html_content += f'data: JSON.stringify({{"match_id": "{row[10]}", "joined_player": "{row[7]}"}}),'
                match_html_content += f'contentType: "application/json",'
                match_html_content += f'success: function(response) {{'
                match_html_content += f'alert(response);'
                match_html_content += f'}},'
                match_html_content += f'error: function(xhr, status, error) {{'
                match_html_content += f'alert("An error occurred: " + error);'
                match_html_content += f'}}'
                match_html_content += f'}});'
                match_html_content += f'}});'
                match_html_content += f'}});'
                match_html_content += f'</script>'
                count += 1

    match_file = open('templates/textFiles/match3.txt', 'r')
    match_html_content += match_file.read()

    #output html file
    with open('templates/match.html', 'w') as file:
        file.write(match_html_content)
    
    return render_template("match.html")

@app.route('/about')
def about():
    #generate html file
    about_file = open('templates/textFiles/about1.txt', 'r')
    about_html_content = about_file.read()

    about_html_content += f'<a href="/joined_match" id="profile"><span>{cur_user.user_id}</span></a>'

    about_file = open('templates/textFiles/about2.txt', 'r')
    about_html_content += about_file.read()

    #output html file
    with open('templates/about.html', 'w') as file:
        file.write(about_html_content)
    
    return render_template("about.html")

@app.route('/joined_match', methods = ['GET', 'POST'])
def joined_match():

    joined_matches = []
    
    #fetch matches from db
    sqlform = "SELECT date, time, event_name, sport_type, gender, location_id, price, joined_player, player_slot, host_name, ID, player_0, player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, player_9 FROM Matches"
    cursor = db.cursor()
    cursor.execute(sqlform)
    matches = cursor.fetchall()

    for row in matches:
        players = row[11:]
        if cur_user.user_id in players:
            joined_matches.append(row)

    #fetch location name from db
    sqlform = "SELECT ID, venue_name, province, city, address FROM Location"
    cursor.execute(sqlform)
    locations = cursor.fetchall()
    cursor.close()

    #generate html file
    joined_match_file = open('templates/textFiles/joined_match1.txt', 'r')
    joined_match_html_content = joined_match_file.read()

    joined_match_html_content += f'<a href="/joined_nmatch" id="profile"><span>{cur_user.user_id}</span></a>'

    joined_match_file = open('templates/textFiles/joined_match2.txt', 'r')
    joined_match_html_content += joined_match_file.read()

    if len(joined_matches) == 0:
        joined_match_html_content += f'<h2>No match joined </h2>'

    else:
        joined_match_html_content += f'<div class="grid_layout">'

        for row in joined_matches:
            for location in locations:
                if row[5] == location[0]:
                    match_loc = location[1]
                    match_loc = {'name': location[1], 'province': location[2], 'city': location[3], 'address': location[4]}
            
            joined_match_html_content += f'<div class="grid_content">'
            day_month_string, suffix, year = date(row[0])
            joined_match_html_content += f'<span id = "date_time">{day_month_string}<sup>{suffix}</sup> {year} &bull; {row[1]}</span><hr>'
            joined_match_html_content += f'<p id="event_name">{row[2]}</p>'
            joined_match_html_content += f'<p id="sport_type"><img src="{{{{url_for("static", filename="img/sport.png") }}}}" alt="Sport Icon">{row[3]}</p>'
            joined_match_html_content += f'<p id="gender"><img src="{{{{ url_for("static", filename = "img/gender-fluid.png")}}}}" alt="Sport Icon">{row[4]}</p>'
            joined_match_html_content += f'<p id="location"><img src="{{{{ url_for("static", filename = "img/location.png")}}}}" alt="Location Icon">{match_loc["name"]}, {match_loc["province"]}, {match_loc["city"]}, {match_loc["address"]}</p>'
            joined_match_html_content += f'<p id="price"><img src="{{{{ url_for("static", filename = "img/price-tag.png")}}}}" alt="Price Icon">&#8361;{row[6]}</p>'
            joined_match_html_content += f'<p id="player_slot">Slots: {row[7]}/{row[8]}</p><hr class="dashed"><h3>Host</h3>'
            joined_match_html_content += f'<p id="host_name">{row[9]}</p></div>'

        joined_match_html_content += f'</div>'

    

        
    joined_match_file = open('templates/textFiles/joined_match3.txt', 'r')
    joined_match_html_content += joined_match_file.read()

    #output html file
    with open('templates/joined_match.html', 'w') as file:
        file.write(joined_match_html_content)
    
    return render_template("joined_match.html")



if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
