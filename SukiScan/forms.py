from flask import request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from SukiScan import app
from .models import connect_db, AccountInfo

#Forms Routes
#Signing up in function
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
    if details:
        if details[1] == email:
            flash("Email already in use. Choose another")
        
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
    conn.close()
    
    #Grab the details again to be used when automatically logging in post signup
    userinfo = AccountInfo.Get_Info(username)
    login_user(userinfo)
    
    #Redirect to mypage after logging in
    return redirect(url_for('mypage'))

#Logging In function
@app.route("/logging-in", methods=['POST'])
def logging_in():
    #Connect to the Database
    conn = connect_db()
    cursor = conn.cursor()
    
    #Grab input from html form
    username_email = request.form['email-username']
    password = request.form['password']
    
    #Grab the details
    #Query to get information for email and username
    query = "SELECT * FROM User WHERE email = ? OR username = ?"
    cursor.execute(query, (username_email))
    details = cursor.fetchone()
    
    #Check user exists
    if details is None:
        flash("Username or Email not found")
        return redirect(request.referrer)  
    
    #Check if password is wrong by comparing hashes
    if not check_password_hash(details.password, password):
        flash("Password Incorrect")
        return redirect(request.referrer)
    
    #Flask session allows us to pass variables through to different url calls, helps store for log in pages
    userinfo = AccountInfo.Get_Info(username_email)
    login_user(userinfo)
    
    #Redirect to mypage after logging in
    return redirect(url_for('mypage'))