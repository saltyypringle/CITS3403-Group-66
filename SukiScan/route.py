from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User, Shares
from SukiScan.models import WaifuCheck, HusbandCheck, OtherCheck
from SukiScan.models import Waifu, Husbando, Other, WaifuLike
from SukiScan.models import WaifuLike, HusbandoLike, OtherLike
from SukiScan.models import ForumPost, ForumComment
from SukiScan.forms import ForumCommentForm
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

@app.route("/myhome")
@login_required
def myhome():
    return render_template("myhome.html")

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
    f_name = full_name[0] if len(full_name) > 0 else ''
    l_name = full_name[1] if len(full_name) > 1 else ''
    
    characters = []
    
    #Check is waifus is selected
    if 'waifu' in type or not type:
        w_query = db.session.query(Waifu)
        #Query for waifus
        w_query = w_query.filter(
            Waifu.first_name.ilike(f"{f_name}%"),
            Waifu.last_name.ilike(f"{l_name}%"),
            Waifu.hair_colour.ilike(f"%{hair}%"),
            Waifu.personality.ilike(f"%{mbti}%"))
        if height:
            w_query = w_query.filter(Waifu.height == int(height))
        if body:
            w_query = w_query.filter(Waifu.body_type.in_(body))

        characters.extend([{
            'id': c.w_char_id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'hair_colour': c.hair_colour,
            'height': c.height,
            'mbti': c.personality,
            'profession': c.profession,
            'body_type': c.body_type,
            'image_url': c.image_url,
            'type' : "Waifu",
        } for c in w_query.all()])
        
    #Check is husbandos is selected
    if 'husbando' in type or not type:
        h_query = db.session.query(Husbando)
        #Query for husbandos
        h_query = h_query.filter(
            Husbando.first_name.ilike(f"{f_name}%"),
            Husbando.last_name.ilike(f"{l_name}%"),
            Husbando.hair_colour.ilike(f"%{hair}%"),
            Husbando.personality.ilike(f"%{mbti}%"))
        if height:
            h_query = h_query.filter(Husbando.height == int(height))
        if body:
            h_query = h_query.filter(Husbando.body_type.in_(body))
        

        characters.extend([{
            'id': c.h_char_id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'hair_colour': c.hair_colour,
            'height': c.height,
            'mbti': c.personality,
            'profession': c.profession,
            'body_type': c.body_type,
            'image_url': c.image_url,
            'type' : "Husbando",
        } for c in h_query.all()])
        
    
    #Check is others is selected
    if 'other' in type or not type:
        o_query = db.session.query(Other)
        #Query for others
        o_query = o_query.filter(
            Other.first_name.ilike(f"{f_name}%"),
            Other.last_name.ilike(f"{l_name}%"),
            Other.hair_colour.ilike(f"%{hair}%"),
            Other.personality.ilike(f"%{mbti}%"))
        if height:
            o_query = o_query.filter(Other.height == int(height))
        if body:
            o_query = o_query.filter(Other.body_type.in_(body))

        characters.extend([{
            'id': c.o_char_id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'hair_colour': c.hair_colour,
            'height': c.height,
            'mbti': c.personality,
            'profession': c.profession,
            'body_type': c.body_type,
            'image_url': c.image_url,
            'type' : "Other",
        } for c in o_query.all()])
    
    return jsonify({'characters': characters})
         
@app.route("/addlike", methods=["POST"])
@login_required
def addlike():
    data = request.get_json()
    char_id = data.get("char_id")
    char_type = data.get("char_type")
    
    if char_type == "Waifu":
        exist = WaifuLike.query.filter_by(user_id=current_user.user_id, w_char_id=int(char_id)).first()
        if not exist:
            db.session.add(WaifuLike(user_id=current_user.user_id, w_char_id=int(char_id)))
        else:
            return jsonify(success=False, message="Character Already Added!")
    
    elif char_type == "Husbando":
        exist = HusbandoLike.query.filter_by(user_id=current_user.user_id, h_char_id=int(char_id)).first()
        if not exist:
            db.session.add(HusbandoLike(user_id=current_user.user_id, h_char_id=int(char_id)))
        else:
            return jsonify(success=False, message="Character Already Added!")
    
    elif char_type == "Other":
        exist = OtherLike.query.filter_by(user_id=current_user.user_id, o_char_id=int(char_id)).first()
        if not exist:
            db.session.add(OtherLike(user_id=current_user.user_id, o_char_id=int(char_id)))
        else:
            return jsonify(success=False, message="Character Already Added!")
    
    db.session.commit()
    return jsonify(success=True, message="Character Added")

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
@login_required
def friends():
    shareto = db.session.query(Shares.recipient_id).filter_by(sharer_id=current_user.user_id).all()
    shareto_ids = [r[0] for r in shareto]
    shareto_users = User.query.filter(User.user_id.in_(shareto_ids)).all()
    
    sharedfrom = db.session.query(Shares.sharer_id).filter_by(recipient_id=current_user.user_id).all()
    sharedfrom_ids = [r[0] for r in sharedfrom]
    sharedfrom_users = User.query.filter(User.user_id.in_(sharedfrom_ids)).all()
    
    return render_template("friends.html", shareto=shareto_users, sharedfrom=sharedfrom_users)

