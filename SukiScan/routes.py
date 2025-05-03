from flask import render_template, session
from flask_login import login_required, logout_user, current_user
from SukiScan import app

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

#HTML Routes Post-Login/Signup
#Mypage Url
@app.route("/mypage")
@login_required
def mypage():
    #Declare variables for session
    #Pass variables into render so they can be used in webpage
    return render_template("mypage.html", id=current_user.id, username=current_user.username, email=current_user.email)

#Home Url
@app.route("/myhome")
@login_required
def myhome():
    return render_template("myhome.html")

#Social Url
@app.route("/mysocial")
@login_required
def mysocial():
    return render_template("mysocial.html")

@app.route("/placeholder")
@login_required
def placeholder():
    return render_template("placeholder.html")

#Logout HTML
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")