from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from SukiScan.config import Config
from flask_wtf import CSRFProtect

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "SukiScan"
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from SukiScan.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf)

from SukiScan import route
from SukiScan import forms
from SukiScan import models 
