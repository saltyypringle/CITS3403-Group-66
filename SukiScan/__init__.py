from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "SukiScan"

login_m = LoginManager()
login_m.init_app(app)
login_m.login_view = "login"

from SukiScan import route
from SukiScan import forms