from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "SukiScan"

#Function that opens the database
def connect_db():
    path_way_to_db = os.path.join(os.path.dirname(__file__), 'data', 'sukiscan.db')
    return sqlite3.connect(path_way_to_db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/social")
def social():
    return render_template("social.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/mypage")
def mypage():
    #Declare variables for session
    id = session['id']
    email = session['email']
    username = session['username']
    return render_template("mypage.html", id=id, username=username, email=email)

@app.route("/myhome")
def myhome():
    return render_template("myhome.html")

@app.route("/mysocial")
def mysocial():
    return render_template("mysocial.html")

@app.route("/placeholder")
def placeholder():
    return render_template("placeholder.html")

@app.route("/add-details", methods=['POST'])
def add_details():
    #Connect to the Database
    conn = connect_db()
    cursor = conn.cursor()
    
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    query = "SELECT * FROM User WHERE email = ? OR username = ?"
    cursor.execute(query, (email, username))
    details = cursor.fetchone()
    
    if details[1] == email:
        flash("Email already in use. Choose another")
        conn.close()
        return redirect(url_for('signup'))
    
    elif details[2] == username:
        flash("Username already in use. Choose another")
        conn.close()
        return redirect(request.referrer)
    
    query = "INSERT INTO User (email, username, password) VALUES (?, ?, ?);"
    cursor.execute(query, (email, username, password))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('mypage'))

@app.route("/logging-in", methods=['POST'])
def logging_in():
    #Connect to database
    conn = connect_db()
    cursor = conn.cursor()
    
    #Grab input from html form
    username_email = request.form['email-username']
    password = request.form['password']
    
    #Query DB for information on user
    query = "SELECT * FROM User WHERE username = ? OR email = ?"
    cursor.execute(query, (username_email, username_email))
    details = cursor.fetchone()

    #Check user exists
    if details is None:
        conn.close()
        flash("Username or Email not found")
        return redirect(request.referrer)  
    
    #Check if password is wrong
    if details[3] != password:
        conn.close()
        flash("Password Incorrect")
        return redirect(request.referrer)
    
    #Flask session allows us to pass variables through to different url calls, helps store for log in pages
    session['id'] = details[0]
    session['email'] = details[1]
    session['username'] = details[2]
    
    #Redirect to mypage after logging in
    conn.close()
    return redirect(url_for('mypage'))

if __name__ == "__main__":
    app.run(debug=True)
