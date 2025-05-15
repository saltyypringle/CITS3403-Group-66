from flask import render_template, request, redirect, url_for, flash, jsonify, session
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
from sqlalchemy import func, union_all


#HTML Routes Pre-Login
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("mypage"))
    
    return render_template("index.html")

def get_most_popular():
    waifus = (
        db.session.query(
            WaifuLike.w_char_id.label('char_id'),
            func.count(WaifuLike.user_id).label('count'),
            db.literal('waifu').label('category')
        )
        .group_by(WaifuLike.w_char_id)
        .all()
    )
    
    husbandos = (
        db.session.query(
            HusbandoLike.h_char_id.label('char_id'),
            func.count(HusbandoLike.user_id).label('count'),
            db.literal('hsubando').label('category')
        )
        .group_by(HusbandoLike.h_char_id)
        .all()
    )
    
    others = (
        db.session.query(
            OtherLike.o_char_id.label('char_id'),
            func.count(OtherLike.user_id).label('count'),
            db.literal('other').label('category')
        )
        .group_by(OtherLike.o_char_id)
        .all()
    )
    
    combined_counts = {}
    
    for c in waifus:
        combined_counts[('waifu', c.char_id)] = c.count

    for c in husbandos:
        combined_counts[('husbando', c.char_id)] = c.count

    for c in others:
        combined_counts[('other', c.char_id)] = c.count
    
    top10 = sorted(combined_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    top_characters = []
    for (category, char_id), count in top10:
        if category == 'waifu':
            character = Waifu.query.filter(Waifu.w_char_id == char_id).first()
        elif category == 'husbando':
            character = Husbando.query.filter(Husbando.h_char_id == char_id).first()
        elif category == 'other':
            character = Other.query.filter(Other.o_char_id == char_id).first()
        
        top_characters.append({'character' : character})
    
    return top_characters

@app.route("/home")
def home():
    top_characters = get_most_popular()
    return render_template("home.html", top_characters=top_characters)

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
    top_characters = get_most_popular()
    return render_template("myhome.html", top_characters=top_characters)

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
    waifu_likes = WaifuLike.query.filter_by(user_id=current_user.user_id).order_by(WaifuLike.w_rank).all()
    
    pie_data = {
        "hair_colour": dict(Counter([wl.waifu.hair_colour for wl in waifu_likes])),
        "height": dict(Counter([wl.waifu.height for wl in waifu_likes])),
        "personality": dict(Counter([wl.waifu.personality for wl in waifu_likes])),
        "profession": dict(Counter([wl.waifu.profession for wl in waifu_likes])),
        "body_type": dict(Counter([wl.waifu.body_type for wl in waifu_likes]))
    }
    return render_template("waifus.html", waifu_likes=waifu_likes, pie_data=pie_data)

@app.route("/like/waifu/<int:w_char_id>", methods=["POST"])
@login_required
def like_waifu(w_char_id):
    existing = WaifuLike.query.filter_by(user_id=current_user.user_id, w_char_id=w_char_id).first()
    if not existing:
        db.session.add(WaifuLike(user_id=current_user.user_id, w_char_id=w_char_id))
        db.session.commit()
    return redirect(request.referrer or url_for("waifus"))

@app.route('/move_waifu/<int:w_char_id>/<direction>', methods=['POST'])
@login_required
def move_waifu(w_char_id, direction):
    waifu_likes = WaifuLike.query.filter_by(user_id=current_user.user_id).order_by(WaifuLike.w_rank).all()
    idx = next((i for i, wl in enumerate(waifu_likes) if wl.w_char_id == w_char_id), None)
    if idx is None:
        flash("Waifu not found in your list.", "warning")
        return redirect(url_for('waifus'))

    if direction == 'up' and idx > 0:
        waifu_likes[idx], waifu_likes[idx-1] = waifu_likes[idx-1], waifu_likes[idx]
    elif direction == 'down' and idx < len(waifu_likes) - 1:
        waifu_likes[idx], waifu_likes[idx+1] = waifu_likes[idx+1], waifu_likes[idx]

    # Reassign ranks to ensure they are sequential
    for new_rank, wl in enumerate(waifu_likes):
        wl.w_rank = new_rank

    print([(wl.w_char_id, wl.w_rank) for wl in waifu_likes])  # <-- Add this line

    db.session.commit()
    return redirect(url_for('waifus'))

@app.route("/husbandos")
@login_required
def husbandos():
    husbando_likes = HusbandoLike.query.filter_by(user_id=current_user.user_id).order_by(HusbandoLike.h_rank).all()
    pie_data = {
        "hair_colour": dict(Counter([hl.husbando.hair_colour for hl in husbando_likes])),
        "height": dict(Counter([hl.husbando.height for hl in husbando_likes])),
        "personality": dict(Counter([hl.husbando.personality for hl in husbando_likes])),
        "profession": dict(Counter([hl.husbando.profession for hl in husbando_likes])),
        "body_type": dict(Counter([hl.husbando.body_type for hl in husbando_likes]))
    }
    return render_template("husbandos.html", husbando_likes=husbando_likes, pie_data=pie_data)

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
    other_likes = OtherLike.query.filter_by(user_id=current_user.user_id).order_by(OtherLike.o_rank).all()
    pie_data = {
        "hair_colour": dict(Counter([ol.other.hair_colour for ol in other_likes])),
        "height": dict(Counter([ol.other.height for ol in other_likes])),
        "personality": dict(Counter([ol.other.personality for ol in other_likes])),
        "profession": dict(Counter([ol.other.profession for ol in other_likes])),
        "body_type": dict(Counter([ol.other.body_type for ol in other_likes]))
    }
    return render_template("others.html", other_likes=other_likes, pie_data=pie_data)

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
    waifu_likes = WaifuLike.query.filter_by(user_id=user_id).order_by(WaifuLike.w_rank).all()
    husbando_likes = HusbandoLike.query.filter_by(user_id=user_id).order_by(HusbandoLike.h_rank).all()
    other_likes = OtherLike.query.filter_by(user_id=user_id).order_by(OtherLike.o_rank).all()

    waifus = [like.waifu for like in waifu_likes]
    husbandos = [like.husbando for like in husbando_likes]
    others = [like.other for like in other_likes]

    # Get preferred gender from session or default to waifu
    preferred_gender = session.get("preferred_gender", "waifu")

    # Get top character of preferred gender
    if preferred_gender == "waifu":
        perfect_match = waifus[0] if waifus else None
    elif preferred_gender == "husbando":
        perfect_match = husbandos[0] if husbandos else None
    elif preferred_gender == "other":
        perfect_match = others[0] if others else None
    else:
        perfect_match = None

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
        top_traits=top_traits,
        perfect_match=perfect_match,
        preferred_gender=preferred_gender
    )

