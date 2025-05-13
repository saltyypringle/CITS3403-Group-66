from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User
from SukiScan.models import WaifuCheck, HusbandCheck, OtherCheck, Waifu, Husbando, Other, WaifuLike, HusbandoLike, OtherLike
from collections import Counter

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

@app.route("/addcharacter", methods=["GET", "POST"])
@login_required
def addcharacter():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
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

@app.route("/search", methods=['GET'])
@login_required
def search():
    #Initialise all the variables to search
    name = request.args.get('name').strip()
    hair = request.args.get('hair_colour').strip()
    height = request.args.get('height').strip()
    mbti = request.args.get('mbti').strip()
    body = request.args.getlist('body_type')
    type = request.args.getlist('character_type')
    
    #Check if a first name and last name is searched
    full_name = name.split()
    if len(full_name) > 0:
        f_name = full_name[0]
    else:
        f_name = ''
    
    if len(name) > 1:
        l_name = full_name[1]
    else:
        l_name = ''
    
    
    characters = []
    
    #Check is waifus is selected
    if 'waifu' in type:
        w_query = db.session.query(Waifu)
        #Query for name
        w_query = w_query.filter(
            Waifu.first_name.ilike(f"%{f_name}%"),
            Waifu.last_name.ilike(f"%{l_name}%")
        )
        #Query for hair colour
        if hair:
            w_query = w_query.filter(Waifu.hair_colour(f"%{hair}%"))
        #Query for Height
        if height:
            w_query = w_query.filter(Waifu.height == int(height))
        #Query for Personality
        if mbti:
            w_query = w_query.filter(Waifu.personality(f"%{mbti}%"))
        #Query for Body Type
        if body:
            w_query = w_query.filter(Waifu.body_type.in_(type))
        #Add Waifu characters to list
        w_characters = w_query.all()
        characters.extend(w_characters)
    
    #Check is husbandos is selected
    if 'husbando' in type:
        h_query = db.session.query(Husbando)
        #Query for name
        h_query = h_query.filter(
            Husbando.first_name.ilike(f"%{f_name}%"),
            Husbando.last_name.ilike(f"%{l_name}%")
        )
        #Query for hair colour
        if hair:
            h_query = h_query.filter(Husbando.hair_colour(f"%{hair}%"))
        #Query for Height
        if height:
            h_query = h_query.filter(Husbando.height == int(height))
        #Query for Personality
        if mbti:
            h_query = h_query.filter(Husbando.personality(f"%{mbti}%"))
        #Query for Body Type
        if body:
            h_query = h_query.filter(Husbando.body_type.in_(type))
        #Add Waifu characters to list
        h_characters = h_query.all()
        characters.extend(h_characters)
    
    #Check is others is selected
    if 'other' in type:
        o_query = db.session.query(Other)
        #Query for name
        o_query = o_query.filter(
            Other.first_name.ilike(f"%{f_name}%"),
            Other.last_name.ilike(f"%{l_name}%")
        )
        #Query for hair colour
        if hair:
            o_query = o_query.filter(Other.hair_colour(f"%{hair}%"))
        #Query for Height
        if height:
            o_query = o_query.filter(Other.height == int(height))
        #Query for Personality
        if mbti:
            o_query = o_query.filter(Other.personality(f"%{mbti}%"))
        #Query for Body Type
        if body:
            o_query = o_query.filter(Other.body_type.in_(type))
        #Add Waifu characters to list
        o_characters = o_query.all()
        characters.extend(o_characters) 
        
    return render_template('searchcharacter.html', characters=characters)

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

@app.route("/waifus")
@login_required
def waifus():
    liked_waifus = [like.waifu for like in WaifuLike.query.filter_by(user_id=current_user.user_id).all()]
    pie_data = {
        "hair_colour": dict(Counter([c.hair_colour for c in liked_waifus])),
        "height": dict(Counter([c.height for c in liked_waifus])),
        "personality": dict(Counter([c.personality for c in liked_waifus])),
        "profession": dict(Counter([c.profession for c in liked_waifus])),
        "body_type": dict(Counter([c.body_type for c in liked_waifus]))
    }
    return render_template("waifus.html", waifus=liked_waifus, pie_data=pie_data)

@app.route("/like/waifu/<int:w_char_id>", methods=["POST"])
@login_required
def like_waifu(w_char_id):
    existing = WaifuLike.query.filter_by(user_id=current_user.user_id, w_char_id=w_char_id).first()
    if not existing:
        db.session.add(WaifuLike(user_id=current_user.user_id, w_char_id=w_char_id))
        db.session.commit()
    return redirect(request.referrer or url_for("waifus"))

@app.route("/husbandos")
@login_required
def husbandos():
    liked_husbandos = [like.husbando for like in HusbandoLike.query.filter_by(user_id=current_user.user_id).all()]
    pie_data = {
        "hair_colour": dict(Counter([c.hair_colour for c in liked_husbandos])),
        "height": dict(Counter([c.height for c in liked_husbandos])),
        "personality": dict(Counter([c.personality for c in liked_husbandos])),
        "profession": dict(Counter([c.profession for c in liked_husbandos])),
        "body_type": dict(Counter([c.body_type for c in liked_husbandos]))
    }
    return render_template("husbandos.html", husbandos=liked_husbandos, pie_data=pie_data)

@app.route("/like/husbando/<int:h_char_id>", methods=["POST"])
@login_required
def like_husbando(h_char_id):
    existing = HusbandoLike.query.filter_by(user_id=current_user.user_id, h_char_id=h_char_id).first()
    if not existing:
        db.session.add(HusbandoLike(user_id=current_user.user_id, h_char_id=h_char_id))
        db.session.commit()
    return redirect(request.referrer or url_for("husbandos"))

@app.route("/others")
@login_required
def others():
    liked_others = [like.other for like in OtherLike.query.filter_by(user_id=current_user.user_id).all()]
    pie_data = {
        "hair_colour": dict(Counter([c.hair_colour for c in liked_others])),
        "height": dict(Counter([c.height for c in liked_others])),
        "personality": dict(Counter([c.personality for c in liked_others])),
        "profession": dict(Counter([c.profession for c in liked_others])),
        "body_type": dict(Counter([c.body_type for c in liked_others]))
    }
    return render_template("others.html", others=liked_others, pie_data=pie_data)

@app.route("/like/other/<int:o_char_id>", methods=["POST"])
@login_required
def like_other(o_char_id):
    existing = OtherLike.query.filter_by(user_id=current_user.user_id, o_char_id=o_char_id).first()
    if not existing:
        db.session.add(OtherLike(user_id=current_user.user_id, o_char_id=o_char_id))
        db.session.commit()
    return redirect(request.referrer or url_for("others"))
