from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)

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
    return render_template("mypage.html")

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
    
    query = "INSERT INTO User (email, username, password) VALUES (?, ?, ?);"
    cursor.execute(query, (email, username, password))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('mypage'))

@app.route("/logging-in", methods=['POST'])
def logging_in():
    conn = connect_db()
    cursor = conn.cursor()
    
    username_email = request.form['email-username']
    password = request.form['password']
    
    print("Received:", username_email, password)
    
    query = "SELECT * FROM User WHERE username = ? OR email = ?"
    cursor.execute(query, (username_email, username_email))
    details = cursor.fetchone()
    
    print(details)
    
    if details is None:
        conn.close()
        return redirect(request.referrer)
    
    stored_password = details[3]   
    
    if stored_password != password:
        conn.close()
        return redirect(request.referrer)
    
    conn.close()
    return redirect(url_for('mypage'))

if __name__ == "__main__":
    app.run(debug=True)
