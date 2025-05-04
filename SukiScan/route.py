from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User

#HTML Routes Pre-Login
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

#Forms Login-Signup Routes
@app.route("/add-details", methods=['POST'])
def add_details():
    # Grab entered details from signup
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    # Check if email or username already exists
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing_user:
        if existing_user.email == email:
            flash("Email already in use. Choose another")
            return redirect(request.referrer)
        elif existing_user.username == username:
            flash("Username already in use. Choose another")
            return redirect(request.referrer)

    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create new user
    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    # Store user in session
    login_user(new_user)
    
    #Redirect to mypage
    return redirect(url_for('mypage'))

@app.route("/logging-in", methods=['POST'])
def logging_in():
    # Grab input from html form
    username_email = request.form['email-username']
    password = request.form['password']
    
    # Query DB for information on user
    user = User.query.filter(
        (User.username == username_email) | (User.email == username_email)
    ).first()
    
    if not user:
        flash("Username or Email not found")
        return redirect(request.referrer)
    
    if not check_password_hash(user.password, password):
        flash("Password Incorrect")
        return redirect(request.referrer)
    
    # Store user in session
    login_user(user)
    
    #Redirect to mypage
    return redirect(url_for('mypage'))

#HTML Route Post Login
@app.route("/mypage")
def mypage():
    #Declare variables for session
    id = session.get('id')
    email = session.get('email')
    username = session.get('username')
    
    #Pass variables into render so they can be used in webpage
    return render_template("mypage.html", id=id, username=username, email=email)

@app.route("/myhome")
@login_required
def myhome():
    return render_template("myhome.html")

@app.route("/mysocial")
@login_required
def mysocial():
    return render_template("mysocial.html")

@app.route("/placeholder")
@login_required
def placeholder():
    return render_template("placeholder.html")

@app.route("/myaddcharacter")
@login_required
def myaddcharacter():
    return render_template("myaddcharacter.html")

@app.route("/mysearchcharacter")
@login_required
def mysearchcharacter():
    return render_template("mysearchcharacter.html")

@app.route("/addcharacter")
@login_required
def addcharacter():
    return render_template("addcharacter.html")

@app.route("/searchcharacter")
@login_required
def searchcharacter():
    return render_template("searchcharacter.html")

@app.route("/loginrequired")
def loginrequired():
    return render_template("loginrequired.html")
