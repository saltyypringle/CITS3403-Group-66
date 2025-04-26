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

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/waifu_list')
def waifu_list():
    return render_template("placeholder.html")
@app.route('/husbando_list')
def husbando_list():
    return render_template("placeholder.html")

@app.route('/other_list')
def other_list():
    return render_template("placeholder.html")

if __name__ == "__main__":
    app.run(debug=True)
