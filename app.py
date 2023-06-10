from flask import Flask, request, render_template, redirect
import mysql.connector

app = Flask(__name__, template_folder = "templates")

db_url = 'mysql+pymysql://'

db = mysql.connector.connect(
    host = "34.22.79.75",
    user = "root",
    password = "alex050601",
    database = "mydb"
)

cur_user = ""

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
                return redirect("/dashboard")

    cursor.close()

    #if user id doesn't exist or password is incorrect
    cur_user = user_id
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
    return render_template("dashboard.html")


@app.route('/match', methods = ['GET', 'POST'])
def match():

    #fetch matches from db
    sqlform = "SELECT date, time, event_name, sport_type, location_id, price, host_name FROM Matches"
    cursor = db.cursor()
    cursor.execute(sqlform)
    matches = cursor.fetchall()

    # #fetch location name from db
    # sqlform = "SELECT ID, venue_name FROM Location"
    # cursor.execute(sqlform)
    # locations = cursor.fetchall()

    #generate html file
    match_file = open('templates/match1.txt', 'r')
    html_content = match_file.read()

    for row in matches:

        html_content += f'<div class="grid_content">'
        html_content += f'<span>{row[0]} &bull; {row[1]}</span><br>'
        html_content += f'<span>{row[2]}</span><br>'
        html_content += f'<span>{row[3]}</span><br>'
        html_content += f'<span>{row[4]}</span><br>'
        html_content += f'<span>{row[5]}</span><br>'
        html_content += f'<span>{row[6]}</span><br> </div>'

    match_file = open('templates/match2.txt', 'r')
    html_content += match_file.read()

    #output html file
    with open('templates/match2.html', 'w') as file:
        file.write(html_content)
    
    return render_template("match2.html")


@app.route('/create_match')
def create_match():
    return render_template("create_match.html")


@app.route('/make_match', methods = ['GET', 'POST'])
def make_match():
    cur_match_id = 1

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
    sqlform = "Insert into Matches(ID, event_name, sport_type, player_slot, Location_ID, gender, date, time, description, price, host_name) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db.cursor()
    match_data = [(cur_match_id, event_name, sport_type, player_num, location_id, gender, date, time, description, price, cur_user)]
    cursor.executemany(sqlform, match_data)
    db.commit()
    cursor.close()

    cur_match_id += 1

    return render_template("dashboard.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)