from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("sukiscan.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/social")
def social():
    return render_template("social.html")

@app.route("/mypage")
def mypage():
    return render_template("mypage.html")

@app.route("/myhome")
def myhome():
    return render_template("myhome.html")

@app.route("/mysocial")
def mysocial():
    return render_template("mysocial.html")

@app.route("/add-details", methods=['POST'])
def add_details():
    conn = connect_db()
    cursor = conn.cursor()
    
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    query = f"INSERT INTO User (email, username, password) VALUES (?, ?, ?);"
    cursor.execute(query, (email, username, password))
    conn.close()
    
    return redirect(url_for('mypage'))

if __name__ == "__main__":
    app.run(debug=True)
