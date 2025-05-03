import sqlite3
import os
from flask import render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, login_m
from SukiScan.forms import DetailsForm
from SukiScan.models import User

#Function that opens the database
def connect_db():
    path_way_to_db = os.path.join(os.path.dirname(__file__), 'data', 'sukiscan.db')
    return sqlite3.connect(path_way_to_db)

#HTML Routes Pre-Login
#Index URL
@app.route("/")
def index():
    return render_template("index.html")

#Home Url
@app.route("/home")
def home():
    return render_template("home.html")

#Social Url
@app.route("/social")
def social():
    return render_template("social.html")

#Login Url
@app.route("/login")
def login():
    return render_template("login.html")

#Signup Url
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Forms Routes
#Signing Up Function
@app.route("/add-details", methods=['POST'])
def add_details():
    #Connect to the Database
    conn = connect_db()
    cursor = conn.cursor()
    
    #Grab entered details from signup
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    #Query to get information for email and username
    query = "SELECT * FROM User WHERE email = ? OR username = ?"
    cursor.execute(query, (email, username))
    details = cursor.fetchone()
    
    #Check if email or username is being used
    if details is not None:
        if details[1] == email:
            flash("Email already in use. Choose another")
            conn.close()
            return redirect(request.referrer)
        
        elif details[2] == username:
            flash("Username already in use. Choose another")
            conn.close()
            return redirect(request.referrer)
    
    #Hash the password
    hashed_password = generate_password_hash(password)
    
    #Add the new details to database
    query = "INSERT INTO User (email, username, password) VALUES (?, ?, ?);"
    cursor.execute(query, (email, username, hashed_password))
    conn.commit()
    
    #Grab the details again to be used when automatically logging in post signup
    query = "SELECT * FROM User WHERE email = ? OR username = ?"
    cursor.execute(query, (email, username))
    details = cursor.fetchone()
    
    #Flask session allows us to pass variables through to different url calls, helps store for log in pages
    session['id'] = details[0]
    session['email'] = details[1]
    session['username'] = details[2]
    
    #Redirect to mypage after logging in
    conn.close()
    return redirect(url_for('mypage'))

#Logging In Function
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
    
    #Check if password is wrong by comparing hashes
    if not check_password_hash(details[3], password):
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

#HTML Routes Post-Login/Signup
#Mypage Url
@app.route("/mypage")
def mypage():
    #Declare variables for session
    id = session.get('id')
    email = session.get('email')
    username = session.get('username')
    
    #Pass variables into render so they can be used in webpage
    return render_template("mypage.html", id=id, username=username, email=email)

#Home Url
@app.route("/myhome")
def myhome():
    return render_template("myhome.html")

#Social Url
@app.route("/mysocial")
def mysocial():
    return render_template("mysocial.html")

@app.route("/placeholder")
def placeholder():
    return render_template("placeholder.html")