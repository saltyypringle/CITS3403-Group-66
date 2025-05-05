from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User
from SukiScan.models import WaifuCheck, HusbandCheck, OtherCheck

#HTML Routes Pre-Login
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

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
    #Pass variables into render so they can be used in webpage
    return render_template("mypage.html", user=current_user)

@app.route("/myhome")
@login_required
def myhome():
    return render_template("myhome.html")

@app.route("/social")
@login_required
def social():
    return render_template("social.html")

@app.route("/placeholder")
@login_required
def placeholder():
    return render_template("placeholder.html")

@app.route("/addcharacter", methods=["GET", "POST"])
@login_required
def addcharacter():
    if request.method == "POST":
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        hair_colour = request.form.get("hair_colour")
        height = request.form.get("height")
        personality = request.form.get("personality")
        profession = request.form.get("profession")
        body_type = request.form.get("body_type")
        character_type = request.form.get("character_type")

        # Normalize the body type to match the allowed values
        valid_body_types = ['Triangle', 'Inverted Triangle', 'Rectangle', 'Hourglass', 'Oval', 'Diamond']
        body_type = body_type.title() if body_type else None  # Capitalize the first letter

        if body_type not in valid_body_types:
            flash(f"Invalid body type. Please choose from {', '.join(valid_body_types)}.", "error")
            return redirect(url_for("addcharacter"))

        # Set full_name based on first and last name comparison
        full_name = f"{first_name} {last_name}".lower() if first_name.lower() != last_name.lower() else first_name.lower()

        check_model_map = {
            "waifu": WaifuCheck,
            "husbando": HusbandCheck,
            "other": OtherCheck
        }

        CheckModel = check_model_map.get(character_type)

        if not CheckModel:
            flash("Invalid character type selected.", "error")
            return redirect(url_for("addcharacter"))

        # Check for existing name (case-insensitive)
        existing = CheckModel.query.filter(
            db.func.lower(CheckModel.first_name) == first_name.lower(),
            db.func.lower(CheckModel.last_name) == last_name.lower()
        ).first()

        if existing:
            flash(f"{full_name.title()} already exists in review list for {character_type}.", "warning")
        else:
            # Create a new check record
            new_check = CheckModel(
                first_name=first_name,
                last_name=last_name,
                hair_colour=hair_colour,  # Now correctly linked
                height=height,
                personality=personality,
                profession=profession,
                body_type=body_type,
                submitted_by=current_user.user_id,  # Refer to current_user.user_id
                submission_date=db.func.current_timestamp(),
                status="Pending"  # Default status
            )
            db.session.add(new_check)
            db.session.commit()
            flash(f"{full_name.title()} has been submitted for review as a {character_type}.", "success")

        return redirect(url_for("addcharacter"))

    return render_template("addcharacter.html")

@app.route("/searchcharacter")
@login_required
def searchcharacter():
    return render_template("searchcharacter.html")

#HTML Route Post Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")

@app.route("/loginrequired")
def loginrequired():
    return render_template("loginrequired.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/friends")
def friends():
    return render_template("friends.html")
