import sqlite3
import os
from flask import request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app

#Function that opens the database
def connect_db():
    path_way_to_db = os.path.join(os.path.dirname(__file__), 'data', 'sukiscan.db')
    return sqlite3.connect(path_way_to_db)

#Forms Routes
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