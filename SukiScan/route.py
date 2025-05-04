from flask import render_template, session
from SukiScan import app

#HTML Routes
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

@app.route("/addcharacter")
def addcharacter():
    return render_template("addcharacter.html")

@app.route("/searchcharacter")
def searchcharacter():
    return render_template("searchcharacter.html")

@app.route("/mypage")
def mypage():
    #Declare variables for session
    id = session.get('id')
    email = session.get('email')
    username = session.get('username')
    
    #Pass variables into render so they can be used in webpage
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

@app.route("/myaddcharacter")
def myaddcharacter():
    return render_template("myaddcharacter.html")

@app.route("/mysearchcharacter")
def mysearchcharacter():
    return render_template("mysearchcharacter.html")

@app.route("/loginrequired")
def loginrequired():
    return render_template("loginrequired.html")
