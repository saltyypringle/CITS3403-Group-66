'''import sqlite3
import os
from flask import request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from SukiScan import app, db
from SukiScan.models import User

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
    session['id'] = new_user.user_id
    session['email'] = new_user.email
    session['username'] = new_user.username
    
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
    session['id'] = user.user_id
    session['email'] = user.email
    session['username'] = user.username
    
    return redirect(url_for('mypage'))'''
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ForumPostForm(FlaskForm):
    title = StringField(
        'Post Title',
        validators=[DataRequired(message="Title is required."), Length(max=120)]
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired(message="Content cannot be empty.")]
    )
    submit = SubmitField('Submit Post')

class ForumCommentForm(FlaskForm):
    content = TextAreaField(
        'Comment',
        validators=[DataRequired(message="Comment cannot be empty.")]
    )
    submit = SubmitField('Submit Comment')
