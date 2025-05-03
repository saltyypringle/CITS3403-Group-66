from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "SukiScan"

login_m = LoginManager()
login_m.init_app(app)
login_m.login_view = "login"

@login_m.user_loader
def get_user(username):
    from .models import AccountInfo
    return AccountInfo.Get_Info(username)

from SukiScan import routes, forms