@app.route("/mypage", methods=["GET", "POST"])
@login_required
def mypage():
    # Handle preferred gender selection
    if request.method == "POST":
        preferred_gender = request.form.get("preferred_gender", "waifu")
        session["preferred_gender"] = preferred_gender
    else:
        preferred_gender = session.get("preferred_gender", "waifu")

    liked_waifus = [like.waifu for like in WaifuLike.query.filter_by(user_id=current_user.user_id).order_by(WaifuLike.w_rank).all()]
    liked_husbandos = [like.husbando for like in HusbandoLike.query.filter_by(user_id=current_user.user_id).order_by(HusbandoLike.h_rank).all()]
    liked_others = [like.other for like in OtherLike.query.filter_by(user_id=current_user.user_id).order_by(OtherLike.o_rank).all()]

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
    if body_types:
        top_traits.append(f"🏋️ {most_common(body_types)} Body Type")
        
    top_traits = top_traits[:3]

    # Select perfect match based on preferred gender
    if preferred_gender == "waifu":
        perfect_match = liked_waifus[0] if liked_waifus else None
    elif preferred_gender == "husbando":
        perfect_match = liked_husbandos[0] if liked_husbandos else None
    elif preferred_gender == "other":
        perfect_match = liked_others[0] if liked_others else None
    else:
        perfect_match = all_liked[0] if all_liked else None

    return render_template(
        "mypage.html",
        user=current_user,
        top_traits=top_traits,
        perfect_match=perfect_match,
        preferred_gender=preferred_gender
    )

@app.route('/update-username', methods=['POST'])
@login_required
def update_username():
    current_password = request.form['current_password']
    new_username = request.form['username']
    
    if check_current_password(current_user, current_password) and is_username_available(new_username):
        update_user_username(current_user, new_username)
        flash('Username successfully updated!', 'success')
    else:
        flash('Invalid password or username already taken!', 'error')
    
    return redirect(url_for('profile'))

def check_current_password(user, password):
    return check_password_hash(user.password, password)

def is_username_available(new_username):
    user = User.query.filter_by(username=new_username).first()
    return user is None

def update_user_username(user, new_username):
    user.username = new_username
    db.session.commit()

@app.route('/update-password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']

    if check_current_password(current_user, current_password):
        update_user_password(current_user, new_password)
        flash('Password successfully updated!', 'success')
    else:
        flash('Current password is incorrect!', 'error')

    return redirect(url_for('profile'))

def update_user_password(user, new_password):
    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()

@app.route('/move_husbando/<int:h_char_id>/<direction>', methods=['POST'])
@login_required
def move_husbando(h_char_id, direction):
    husbando_likes = HusbandoLike.query.filter_by(user_id=current_user.user_id).order_by(HusbandoLike.h_rank).all()
    idx = next((i for i, hl in enumerate(husbando_likes) if hl.h_char_id == h_char_id), None)
    if idx is None:
        flash("Husbando not found in your list.", "warning")
        return redirect(url_for('husbandos'))

    if direction == 'up' and idx > 0:
        husbando_likes[idx], husbando_likes[idx-1] = husbando_likes[idx-1], husbando_likes[idx]
    elif direction == 'down' and idx < len(husbando_likes) - 1:
        husbando_likes[idx], husbando_likes[idx+1] = husbando_likes[idx+1], husbando_likes[idx]

    # Reassign ranks to ensure they are sequential
    for new_rank, hl in enumerate(husbando_likes):
        hl.h_rank = new_rank

    db.session.commit()
    return redirect(url_for('husbandos'))

@app.route('/move_other/<int:o_char_id>/<direction>', methods=['POST'])
@login_required
def move_other(o_char_id, direction):
    other_likes = OtherLike.query.filter_by(user_id=current_user.user_id).order_by(OtherLike.o_rank).all()
    idx = next((i for i, ol in enumerate(other_likes) if ol.o_char_id == o_char_id), None)
    if idx is None:
        flash("Character not found in your list.", "warning")
        return redirect(url_for('others'))

    if direction == 'up' and idx > 0:
        other_likes[idx], other_likes[idx-1] = other_likes[idx-1], other_likes[idx]
    elif direction == 'down' and idx < len(other_likes) - 1:
        other_likes[idx], other_likes[idx+1] = other_likes[idx+1], other_likes[idx]

    # Reassign ranks to ensure they are sequential
    for new_rank, ol in enumerate(other_likes):
        ol.o_rank = new_rank

    db.session.commit()
    return redirect(url_for('others'))
