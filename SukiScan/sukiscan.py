from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
