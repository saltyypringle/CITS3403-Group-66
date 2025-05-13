from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User, Friends
from SukiScan.models import WaifuCheck, HusbandCheck, OtherCheck
from SukiScan.models import Waifu, Husbando, Other, WaifuLike
from SukiScan.models import WaifuLike, HusbandoLike, OtherLike
from SukiScan.models import ForumPost, ForumComment
from SukiScan.forms import ForumCommentForm

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

@app.route("/placeholder")
@login_required
def placeholder():
    return render_template("placeholder.html")

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
            return jsonify({"message": "Character already added"})
    
    elif char_type == "Husbando":
        exist = HusbandoLike.query.filter_by(user_id=current_user.user_id, h_char_id=int(char_id)).first()
        if not exist:
            db.session.add(HusbandoLike(user_id=current_user.user_id, h_char_id=int(char_id)))
        else:
            return jsonify({"message": "Character already added"})
    
    elif char_type == "Other":
        exist = OtherLike.query.filter_by(user_id=current_user.user_id, o_char_id=int(char_id)).first()
        if not exist:
            db.session.add(OtherLike(user_id=current_user.user_id, o_char_id=int(char_id)))
        else:
            return jsonify({"message": "Character already added"})
    
    db.session.commit()
    return jsonify({"message": "Character Added"})

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
    # Get current user's friends (accepted requests)
    friends_sent = Friends.query.filter_by(
        user_id=current_user.user_id, 
        status='accepted'
    ).all()
    friends_received = Friends.query.filter_by(
        friend_id=current_user.user_id, 
        status='accepted'
    ).all()
    
    # Get friend objects
    friend_list = []
    for f in friends_sent:
        friend_list.append(User.query.get(f.friend_id))
    for f in friends_received:
        friend_list.append(User.query.get(f.user_id))
    
    # Get pending friend requests
    pending_requests = Friends.query.filter_by(
        friend_id=current_user.user_id, 
        status='pending'
    ).all()
    
    pending_users = [User.query.get(f.user_id) for f in pending_requests]
    
    return render_template(
        "friends.html",
        friends=friend_list,
        pending_requests=pending_users
    )

@app.route("/search_users")
@login_required
def search_users():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    
    # Search for users whose username contains the query (case-insensitive)
    users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.user_id != current_user.user_id  # Exclude current user
    ).limit(10).all()
    
    # Format results
    results = []
    for user in users:
        # Check if already friends or has pending request
        existing_friendship = Friends.query.filter(
            ((Friends.user_id == current_user.user_id) & (Friends.friend_id == user.user_id)) |
            ((Friends.user_id == user.user_id) & (Friends.friend_id == current_user.user_id))
        ).first()
        
        status = existing_friendship.status if existing_friendship else None
        
        results.append({
            'id': user.user_id,
            'username': user.username,
            'status': status
        })
    
    return jsonify(results)

@app.route("/add_friend/<int:friend_id>", methods=['POST'])
@login_required
def add_friend(friend_id):
    if friend_id == current_user.user_id:
        return jsonify({'error': 'Cannot add yourself as friend'}), 400
        
    # Check if friendship already exists
    existing_friendship = Friends.query.filter(
        ((Friends.user_id == current_user.user_id) & (Friends.friend_id == friend_id)) |
        ((Friends.user_id == friend_id) & (Friends.friend_id == current_user.user_id))
    ).first()
    
    if existing_friendship:
        return jsonify({'error': 'Friend request already exists'}), 400
    
    # Create new friend request
    friend_request = Friends(
        user_id=current_user.user_id,
        friend_id=friend_id,
        status='pending'
    )
    
    db.session.add(friend_request)
    db.session.commit()
    
    return jsonify({'message': 'Friend request sent successfully'})

@app.route("/accept_friend/<int:request_id>", methods=['POST'])
@login_required
def accept_friend(request_id):
    friend_request = Friends.query.get_or_404(request_id)
    
    # Verify the request is for the current user
    if friend_request.friend_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    friend_request.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Friend request accepted'})

@app.route("/reject_friend/<int:request_id>", methods=['POST'])
@login_required
def reject_friend(request_id):
    friend_request = Friends.query.get_or_404(request_id)
    
    # Verify the request is for the current user
    if friend_request.friend_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    friend_request.status = 'rejected'
    db.session.commit()
    
    return jsonify({'message': 'Friend request rejected'})

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