@app.route("/searchfriends")
@login_required
def searchfriends():
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify([])
    
    results = User.query.filter(User.username.ilike(f"{query}%")).all()
    
    return jsonify([
        {"username": user.username, "user_id": user.user_id}
        for user in results if user.user_id != current_user.user_id
    ])

@app.route("/addshare/<int:user_id>", methods=["POST"])
@login_required
def addShare(user_id):
    db.session.add(Shares(sharer_id=current_user.user_id, recipient_id=user_id))
    db.session.commit()
    
    return jsonify({"success" : True})

@app.route("/removeshare/<int:user_id>", methods=["POST"])
@login_required
def removeShare(user_id):
    share = Shares.query.filter_by(sharer_id=current_user.user_id, recipient_id=user_id).first()
    db.session.delete(share)
    db.session.commit()
    return jsonify({"success" : True})


@app.route("/social", methods=["GET", "POST"])
@login_required
def social():
    if request.method == "POST":
        title = request.form.get("title")  # <-- get the title from the form
        content = request.form.get("content")
        if title and content:
            new_post = ForumPost(
                title=title,  # <-- use the actual title
                content=content,
                user_id=current_user.user_id
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Post submitted!")
        return redirect(url_for('social'))

    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template("social.html", posts=posts)

@app.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    content = request.form.get("comment")
    if content:
        new_comment = ForumComment(content=content, user_id=current_user.user_id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added!")
    return redirect(url_for('social'))

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = post.comments
    form = ForumCommentForm()
    if form.validate_on_submit():
        new_comment = ForumComment(
            content=form.content.data,
            user_id=current_user.user_id,
            post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added!")
        return redirect(url_for('view_post', post_id=post_id))
    return render_template("post_detail.html", post=post, comments=comments, form=form)

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

@app.route('/remove_waifu/<int:waifu_id>', methods=['POST'])
@login_required
def remove_waifu(waifu_id):
    waifu_like = WaifuLike.query.filter_by(user_id=current_user.user_id, w_char_id=waifu_id).first()
    if waifu_like:
        db.session.delete(waifu_like)
        db.session.commit()
        flash('Waifu removed from your list.', 'success')
    else:
        flash('Waifu not found in your list.', 'warning')
    return redirect(url_for('waifus'))

@app.route('/remove_husbando/<int:husbando_id>', methods=['POST'])
@login_required
def remove_husbando(husbando_id):
    husbando_like = HusbandoLike.query.filter_by(user_id=current_user.user_id, h_char_id=husbando_id).first()
    if husbando_like:
        db.session.delete(husbando_like)
        db.session.commit()
        flash('Husbando removed from your list.', 'success')
    else:
        flash('Husbando not found in your list.', 'warning')
    return redirect(url_for('husbandos'))

@app.route('/remove_other/<int:other_id>', methods=['POST'])
@login_required
def remove_other(other_id):
    other_like = OtherLike.query.filter_by(user_id=current_user.user_id, o_char_id=other_id).first()
    if other_like:
        db.session.delete(other_like)
        db.session.commit()
        flash('Other character removed from your list.', 'success')
    else:
        flash('Character not found in your list.', 'warning')
    return redirect(url_for('others'))

@app.route("/share/<int:user_id>")
@login_required
def share(user_id):
    # Only allow if the user is a friend
    is_friend = Shares.query.filter(
        ((Shares.sharer_id == current_user.user_id) & (Shares.recipient_id == user_id)) |
        ((Shares.sharer_id == user_id) & (Shares.recipient_id == current_user.user_id))
    ).first()
    if not is_friend and user_id != current_user.user_id:
        flash("You are not friends with this user.", "warning")
        return redirect(url_for("mypage"))

    user = User.query.get_or_404(user_id)
    waifus = [like.waifu for like in WaifuLike.query.filter_by(user_id=user_id).all()]
    husbandos = [like.husbando for like in HusbandoLike.query.filter_by(user_id=user_id).all()]
    others = [like.other for like in OtherLike.query.filter_by(user_id=user_id).all()]

    def count_traits(characters, attr):
        return dict(Counter(getattr(c, attr) for c in characters if getattr(c, attr)))

    pie_data = {
        "waifus": {
            "hair_colour": count_traits(waifus, "hair_colour"),
            "height": count_traits(waifus, "height"),
            "personality": count_traits(waifus, "personality"),
            "profession": count_traits(waifus, "profession"),
            "body_type": count_traits(waifus, "body_type"),
        },
        "husbandos": {
            "hair_colour": count_traits(husbandos, "hair_colour"),
            "height": count_traits(husbandos, "height"),
            "personality": count_traits(husbandos, "personality"),
            "profession": count_traits(husbandos, "profession"),
            "body_type": count_traits(husbandos, "body_type"),
        },
        "others": {
            "hair_colour": count_traits(others, "hair_colour"),
            "height": count_traits(others, "height"),
            "personality": count_traits(others, "personality"),
            "profession": count_traits(others, "profession"),
            "body_type": count_traits(others, "body_type"),
        }
    }

    all_liked = waifus + husbandos + others

    hair_colours = [c.hair_colour for c in all_liked if c.hair_colour]
    heights = [c.height for c in all_liked if c.height]
    personalities = [c.personality for c in all_liked if c.personality]
    professions = [c.profession for c in all_liked if c.profession]
    body_types = [c.body_type for c in all_liked if c.body_type]

    def most_common(lst):
        return Counter(lst).most_common(1)[0][0] if lst else None

    top_traits = []
    if hair_colours:
        top_traits.append(f"💛 {most_common(hair_colours)} Hair")
    if heights:
        top_traits.append(f"📏 {most_common(heights)}cm")
    if personalities:
        top_traits.append(f"🧠 {most_common(personalities)} Personality")
    if professions:
        top_traits.append(f"💼 {most_common(professions)}")
    if body_types:
        top_traits.append(f"🏋️ {most_common(body_types)} Body Type")
    top_traits = top_traits[:3]

    return render_template(
        "share.html",
        user=user,
        pie_data=pie_data,
        top_traits=top_traits
    )

@app.route("/mypage")
@login_required
def mypage():
    liked_waifus = [like.waifu for like in WaifuLike.query.filter_by(user_id=current_user.user_id).all()]
    liked_husbandos = [like.husbando for like in HusbandoLike.query.filter_by(user_id=current_user.user_id).all()]
    liked_others = [like.other for like in OtherLike.query.filter_by(user_id=current_user.user_id).all()]

    all_liked = liked_waifus + liked_husbandos + liked_others

    hair_colours = [c.hair_colour for c in all_liked if c.hair_colour]
    heights = [c.height for c in all_liked if c.height]
    personalities = [c.personality for c in all_liked if c.personality]
    professions = [c.profession for c in all_liked if c.profession]
    body_types = [c.body_type for c in all_liked if c.body_type]

    def most_common(lst):
        return Counter(lst).most_common(1)[0][0] if lst else None

    top_traits = []
    if hair_colours:
        top_traits.append(f"💛 {most_common(hair_colours)} Hair")
    if heights:
        top_traits.append(f"📏 {most_common(heights)}cm")
    if personalities:
        top_traits.append(f"🧠 {most_common(personalities)} Personality")
    if professions:
        top_traits.append(f"💼 {most_common(professions)}")
    if body_types:
        top_traits.append(f"🏋️ {most_common(body_types)} Body Type")

    top_traits = top_traits[:3]
    perfect_match = all_liked[0] if all_liked else None

    return render_template(
        "mypage.html",
        user=current_user,
        top_traits=top_traits,
        perfect_match=perfect_match
    )

    )